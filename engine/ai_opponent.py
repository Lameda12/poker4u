"""AI opponent personalities for Poker4U."""

import random
from enum import Enum
from typing import List, Optional, Tuple

from engine.cards import Card, HoleCards
from engine.evaluator import hand_strength, hand_percentile, evaluate_hand


class AIStyle(Enum):
    TIGHT = "tight"
    LOOSE = "loose"
    GTO = "gto"


class AIOpponent:
    """An AI poker opponent with a defined playing style."""

    def __init__(self, name: str, style: AIStyle, description: str):
        self.name = name
        self.style = style
        self.description = description
        self.chips = 200
        self.hole_cards: Optional[HoleCards] = None
        self.folded = False
        self.current_bet = 0
        self.total_invested = 0

    def reset_for_hand(self):
        self.hole_cards = None
        self.folded = False
        self.current_bet = 0
        self.total_invested = 0

    def decide(self, community: List[Card], pot_size: float,
               current_bet: float, min_raise: float) -> Tuple[str, float]:
        """Make a decision: returns (action, amount).

        action is one of: 'fold', 'check', 'call', 'raise'
        """
        if self.folded or self.hole_cards is None:
            return "fold", 0

        to_call = current_bet - self.current_bet

        # Get hand strength
        if community:
            strength = hand_strength(
                self.hole_cards.cards, community,
                num_opponents=1, iterations=200
            )
        else:
            strength = hand_percentile(self.hole_cards) / 100.0

        # Apply style bias
        if self.style == AIStyle.TIGHT:
            threshold_fold = 0.35
            threshold_call = 0.55
            threshold_raise = 0.72
            bluff_freq = 0.05
        elif self.style == AIStyle.LOOSE:
            threshold_fold = 0.15
            threshold_call = 0.30
            threshold_raise = 0.55
            bluff_freq = 0.20
        else:  # GTO
            threshold_fold = 0.25
            threshold_call = 0.42
            threshold_raise = 0.62
            bluff_freq = 0.12

        # Add randomness
        noise = random.gauss(0, 0.08)
        adjusted_strength = strength + noise

        # Bluff occasionally
        is_bluffing = random.random() < bluff_freq

        if to_call <= 0:
            # Facing no bet (can check or bet)
            if adjusted_strength >= threshold_raise or is_bluffing:
                bet_size = self._calculate_bet_size(strength, pot_size, is_bluffing)
                bet_size = min(bet_size, self.chips)
                if bet_size >= min_raise:
                    return "raise", bet_size
            return "check", 0

        # Facing a bet
        if adjusted_strength < threshold_fold and not is_bluffing:
            return "fold", 0
        elif adjusted_strength >= threshold_raise or is_bluffing:
            raise_amount = self._calculate_bet_size(strength, pot_size + to_call, is_bluffing)
            raise_amount = min(raise_amount, self.chips)
            if raise_amount >= min_raise and raise_amount > to_call:
                return "raise", raise_amount
            else:
                to_call = min(to_call, self.chips)
                return "call", to_call
        elif adjusted_strength >= threshold_call:
            to_call = min(to_call, self.chips)
            return "call", to_call
        else:
            return "fold", 0

    def _calculate_bet_size(self, strength: float, pot_size: float, is_bluff: bool) -> float:
        """Calculate a bet size based on hand strength and pot size."""
        if is_bluff:
            # Bluffs should be ~50-75% of pot
            return pot_size * random.uniform(0.5, 0.75)

        if strength >= 0.85:
            # Very strong - value bet big
            return pot_size * random.uniform(0.66, 1.0)
        elif strength >= 0.65:
            # Strong - medium bet
            return pot_size * random.uniform(0.5, 0.75)
        else:
            # Marginal - small bet
            return pot_size * random.uniform(0.33, 0.5)

    def should_play_preflop(self) -> bool:
        """Decide whether to play a preflop hand (for lesson purposes)."""
        if self.hole_cards is None:
            return False
        pct = hand_percentile(self.hole_cards)
        if self.style == AIStyle.TIGHT:
            return pct >= 65
        elif self.style == AIStyle.LOOSE:
            return pct >= 25
        else:
            return pct >= 45


def create_opponents() -> List[AIOpponent]:
    """Create the three AI opponents."""
    return [
        AIOpponent(
            name="Tight Tim",
            style=AIStyle.TIGHT,
            description="Only plays premium hands. Teaches about range advantage and patience.",
        ),
        AIOpponent(
            name="Loose Lucy",
            style=AIStyle.LOOSE,
            description="Plays too many hands. Teaches about hand selection and discipline.",
        ),
        AIOpponent(
            name="GTO Gary",
            style=AIStyle.GTO,
            description="Plays near-optimal. Shows what balanced, unexploitable play looks like.",
        ),
    ]
