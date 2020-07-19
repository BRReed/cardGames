# NOTE: """Create a deck of cards."""
import random


class Card:
    """Create card."""

    def __init__(self, suit, rank):
        """Set x equal to self.x."""
        self.suit = suit
        self.rank = rank

    def show(self):
        """Print cards in deck."""
        for c in deck.cards:
            print(f'{self.rank} of {self.suit}')

    def __repr__(self):
        """Assign string to equivalent rank and suit."""
        if self.suit == 1:
            suit_str = 'Clubs'
        elif self.suit == 2:
            suit_str = 'Diamonds'
        elif self.suit == 3:
            suit_str = 'Hearts'
        elif self.suit == 4:
            suit_str = 'Spades'
        else:
            suit_str = 'fuck'

        if self.rank == 11:
            rank_str = 'Jack'
        elif self.rank == 12:
            rank_str = 'Queen'
        elif self.rank == 13:
            rank_str = 'King'
        elif self.rank == 14:
            rank_str = 'Ace'
        else:
            rank_str = str(self.rank)

        return f'{rank_str} of {suit_str}'


class Deck:
    """Create a deck."""

    def __init__(self):
        """Initialize deck."""
        self.cards = []
        self.build()

    def build(self):
        """Build deck."""
        for s in [1, 2, 3, 4]:
            for r in range(2, 15):
                self.cards.append(Card(s, r))

    def show(self):
        """Print card."""
        for c in self.cards:
            c.show()

    def shuffle(self):
        """Shuffle deck."""
        random.seed()
        random.shuffle(self.cards)

    def drawCard(self):
        """Draw card."""
        return self.cards.pop()
