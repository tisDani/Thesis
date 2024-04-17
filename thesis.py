#references: https://docs.replit.com/tutorials/python/build-card-game-pygame
import random
from colorama import Back, Back, init
init(autoreset=True)

random.seed(10)

carryon = [0, 0, 0, 0, 0, 0, 0]
game_round = [0]

class Card:

    def __init__(self, number, colour, text, id, position):
        self.number = number
        self.colour = colour   
        self.text = text
        self.id = id
        self.position = position

    def paint(self):     
        print(self.text +'{} '.format(self.number), end =" ")

    def paint_big(self):
        print(self.text + '       \n   {}   \n      .'.format(self.number))

class Player: 
    hand = None
    played = None
    discarded = None
    store = None
    name = None
    moves = None

    def __init__(self, name):
        self.hand = Deck('hand ' + name)
        self.played = Deck('played ' + name)
        self.discarded = Deck('discarded ' + name)
        self.store = Deck('store ' + name)
        self.name = name
        self.moves = [0, 0, 0, 0]

    def draw(self, deck, num):
        deck.deal(self.hand, num)  #take n cards from deck
    
    def pshow(self):
        print("\n {} {: >20} {: >25} {: >20}   ".format(self.name, 'Hand', 'Discard', 'Store'))
        self.hand.printdeck()
        self.discarded.printdeck()
        self.store.printdeck()
        print('\n')

class Deck:
    cards = None
    name = None
    score = None

    def __init__(self, name):
        self.cards = []
        self.name = name
        self.score = [0, 0, 0, 0, 0, 0, 0]
       
    def build(self):
        colours = [[2,'purple',Back.CYAN, '2p', 1], [2, 'red',Back.RED, '2r', 2], [2, 'yellow',Back.YELLOW, '2y', 3], [3, 'blue',Back.BLUE, '3b', 4], [3, 'orange',Back.MAGENTA, '3o', 5], [4, 'green',Back.GREEN, '4g', 6], [5, 'black',Back.WHITE, '5b', 7]]
        for colour in colours:
            for i in range(0,colour[0]):
                self.cards.append(Card(colour[0], colour[1], colour[2], colour[3], colour[4])) 

    def build_big(self):
        colours = [[2,'purple',Back.CYAN, '2p', 1], [2, 'red',Back.RED, '2r', 2], [2, 'yellow',Back.YELLOW, '2y', 3], [3, 'blue',Back.BLUE, '3b', 4], [3, 'orange',Back.MAGENTA, '3o', 5], [4, 'green',Back.GREEN, '4g', 6], [5, 'black',Back.WHITE, '5b', 7]]
        colors =  [u'2\u0305', u'2\u0304', u'2\u0304', u'3\u0304', u'3\u0304', u'4\u0304', u'5\u0304',u'2\u0332', u'2\u0332', u'2\u0332', u'3\u0332', u'3\u0332', u'4\u0332', u'5\u0332']
        for i in range(0,7):
            if carryon[i] == 1:
                colours[i][0] = colors[i]
            elif carryon[i] == 2:
                colours[i][0] = colors[i+7]
            self.cards.append(Card(colours[i][0], colours[i][1], colours[i][2], colours[i][3], colours[i][4]))   

    def build_sample(self):
        colours = [[2,'purple',Back.CYAN, '2p', 1], [2, 'red',Back.RED, '2r', 2], [2, 'yellow',Back.YELLOW, '2y', 3], [3, 'blue',Back.BLUE, '3b', 4], [3, 'orange',Back.MAGENTA, '3o', 5], [4, 'green',Back.GREEN, '4g', 6], [5, 'black',Back.WHITE, '5b', 7]]
        for i in range(0,7):
            self.cards.append(Card(colours[i][0], colours[i][1], colours[i][2], colours[i][3], colours[i][4]))   

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, to, num):   #sample without replacement
        for i in range(0,num):
            to.cards.append(self.cards.pop())

    def length(self):
        return len(self.cards)
    
    def printdeck(self):
        print(' ', end = '                 ')
        for card in self.cards:
            card.paint()

    def count(self):
        self.score = [0, 0, 0, 0, 0, 0, 0]
        for card in self.cards:
            self.score[card.position - 1] +=1


