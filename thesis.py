#references: https://docs.replit.com/tutorials/python/build-card-game-pygame
import random
from itertools import combinations
import copy
import json
from colorama import Back, Back, init
init(autoreset=True)

import numpy as np
from collections import defaultdict
SEED = 11
#np.random.seed(SEED)
#random.seed(SEED)   #11 = win first round, 10 = not

carryon = [0, 0, 0, 0, 0, 0, 0]
game_round = [0]
num_phases = 4
pointer = [0]
all_moves = []
all_choices = []
S = 10000

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
        print(' {} draw'.format(self.name))
        deck.deal(self.hand, num)  #take n cards from deck
        self.hand.printdeck()
    
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
            self.winner = 1
        elif points2 >= 11:
            print('Player 2 wins')
            self.winner = -1
        elif geishas1 >= 4:
            print('Player 1 wins')
            self.winner = 1
        elif geishas2 >= 4:
            print('Player 2 wins')
            self.winner = -1
        else:
            print('No winner yet') 
            #round2 = HanamikojiEngine(name_player1, name_player2)
            #round2.start()
        all_moves.append(self.winner)
        
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
                if self.cPlayer.name == 'Random 1' or self.cPlayer.name == 'Random 2':
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
        movs = ['Store', 'Discard', 'Trade 3x1', 'Trade 2x2']
        l = random.randint(0, 3)
        
        if movs[l] == 'Store' and self.cPlayer.moves[0][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 1)
            print('Store: {}'. format(select[0].id))
            self.store(select[0].id)
            self.cPlayer.moves[0][1] = 1
        
        elif movs[l] == 'Discard' and self.cPlayer.moves[1][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 2)
            print('Discard: {} {}'. format(select[0].id, select[1].id))
            self.discard(select[0].id, select[1].id)
            self.cPlayer.moves[1][1] = 1
        
        elif movs[l] == 'Trade 3x1' and self.cPlayer.moves[2][1] == 0:
            select = random.sample(self.cPlayer.hand.cards, 3)
            print('Trade 3x1: {} {} {}'. format(select[0].id, select[1].id, select[2].id))
            self.trade3x1(select[0].id, select[1].id, select[2].id)
            self.cPlayer.moves[2][1] = 1

        elif movs[l] == 'Trade 2x2' and self.cPlayer.moves[3][1] == 0:   
            select = random.sample(self.cPlayer.hand.cards, 4)
            print('Trade 2x2: {} {} {} {}'. format(select[0].id, select[1].id, select[2].id, select[3].id))
            self.trade2x2(select[0].id, select[1].id, select[2].id, select[3].id)
            self.cPlayer.moves[3][1] = 1
        else:
            print('Move already used')
            
            print(self.cPlayer.moves)
            self.random_move()

    def monte_carlo(self, action):   #action :[[cards], [move]]            [[['3o', '2p'], ['5b', '3b']], ['Trade2x2', 0, 4]]
        print(action)
        all_moves.append(action)

        if action[1][0] == 'Store' and self.cPlayer.moves[0][1] == 0:
            self.store(action[0][0])
            self.cPlayer.moves[0][1] = 1

        elif action[1][0] == 'Discard' and self.cPlayer.moves[1][1] == 0:
            self.discard(action[0][0], action[0][1])
            self.cPlayer.moves[1][1] = 1
           
        elif action[1][0] == 'Trade 3x1' and self.cPlayer.moves[2][1] == 0:
            self.trade3x1(action[0][0], action[0][1], action[0][2])
            self.cPlayer.moves[2][1] = 1

        elif action[1][0] == 'Trade 2x2' and self.cPlayer.moves[3][1] == 0:   
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

    def redirect(self, inpt):
        if inpt == 'Random 1' or inpt == 'Random 2':
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

    def trade2x2(self, a1, a2, b1, b2):
        print('{}'.format(self.oPlayer.name), end=' ')
        if self.oPlayer.name == 'Monte Carlo':
            pass
            #mc_trade
            #need to make a Monte Carlo agent that can analyze the outcomes of trades. 
            #This means making a new node in the game tree where decisions happen - expand game tree. Or Make a different MC agent just for decisions
        elif self.oPlayer.name == 'Random 2' or self.oPlayer.name == 'Random 1':
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
        if self.oPlayer.name == 'Random 1' or self.oPlayer.name == 'Random 2':
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

if input('Both Random? ') == 'yes':
    name_player1 = 'Random 1'
    name_player2 = 'Random 2'
else:
    name_player1 = input('Enter Player 1 name:') #Enter 'Random' for random player 
    name_player2 = input('Enter Player 2 name:')
game = HanamikojiEngine(name_player1, name_player2)
game.start()
#game.cPlayer.draw(game.deck, 1)
#game.interactive()

#monte carlo tree search


