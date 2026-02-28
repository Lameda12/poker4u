"""Texas Hold'em game flow for Poker4U."""

from enum import Enum
from typing import List, Optional, Dict, Callable
from dataclasses import dataclass, field

from engine.cards import Card, Deck, HoleCards
from engine.evaluator import evaluate_hand, hand_strength, count_outs, hand_percentile, HandResult
from engine.ai_opponent import AIOpponent, create_opponents
from engine.game_theory import (
    pot_odds, pot_odds_ratio, expected_value_call,
    expected_value_raise, ev_fold, action_recommendation,
)


class Street(Enum):
    PREFLOP = "Preflop"
    FLOP = "Flop"
    TURN = "Turn"
    RIVER = "River"
    SHOWDOWN = "Showdown"


@dataclass
class PlayerState:
    name: str
    chips: int = 200
    hole_cards: Optional[HoleCards] = None
    folded: bool = False
    current_bet: int = 0
    total_invested: int = 0
    is_human: bool = False
    ai: Optional[AIOpponent] = None

    def reset_for_hand(self):
        self.hole_cards = None
        self.folded = False
        self.current_bet = 0
        self.total_invested = 0
        if self.ai:
            self.ai.reset_for_hand()


@dataclass
class HandAction:
    player_name: str
    street: Street
    action: str  # fold, check, call, raise, bet
    amount: int
    ev: Optional[float] = None
    is_correct: Optional[bool] = None


@dataclass
class HandHistory:
    actions: List[HandAction] = field(default_factory=list)
    community: List[Card] = field(default_factory=list)
    pot_size: int = 0
    player_decisions: int = 0
    correct_decisions: int = 0
    ev_earned: float = 0.0


