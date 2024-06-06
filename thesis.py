#references: https://docs.replit.com/tutorials/python/build-card-game-pygame
import random
from itertools import combinations
import copy
import json
from colorama import Back, Back, init
init(autoreset=True)

SEED = 11
import os
os.environ["PYTHONHASHSEED"] = str(SEED)

import numpy as np
from collections import defaultdict
np.random.seed(SEED)
random.seed(SEED)   #11 = win first round, 10 = not

cunter = [0]
cnter = [0]

carryon = [0, 0, 0, 0, 0, 0, 0]
game_round = [0]
num_phases = 4
pointer = [0]
all_moves = []
all_choices = []
node_history = []
S = 1000


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
            print('last card')

        elif deck.last_draw == self.name or (deck.last_draw == 'Monte Carlo' and self.name == 'Monte Carlo Expand'):
            all_moves.append(['repeat', deck.last_draw, self.name])
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
            self.winner = 1
            w_name = self.player1.name
        elif points2 >= 11:
            print('Player 2 wins')
            self.winner = -1
            w_name = self.player2.name
        elif geishas1 >= 4:
            print('Player 1 wins')
            self.winner = 1
            w_name = self.player1.name
        elif geishas2 >= 4:
            print('Player 2 wins')
            self.winner = -1
            w_name = self.player2.name
        else:
            print('No winner yet') 
            #round2 = HanamikojiEngine(name_player1, name_player2)
            #round2.start()
        all_moves.append([self.winner, w_name])
        
    def interactive(self):
        game_round[0] += 1
        for i in range(0,num_phases):
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

    def play_stored(self):
        print('Play stored cards')
        if self.player1.store.cards != []:
            move(self.player1.store, self.player1.played, self.player1.store.cards[0].id)
        if self.player2.store.cards != []:
            move(self.player2.store, self.player2.played, self.player2.store.cards[0].id)
        
    def random_move(self):
        print('random move')
        movs = ['Store', 'Discard', 'Trade 3x1', 'Trade 2x2']
        l = random.randint(0, 3) 
        select = []
        action = []
        
        all_moves.append(['random move' , action, self.cPlayer.name])
        if self.decision == 'trade':
            if len(self.trade) == 4:
                inpt = random.randint(1,2)
                self.trade2x2_inpt(self.trade, inpt)
                self.decision = 'move'
                self.switch_players()
                return
            elif len(self.trade) == 3:
                inpt = random.randint(1,3)
                self.trade3x1_inpt(self.trade, inpt)
                self.decision = 'move'
                self.switch_players()
                return

        elif self.cPlayer.moves[0][1] == 1 and self.cPlayer.moves[1][1] == 1 and self.cPlayer.moves[2][1] == 1 and self.cPlayer.moves[3][1] == 1:
            print('all moves used')

        elif movs[l] == 'Store' and self.cPlayer.moves[0][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 1)
            print('Store: {}'. format(select[0].id))
            self.store(select[0].id)
            self.cPlayer.moves[0][1] = 1
            action.append(movs[l])
        
        elif movs[l] == 'Discard' and self.cPlayer.moves[1][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 2)
            print('Discard: {} {}'. format(select[0].id, select[1].id))
            self.discard(select[0].id, select[1].id)
            self.cPlayer.moves[1][1] = 1
            action.append(movs[l])
        
        elif movs[l] == 'Trade 3x1' and self.cPlayer.moves[2][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 3)
            print('Trade 3x1: {} {} {}'. format(select[0].id, select[1].id, select[2].id))
            self.cPlayer.moves[2][1] = 1
            self.trade3x1(select[0].id, select[1].id, select[2].id)
            action.append(movs[l])
            return 

        elif movs[l] == 'Trade 2x2' and self.cPlayer.moves[3][1] == 0:   
            select = random.sample(self.cPlayer.hand.cards, 4)
            print('Trade 2x2: {} {} {} {}'. format(select[0].id, select[1].id, select[2].id, select[3].id))
            self.cPlayer.moves[3][1] = 1
            self.trade2x2(select[0].id, select[1].id, select[2].id, select[3].id)
            action.append(movs[l])
            return 
        else:
            print('Move already used')
            cnter[0] += 1 
            print(self.cPlayer.moves)
            if cnter[0] < 10:
                self.random_move()

        for card in select:
            action.append(card.id)
    
        all_moves.append(['random move' , action, self.cPlayer.name])
        

    def monte_carlo(self, action):   #action :[[cards], [move]]            [[['3o', '2p'], ['5b', '3b']], ['Trade2x2', 0, 4]]
        #print('\n MC action:  {} {}'.format(action, self.cPlayer.name))
        all_moves.append(['Monte Carlo ' , action, self.cPlayer.name])

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
        print('{} Discards  '.format(self.cPlayer.name), end=' ')
        mul_move(self.cPlayer.hand, self.cPlayer.discarded, [inpt1, inpt2])

    def trade3x1_inpt(self, trade, inpt):
        choice = [trade.pop(int(inpt)-1)]
        mul_move(self.cPlayer.hand, self.oPlayer.played, choice)
        mul_move(self.cPlayer.hand, self.cPlayer.played, trade)

    def trade2x2_inpt(self, trade, inpt):   #trade: [a1, a2, b1, b2]
        lst = [[trade[0], trade[1]], [trade[2], trade[3]]]
        choice = lst.pop(int(inpt)-1)
        #print('2x2inpt choose{} from  '.format(choice))
        #self.cPlayer.hand.printdeck()
        mul_move(self.cPlayer.hand, self.oPlayer.played, choice)
        mul_move(self.cPlayer.hand, self.cPlayer.played, lst[0])

    def trade2x2(self, a1, a2, b1, b2):
        print('{}'.format(self.oPlayer.name), end=' ')
        if self.oPlayer.name == 'Monte Carlo Expand':
            self.decision = 'trade'
            self.trade = [a1, a2, b1, b2]
            coy = copy.deepcopy(self)
            new_node = MonteCarloTreeSearchNode(state = self, original = coy ,parent = None, decision= 'trade')  #ROOT!
            new_node.untried_actions()  #indeed, 1,2,3
            node_history.append(copy.deepcopy(new_node))
            all_moves.append(['interesting 2x2 trade', self.trade, self.oPlayer.name, self.cPlayer.name])
            sel_node = new_node.best_action()    #returns state with trade done, sel_node is a node
            self.monte_carlo(sel_node.parent_action) 
            #all_moves.append(['Best child trade', sel_node.parent_action, sel_node.state.cPlayer.name])
            return 
            #mc_trade
            #need to make a Monte Carlo agent that can analyze the outcomes of trades. 
            #This means making a new node in the game tree where decisions happen - expand game tree. Or Make a different MC agent just for decisions
        elif self.oPlayer.name == 'Random 2' or self.oPlayer.name == 'Random 1' or self.oPlayer.name == 'Monte Carlo Rollout':
            inpt = random.randint(1,2)
            print('Chooses: {}'.format(inpt))
            all_moves.append([inpt, self.oPlayer.name])
        else:
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
            new_node = MonteCarloTreeSearchNode(state = self, original = copy.deepcopy(self) ,parent = None, decision= 'trade')  #ROOT!
            new_node.untried_actions()  #indeed, 1,2,3
            node_history.append(copy.deepcopy(new_node))
            all_moves.append(['interesting 3x1 trade', self.trade, self.oPlayer.name, self.cPlayer.name])
            sel_node = new_node.best_action()    #returns state with trade done, sel_node is a node
            self.monte_carlo(sel_node.parent_action) 
            #all_moves.append(['Best child trade', sel_node.parent_action, sel_node.state.cPlayer.name])
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

