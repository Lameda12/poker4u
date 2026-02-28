"""Game theory calculations: EV, pot odds, Nash equilibrium basics."""

from typing import List, Optional, Tuple, Dict
from engine.cards import Card, HoleCards
from engine.evaluator import hand_strength, count_outs


def pot_odds(pot_size: float, bet_to_call: float) -> float:
    """Calculate pot odds as a percentage.

    Pot odds = bet_to_call / (pot_size + bet_to_call)
    This is the minimum equity needed to break even on a call.
    """
    if bet_to_call <= 0:
        return 0.0
    return bet_to_call / (pot_size + bet_to_call) * 100


def pot_odds_ratio(pot_size: float, bet_to_call: float) -> str:
    """Return pot odds as a ratio string like '3:1'."""
    if bet_to_call <= 0:
        return "∞:1"
    ratio = pot_size / bet_to_call
    if ratio == int(ratio):
        return f"{int(ratio)}:1"
    return f"{ratio:.1f}:1"


def expected_value_call(equity: float, pot_size: float, bet_to_call: float) -> float:
    """Calculate EV of calling.

    EV = (equity × pot_after_call) - bet_to_call
    """
    pot_after = pot_size + bet_to_call
    return (equity * pot_after) - ((1 - equity) * bet_to_call)


def expected_value_raise(equity: float, pot_size: float, raise_amount: float,
                         fold_equity: float = 0.0) -> float:
    """Calculate EV of raising.

    Considers fold equity - probability opponent folds.
    """
    # If opponent folds
    ev_fold = fold_equity * pot_size
    # If opponent calls
    pot_if_called = pot_size + raise_amount * 2
    ev_called = (1 - fold_equity) * ((equity * pot_if_called) - ((1 - equity) * raise_amount))
    return ev_fold + ev_called


def ev_fold() -> float:
    """EV of folding is always 0 (you lose nothing more)."""
    return 0.0


def draw_odds_rule_of_two(outs: int) -> float:
    """Approximate probability of hitting on the next card."""
    return min(outs * 2, 100)


def draw_odds_rule_of_four(outs: int) -> float:
    """Approximate probability of hitting by the river (from flop)."""
    return min(outs * 4, 100)


def exact_draw_odds(outs: int, cards_remaining: int) -> float:
    """Exact probability of hitting at least one out."""
    if cards_remaining <= 0 or outs <= 0:
        return 0.0
    return (outs / cards_remaining) * 100


def action_recommendation(equity: float, pot_size: float, bet_to_call: float,
                           hand_percentile: float = 50) -> Dict:
    """Get a complete action recommendation with math breakdown.

    Returns dict with EVs, recommendation, and explanation.
    """
    odds = pot_odds(pot_size, bet_to_call)
    odds_ratio = pot_odds_ratio(pot_size, bet_to_call)
    ev_c = expected_value_call(equity, pot_size, bet_to_call)
    ev_f = ev_fold()

    # Estimate fold equity based on hand percentile
    fold_eq = max(0, min(0.6, (hand_percentile - 30) / 100))
    raise_amount = bet_to_call * 2.5 if bet_to_call > 0 else pot_size * 0.66
    ev_r = expected_value_raise(equity, pot_size, raise_amount, fold_eq)

    # Determine best action
    actions = {"fold": ev_f, "call": ev_c, "raise": ev_r}
    best_action = max(actions, key=actions.get)

    # Color coding
    def ev_color(ev):
        if ev > 0.5:
            return "green"
        elif ev < -0.5:
            return "red"
        return "yellow"

    return {
        "equity": equity,
        "equity_pct": f"{equity * 100:.1f}%",
        "pot_odds": odds,
        "pot_odds_pct": f"{odds:.1f}%",
        "pot_odds_ratio": odds_ratio,
        "ev_fold": ev_f,
        "ev_call": ev_c,
        "ev_raise": ev_r,
        "ev_fold_color": "yellow",
        "ev_call_color": ev_color(ev_c),
        "ev_raise_color": ev_color(ev_r),
        "best_action": best_action,
        "raise_amount": raise_amount,
        "fold_equity": fold_eq,
        "math_breakdown": _math_breakdown(equity, pot_size, bet_to_call, ev_c),
    }


def _math_breakdown(equity: float, pot: float, bet: float, ev: float) -> List[str]:
    """Generate step-by-step math breakdown."""
    steps = [
        f"Your equity: {equity * 100:.1f}%",
        f"Pot size: {pot:.0f} chips",
        f"Bet to call: {bet:.0f} chips",
        f"Pot odds needed: {pot_odds(pot, bet):.1f}%",
        f"",
        f"EV of calling = (equity × total pot) - ((1-equity) × bet)",
        f"EV = ({equity:.3f} × {pot + bet:.0f}) - ({1 - equity:.3f} × {bet:.0f})",
        f"EV = {equity * (pot + bet):.1f} - {(1 - equity) * bet:.1f}",
        f"EV = {ev:+.1f} chips",
    ]
    if ev > 0:
        steps.append("")
        steps.append("Your equity exceeds the pot odds → profitable call!")
    elif ev < 0:
        steps.append("")
        steps.append("Your equity is below the pot odds → fold is better.")
    return steps


# --- Nash Equilibrium Helpers ---

