"""Hand evaluation and ranking for Texas Hold'em."""

from enum import IntEnum
from itertools import combinations
from typing import List, Tuple, Optional
import random

from engine.cards import Card, Deck, HoleCards


class HandRank(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


HAND_RANK_NAMES = {
    HandRank.HIGH_CARD: "High Card",
    HandRank.ONE_PAIR: "One Pair",
    HandRank.TWO_PAIR: "Two Pair",
    HandRank.THREE_OF_A_KIND: "Three of a Kind",
    HandRank.STRAIGHT: "Straight",
    HandRank.FLUSH: "Flush",
    HandRank.FULL_HOUSE: "Full House",
    HandRank.FOUR_OF_A_KIND: "Four of a Kind",
    HandRank.STRAIGHT_FLUSH: "Straight Flush",
    HandRank.ROYAL_FLUSH: "Royal Flush",
}

# Approximate probability of being dealt each hand (5-card)
HAND_PROBABILITIES = {
    HandRank.ROYAL_FLUSH: 0.000154,
    HandRank.STRAIGHT_FLUSH: 0.00139,
    HandRank.FOUR_OF_A_KIND: 0.0240,
    HandRank.FULL_HOUSE: 0.1441,
    HandRank.FLUSH: 0.1965,
    HandRank.STRAIGHT: 0.3925,
    HandRank.THREE_OF_A_KIND: 2.1128,
    HandRank.TWO_PAIR: 4.7539,
    HandRank.ONE_PAIR: 42.2569,
    HandRank.HIGH_CARD: 50.1177,
}


class HandResult:
    """Result of evaluating a hand."""

    def __init__(self, rank: HandRank, tiebreakers: Tuple[int, ...], best_five: List[Card]):
        self.rank = rank
        self.tiebreakers = tiebreakers
        self.best_five = best_five

    @property
    def name(self) -> str:
        return HAND_RANK_NAMES[self.rank]

    def __lt__(self, other: "HandResult") -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.tiebreakers < other.tiebreakers

    def __eq__(self, other) -> bool:
        if not isinstance(other, HandResult):
            return NotImplemented
        return self.rank == other.rank and self.tiebreakers == other.tiebreakers

    def __le__(self, other) -> bool:
        return self == other or self < other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other

    def __repr__(self) -> str:
        return f"{self.name} ({', '.join(str(c) for c in self.best_five)})"


def _evaluate_five(cards: List[Card]) -> HandResult:
    """Evaluate exactly 5 cards and return a HandResult."""
    assert len(cards) == 5

    ranks = sorted([c.rank for c in cards], reverse=True)
    suits = [c.suit for c in cards]

    is_flush = len(set(suits)) == 1

    # Check straight
    is_straight = False
    straight_high = 0
    unique_ranks = sorted(set(ranks), reverse=True)

    if len(unique_ranks) == 5:
        if unique_ranks[0] - unique_ranks[4] == 4:
            is_straight = True
            straight_high = unique_ranks[0]
        # Ace-low straight (A-2-3-4-5)
        elif unique_ranks == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high = 5

    # Count rank frequencies
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    # Sort by count desc, then rank desc
    sorted_groups = sorted(rank_counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    counts = [g[1] for g in sorted_groups]
    group_ranks = tuple(g[0] for g in sorted_groups)

    if is_straight and is_flush:
        if straight_high == 14:
            return HandResult(HandRank.ROYAL_FLUSH, (14,), cards)
        return HandResult(HandRank.STRAIGHT_FLUSH, (straight_high,), cards)

    if counts == [4, 1]:
        return HandResult(HandRank.FOUR_OF_A_KIND, group_ranks, cards)

    if counts == [3, 2]:
        return HandResult(HandRank.FULL_HOUSE, group_ranks, cards)

    if is_flush:
        return HandResult(HandRank.FLUSH, tuple(ranks), cards)

    if is_straight:
        return HandResult(HandRank.STRAIGHT, (straight_high,), cards)

    if counts == [3, 1, 1]:
        return HandResult(HandRank.THREE_OF_A_KIND, group_ranks, cards)

    if counts == [2, 2, 1]:
        return HandResult(HandRank.TWO_PAIR, group_ranks, cards)

    if counts == [2, 1, 1, 1]:
        return HandResult(HandRank.ONE_PAIR, group_ranks, cards)

    return HandResult(HandRank.HIGH_CARD, tuple(ranks), cards)


def evaluate_hand(hole_cards: List[Card], community: List[Card]) -> HandResult:
    """Evaluate the best 5-card hand from hole cards + community cards."""
    all_cards = hole_cards + community
    if len(all_cards) < 5:
        # Pad evaluation for partial boards
        while len(all_cards) < 5:
            all_cards = all_cards + [Card(2, all_cards[0].suit)]
        return _evaluate_five(all_cards)

    best = None
    for combo in combinations(all_cards, 5):
        result = _evaluate_five(list(combo))
        if best is None or result > best:
            best = result
    return best


def hand_strength(hole_cards: List[Card], community: List[Card],
                  num_opponents: int = 1, iterations: int = 1000) -> float:
    """Monte Carlo simulation to estimate hand equity (0.0 to 1.0)."""
    wins = 0
    ties = 0
    known_cards = set((c.rank, c.suit) for c in hole_cards + community)

    for _ in range(iterations):
        deck = Deck()
        deck.remove(hole_cards + community)
        deck.shuffle()

        # Deal remaining community cards
        remaining_community = 5 - len(community)
        sim_community = community + deck.deal(remaining_community)

        my_result = evaluate_hand(hole_cards, sim_community)

        # Simulate opponents
        opponent_beats = False
        is_tie = False
        for _ in range(num_opponents):
            opp_cards = deck.deal(2)
            opp_result = evaluate_hand(opp_cards, sim_community)
            if opp_result > my_result:
                opponent_beats = True
                break
            elif opp_result == my_result:
                is_tie = True

        if not opponent_beats:
            if is_tie:
                ties += 1
            else:
                wins += 1

    return (wins + ties * 0.5) / iterations


def count_outs(hole_cards: List[Card], community: List[Card]) -> Tuple[int, List[str]]:
    """Count outs that improve the hand on the next card."""
    if len(community) < 3 or len(community) >= 5:
        return 0, []

    current_result = evaluate_hand(hole_cards, community)
    known = set((c.rank, c.suit) for c in hole_cards + community)
    outs = []

    from engine.cards import Suit
    for rank in range(2, 15):
        for suit in Suit:
            if (rank, suit) in known:
                continue
            test_card = Card(rank, suit)
            new_result = evaluate_hand(hole_cards, community + [test_card])
            if new_result > current_result:
                outs.append(str(test_card))

    return len(outs), outs


def hand_percentile(hole_cards: HoleCards) -> float:
    """Estimate preflop hand strength as a percentile (0-100)."""
    # Simplified ranking based on common preflop hand charts
    r1, r2 = hole_cards.cards[0].rank, hole_cards.cards[1].rank
    high, low = max(r1, r2), min(r1, r2)

    score = 0.0

    if hole_cards.is_pair:
        score = 50 + (high - 2) * 4.0  # Pairs: 50-98
    else:
        gap = high - low - 1
        score = (high + low) * 1.5
        if hole_cards.is_suited:
            score += 4
        score -= gap * 3
        score = max(0, min(score, 49))

    return round(score, 1)
