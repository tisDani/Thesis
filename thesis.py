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

#random.seed(10)

class Card:

    def __init__(self, number, colour, text, id):
        self.number = number
        self.colour = colour   
        self.text = text
        self.id = id

    #def show(self):
    #    print('{} {}  '.format(self.number , self.colour))

    def paint(self):     
        print(self.text +'{} '.format(self.number), end =" ")

    def paint_big(self):
        print(self.text + '       \n   {}   \n      .'.format(self.number))


class Player: 
    hand = None
    played = None
    discarded = None
    store = None
    trade3x1 = None
    trade2x2 = None
    name = None

    def __init__(self, name):
        self.hand = Deck('hand ' + name)
        self.played = Deck('played ' + name)
        self.discarded = Deck('discarded ' + name)
        self.store = Deck('store ' + name)
        self.trade3x1 = Deck('trade 3x1 ' + name)
        self.trade2x2 = Deck('trade 2x2 ' + name)
        self.name = name

    def draw(self, deck, num):
        deck.deal(self.hand, num)  #take n cards from deck
    
    def pshow(self):
        print("\n {} {: >20} {: >25} {: >20} {: >20} {: >20} ".format(self.name,'Hand', 'Discard', 'Store', 'Trade 3x1', 'Trade 2x2'))
        self.hand.printdeck()
        self.discarded.printdeck()
        self.store.printdeck()
        self.trade3x1.printdeck()
        self.trade2x2.printdeck()
        print('\n')

class Deck:
    cards = None
    name = None

    def __init__(self, name):
        self.cards = []
        self.name = name
       
    def build(self):
        colours = [(2,'purple',Back.CYAN, '2p'), (2, 'red',Back.RED, '2r'), (2, 'yellow',Back.YELLOW, '2y'), (3, 'blue',Back.BLUE, '3b'), (3, 'orange',Back.MAGENTA, '3o'), (4, 'green',Back.GREEN, '4g'), (5, 'black',Back.WHITE, '5b')]
        for colour in colours:
            for i in range(0,colour[0]):
                self.cards.append(Card(colour[0], colour[1], colour[2], colour[3])) 

    def build_big(self):
        colours = [(2,'purple',Back.CYAN, '2p'), (2, 'red',Back.RED, '2r'), (2, 'yellow',Back.YELLOW, '2y'), (3, 'blue',Back.BLUE, '3b'), (3, 'orange',Back.MAGENTA, '3o'), (4, 'green',Back.GREEN, '4g'), (5, 'black',Back.WHITE, '5b')]
        for colour in colours:
            self.cards.append(Card(colour[0], colour[1], colour[2], colour[3]))   

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, to, num):   #sample without replacement
        for i in range(0,num):
            to.cards.append(self.cards.pop())

    def length(self):
        return len(self.cards)
    
    def printdeck(self):
        print(' ', end = '                 .')
        for i in range(0, self.length()):
            self.cards[i].paint()

def move(fromm, to, item):
    item.paint()
    fromm.remove(item) #list.remove(x): x not in list
    to.append(item)

def id_move(fromm, iD):
    s = fromm.index(fromm[id==iD])
    print(s)

def i_d(dck, iD):
    o = (card for card in dck.cards 
        if card.id == iD)
    next(o).paint()
    

def mul_move(fromm, to, items):
    for i in range(0, len(items)): #doesn't always work
        move(fromm, to, items[i])

 
class HanamikojiEngine:
    deck = None
    big_deck = None
    player1 = None
    player2 = None
    currentPlayer = None
    result = None

    def __init__(self):
        self.deck = Deck('stack')
        self.big_deck = Deck('big')
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.currentPlayer = self.player1

    def start(self):
        self.deck.build()
        self.deck.shuffle()
        self.big_deck.build_big()
        self.player1.draw(self.deck, 5)
        self.player2.draw(self.deck, 5)

    def interactive(self):
        self.currentPlayer = self.player1
        for i in range(0,1):
            print('{} Move: '.format(self.currentPlayer.name), end=' ')
            self.redirect(input())
            self.currentPlayer = self.player2

    def redirect(self, inpt):
        if inpt == 'Discard':
            self.diiscard(self.currentPlayer, input())
            #self.currentPlayer.discarded.cards.append(self.currentPlayer.hand.cards.pop(int(input('Index'))))
            
        elif inpt == 'Store':
            pass
        elif inpt == 'Trade 3x1':
            pass
        elif inpt == 'Trade 2x2':   
            pass         

    def show_table(self):
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        self.player1.pshow()
        print('\n')
        game.big_deck.printdeck()
        print('\n')
        self.player2.pshow()
        self.deck.printdeck()
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
    def diiscard(self, x, y):
        print('{} Discards {} '.format(x.name, y))
        #x.hand.cards[id==y].paint()
        #id_move(x.hand.cards, y)

    def trade2x2(self, fromm, to, a1, a2, b1, b2):
        pass

    def trade3x1(self, fromm, to, a, b, c):
        
        #player x offer nxm cards
        choice = input()
        
        #player y choose axb cards
        #redistribute

        pass

    def discard(self, fromm, a, b):
        mul_move(fromm.hand.cards, fromm.discarded.cards, [a,b])

    def store(self, fromm, a):
        move(fromm.hand.cards, fromm.store.cards, a)

game = HanamikojiEngine()
game.start()
#game.show_table()
#game.discard(game.player1, game.player1.hand.cards[0],  game.player1.hand.cards[1])
#game.show_table()
#game.store(game.player2, game.player2.hand.cards[3])
game.deck.printdeck()
print('--------')
#i_move(game.deck, input('here Id:'))
i_d(game.deck, '2y')
#game.show_table()
#game.interactive()
#game.show_table()


# 2p, 2r, 2y, 3b, 3o, 4g, 5b



#game.player1.pshow()
#game.player1.hand.cards[2].paint_big()
#print('---------------------------1----------------------------------------------')

#print('~~~~~~~~~~~~~~~~~~~~~~~~~~2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

#print('~~~~~~~~~~~~~~~~~~~~~~~~~~3~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


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
