import random
import copy
import json

class Card:
    def __init__(self, value, suite, card_name, code, color):
        self.value = value
        self.suite = suite
        self.card_name = card_name
        self.code = code
        self.color = color



class Deck:
    cards = []

    def __init__(self):
        with open('cards.json') as f:
            data = json.load(f)
        for n in data:
            self.cards.append(Card(n["value"], n["suit"], n['card_name'], n['code'], n['color']))
        self.shuffle_deck()

    def print_cards(self):
        for n in self.cards:
            print(n.cardName + " of " + n.suite)

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_card(self):
        drawed = copy.deepcopy(self.cards[0])
        self.cards.pop(0)
        return drawed