def push_fold_nash_ranges() -> Dict[str, Dict]:
    """Simplified push/fold Nash equilibrium ranges for short-stack play.

    Returns ranges for different stack sizes (in big blinds).
    """
    return {
        "5bb": {
            "push": [
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o",
                "KQs", "KJs", "KTs", "K9s", "K8s",
                "KQo", "KJo",
                "QJs", "QTs", "Q9s",
                "JTs", "J9s",
                "T9s", "98s",
            ],
            "description": "With 5 big blinds, push or fold. No calling, no limping.",
        },
        "10bb": {
            "push": [
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A5s", "A4s",
                "AKo", "AQo", "AJo", "ATo",
                "KQs", "KJs",
                "KQo",
                "QJs",
            ],
            "description": "With 10 big blinds, push range tightens significantly.",
        },
        "15bb": {
            "push": [
                "AA", "KK", "QQ", "JJ", "TT", "99",
                "AKs", "AQs", "AJs",
                "AKo", "AQo",
                "KQs",
            ],
            "description": "With 15 big blinds, only push premium hands.",
        },
    }


def is_in_nash_range(hand: HoleCards, stack_bb: int) -> bool:
    """Check if a hand is in the Nash push range for a given stack size."""
    ranges = push_fold_nash_ranges()
    if stack_bb <= 7:
        key = "5bb"
    elif stack_bb <= 12:
        key = "10bb"
    else:
        key = "15bb"

    hand_name = hand.short_name()
    return hand_name in ranges[key]["push"]


# --- Glossary ---

GLOSSARY = {
    "Expected Value (EV)": {
        "definition": "The average outcome of a decision if repeated many times. "
                      "Calculated as the sum of each outcome multiplied by its probability.",
        "poker_example": "If you have 60% chance to win a 100-chip pot, "
                         "your EV = 0.6 × 100 - 0.4 × 50 = 40 chips.",
        "real_life": "When choosing between job offers, multiply salary × probability "
                     "of enjoying/staying at each job to find the best expected outcome.",
    },
    "Nash Equilibrium": {
        "definition": "A situation where no player can improve their outcome by "
                      "changing strategy, assuming other players keep theirs.",
        "poker_example": "In push/fold poker, the Nash equilibrium tells you exactly "
                         "which hands to shove with so your opponent can't exploit you.",
        "real_life": "In pricing wars, two companies reach Nash equilibrium when "
                     "neither can gain by changing price alone (think Coca-Cola vs Pepsi).",
    },
    "Dominant Strategy": {
        "definition": "A strategy that produces a better outcome regardless of "
                      "what your opponent does.",
        "poker_example": "Folding 72 offsuit from early position is a dominant strategy — "
                         "it's always better than playing it, no matter what happens.",
        "real_life": "Diversifying investments is often a dominant strategy — it "
                     "reduces risk regardless of which individual asset performs best.",
    },
    "Information Asymmetry": {
        "definition": "When one party in a transaction has more or better information "
                      "than the other.",
        "poker_example": "You know your hole cards but opponents don't. Acting last "
                         "gives you even more information about others' likely hands.",
        "real_life": "A used car seller knows the car's history better than the buyer. "
                     "This is why inspections and disclosures matter.",
    },
    "Sunk Cost": {
        "definition": "Money or resources already spent that cannot be recovered, "
                      "and should NOT influence future decisions.",
        "poker_example": "The chips you've already put in the pot are gone. Your decision "
                         "should only consider future pot odds, not past bets.",
        "real_life": "Don't stay in a bad movie just because you bought the ticket. "
                     "Don't keep a failing project just because you've invested time.",
    },
    "Variance": {
        "definition": "The natural fluctuation in outcomes even when making correct "
                      "decisions. Short-term results may not reflect long-term expectation.",
        "poker_example": "You can go all-in with AA vs 72 and lose. That doesn't mean "
                         "it was wrong — variance just hit. Over 1000 hands, AA wins ~87%.",
        "real_life": "A good business strategy might fail once. Don't abandon "
                     "a positive-EV approach because of one bad outcome.",
    },
    "Risk Premium": {
        "definition": "The extra return demanded for taking on additional risk "
                      "beyond a safe alternative.",
        "poker_example": "Going all-in with a marginal hand has high variance. You might "
                         "need better than break-even odds to justify the risk to your stack.",
        "real_life": "Stocks historically return more than bonds because investors "
                     "demand compensation for the higher risk of losing money.",
    },
    "Bayesian Updating": {
        "definition": "Revising your beliefs based on new evidence, using prior "
                      "probability and the likelihood of the new information.",
        "poker_example": "Your opponent raises preflop (narrows range), then bets flop "
                         "(narrows further). Each action updates your belief about their hand.",
        "real_life": "A doctor updates a diagnosis as test results come in. "
                     "Start with base rates, adjust with each new piece of evidence.",
    },
    "Zero-Sum vs Positive-Sum": {
        "definition": "In a zero-sum game, one player's gain equals another's loss. "
                      "In positive-sum, total value can increase for all players.",
        "poker_example": "Poker is zero-sum (minus rake): every chip you win, "
                         "someone else loses. Your profit = others' losses.",
        "real_life": "Trade is positive-sum — both parties can benefit. "
                     "Negotiating a raise isn't zero-sum if you also create more value.",
    },
    "Minimax": {
        "definition": "A strategy that minimizes your maximum possible loss. "
                      "You play to minimize the worst-case scenario.",
        "poker_example": "GTO (Game Theory Optimal) play is a minimax strategy — "
                         "it can't be exploited, guaranteeing at least break-even results.",
        "real_life": "Insurance is a minimax strategy: you accept a small certain cost "
                     "(premium) to avoid a potentially catastrophic loss.",
    },
}
