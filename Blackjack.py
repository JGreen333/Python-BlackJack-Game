import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        return f"This deck contains {len(self.deck)} card(s)."

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.suit == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        if self.value > 21 and self.cards[-1].rank == "Ace":
            self.value -= 10

    def new_hand(self):
        self.cards = []
        self.value = 0
        self.aces = 0


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += (self.bet * 2)
        self.bet = 0

    def blackjack(self):
        self.total += (self.bet * 2.5)
        self.bet = 0

    def push(self):
        self.total += self.bet
        self.bet = 0

    def lose_bet(self):
        self.bet = 0

    def take_bet(self):
        while True:
            try:
                bet_input = int(input("How much would you like to wager?"))
                if bet_input > self.total or bet_input < 0:
                    raise ValueError
            except:
                print(
                    "Your bet must be a number greater than 0 and no higher than your total number of chips.\n")
            else:
                self.bet = bet_input
                self.total -= bet_input
                print(f"You have wagered {bet_input} chip(s).\n")
                break


def hit(deck, hand):
    hand.add_card(deck.deal())


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop
    player_choice = ''

    while player_choice not in ['H', 'S']:
        player_choice = input(
            "Would you like to Hit or Stand? (Type 'H' or 'S')").upper()

    if player_choice == 'H':
        hit(deck, hand)
    else:
        playing = False


def show_some(player, dealer):
    # Player
    print(f"Player has {player.value}.")
    for card in player.cards:
        print(card)
    print('\n')

    # Dealer
    print(f"Dealer showing {dealer.cards[0].value}.")
    print(dealer.cards[0])
    print('\n' * 5)


def show_all(player, dealer):
    # Player
    print(f"Player has {player.value}.")
    for card in player.cards:
        print(card)
    print('\n')

    # Dealer
    print(f"Dealer showing {dealer.value}.")
    for card in dealer.cards:
        print(card)
    print('\n' * 5)


def player_busts(chips, dealer, player):
    chips.lose_bet()
    dealer.new_hand()
    player.new_hand()

    print(f"Player busts! Player now has {chips.total} chips.\n")


def player_wins(chips, dealer, player):
    chips.win_bet()
    dealer.new_hand()
    player.new_hand()

    print(f"Player wins! Player now has {chips.total} chips.\n")


def dealer_busts(chips, dealer, player):
    chips.win_bet()
    dealer.new_hand()
    player.new_hand()

    print(f"Dealer busts! Player now has {chips.total} chips.\n")


def dealer_wins(chips, dealer, player):
    chips.lose_bet()
    dealer.new_hand()
    player.new_hand()

    print(f"Dealer wins! Player now has {chips.total} chips.\n")


def push(chips, dealer, player):
    chips.push()
    dealer.new_hand()
    player.new_hand()

    print(f"Player pushes! Player now has {chips.total} chips.\n")


def player_blackjack(chips, dealer, player):
    chips.blackjack()
    dealer.new_hand()
    player.new_hand()

    print(f"Player blackjack! Player now has {chips.total} chips.\n")

# RUN GAME


print("Welcome to BlackJack! Player starts with 100 Chips. BlackJack pays out 3:2.\n")

# Set up the Player's chips
player_chips = Chips()

while True:

    # Create & shuffle the deck, deal two cards to each player
    game_deck = Deck()
    game_deck.shuffle()

    dealer = Hand()
    player = Hand()

    player.add_card(game_deck.deal())
    dealer.add_card(game_deck.deal())
    player.add_card(game_deck.deal())
    dealer.add_card(game_deck.deal())

    # Prompt the Player for their bet
    print("Please place bet!\n")
    player_chips.take_bet()

    # Check for Blackjack
    blackjack = True

    if dealer.value == 21 and player.value == 21:
        push(player_chips, dealer, player)
    elif dealer.value == 21 and player.value != 21:
        dealer_wins(player_chips, dealer, player)
    elif dealer.value != 21 and player.value == 21:
        player_blackjack(player_chips, dealer, player)
    else:
        print("No Blackjack! Would you like to hit or stand?\n")
        blackjack = False

    while blackjack == False:
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)

        playing = True

        while playing:  # recall this variable from our hit_or_stand function

            # Prompt for Player to Hit or Stand
            hit_or_stand(game_deck, player)

            # Show cards (but keep one dealer card hidden)
            show_some(player, dealer)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player.value > 21:
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player.value > 21:
            player_busts(player_chips, dealer, player)
            break
        elif player.value != 0:
            show_all(player, dealer)
            while dealer.value < 17:
                hit(game_deck, dealer)
                show_all(player, dealer)
            # Show all cards

            # Run different winning scenarios
            if dealer.value > 21:
                dealer_busts(player_chips, dealer, player)
            elif dealer.value != 21 and dealer.value < player.value:
                player_wins(player_chips, dealer, player)
            elif dealer == 21 or dealer.value > player.value:
                dealer_wins(player_chips, dealer, player)
            else:
                push(player_chips, dealer, player)

            break

    # Inform Player of their chips total

    # Ask to play again
    new_round = ''

    while new_round not in ['Y', 'N']:
        new_round = input("Would you like to play again? ('Y' or 'N')").upper()

    if new_round == 'Y':
        new_round = ''
        print("Beginning new round!\n")
        continue
    else:
        new_round = ''
        print("Thanks for playing! Cashing chips out now.")
        break
