"""Card, Deck, and Hand classes for Poker4U."""

import random
from enum import IntEnum
from typing import List, Optional


class Suit(IntEnum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3


SUIT_SYMBOLS = {
    Suit.CLUBS: "♣",
    Suit.DIAMONDS: "♦",
    Suit.HEARTS: "♥",
    Suit.SPADES: "♠",
}

SUIT_COLORS = {
    Suit.CLUBS: "white",
    Suit.DIAMONDS: "red",
    Suit.HEARTS: "red",
    Suit.SPADES: "white",
}

RANK_NAMES = {
    2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",
    9: "9", 10: "T", 11: "J", 12: "Q", 13: "K", 14: "A",
}

RANK_FROM_CHAR = {v: k for k, v in RANK_NAMES.items()}
RANK_FROM_CHAR["10"] = 10

SUIT_FROM_CHAR = {
    "c": Suit.CLUBS, "d": Suit.DIAMONDS,
    "h": Suit.HEARTS, "s": Suit.SPADES,
    "♣": Suit.CLUBS, "♦": Suit.DIAMONDS,
    "♥": Suit.HEARTS, "♠": Suit.SPADES,
}


class Card:
    """A single playing card."""

    __slots__ = ("rank", "suit")

    def __init__(self, rank: int, suit: Suit):
        self.rank = rank  # 2-14 (14=Ace)
        self.suit = suit

    @classmethod
    def from_str(cls, s: str) -> "Card":
        """Parse a card from string like 'As', 'Th', '2c'."""
        s = s.strip()
        rank_char = s[:-1]
        suit_char = s[-1].lower()
        return cls(RANK_FROM_CHAR[rank_char], SUIT_FROM_CHAR[suit_char])

    @property
    def rank_str(self) -> str:
        return RANK_NAMES[self.rank]

    @property
    def suit_symbol(self) -> str:
        return SUIT_SYMBOLS[self.suit]

    @property
    def color(self) -> str:
        return SUIT_COLORS[self.suit]

    def __repr__(self) -> str:
        return f"{self.rank_str}{self.suit_symbol}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __lt__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (self.rank, self.suit) < (other.rank, other.suit)

    def rich_str(self) -> str:
        """Return a rich-formatted string for this card."""
        return f"[{self.color}]{self.rank_str}{self.suit_symbol}[/{self.color}]"


class Deck:
    """A standard 52-card deck."""

    def __init__(self):
        self.cards: List[Card] = []
        self.reset()

    def reset(self):
        """Reset and shuffle the deck."""
        self.cards = [
            Card(rank, suit)
            for suit in Suit
            for rank in range(2, 15)
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n: int = 1) -> List[Card]:
        """Deal n cards from the top of the deck."""
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt

    def deal_one(self) -> Card:
        return self.deal(1)[0]

    def remove(self, cards: List[Card]):
        """Remove specific cards from the deck."""
        card_set = set((c.rank, c.suit) for c in cards)
        self.cards = [c for c in self.cards if (c.rank, c.suit) not in card_set]

    def __len__(self) -> int:
        return len(self.cards)


class HoleCards:
    """A player's two hole cards."""

    def __init__(self, cards: List[Card]):
        assert len(cards) == 2
        self.cards = sorted(cards, reverse=True)

    @property
    def card1(self) -> Card:
        return self.cards[0]

    @property
    def card2(self) -> Card:
        return self.cards[1]

    @property
    def is_pair(self) -> bool:
        return self.cards[0].rank == self.cards[1].rank

    @property
    def is_suited(self) -> bool:
        return self.cards[0].suit == self.cards[1].suit

    def short_name(self) -> str:
        """E.g. 'AKs', 'TT', '72o'."""
        r1, r2 = self.cards[0].rank_str, self.cards[1].rank_str
        if self.is_pair:
            return f"{r1}{r2}"
        suffix = "s" if self.is_suited else "o"
        return f"{r1}{r2}{suffix}"

    def __repr__(self) -> str:
        return f"[{self.cards[0]} {self.cards[1]}]"

    def rich_str(self) -> str:
        return f"{self.cards[0].rich_str()} {self.cards[1].rich_str()}"
