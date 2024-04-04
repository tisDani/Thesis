#2 : purple, red, yellow
#3 : blue, orange
#4 : green
#5 : black

#references: https://docs.replit.com/tutorials/python/build-card-game-pygame

from itertools import groupby
from enum import Enum
import random

from colorama import Back, Back, Style, init
init(autoreset=True)

class Card:

    def __init__(self, number, colour, text, player, position):
        self.number = number
        self.colour = colour   
        self.player = player #sub position, deck
        self.position = position   #hand, discard, table, Player, deck, middle
        self.text = text

    def show(self):
        print('{} {} Player: {} Position: {} '.format(self.number , self.colour, self.player, self.position))

    def paint(self):     
        print(self.text +'{} '.format(self.number))

    def move(self, new_player, new_position):
         self.player = new_player
         self.position = new_position
  

class Player: 
    hand = None
    played = None
    discarded = None
    name = None

    def __init__(self, name):
        self.hand = Deck()
        self.played = Deck()
        self.discarded = Deck()
        self.name = name

    def draw(self, deck):
        self.hand.append(deck.deal())
        #take card from deck

    def play(self):
        return self.hand.pop(0)
    
    #def pshow(self):
    #    print("{: >20} {: >20} {: >20}".format(printdeck(self.hand), 2, 3))


class Deck:
    cards = None

    def __init__(self):
        self.cards = []
       
    def build(self):
        colours = [(2,'purple',Back.CYAN), (2, 'red',Back.RED), (2, 'yellow',Back.YELLOW), (3, 'blue',Back.BLUE), (3, 'orange',Back.MAGENTA), (4, 'green',Back.GREEN), (5, 'black',Back.WHITE)]
        for colour in colours:
            for i in range(0,colour[0]):
                self.cards.append(Card(colour[0], colour[1], colour[2], 'deck', 'deck'))
        

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def length(self):
        return len(self.cards)
    
    def printdeck(self):
        for i in range(0, self.length()):
            self.cards[i].paint()


class Table:

    def __init__(self, p1, p2):
        self.cards = [p1,p2]

    def play(self, player, item):
        player.hand.remove(item)
        player.played.append (item)

    def popAll(self):
        return self.cards

    def clear(self):
        self.cards = []

    def showtable(self) :
        pass
        #for card in deck:
        #print("{: >20} {: >20} {: >20}".format(self.cards[0].hand, 2, 3))

    
class HanamikojiEngine:
    deck = None
    player1 = None
    player2 = None
    pile = None
    currentPlayer = None
    result = None

    def __init__(self):
        self.deck = Deck()
        self.deck.build()
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        #self.pile = Pile()
        self.deal()
        self.currentPlayer = self.player1



deck2 = Deck()
deck2.build()
deck2.printdeck()





#Back: RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
#colours = [(2,'purple',Back.CYAN), (2, 'red',Back.RED), (2, 'yellow',Back.YELLOW), (3, 'blue',Back.BLUE), (3, 'orange',Back.MAGENTA), (4, 'green',Back.GREEN), (5, 'black',Back.WHITE)]
#deck1 =  [Card(colour[0], colour[1], colour[2], 'deck', 'deck') for colour in colours for i in range(0, colour[0])]
#colours = ['purple', 'red', 'yellow', 'blue', 'orange', 'green', 'black']
#numbers = [2,2,2,3,3,4,5]
#deck1 =  [Card(number, colour, 'deck', 'deck') for colour in colours for number in range(0,numbers)]


#b = table(deck1)
#print(b)
#print('----------2--------')
#print(deck1)

# define a function for key
#def key_func(k):
#    return k['posiion']
 
# sort INFO data by 'company' key.
#INFO = sorted(deck1, key=key_func)
 
#for key, value in groupby(deck1, key_func):
#    print(key)
#    print(list(value))
#Dealing :
#Move: