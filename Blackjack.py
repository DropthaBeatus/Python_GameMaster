import copy
from Pieces import Deck
import image_handler


# TODO: add rules: push, naturals, ties, double down, splitting pairs, dealer's pay and settlement
class playerBlackJack:
    points = 0
    name = ""
    betAmount = 0
    hand = []
    count = 0
    images = None
    file_name = ""
    public_images = ""
    pub_file_name = ""

    def __init__(self, name):
        self.points = 1000
        self.name = str(name)
        self.name_client = name
        self.file_name = 'Image_Tmp/' + self.name + '_tmp' + '.png'

    def bet(self, betted):
        if betted > self.points:
            print("You betted {} points. You only have {} points. Bet a lower amount before you have to sell your "
                  "car, kids, and soul", betted, self.points)
        else:
            self.points -= betted
            self.betAmount = self.betAmount + betted

    def win(self):
        self.points += self.betAmount + (self.betAmount * 1.5)

    def newhand(self, cards):
        self.count = 0
        self.hand = []
        self.betAmount = 0
        self.images = []
        self.bet(10)
        #TODO: make a check for black jack
        print("card amount {}".format(len(cards)))
        for card in cards:
            self.count = self.count + card.value
            self.images.append('card_pics/' + card.code + ".png")
        self.hand = cards
        self.file_name = image_handler.image_combine(self.images, self.name)
        self.prepare_public_hand()

    def prepare_public_hand(self):
        self.public_images = []
        self.public_images.append('card_pics/' + self.hand[0].code + ".png")
        self.public_images.append('card_pics/red_back.png')
        self.pub_file_name = image_handler.image_combine(self.public_images, self.name + "_pub")

    def switch_ace_up(self):
        switched = False
        for card in self.hand:
            print(card.card_name)
            if card.card_name == "Ace" and card.value == 1:
                card.value = 11
                switched = True
                self.count += 10
        return switched

    def switch_ace_down(self):
        switched = False
        for card in self.hand:
            print(card.card_name)
            if card.card_name == "Ace" and card.value == 11:
                card.value = 1
                switched = True
                self.count -= 10
        return switched

    def hit(self, card):
        self.count = self.count + card.value
        self.hand.append(card)
        self.images = []
        #TODO make an append and fix the open issue with image_handler.image_combine(): This will save processing time
        for card in self.hand:
            self.images.append('card_pics/' + card.code + ".png")

        self.file_name = image_handler.image_combine(self.images, self.name)
        self.prepare_public_hand()

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
                p.bet(10)

    def draw_cards(self):
        self.topAmount = 0
        self.check_card_count(self.player_amount * 2)
        for n in range(self.player_amount):
            self.hand = []
            self.hand.append(self.deck.draw_card())
            self.hand.append(self.deck.draw_card())
            self.players[n].newhand(self.hand)

    def compare_cards(self):
        self.winningOrder = []
        self.winningOrder = copy.copy(self.players)
        sorted(self.winningOrder, key=lambda player: player.count)
        prev = -1
        for n in range(len(self.winningOrder)-1, -1, -1):
            print("A count of {} for player: {}" .format(self.winningOrder[n].count, self.winningOrder[n].name))
            if self.winningOrder[n].count > 21:
                self.winningOrder.pop(n)
            elif self.winningOrder[n].count > self.topAmount:
                self.topAmount = self.winningOrder[n].count
                if prev == -1:
                    prev = n
                else:
                    self.winningOrder.pop(prev)
            elif self.winningOrder[n].count < self.topAmount:
                self.winningOrder.pop(n)

        if len(self.winningOrder) == 1:
            for player in self.players:
                if player.name == self.winningOrder[0].name:
                    player.win()
                    return "Player {} wins with {} and now has a point total of {}".format(player.name, player.count, player.points)
        else:
            tie_string = ""
            for player in self.winningOrder:
                tie_string = tie_string + str(player.name) + " "

            return ("Players: " + tie_string + " .... All tie!")
            #TODO give back players their money
        print("Cards left {}".format(len(self.deck.cards)))

    def check_card_count(self, drawn):
        if len(self.deck.cards) <= drawn:
            tempdeck = Deck()
            for card in tempdeck:
                self.deck.cards.append(card)

    def hit_hand(self, player_name):
        self.check_card_count(1)
        card = self.deck.draw_card()
        self.players[player_name].hand.append(card)
        self.players[player_name].count += card.value
