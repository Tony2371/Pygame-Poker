from random import shuffle
from operator import itemgetter
from itertools import groupby

class Card(object):
    def __init__(self, name, value, suit):
        self.value = value
        self.suit = suit
        self.name = name
        self.showing = False
    def __repr__(self):
        if self.showing and self.value <=10:
            return str(self.value)+" of "+self.suit
        elif self.showing:
            return str(self.name)+" of "+self.suit
        else:
            return "Card"

class StandardDeck(list):
    def __init__(self):
        suits = ["\u2660", "\u2665", "\u2666", "\u2663"]
        values = {
        	    "Two":2,
        	    "Three":3,
        	    "Four":4,
        	    "Five":5,
        	    "Six":6,
        	    "Seven":7,
        	    "Eight":8,
        	    "Nine":9,
        	    "Ten":10,
        	    "Jack":11,
        	    "Queen":12,
        	    "King":13,
        	    "Ace":14}
        for name in values:
            for suit in suits:
                self.append(Card(name,values[name],suit))
    
    def __repr__(self):
        return "{0} cards remaining in deck".format(len(self))
    
    def shuffle(self):
        shuffle(self)
        shuffle(self)
        shuffle(self)
        print("Deck shuffled")

class Player(object):   
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.val_list = []
        self.count_list = []
        self.suit_list = []
        self.chip_amount = 1000
        self.current_bet = 0

        self.combination = [0,0,0]
        # combination takes 3 arguments
        # where first - combination index
        # second - highest card value in combination
        # third - second high card (for two pairs and Full house)
        self.kicker = [0,0,0]

    def __repr__(self):
        return str("Player "+self.name)

    def straight_eval(self,card_list):
        data_set = list(set(card_list))
        ranges = []
        for k, g in groupby(enumerate(data_set), lambda x:x[0]-x[1]):
            group = list(map(itemgetter(1),g))
            ranges.append(range(group[0],group[-1]))
            if any(True for x in [len(a) for a in ranges] if x >= 4): 
                return max([x for x in ranges if len(x) >= 4][0])+1
            else:
                return 0
   
    def straight_flush_eval(self, board, suits):
        test = []
        if self.straight_eval(board) != 0 and 5 in [suits.count(x) for x in suits]:
            main_suit = [x for x in suits if suits.count(x)>=5][0]            
            high_card = self.straight_eval(board)
            if suits[board.index(high_card)] == main_suit or suits[::-1][board[::-1].index(high_card)] == main_suit:
                test.append(1)            
            if suits[board.index(high_card-1)] == main_suit or suits[::-1][board[::-1].index(high_card-1)] == main_suit:
                test.append(1)            
            if suits[board.index(high_card-2)] == main_suit or suits[::-1][board[::-1].index(high_card-2)] == main_suit:
                test.append(1)            
            if suits[board.index(high_card-3)] == main_suit or suits[::-1][board[::-1].index(high_card-3)] == main_suit:
                test.append(1)            
            if suits[board.index(high_card-4)] == main_suit or suits[::-1][board[::-1].index(high_card-4)] == main_suit:
                test.append(1)            
            return sum(test)

    def low_straight_flush_eval(self, board, suits):
        test = []
        if 5 in [suits.count(x) for x in suits] and sum([1 for x in set(self.val_list) if x in [2,3,4,5,14]]) == 5:
            main_suit = [x for x in suits if suits.count(x) >= 5][0]
            high_card = 5
            if suits[board.index(high_card)] == main_suit or suits[::-1][board[::-1].index(high_card)] == main_suit:
                test.append(1)
            if suits[board.index(high_card-1)] == main_suit or suits[::-1][board[::-1].index(high_card-1)] == main_suit:
                test.append(1)
            if suits[board.index(high_card-2)] == main_suit or suits[::-1][board[::-1].index(high_card-2)] == main_suit:
                test.append(1)
            if suits[board.index(high_card-3)] == main_suit or suits[::-1][board[::-1].index(high_card-3)] == main_suit:
                test.append(1)
            if suits[board.index(14)] == main_suit or suits[::-1][board[::-1].index(14)] == main_suit:
                test.append(1)
            return sum(test)

    def evaluate(self, board):
        self.val_list = [x.value for x in self.hand]+[x.value for x in board]
        self.count_list = [self.val_list.count(x) for x in self.val_list]
        self.suit_list = [x.suit for x in self.hand]+[x.suit for x in board]
        self.suit_count_list = [self.suit_list.count(x) for x in self.suit_list]

            #9 - Straight flush
        if self.straight_flush_eval(self.val_list, self.suit_list) == 5:
            self.combination[0] = 9
            self.combination[1] = self.straight_eval(self.val_list)

            #9.1 - Low straight flush
        elif self.low_straight_flush_eval(self.val_list, self.suit_list) == 5:
            self.combination[0] = 9
            self.combination[1] = 5           
                  
            #8 - Four of a kind
        elif 4 in self.count_list:
            self.combination[0] = 8
            self.combination[1] = self.val_list[self.count_list.index(4)]
            self.kicker[0] = max([x for x,y in zip(self.val_list,self.count_list) if y == 1])
           
            #7 - Full House
        elif 3 in self.count_list and 2 in self.count_list:
            self.combination[0] = 7
            self.combination[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2 or y == 3])[-1]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2 or y == 3])[0]
           
            #6 - Flush
        elif 5 in [self.suit_list.count(x) for x in self.suit_list] or 6 in [self.suit_list.count(x) for x in self.suit_list] or 7 in [self.suit_list.count(x) for x in self.suit_list]:
            self.combination[0] = 6
            self.combination[1] = max([x for x,y in zip(self.val_list,self.suit_count_list) if y >= 5])
           
            #5 - Straight
        elif self.straight_eval(self.val_list) != 0:
            self.combination[0] = 5
            self.combination[1] = self.straight_eval(self.val_list)

            #5.1 - Low Straight
        elif sum([1 for x in set(self.val_list) if x in [2,3,4,5,14]]) == 5:
            self.combination[0] = 5
            self.combination[1] = 5

            #4 - Three of a kind (Set)
        elif 3 in self.count_list:
            self.combination[0] = 4
            self.combination[1] = self.val_list[self.count_list.index(3)]
            self.kicker[0] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-1]
            #self.kicker[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-2]
      
            #3 - Two Pairs
        elif self.count_list.count(2) >= 4:            
            self.combination[0] = 3
            self.combination[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2])[-1]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2])[-3]
            self.kicker[0] = max([x for x,y in zip(self.val_list,self.count_list) if y == 1])

            #2 - One Pair
        elif len(self.val_list) != len(set(self.val_list)):
            self.combination[0] = 2
            self.combination[1] = self.val_list[self.count_list.index(2)]
            self.kicker[0] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-1]
            self.kicker[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-2]
            self.kicker[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-3]
        
            #1 - High Card
        else:
            self.combination[0] = 1
            self.combination[1] = max(self.val_list)
            self.kicker[0] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-1]
            self.kicker[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-2]
            self.kicker[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-3]

    def bet(self, bet_amount):
        self.chip_amount -= bet_amount
        self.current_bet += bet_amount
        return bet_amount
   
class StandardBoard(list):
    def __init__(self):
        self.bank = 0
        self.game_round = -1

    def blind_bet(self, players, big_blind):
        bb = players[0]
        sb = players[1]
        self.bank += bb.bet(big_blind)
        self.bank += sb.bet(big_blind//2)