if input('Both Random? ') == 'yes':
    name_player1 = 'Monte Carlo'
    name_player2 = 'Random 2'
else:
    name_player1 = input('Enter Player 1 name:') #Enter 'Random' for random player 
    name_player2 = input('Enter Player 2 name:')
game = HanamikojiEngine(name_player1, name_player2)
game.start()
#game.cPlayer.draw(game.deck, 1)
#game.interactive()

class MonteCarloTreeSearchNode():
    def __init__(self, state, original, parent=None, decision = None, parent_action=None):       #sets defauults?
        print('new node')
        all_moves.append(['new node', decision, parent_action])
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
        print('untried actions')
        self._untried_actions = self.get_legal_actions()
        return self._untried_actions

    def n(self):
        return self._number_of_visits

    def q(self):
        return self._results[1] #times won

    def expand(self):
        print('expand open')
        self.state.player1.name = 'Monte Carlo Expand'
        action = self._untried_actions.pop()
        #self.state.show_table()
        #print(action)
        if action[1][0] == 'Trade 2x2':
            #print('expand 2x2')
            next_node = copy.deepcopy(self)
            next_node.decision = 'trade'
            next_node.state.decision = 'trade'
            if len(next_node.state.trade) != 0:
                next_node.state.trade = []
            for card in action[0]:
                next_node.state.trade.append(card[0])
                next_node.state.trade.append(card[1])
            next_node.state.cPlayer.moves[3][1] = 1
            child_node = MonteCarloTreeSearchNode(next_node.state, copy.deepcopy(next_node.state), parent=self, decision='trade', parent_action=action)
            node_history.append(copy.deepcopy(child_node))

        elif action[1][0] == 'Trade 3x1' :
            #print('expand 3x1')
            next_node = copy.deepcopy(self)
            next_node.decision = 'trade'
            next_node.state.decision = 'trade'
            if len(next_node.state.trade) != 0:
                next_node.state.trade = []
            for card in action[0]:
                next_node.state.trade.append(card)
            next_node.state.cPlayer.moves[2][1] = 1
            child_node = MonteCarloTreeSearchNode(next_node.state, copy.deepcopy(next_node.state), parent=self, decision='trade', parent_action=action)
            node_history.append(copy.deepcopy(child_node))

        elif self.decision == 'trade':
            #print('expand trade')
            next_node = copy.deepcopy(self)
            next_node.state.choice = action[0]
            next_node.move(action)
            self.decision = 'move'
            next_state = copy.deepcopy(self.state)  #BIG RED FLAG
            child_node = MonteCarloTreeSearchNode(next_state, copy.deepcopy(next_node.state), parent=self, decision='move', parent_action=action)
            node_history.append(copy.deepcopy(child_node))

        elif self.decision == 'move':
            #print('expand move')
            next_node = copy.deepcopy(self)
            next_node.move(action)
            child_node = MonteCarloTreeSearchNode(next_node.state, copy.deepcopy(next_node.state), parent=self, decision = 'move', parent_action=action)
            node_history.append(copy.deepcopy(child_node))
        self.children.append(child_node)
        print('expand close')
        return child_node 

    def is_terminal_node(self):
        print('terminal?')
        print(self.is_game_over())
        return self.is_game_over()

    def rollout(self):
        print('rollout')
        while self.state.winner == 0:
            print('rolling')
            self.state.player1.name = 'Monte Carlo Rollout'
            possible_moves = self.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            self.move(action) 
        #print('rollout close')
        return self.game_result()

    def backpropagate(self, result):
        #print('backpropagate')
        self._number_of_visits += 1.
        self._results[result] += 1.   #q
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def decide(self):
        return self._untried_actions.pop()

    def best_child(self, c_param=0.2):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        #print(' A CHILD!')
        #self.children[1].state.show_table()
        #self.children[1].original_state.show_table()
        rounded_list = [ round(elem, 3) for elem in choices_weights ]
        self.choices = rounded_list
        all_choices.append(rounded_list)
        #print(c.q())
        #print(c.n())
        print(choices_weights)
        #all_moves.append(['Best Child', self.children[np.argmax(choices_weights)], choices_weights, len(self.children)])
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        if len(possible_moves) == 0:
            print('no moves')
            print(self.state.player1.moves)
            print(self.state.player2.moves)
            print_all()
        else:
            return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self     #????????????????????????
        print(len(current_node._untried_actions))
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                print('is fully expanded')
                current_node = current_node.best_child()
                print(current_node._untried_actions)
                current_node.original_state.show_table()
        return current_node

    def best_action(self):
        simulation_no = 20

        for i in range(simulation_no):
            print('simulation {} '.format(i))
            all_moves.append(['simulation', i])
            v = self._tree_policy()   #checks if it's terminal, if not return ned node expanded, if yes return best child??
            reward = v.rollout()      #go till the end randomly, return 1 or -1
            print(reward)
            v.backpropagate(reward)   #update fractions
            all_moves.append('Backpropagate')
        print(len(self.children))
        print('a family')
        self.print_children()
        return self.best_child(c_param=0.1)        #gives MonteCarlo node back

    def print_children(self):
        for child in self.children:
            child.original_state.show_table()

    def get_legal_actions(self): 
            #print('getlegalactions')
        
            legal_actions = []
            if self.state.decision == 'trade':
                #print('legal actions trade')
                #print(self.state.trade)   #should be [cards]
                if len(self.state.trade) == 3:
                    legal_actions.append([1, 'trade 3x1'])
                    legal_actions.append([2, 'trade 3x1'])
                    legal_actions.append([3, 'trade 3x1'])
                elif len(self.state.trade) == 4:
                    legal_actions.append([1, 'trade 2x2'])
                    legal_actions.append([2, 'trade 2x2'])
            
            elif self.state.decision == 'move' or self.state.decision == None :
                #print('legal actions move')
                self.state.trade = []
                for m in self.state.cPlayer.moves:
                    if m[1] == 0:
                        if m[0] == 'Trade 2x2':
                            cCards = self.state.cPlayer.hand.deck_id()
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
                            cCards = self.state.cPlayer.hand.deck_id()
                            combi = list(set(combinations(cCards, m[2])))
                            for mov in combi :
                                legal_actions.append([list(mov), m])
                        #find move, do all play combinations
                    else:
                        pass 
            #print(len(legal_actions))
            return legal_actions

    def is_game_over(self):
        return self.original_state.winner != 0 

    def game_result(self):
        return self.state.winner

    def move(self,action):  #action: [[],[]]
        l = self.state.monte_carlo(action)

        if self.state.player1.name == 'Monte Carlo Rollout' and self.state.decision == 'trade':
            #print('rollout pt 2')
            possible_moves = self.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            l = self.state.monte_carlo(action)
        if len(self.state.deck.cards) != 0:
            self.state.cPlayer.draw(self.state.deck, 1)
        if l == 0:
            print('No winner, new round')
            self.state = HanamikojiEngine(name_player1, name_player2)
            self.state.start()
            self.state.cPlayer.draw(self.state.deck, 1)


