import copy
from Pieces import Deck
import discord
import image_handler


class playerBlackJack:
    points = 0
    name = ""
    betAmount = 0
    hand = []
    count = 0
    images = None
    discord_img = None
    file_name = ""

    def __init__(self, name):
        self.points = 100
        self.name = str(name)
        self.name_client = name
        self.file_name = self.name + '_tmp' + '.png'

    def bet(self, betted):
        if betted > self.points:
            print("You betted {} points. You only have {} points. Bet a lower amount before you have to sell your "
                  "car, kids, and soul", betted, self.points)
        else:
            self.points -= betted
            self.betAmount = betted

    def win(self):
        self.points += self.betAmount + (self.betAmount * 1.5)

    def newHand(self, cards):
        self.count = 0
        self.hand = []
        self.images = []
        self.bet(10)
        #TODO: make a check for black jack
        #TODO: make permiations for Aces
        for card in cards:
            self.count = self.count + card.value
            self.images.append('card_pics/' + card.code + ".png")
        self.hand = cards
        image_handler.image_combine(self.images, self.file_name)
        self.discord_img = discord.File(self.file_name)

    def switch_ace_up(self):
        switched = False
        for card in self.hand:
            if card.hand_name == "Ace" and card.value == 1:
                card.value = 11
                return switched

    def switch_ace_down(self):
        switched = False
        for card in self.hand:
            if card.hand_name == "Ace" and card.value == 11:
                card.value = 1
                return switched

    def hit(self, card):
        self.count = self.count + card.value
        self.images.append(discord.File('card_pics/' + card.code + ".png"))
        self.hand.append(card)
        image_handler.delete_image(self.file_name)
        self.discord_img = image_handler.image_combine(self.images, self.file_name)

    def return_count(self):
        return "player " + self.name + " has a hand total of " + str(self.count) + " with a point total of " + str(self.points) + "\n"

    def __repr__(self):
        return repr((self.count, self.name))


class blackJack:
    winningOrder = []
    topAmount = 0
    player_amount = 2

    def __init__(self, player_names):
        self.player_amount = len(player_names)
        self.deck = Deck()
        self.players = []
        x = 0
        while x < self.player_amount:
            self.players.append(playerBlackJack(player_names[x]))
            x += 1

    def draw_card(self, player_name):
        for p in self.players:
            if p.name == player_name:
                p.hit(self.deck.draw_card())

    def draw_cards(self):
        self.topAmount = 0
        self.check_card_count(self.player_amount * 2)
        for n in range(self.player_amount):
            self.hand = []
            self.hand.append(self.deck.draw_card())
            self.hand.append(self.deck.draw_card())
            self.players[n].newHand(self.hand)

        # TODO remove this later
        #self.compare_cards()

    def compare_cards(self):
        self.winningOrder = []
        self.winningOrder = copy.deepcopy(self.players)
        sorted(self.winningOrder, key=lambda player: player.count)

        for n in range(len(self.winningOrder)-1, -1, -1):
            if self.winningOrder[n].count > 21:
                self.winningOrder.pop(n)
            elif self.winningOrder[n].count > self.topAmount:
                self.topAmount = self.winningOrder[n].count
            elif self.winningOrder[n].count < self.topAmount:
                self.winningOrder.pop(n)

        if len(self.winningOrder) == 1:
            index = self.winningOrder[0].name
            self.players[index].win()
            return ("Player {0} wins with {1} and now has a point total of {2}".format(self.players[index].name, self.players[index].count,  self.players[index].points))
        else:
            tie_string = ""
            for player in self.winningOrder:
                tie_string = tie_string + str(player.name) + " "

            return ("Players: " + tie_string + " .... All tie!")
            #TODO give back players their money
        print("Cards left {}".format(len(self.deck.cards)))

    def check_card_count(self, drawn):
        if len(self.deck.cards) <= drawn:
            tmpdeck = self.deck.cards
            self.deck = Deck()
            for card in tmpdeck:
                self.deck.cards.append(card)

    def hit_hand(self, player_name):
        self.check_card_count(1)
        card = self.deck.draw_card()
        self.players[player_name].hand.append(card)
        self.players[player_name].count += card.value