class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, decision = None, trade = None, parent_action=None):       #sets defauults?
        print('new node')
        self.state = state   #Class:Hanamikoji Engine
        self.parent = parent   #Class:Hanamikoji Engine
        self.decision = decision   #trade or move
        self.trade = trade          #[cards] 
        self.parent_action = parent_action     #[[cards],[move]]
        self.children = []      #Class: list of Hanamikoji Engine
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None       #Class: list [[],[]]
        #self._untried_actions = self.untried_actions()
        self.choices = []
        return

    def untried_actions(self):
        print('untried actions')
        self._untried_actions = self.get_legal_actions()
        return self._untried_actions

    def print_history(self):
        print('parent history')
        if self.parent :
            self.parent.state.show_table()
            self.parent.print_history()
        else:
            print(self.parent)

    def n(self):
        return self._number_of_visits

    def q(self):
        return self._results[1] #times won

    def expand(self):
        print('expand open')
        action = self._untried_actions.pop()
        next_state = self.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self, decision = None, trade = None, parent_action=action)
        self.children.append(child_node)
        print('expand close')
        return child_node 

    def is_terminal_node(self):
        print('is terminal')
        return self.is_game_over()

    def rollout(self):
        print('rollout')
        current_rollout_state = self

        #while not current_rollout_state.is_game_over():
        while self.state.winner == 0:
            print('random move')
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state.state = current_rollout_state.move(action)
        print('rollout close')
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        print('backpropagate')
        self._number_of_visits += 1.
        self._results[result] += 1.   #q
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        print('isfullyexpanded')
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.2):
        print('bestchild')
        #print(len(self.children))
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        rounded_list = [ round(elem, 3) for elem in choices_weights ]
        self.choices = rounded_list
        all_choices.append(rounded_list)
        #print(c.q())
        #print(c.n())
        #print(choices_weights)
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        print('rollout policy')
        print(len(possible_moves))
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        print('tree policy')
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        print('bestaction')
        simulation_no = S

        for i in range(simulation_no):
            v = self._tree_policy()   #checks if it's terminal, if not expand, if yes return best child??
            reward = v.rollout()      #go till the end randomly, return 1 or -1
            v.backpropagate(reward)   #update fractions
        
        return self.best_child(c_param=0.1)

    def get_legal_actions(self): 
            print('getlegalactions')
            legal_actions = []
            if self.decision == 'trade':
                pass
            elif self.decision == 'move':
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
            #print(legal_actions)
            print(len(legal_actions))
            return legal_actions

    def is_game_over(self):
        print('isgameover?')
        print(self.state.winner)
        return self.state.winner != 0 

    def game_result(self):
        print('gameresult')
        return self.state.winner

    def move(self,action):  #action: [[],[]]
        print('move')
        new_state = copy.deepcopy(self.state)
        l = new_state.monte_carlo(action)
        if len(new_state.deck.cards) != 0:
            new_state.cPlayer.draw(new_state.deck, 1)
        if l == 0:
            print('No winner, new round')
            new_state = HanamikojiEngine(name_player1, name_player2)
            new_state.start()
            new_state.cPlayer.draw(new_state.deck, 1)
        return new_state


actual_game = []
state = copy.deepcopy(game)      #not sure if necessary
def main(decision):
        root = MonteCarloTreeSearchNode(state, None, decision)  #root: does this mean that this is only applicable to the very start or is parent(None) for any new decision
        root.state.cPlayer.draw(root.state.deck, 1)
        root._untried_actions = root.untried_actions()
        selected_node = root.best_action()
        print(root.choices)

        return selected_node   #should be a node. from this we can extract the move? (it's the best child)


def MC_vs_random(game):
    for i in range(0,4):
        print('0000000000000000000000000000000000000000000000000000000000000000000000000000000')
        print(i)
        print('actual game')
        print(actual_game)
        out = main()
        game.show_table()
        actual_game.append(out.parent_action)
        game.monte_carlo(out.parent_action)
        game.show_table()
        game.cPlayer.draw(state.deck, 1)
        game.random_move()
        game.switch_players()
        print('last draw')
        game.show_table()

MC_vs_random(state)
state.win()
if state.winner == 0:  
    new_state = HanamikojiEngine(name_player1, name_player2)
    new_state.start()
    new_state.cPlayer.draw(new_state.deck, 1)
    MC_vs_random(new_state)





#print(out.parent.choices)
#print(out.parent_action) #is monte carlo tree search: to get move find parent_action
#print(all_moves)

with open("game_history.json", "w") as file:
    json.dump(all_moves, file)
    
with open("choice_history.json", "w") as file:
    json.dump(all_choices, file)   #list of lists: each list is the choice array for every child. The only relevant one is the last one?

#with open("node_history.json", "w") as file:
#    json.dump(out.parent_action, file)
#    json.dump(out.parent.choices, file)
# 2p, 2r, 2y, 3b, 3o, 4g, 5b

#print('---------------------------1----------------------------------------------')
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print('~~~~~~~~~~~~~~~~~~~~~~~~~~3~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#Back: RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