actual_game = []
state = copy.deepcopy(game)      #not sure if necessary
def main(decision):
        root = MonteCarloTreeSearchNode(state, copy.deepcopy(state),  None, decision)  #root: does this mean that this is only applicable to the very start or is parent(None) for any new decision
        root.state.cPlayer.draw(root.state.deck, 1)
        root._untried_actions = root.untried_actions()
        node_history.append(copy.deepcopy(root))
        selected_node = root.best_action()
        return selected_node   #yes: state where best action has been done--------no:should be a node. from this we can extract the move? (it's the best child)


def MC_vs_random(game):
    for i in range(0,2):
        print('\n 000000000000000000000000000000000000000000000000000000000000000000000000000 {}'.format(i))
        game.show_table()
        print(game.player1.moves)
        print(game.player2.moves)
        game.new_round_p()
        all_moves.append(['Round', i])
        out = main('move')  #Each decision has it's own monte Carlo tree, out should be the best child node. Now Idk what it is
        game.monte_carlo(out.parent_action)
        if game.decision == 'trade':
            game.random_move()
        game.show_table()
        game.cPlayer.draw(state.deck, 1)
        game.random_move()
        #print_all()
        print('round over')
        #history(node_history)

def history(node_list):
    print('history time')
    for node in node_list:
        node.state.show_table()        

MC_vs_random(state)
state.show_table()
print(state.player1.moves)
print(state.player2.moves)
print('the end')
state.win()
#if state.winner == 0:  
#    new_state = HanamikojiEngine(name_player1, name_player2)
#    new_state.start()
#    new_state.cPlayer.draw(new_state.deck, 1)
#    MC_vs_random(new_state)

#print(out.parent.choices)
#print(out.parent_action) #is monte carlo tree search: to get move find parent_action
#print(all_moves)

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