class Game:
    """Manages a Texas Hold'em game session."""

    SMALL_BLIND = 1
    BIG_BLIND = 2
    STARTING_STACK = 200

    def __init__(self):
        self.deck = Deck()
        self.community: List[Card] = []
        self.pot = 0
        self.current_bet = 0
        self.min_raise = self.BIG_BLIND
        self.street = Street.PREFLOP
        self.players: List[PlayerState] = []
        self.dealer_pos = 0
        self.hand_history = HandHistory()
        self.hand_number = 0

    def setup_players(self, num_ai: int = 3) -> List[PlayerState]:
        """Set up the human player and AI opponents."""
        self.players = [
            PlayerState(name="You", chips=self.STARTING_STACK, is_human=True)
        ]

        ai_opponents = create_opponents()
        for i in range(min(num_ai, len(ai_opponents))):
            ai = ai_opponents[i]
            ai.chips = self.STARTING_STACK
            self.players.append(
                PlayerState(
                    name=ai.name,
                    chips=self.STARTING_STACK,
                    is_human=False,
                    ai=ai,
                )
            )

        return self.players

    def start_hand(self) -> Dict:
        """Start a new hand. Returns hand info."""
        self.hand_number += 1
        self.deck = Deck()
        self.community = []
        self.pot = 0
        self.current_bet = 0
        self.min_raise = self.BIG_BLIND
        self.street = Street.PREFLOP
        self.hand_history = HandHistory()

        for p in self.players:
            p.reset_for_hand()

        # Remove busted players
        active = [p for p in self.players if p.chips > 0]
        if len(active) < 2:
            return {"error": "Not enough players with chips"}

        # Post blinds
        sb_pos = (self.dealer_pos + 1) % len(self.players)
        bb_pos = (self.dealer_pos + 2) % len(self.players)

        sb_player = self.players[sb_pos]
        bb_player = self.players[bb_pos]

        sb_amount = min(self.SMALL_BLIND, sb_player.chips)
        bb_amount = min(self.BIG_BLIND, bb_player.chips)

        sb_player.chips -= sb_amount
        sb_player.current_bet = sb_amount
        sb_player.total_invested = sb_amount

        bb_player.chips -= bb_amount
        bb_player.current_bet = bb_amount
        bb_player.total_invested = bb_amount

        self.pot = sb_amount + bb_amount
        self.current_bet = bb_amount

        # Deal hole cards
        for p in self.players:
            if p.chips > 0 or p.current_bet > 0:
                cards = self.deck.deal(2)
                p.hole_cards = HoleCards(cards)
                if p.ai:
                    p.ai.hole_cards = p.hole_cards

        self.dealer_pos = (self.dealer_pos + 1) % len(self.players)

        return {
            "hand_number": self.hand_number,
            "small_blind": sb_player.name,
            "big_blind": bb_player.name,
            "sb_amount": sb_amount,
            "bb_amount": bb_amount,
        }

    def deal_street(self) -> List[Card]:
        """Deal the next street's community cards."""
        if self.street == Street.PREFLOP:
            self.street = Street.FLOP
            self.deck.deal_one()  # Burn
            new_cards = self.deck.deal(3)
        elif self.street == Street.FLOP:
            self.street = Street.TURN
            self.deck.deal_one()  # Burn
            new_cards = self.deck.deal(1)
        elif self.street == Street.TURN:
            self.street = Street.RIVER
            self.deck.deal_one()  # Burn
            new_cards = self.deck.deal(1)
        else:
            return []

        self.community.extend(new_cards)
        self.hand_history.community = self.community[:]

        # Reset bets for new street
        for p in self.players:
            p.current_bet = 0
        self.current_bet = 0
        self.min_raise = self.BIG_BLIND

        return new_cards

    def get_active_players(self) -> List[PlayerState]:
        """Get players still in the hand."""
        return [p for p in self.players if not p.folded and (p.chips > 0 or p.current_bet > 0)]

    def get_player_analysis(self, player: PlayerState) -> Dict:
        """Get educational analysis for the current situation."""
        if player.hole_cards is None:
            return {}

        equity = hand_strength(
            player.hole_cards.cards, self.community,
            num_opponents=len(self.get_active_players()) - 1,
            iterations=500,
        )

        to_call = self.current_bet - player.current_bet
        pct = hand_percentile(player.hole_cards)

        analysis = {
            "equity": equity,
            "hand_percentile": pct,
            "pot_size": self.pot,
            "to_call": to_call,
        }

        if to_call > 0:
            rec = action_recommendation(equity, self.pot, to_call, pct)
            analysis["recommendation"] = rec
        else:
            analysis["recommendation"] = {
                "equity": equity,
                "equity_pct": f"{equity * 100:.1f}%",
                "pot_odds": 0,
                "pot_odds_pct": "0%",
                "pot_odds_ratio": "free",
                "ev_fold": 0,
                "ev_call": 0,
                "ev_raise": expected_value_raise(equity, self.pot, self.pot * 0.66, 0.3),
                "ev_fold_color": "yellow",
                "ev_call_color": "yellow",
                "ev_raise_color": "green" if equity > 0.5 else "yellow",
                "best_action": "raise" if equity > 0.55 else "check",
                "raise_amount": self.pot * 0.66,
                "fold_equity": 0.3,
                "math_breakdown": [
                    f"Your equity: {equity * 100:.1f}%",
                    f"No bet to call — you can check for free.",
                    f"Consider betting if equity > 50%.",
                ],
            }

        if self.community:
            outs_count, outs_list = count_outs(player.hole_cards.cards, self.community)
            analysis["outs"] = outs_count
            analysis["outs_list"] = outs_list

        hand_result = None
        if self.community:
            hand_result = evaluate_hand(player.hole_cards.cards, self.community)
            analysis["current_hand"] = hand_result.name

        return analysis

    def process_action(self, player: PlayerState, action: str, amount: int = 0) -> Dict:
        """Process a player's action. Returns result info."""
        result = {"player": player.name, "action": action, "amount": 0}

        if action == "fold":
            player.folded = True
            result["action"] = "fold"

        elif action == "check":
            result["action"] = "check"

        elif action == "call":
            to_call = min(self.current_bet - player.current_bet, player.chips)
            player.chips -= to_call
            player.current_bet += to_call
            player.total_invested += to_call
            self.pot += to_call
            result["amount"] = to_call
            result["action"] = "call"

        elif action in ("raise", "bet"):
            actual_amount = min(amount, player.chips)
            # Ensure minimum raise
            actual_amount = max(actual_amount, self.min_raise)
            actual_amount = min(actual_amount, player.chips)

            to_call = self.current_bet - player.current_bet
            total_put_in = actual_amount

            player.chips -= total_put_in
            player.current_bet += total_put_in
            player.total_invested += total_put_in
            self.pot += total_put_in
            self.current_bet = player.current_bet
            self.min_raise = max(self.BIG_BLIND, actual_amount - to_call)
            result["amount"] = total_put_in
            result["action"] = "raise" if to_call > 0 else "bet"

        # Record in hand history
        ha = HandAction(
            player_name=player.name,
            street=self.street,
            action=result["action"],
            amount=result.get("amount", 0),
        )
        self.hand_history.actions.append(ha)

        return result

    def get_ai_action(self, ai_player: PlayerState) -> tuple:
        """Get an AI player's decision."""
        if ai_player.ai is None:
            return "fold", 0
        action, amount = ai_player.ai.decide(
            self.community, self.pot,
            self.current_bet, self.min_raise,
        )
        # Sync AI chip count
        ai_player.ai.chips = ai_player.chips
        ai_player.ai.current_bet = ai_player.current_bet
        return action, int(amount)

    def showdown(self) -> Dict:
        """Determine the winner at showdown."""
        active = self.get_active_players()

        if len(active) == 1:
            winner = active[0]
            winner.chips += self.pot
            return {
                "winners": [winner.name],
                "pot": self.pot,
                "method": "fold",
                "results": {winner.name: None},
            }

        results = {}
        best_result = None
        winners = []

        for p in active:
            if p.hole_cards is None:
                continue
            result = evaluate_hand(p.hole_cards.cards, self.community)
            results[p.name] = {
                "hand": result,
                "hole_cards": p.hole_cards,
            }
            if best_result is None or result > best_result:
                best_result = result
                winners = [p]
            elif result == best_result:
                winners.append(p)

        # Split pot among winners
        share = self.pot // len(winners)
        remainder = self.pot % len(winners)
        for i, w in enumerate(winners):
            w.chips += share + (1 if i < remainder else 0)

        return {
            "winners": [w.name for w in winners],
            "pot": self.pot,
            "method": "showdown",
            "results": results,
        }

    def is_hand_over(self) -> bool:
        """Check if the hand is over (only one player remains or river is complete)."""
        active = self.get_active_players()
        if len(active) <= 1:
            return True
        if self.street == Street.RIVER:
            # Check if all bets are settled
            bets = set(p.current_bet for p in active)
            return len(bets) <= 1
        return False

    def is_betting_complete(self) -> bool:
        """Check if betting is complete for the current street."""
        active = self.get_active_players()
        if len(active) <= 1:
            return True
        bets = set(p.current_bet for p in active)
        return len(bets) <= 1

    def get_hand_summary(self) -> Dict:
        """Get a summary of the completed hand for analysis."""
        return {
            "hand_number": self.hand_number,
            "actions": self.hand_history.actions,
            "community": self.community[:],
            "pot": self.pot,
            "player_decisions": self.hand_history.player_decisions,
            "correct_decisions": self.hand_history.correct_decisions,
            "ev_earned": self.hand_history.ev_earned,
        }
