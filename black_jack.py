"""Black Jack class."""
from card_deck import Deck, Card


class BlackJack:
    """Play black jack."""

    def __init__(self):
        """Initialize."""
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = []
        self.dealer_hand = []
        self.player_bet = 0
        self.player_money = 0
        self.rounds_played = 0

    def checkDeck(self):
        """Check card amount in deck."""
        if len(self.deck.cards) < 20:
            self.deck.build()
            self.deck.shuffle()

    def roundBet(self):
        """Get bet for current round."""
        while True:
            if self.player_bet > 0 and self.player_bet < self.player_money:
                return self.player_bet
            else:
                continue

    def natural21(self, hand):
        """Check for a natural 21."""
        self.hand = hand
        if ((self.hand[0].rank == 14 or self.hand[1].rank == 14)
            and (self.hand[0].rank in range(10, 14) or
                 self.hand[1].rank in range(10, 14))):
            if self.dealer_hand != 21:
                self.endRound()

    def insurance(self, ins_bet):
        """Insure round per user input."""
        self.ins_bet = ins_bet
        if self.dealer_hand[1].rank in range(10, 14):
            self.ins_bet *= 2
            self.player_money -= self.player_bet
            self.player_money += self.ins_bet
        else:
            self.player_money -= self.ins_bet


    def splitPairs(self):
        """Split pairs."""
        self.split_hand = []
        self.split_bet = self.player_bet
        self.split_hand.append(self.player_hand.pop())
        self.split_hand.append(self.deck.drawCard())
        self.player_hand.append(self.deck.drawCard())

    def playerHit(self, hand):
        """Append cards to player's hand."""
        self.hand = hand
        self.hand.append(self.deck.drawCard())

    def dealerHit(self):
        while self.cardSum(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.drawCard())

    def cardSum(self, hand):
        """Count card values in hand."""
        self.hand = hand
        self.card_total = 0
        self.ace_total = 0

        for c in self.hand:
            if c.rank == 14:
                self.card_total += 11
                self.ace_total += 1
            elif c.rank in range(10, 14):
                self.card_total += 10
            else:
                self.card_total += c.rank
        while self.card_total > 21 and self.ace_total > 0:
            self.card_total -= 10
            self.ace_total -= 1
        return self.card_total

    def startRound(self):
        """Deal cards at start of round."""
        self.checkDeck()
        self.player_hand.append(self.deck.drawCard())
        self.player_hand.append(self.deck.drawCard())
        self.dealer_hand.append(self.deck.drawCard())
        self.dealer_hand.append(self.deck.drawCard())

    def endRound(self, ehand):
        """End round."""
        self.ehand = ehand
        if (self.cardSum(self.ehand) <= 21) and (self.cardSum(self.dealer_hand) 
                                                 > 21):
           self.player_money += self.player_bet
        elif (self.cardSum(self.ehand) > self.cardSum(
              self.dealer_hand)) and (self.cardSum(self.ehand) <= 21):
             self.player_money += self.player_bet
        elif self.cardSum(self.ehand) == self.cardSum(self.dealer_hand):
            pass
        else:
            self.player_money -= self.player_bet
        print (self.player_money)