def move(from_deck, to_deck, card_id):  
    card = i_d(from_deck, card_id)
    from_deck.cards.remove(card) 
    to_deck.cards.append(card)
    if 'played' in to_deck.name:
        to_deck.count()

def i_d(deck, iD):
    cards = (card for card in deck.cards 
        if card.id == iD)
    return next(cards)

def mul_move(from_deck, to_deck, items):
    for i in range(0, len(items)): 
        move(from_deck, to_deck, items[i])

class HanamikojiEngine:
    deck = None
    big_deck = None
    sample_deck = None
    player1 = None
    player2 = None
    cPlayer = None
    oPlayer = None

    def __init__(self, name1, name2):
        self.deck = Deck('stack')
        self.big_deck = Deck('big')
        self.sample_deck = Deck('sample')
        self.player1 = Player(name1)
        self.player2 = Player(name2)
        self.cPlayer = self.player1
        self.oPlayer = self.player2

    def start(self):
        self.deck.build()
        self.deck.shuffle()
        self.big_deck.build_big()
        self.sample_deck.build_sample()
        self.player1.draw(self.deck, 6)
        self.player2.draw(self.deck, 6)
        self.show_table()

    def win(self):
        colours = [2,2,2,3,3,4,5]
        points1 = 0
        geishas1 = 0
        points2 = 0
        geishas2 = 0
        
        for i in range(0,7):
            if self.player1.played.score[i] == 0 and self.player2.played.score[i] == 0:
                pass
            elif self.player1.played.score[i] > self.player2.played.score[i]:
                points1 += colours[i]
                geishas1 += 1
                carryon[i] = 1
            elif self.player1.played.score[i] < self.player2.played.score[i]:
                points2 += colours[i]
                geishas2 += 1
                carryon[i] = 2
            elif carryon[i] == 1 :
                points1 += colours[i]
                geishas1 += 1
            elif carryon[i] == 2 :
                points2 += colours[i]
                geishas2 += 1
        
        print('{}: {} Geishas, {} Points. {}: {} Geishas, {} Points '.format(self.player1.name, geishas1, points1,self.player2.name, geishas2, points2 ))
        
        if points1 >= 11:  
            print('Player 1 wins')
        elif points2 >= 11:
            print('Player 2 wins')
        elif geishas1 >= 4:
            print('Player 1 wins')
        elif geishas2 >= 4 :
            print('Player 2 wins')
        else:
            print('No winner yet') 
            round2 = HanamikojiEngine(name_player1, name_player2)
            round2.start()
            round2.interactive()
            
    def interactive(self):
        game_round[0] += 1
        for i in range(0,1):
            self.cPlayer = self.player1
            self.oPlayer = self.player2
            for j in range(0,2):
                print('Round {} Phase {} Turn {}. {} draws :'.format(game_round[0] , i + 1, j + 1, self.cPlayer.name))
                self.cPlayer.draw(self.deck, 1)
                self.cPlayer.pshow()
                print('{} Move: '.format(self.cPlayer.name), end=' ')
                if self.cPlayer.name == 'Random':
                    self.random_move()
                else: 
                    self.redirect(input())
                self.show_table()
                self.cPlayer = self.player2
                self.oPlayer = self.player1
        print('Play stored cards')
        if self.player1.store.cards != []:
            move(self.player1.store, self.player1.played, self.player1.store.cards[0].id)
        if self.player2.store.cards != []:
            move(self.player2.store, self.player2.played, self.player2.store.cards[0].id)
        self.show_table()
        self.win()

    def random_move(self):
        movs = ['Discard', 'Store', 'Trade 3x1', 'Trade 2x2']
        l = random.randint(0, 3)
        if movs[l] == 'Discard' and self.cPlayer.moves[0] == 0:
            select = random.sample(self.cPlayer.hand.cards, 2)
            print('Discard: {} {}'. format(select[0].id, select[1].id))
            self.discard(select[0].id, select[1].id)
            self.cPlayer.moves[0] = 1
        
        elif movs[l] == 'Store' and self.cPlayer.moves[1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 1)
            print('Store: {}'. format(select[0].id))
            self.store(select[0].id)
            self.cPlayer.moves[1] = 1
        
        elif movs[l] == 'Trade 3x1' and self.cPlayer.moves[2] == 0:
            select = random.sample(self.cPlayer.hand.cards, 3)
            print('Trade 3x1: {} {} {}'. format(select[0].id, select[1].id, select[2].id))
            self.trade3x1(select[0].id, select[1].id, select[2].id)
            self.cPlayer.moves[2] = 1

        elif movs[l] == 'Trade 2x2' and self.cPlayer.moves[3] == 0:   
            select = random.sample(self.cPlayer.hand.cards, 4)
            print('Trade 2x2: {} {} {} {}'. format(select[0].id, select[1].id, select[2].id, select[3].id))
            self.trade2x2(select[0].id, select[1].id, select[2].id, select[3].id)
            self.cPlayer.moves[3] = 1
        else:
            print('Move already used')
            self.random_move()

    def redirect(self, inpt):
        if inpt == 'Random':
            self.random_move()

        elif inpt == 'Discard' and self.cPlayer.moves[0] == 0:
            self.discard(input('First discard: '), input('Second discard: '))
            self.cPlayer.moves[0] = 1
           
        elif inpt == 'Store' and self.cPlayer.moves[1] == 0:
            self.store(input('Store: '))
            self.cPlayer.moves[1] = 1
           
        elif inpt == 'Trade 3x1' and self.cPlayer.moves[2] == 0:
            self.trade3x1(input('First trade: '), input('Second trade: '), input('Third trade: '))
            self.cPlayer.moves[2] = 1

        elif inpt == 'Trade 2x2' and self.cPlayer.moves[3] == 0:   
            self.trade2x2(input('First pair: '), input('- '), input('Second pair: '), input('- '))
            self.cPlayer.moves[3] = 1
        else:
            print('Move already used')
                
    def discard(self, inpt1, inpt2):
        print('{} Discards  '.format(self.cPlayer.name), end=' ')
        mul_move(self.cPlayer.hand, self.cPlayer.discarded, [inpt1, inpt2])

    def trade2x2(self, a1, a2, b1, b2):
        print('{}'.format(self.oPlayer.name), end=' ')
        if self.oPlayer.name == 'Random':
            inpt = random.randint(1,2)
            print('Chooses: {}'.format(inpt))
        else:
            inpt = input('chooses: ') #1,2
        lst = [[a1, a2], [b1, b2]]
        choice = lst.pop(int(inpt)-1)
        mul_move(self.cPlayer.hand, self.oPlayer.played, choice)
        mul_move(self.cPlayer.hand, self.cPlayer.played, lst[0])
        
    def trade3x1(self, a, b, c):
        print('{}'.format(self.oPlayer.name), end=' ')
        if self.oPlayer.name == 'Random':
            inpt = random.randint(1,3)
            print('Chooses: {}'.format(inpt))
        else:
            inpt = input('Chooses: ') #1,2,3
        lst = [a, b, c]
        choice = [lst.pop(int(inpt)-1)]
        mul_move(self.cPlayer.hand, self.oPlayer.played, choice)
        mul_move(self.cPlayer.hand, self.cPlayer.played, lst)

    def store(self, inpt1):
        move(self.cPlayer.hand, self.cPlayer.store, inpt1)
    
    def show_table(self):
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        self.player1.pshow()
        print('             ----------------------------\n')
        for i in range(max(self.player1.played.score), 0, -1): 
            print(' ', end = '                 ')
            for k in range(0,len(self.player1.played.score)):
                j = self.player1.played.score[k]
                if i<=j :
                    self.sample_deck.cards[k].paint()
                else:
                    print('  ', end = ' ')
            print('\n')
        self.big_deck.printdeck()
        print('\n')
        for i in range(0,max(self.player2.played.score)): 
            print(' ', end = '                 ')
            for k in range(0,len(self.player2.played.score)):
                j = self.player2.played.score[k]
                if i<j :
                    self.sample_deck.cards[k].paint()    #-----------------------
                else:
                    print('  ', end = ' ')
            print('\n')
        print('\n             ----------------------------\n')
        self.player2.pshow()
        print('\n \n Deck:  ', end=' ')
        self.deck.printdeck()
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')     

name_player1 = input('Enter Player 1 name:') #Enter 'Random' for random player 
name_player2 = input('Enter Player 2 name:')
game = HanamikojiEngine(name_player1, name_player2)
game.start()
game.interactive()


# 2p, 2r, 2y, 3b, 3o, 4g, 5b

#print('---------------------------1----------------------------------------------')
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~3~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#Back: RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE

