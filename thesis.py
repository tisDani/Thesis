#references: https://docs.replit.com/tutorials/python/build-card-game-pygame
import random
from itertools import combinations
import copy
import csv
import gc
from colorama import Back, Back, init
init(autoreset=True)

import pandas as pd
#pd.options.display.max_rows = 10
#np.set_printoptions(precision=4, suppress=True)

SEED = 10
import os
os.environ["PYTHONHASHSEED"] = str(SEED)

import numpy as np
from collections import defaultdict
np.random.seed(SEED)
random.seed(SEED)   #11 = win first round, 10 = not

cnter = [0]
C_SEL = 1.4
C_CHOICE = 0.2
N_SIM_B = 1000
N_SIM_M = 300
N_SIM_T = 100

PARAMETERS = [C_SEL, C_CHOICE, N_SIM_B, N_SIM_M, N_SIM_T]

carryon = [0, 0, 0, 0, 0, 0, 0]
game_round = [0]
all_moves = []
childs = [PARAMETERS, ['round', 'parent move', 'fraction', 'c-value']]

def print_all():
    for move in all_moves:
        print(move)


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
        self.moves = [['Store', 0, 1], ['Discard', 0, 2], ['Trade 3x1', 0, 3], ['Trade 2x2', 0, 4]]

    def draw(self, deck, num):
        if num > 1:
            #print(' {} draws hand'.format(self.name), end = ' ')
            deck.deal(self.hand, num)  #take n cards from deck
            #self.hand.printdeck()
            return

        if len(deck.cards) <= 1:
            pass
            #print('last card')

        elif deck.last_draw == self.name or (deck.last_draw == 'Monte Carlo' and self.name == 'Monte Carlo Expand'):
            #all_moves.append(['repeat', deck.last_draw, self.name])
            return

        else:
            #print(' {} draw, last was {}'.format(self.name, deck.last_draw), end = ' ')
            deck.deal(self.hand, num)  #take n cards from deck
            #self.hand.printdeck()
            deck.last_draw = self.name
    
    def pshow(self):
        print("\n {} {: >20} {: >25} {: >20}   ".format(self.name, 'Hand', 'Discard', 'Store'))
        self.hand.printdeck()
        self.discarded.printdeck()
        self.store.printdeck()
        print('\n')

    def ptable(self):
        tble = [self.name, 'hand' ,self.hand.deck_id(), 'discard', self.discarded.deck_id(), 'store', self.store.deck_id(), 'played',self.played.deck_id()]
        return tble
    

class Deck:
    cards = None
    name = None
    score = None
    last_draw = None

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

    def deck_id(self):
        ids = []
        for card in self.cards:
            ids.append(card.id)
        return ids
    

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
    trade = []
    decision = 'move'
    choice = 0
    winner = 0

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

    def win(self):
        colours = [2,2,2,3,3,4,5]
        points1 = 0
        geishas1 = 0
        points2 = 0
        geishas2 = 0
        w_name = 'None'
        self.play_stored()
        
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
        
        #print('{}: {} Geishas, {} Points. {}: {} Geishas, {} Points '.format(self.player1.name, geishas1, points1,self.player2.name, geishas2, points2 ))
        
        if points1 >= 11:  
            #print('Player 1 wins')
            self.winner = 1
            w_name = self.player1.name
        elif points2 >= 11:
            #print('Player 2 wins')
            self.winner = -1
            w_name = self.player2.name
        elif geishas1 >= 4:
            #print('Player 1 wins')
            self.winner = 1
            w_name = self.player1.name
        elif geishas2 >= 4:
            #print('Player 2 wins')
            self.winner = -1
            w_name = self.player2.name
        else:
            pass
            #print('No winner yet') 
            #round2 = HanamikojiEngine(name_player1, name_player2)
            #round2.start()
        
    def interactive(self):
        game_round[0] += 1
        for i in range(0, 4):
            self.cPlayer = self.player1
            self.oPlayer = self.player2
            for j in range(0,2):
                print('Round {} Phase {} Turn {}. {} draws :'.format(game_round[0] , i + 1, j + 1, self.cPlayer.name))
                self.cPlayer.draw(self.deck, 1)
                self.cPlayer.pshow()
                print('{} Move: '.format(self.cPlayer.name), end=' ')
                if self.cPlayer.name == 'Random 1' or self.cPlayer.name == 'Random 2' or self.cPlayer.name == 'Monte Carlo':
                    self.random_move()
                else: 
                    self.redirect(input())
                self.show_table()
                self.cPlayer = self.player2
                self.oPlayer = self.player1
        self.play_stored()
        self.show_table()
        next_round = self.win()
        if self.winner == 0:
            next_round.interactive()

    def print_winner(self, csv_lst):
        if self.winner == 0:
            csv_lst.append('No winner')
        elif self.winner == 1:
            csv_lst.append(['Player 1 wins:', self.player1.name])
        elif self.winner == -1:
            csv_lst.append(['Player 2 wins:', self.player2.name])

    def play_stored(self):
        if self.player1.store.cards != []:
            move(self.player1.store, self.player1.played, self.player1.store.cards[0].id)
        if self.player2.store.cards != []:
            move(self.player2.store, self.player2.played, self.player2.store.cards[0].id)
        
    def random_move(self):
        print('random move')
        movs = ['Store', 'Discard', 'Trade 3x1', 'Trade 2x2']
        l = random.randint(0, 3) 
        select = []
        if self.decision == 'trade':
            if len(self.trade) == 4:
                inpt = random.randint(1,2)
                self.choice = inpt
                self.trade2x2_inpt(self.trade, inpt)
                self.decision = 'move'
                self.switch_players()
                childs.append([['Random move answer 2x2'], [self.cPlayer.name], [inpt], [self.trade] ])
                return
            elif len(self.trade) == 3:
                inpt = random.randint(1,3)
                self.choice = inpt
                self.trade3x1_inpt(self.trade, inpt)
                self.decision = 'move'
                self.switch_players()
                childs.append([[['Random move answer 3x1'], [self.cPlayer.name], [inpt], [self.trade] ]])
                return

        elif self.cPlayer.moves[0][1] == 1 and self.cPlayer.moves[1][1] == 1 and self.cPlayer.moves[2][1] == 1 and self.cPlayer.moves[3][1] == 1:
            print('all moves used')

        elif movs[l] == 'Store' and self.cPlayer.moves[0][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 1)
            print('Store: {}'. format(select[0].id))
            self.store(select[0].id)
            self.cPlayer.moves[0][1] = 1
            childs.append([[['Random move Store'], [self.oPlayer.name],[select[0].id] ]])
        
        elif movs[l] == 'Discard' and self.cPlayer.moves[1][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 2)
            print('Discard: {} {}'. format(select[0].id, select[1].id))
            self.discard(select[0].id, select[1].id)
            self.cPlayer.moves[1][1] = 1
            childs.append([[['Random move Discard'], [self.oPlayer.name], [select[0].id, select[1].id]]])
        
        elif movs[l] == 'Trade 3x1' and self.cPlayer.moves[2][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 3)
            print('Trade 3x1: {} {} {}'. format(select[0].id, select[1].id, select[2].id))
            self.cPlayer.moves[2][1] = 1
            childs.append([['Random move 3x1 trade'], [self.cPlayer.name], [select[0].id, select[1].id, select[2].id]])
            self.trade3x1(select[0].id, select[1].id, select[2].id)
            return 

        elif movs[l] == 'Trade 2x2' and self.cPlayer.moves[3][1] == 0:   
            select = random.sample(self.cPlayer.hand.cards, 4)
            print('Trade 2x2: {} {} {} {}'. format(select[0].id, select[1].id, select[2].id, select[3].id))
            self.cPlayer.moves[3][1] = 1
            childs.append([['Random move 2x2 trade'], [self.cPlayer.name], [select[0].id, select[1].id, select[2].id, select[3].id]])
            self.trade2x2(select[0].id, select[1].id, select[2].id, select[3].id)
            return 
        else:
            #print('Move already used')
            cnter[0] += 1 
            print(self.cPlayer.moves)
            if cnter[0] < 10:
                self.random_move()

    
        #all_moves.append(['random move' , action, self.cPlayer.name])
        

    def monte_carlo(self, action):   #action :[[cards], [move]]            [[['3o', '2p'], ['5b', '3b']], ['Trade2x2', 0, 4]]
        #print('\n MC action:  {} {}'.format(action, self.cPlayer.name))
        #all_moves.append(['Monte Carlo ' , action, self.cPlayer.name])

        if action[1] == 'trade 3x1':#[2, 'trade 2x2']
            #print('trade 3x1 MC ')
            self.trade3x1_inpt(self.trade, action[0])
            self.decision = 'move'

        elif action[1] == 'trade 2x2':    #[2, 'trade 2x2']
            #print('trade 2x2 MC ')
            self.trade2x2_inpt(self.trade, action[0])
            self.decision = 'move'

        elif action[1][0] == 'Store' and self.cPlayer.moves[0][1] == 0:
            self.store(action[0][0])
            self.cPlayer.moves[0][1] = 1

        elif action[1][0] == 'Discard' and self.cPlayer.moves[1][1] == 0:
            self.discard(action[0][0], action[0][1])
            self.cPlayer.moves[1][1] = 1
           
        elif action [1][0] == 'Trade 3x1' and self.decision == 'move' and self.cPlayer.moves[2][1] == 0:
            self.decision = 'trade'
            if len(self.trade) != 0:
                self.trade = []
            for card in action[0]:
                self.trade.append(card)
            self.cPlayer.moves[2][1] = 1
            return

        elif action [1][0] == 'Trade 2x2' and self.decision == 'move' and self.cPlayer.moves[3][1] == 0:
            self.decision = 'trade'
            if len(self.trade) != 0:
                self.trade = []
            for card in action[0]:
                self.trade.append(card[0])
                self.trade.append(card[1])
            self.cPlayer.moves[3][1] = 1
            return
        
        elif action[1][0] == 'Trade 3x1' and self.decision == 'trade':
            self.decision = 'move'
            self.trade3x1(action[0][0], action[0][1], action[0][2])
            self.cPlayer.moves[2][1] = 1

        elif action[1][0] == 'Trade 2x2' and self.decision == 'trade':   
            self.decision = 'move'
            self.trade2x2(action[0][0][0], action[0][0][1], action[0][1][0], action[0][1][1])
            self.cPlayer.moves[3][1] = 1
       
        else:
            print('Move already used')

        self.switch_players()

        if self.turn_over():
            self.win()
            if self.winner == 0:
                return 0

    def switch_players(self):
        #print('switch players')
        if self.cPlayer == self.player1:
            self.cPlayer = self.player2
            self.oPlayer = self.player1
        else:
            self.cPlayer = self.player1
            self.oPlayer = self.player2

    def turn_over(self):
        counter = 0
        for move in self.cPlayer.moves:
            if move[1] == 1:
                counter += 1
        
        for move in self.oPlayer.moves:
            if move[1] == 1:
                counter += 1
        
        is_over = (counter == 8)
        return is_over
    
    def new_round_p(self):
        self.cPlayer = self.player1
        self.oPlayer = self.player2

    def redirect(self, inpt):
        if inpt == 'Random 1' or inpt == 'Random 2' or self.cPlayer.name == 'Monte Carlo':
            self.random_move()
                   
        elif inpt == 'Store' and self.cPlayer.moves[0][1] == 0:
            self.store(input('Store: '))
            self.cPlayer.moves[0][1] = 1

        elif inpt == 'Discard' and self.cPlayer.moves[1][1] == 0:
            self.discard(input('First discard: '), input('Second discard: '))
            self.cPlayer.moves[1][1] = 1
           
        elif inpt == 'Trade 3x1' and self.cPlayer.moves[2][1] == 0:
            self.trade3x1(input('First trade: '), input('Second trade: '), input('Third trade: '))
            self.cPlayer.moves[2][1] = 1

        elif inpt == 'Trade 2x2' and self.cPlayer.moves[3][1] == 0:   
            self.trade2x2(input('First pair: '), input('- '), input('Second pair: '), input('- '))
            self.cPlayer.moves[3][1] = 1
        else:
            print('Move already used')
                
    def discard(self, inpt1, inpt2):
        mul_move(self.cPlayer.hand, self.cPlayer.discarded, [inpt1, inpt2])

    def trade3x1_inpt(self, trade, inpt):
        dummy = copy.deepcopy(trade)
        choice = [dummy.pop(int(inpt)-1)]
        mul_move(self.cPlayer.hand, self.oPlayer.played, choice)
        mul_move(self.cPlayer.hand, self.cPlayer.played, dummy)

    def trade2x2_inpt(self, trade, inpt):   #trade: [a1, a2, b1, b2]
        dummy = [[trade[0], trade[1]], [trade[2], trade[3]]]
        choice = dummy.pop(int(inpt)-1)
        mul_move(self.cPlayer.hand, self.oPlayer.played, choice)
        mul_move(self.cPlayer.hand, self.cPlayer.played, dummy[0])

    def trade2x2(self, a1, a2, b1, b2):
        print('{}'.format(self.oPlayer.name), end=' ')
        if self.oPlayer.name == 'Monte Carlo Expand':
            self.decision = 'trade'
            self.trade = [a1, a2, b1, b2]
            root_node = MonteCarloTreeSearchNode(state = self, original = copy.deepcopy(self) ,parent = None, decision= 'trade')  #ROOT!
            root_node.untried_actions()  #indeed, 1,2,3
            out = root_node.best_action()    #returns state with trade done, sel_node is a node
            self.monte_carlo(out.parent_action) 
            return 
            #mc_trade
            #need to make a Monte Carlo agent that can analyze the outcomes of trades. 
            #This means making a new node in the game tree where decisions happen - expand game tree. Or Make a different MC agent just for decisions
        elif self.oPlayer.name == 'Random 2' or self.oPlayer.name == 'Random 1' or self.oPlayer.name == 'Monte Carlo Rollout':
            inpt = random.randint(1,2)
            print('Chooses: {}'.format(inpt))
        else:
            print('all trade 2x2 failed. {} {} {}'.format)
            inpt = input('chooses: ') #1,2
        lst = [[a1, a2], [b1, b2]]
        choice = lst.pop(int(inpt)-1)
        mul_move(self.cPlayer.hand, self.oPlayer.played, choice)
        mul_move(self.cPlayer.hand, self.cPlayer.played, lst[0])
        
    def trade3x1(self, a, b, c):
        print('{}'.format(self.oPlayer.name), end=' ')
        self.trade = [a, b, c]
        if self.oPlayer.name == 'Monte Carlo Expand':
            self.decision = 'trade'
            self.trade = [a, b, c]
            root_node = MonteCarloTreeSearchNode(state = self, original = copy.deepcopy(self) ,parent = None, decision= 'trade')  #ROOT!
            root_node.untried_actions()  #indeed, 1,2,3
            out = root_node.best_action()    #returns state with trade done, sel_node is a node
            self.monte_carlo(out.parent_action) 
            return 
        elif self.oPlayer.name == 'Random 1' or self.oPlayer.name == 'Random 2' or self.oPlayer.name == 'Monte Carlo Rollout':
            inpt = random.randint(1,3)
            print('Chooses: {}'.format(inpt))
        else:
            inpt = input('Chooses: ') #1,2,3
        lst = [a, b, c]
        self.choice = inpt
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
        print('Knowledge. Trade: {}  Decision {} Choice {} Winner {} '.format(self.trade, self.decision, self.choice, self.winner)) 

    def print_table(self):
        table = [self.deck.deck_id(), self.player1.ptable(), self.player2.ptable()]
        return table

if input('Both Random? ') == 'yes':
    name_player1 = 'Monte Carlo'
    name_player2 = 'Random 2'
else:
    name_player1 = input('Enter Player 1 name:') #Enter 'Random' for random player 
    name_player2 = input('Enter Player 2 name:')
game = HanamikojiEngine(name_player1, name_player2)
game.start()

h = game.print_table()
print(h)
#game.cPlayer.draw(game.deck, 1)
#game.interactive()

class MonteCarloTreeSearchNode():
    def __init__(self, state, original, parent=None, decision = None, parent_action=None):       #sets defauults?
        self.state = state   #Class:Hanamikoji Engine
        self.original_state = original
        self.parent = parent   #Class:Hanamikoji Engine
        self.decision = decision   #trade or move
        self.choice = 0       #will be 1,2,3
        self.parent_action = parent_action     #[[cards],[move]]
        self.children = []      #Class: list of Hanamikoji Engine
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None       #Class: list [[],[]]
        self.choices = []
        return

    def untried_actions(self):
        self._untried_actions = self.get_legal_actions(self.original_state)
        return self._untried_actions

    def n(self):
        return self._number_of_visits

    def q(self):
        return self._results[1] #times won

    def expand(self):
        self.original_state.player1.name = 'Monte Carlo Expand'
        action = self._untried_actions.pop()
        if action[1][0] == 'Trade 2x2':
            next_node = copy.deepcopy(self)
            next_node.decision = 'trade'
            next_node.original_state.decision = 'trade'
            if len(next_node.original_state.trade) != 0:
                next_node.original_state.trade = []
            for card in action[0]:
                next_node.original_state.trade.append(card[0])
                next_node.original_state.trade.append(card[1])
            next_node.original_state.cPlayer.moves[3][1] = 1
            child_node = MonteCarloTreeSearchNode(next_node.original_state, copy.deepcopy(next_node.original_state), parent=self, decision='trade', parent_action=action)

        elif action[1][0] == 'Trade 3x1' :
            next_node = copy.deepcopy(self)
            next_node.decision = 'trade'
            next_node.original_state.decision = 'trade'
            if len(next_node.original_state.trade) != 0:
                next_node.original_state.trade = []
            for card in action[0]:
                next_node.original_state.trade.append(card)
            next_node.original_state.cPlayer.moves[2][1] = 1
            child_node = MonteCarloTreeSearchNode(next_node.original_state, copy.deepcopy(next_node.original_state), parent=self, decision='trade', parent_action=action)
        elif self.decision == 'trade':
            next_node = copy.deepcopy(self)
            next_node.original_state.choice = action[0]
            next_node.exp_move(action)
            child_node = MonteCarloTreeSearchNode(next_node.original_state, copy.deepcopy(next_node.original_state), parent=self, decision='move', parent_action=action)

        elif self.decision == 'move':
            next_node = copy.deepcopy(self)
            next_node.exp_move(action)
            child_node = MonteCarloTreeSearchNode(next_node.original_state, copy.deepcopy(next_node.original_state), parent=self, decision = 'move', parent_action=action)
        self.children.append(child_node)
        return child_node 

    def is_terminal_node(self):
        return self.is_game_over()

    def rollout(self):
        while self.state.winner == 0:
            self.state.player1.name = 'Monte Carlo Rollout'
            possible_moves = self.get_legal_actions(self.state)
            if len(possible_moves) == 0:
                self.state.show_table()
            action = self.rollout_policy(possible_moves)
            self.move(action) 
        return self.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.   #q
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def decide(self):
        return self._untried_actions.pop()

    def best_child(self, printt, c_param):
        fractions = [[int(c.q()), int(c.n())] for c in self.children]
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        rollout_options = [ [c.parent_action, c.original_state.cPlayer.name, c.original_state.choice] for c in self.children]
        rounded_list = [ round(elem, 3) for elem in choices_weights ]
        self.choices = rounded_list
        if printt == 'print':   
            print('fractions')
            print(rounded_list)
            print(fractions)
            for i in range(0,len(self.children)):
                childs.append([rollout_options[i], fractions[i], rounded_list[i]])

        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        if len(possible_moves) == 0:
            print('no moves')
            print(self.state.player1.moves)
            print(self.state.player2.moves)
        else:
            return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self     #????????????????????????
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child('no', C_SEL)
                current_node.untried_actions()
        return current_node

    def best_action(self):
        ll = len(self._untried_actions)
    
        if ll > 50:
            S = N_SIM_B
        elif ll > 4 and ll < 25:
            S = N_SIM_M
        else:
            S = N_SIM_T
        print(S)
        print('\n \n best action {} \n \n'.format(len(self._untried_actions)))

        for i in range(S):
            print('simulation {} '.format(i))
            v = self._tree_policy()   #checks if it's terminal, if not return new node expanded, if yes return best child??
            reward = v.rollout()      #go till the end randomly, return 1 or -1
            v.backpropagate(reward)   #update fractions
            gc.collect()
        return self.best_child('print', C_CHOICE)        #gives MonteCarlo node back

    def print_children(self):
        print('family time')
        for child in self.children:
            print(child.parent_action)
            child.original_state.show_table()

    def get_legal_actions(self, state): 
        
            legal_actions = []
            if state.decision == 'trade':
                if len(state.trade) == 3:
                    legal_actions.append([1, 'trade 3x1'])
                    legal_actions.append([2, 'trade 3x1'])
                    legal_actions.append([3, 'trade 3x1'])
                elif len(state.trade) == 4:
                    legal_actions.append([1, 'trade 2x2'])
                    legal_actions.append([2, 'trade 2x2'])
            
            elif state.decision == 'move' or state.decision == None :
                state.trade = []
                for m in state.cPlayer.moves:
                    if m[1] == 0:
                        if m[0] == 'Trade 2x2':
                            cCards = state.cPlayer.hand.deck_id()
                            combi = list((combinations(cCards, m[2])))
                            pairs = []
                            double_pairs = []
                            for comb in combi:
                                pairs.append(list(set(combinations(comb, 2))))
                            for i in range(0,len(pairs)):
                                for pair in pairs[i]:
                                    k = list(combi[i])
                                    k.remove(pair[0])
                                    k.remove(pair[1])
                                    double_pair = [k, list(pair)]
                                    double_pairs.append(double_pair)

                            for d_pair in double_pairs :
                                legal_actions.append([d_pair, m])

                        else:
                            cCards = state.cPlayer.hand.deck_id()
                            combi = list(set(combinations(cCards, m[2])))
                            for mov in combi :
                                legal_actions.append([list(mov), m])
                        #find move, do all play combinations
                    else:
                        pass 
            return legal_actions

    def is_game_over(self):
        return self.original_state.winner != 0 

    def game_result(self):
        return self.state.winner
    
    def exp_move(self, action):
        l = self.original_state.monte_carlo(action)

        if len(self.state.deck.cards) != 0:
            self.original_state.cPlayer.draw(self.original_state.deck, 1)
        if l == 0:
            self.original_state = HanamikojiEngine(name_player1, name_player2)
            self.original_state.start()
            self.original_state.cPlayer.draw(self.original_state.deck, 1)        

    def move(self,action):  #action: [[],[]]
        l = self.state.monte_carlo(action)

        if self.state.player1.name == 'Monte Carlo Rollout' and self.state.decision == 'trade':
            possible_moves = self.get_legal_actions(self.state)
            action = self.rollout_policy(possible_moves)
            l = self.state.monte_carlo(action)
        if len(self.state.deck.cards) != 0:
            self.state.cPlayer.draw(self.state.deck, 1)
        if l == 0:
            self.state = HanamikojiEngine(name_player1, name_player2)
            self.state.start()
            self.state.cPlayer.draw(self.state.deck, 1)


actual_game = []

def main(decision, stat):
        root = MonteCarloTreeSearchNode(stat, copy.deepcopy(stat),  None, decision)  #root: does this mean that this is only applicable to the very start or is parent(None) for any new decision
        root.original_state.cPlayer.draw(root.original_state.deck, 1)
        root._untried_actions = root.untried_actions()
        selected_node = root.best_action()
        return selected_node   #yes: state where best action has been done--------no:should be a node. from this we can extract the move? (it's the best child)


def MC_vs_random(gam):
    for i in range(1,5):
        print('\n 000000000000000000000000000000000000000000000000000000000000000000000000000 {}'.format(i))
        gam.show_table()
        print(gam.player1.moves)
        print(gam.player2.moves)
        gam.new_round_p()
        out = main('move', gam)  #Each decision has it's own monte Carlo tree, out should be the best child node. Now Idk what it is
        childs.append([i, out.parent_action, out.original_state.cPlayer.name])
        childs.append(out.original_state.print_table())
        print('out')
        gam = out.original_state
        gam.show_table()
        if gam.decision == 'trade':
            gam.random_move()
            gam.show_table()
            childs.append(gam.print_table())
        gam.cPlayer.draw(gam.deck, 1)
        gam.random_move()
        print('round over')
        gam.show_table()
        childs.append(gam.print_table())

    return gam

def history(node_list):
    print('history time')
    for node in node_list:
        node.state.show_table()    

out = MC_vs_random(game)
print('over?')
out.show_table()
print(out.player1.moves)
print(out.player2.moves)
print('the end')
out.win()
print(out.winner)
out.print_winner(childs)
out.show_table()





with open('file.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(childs)



#if state.winner == 0:  
#    new_state = HanamikojiEngine(name_player1, name_player2)
#    new_state.start()
#    new_state.cPlayer.draw(new_state.deck, 1)
#    MC_vs_random(new_state)

#print(out.parent.choices)
#print(out.parent_action) #is monte carlo tree search: to get move find parent_action

#with open("game_history.json", "w") as file:
#    json.dump(all_moves, file)
    
#with open("choice_history.json", "w") as file:
#    json.dump(all_choices, file)   #list of lists: each list is the choice array for every child. The only relevant one is the last one?

#with open("node_history.json", "w") as file:
#    json.dump(out.parent_action, file)
#    json.dump(out.parent.choices, file)
# 2p, 2r, 2y, 3b, 3o, 4g, 5b

#print('---------------------------1----------------------------------------------')
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~3~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#Back: RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE



