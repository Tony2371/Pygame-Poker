from random import shuffle
from operator import itemgetter
from itertools import groupby
import pygame


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

    #---------- GUI functions ----------
    def draw_card(self):
        if self.showing:
            self.card_image = pygame.transform.scale(pygame.image.load("deck_images/{0}{1}.jpg".format(self.value,self.suit)),(128//3, 178//3))
            return self.card_image
        else:
            self.card_image = pygame.transform.scale(pygame.image.load("deck_images/back.jpg"),(128//3, 178//3))
            return self.card_image

class StandardDeck(list):
    def __init__(self):
        self.shuffled = False
        suits = ["s","h","d","c"]
        #suits = ["\u2660", "\u2665", "\u2666", "\u2663"]
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
        [shuffle(self) for x in range(71)]
        print("Deck shuffled")
        self.shuffled = True

class Player(object):   
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.val_list = []
        self.count_list = []
        self.suit_list = []
        self.chip_amount = 1000
        self.current_bet = 0
        self.ingame = True
        self.made_action = False

        self.combination = [0,0,0]
        # combination takes 3 arguments
        # where first - combination index
        # second - highest card value in combination
        # third - second high card (for two pairs and Full house)
        self.kicker = [0,0,0]
        self.comb_names = {
            1:"High Card",
            2:"Pair",
            3:"Two pairs",
            4:"Three of a kind",
            5:"Straight",
            6:"Flush",
            7:"Full house",
            8:"Four of a kind",
            9:"Straight flush"}

        # GUI variables and functions
        self.surface = pygame.Surface(((128//3)*2+30, 200))

    def draw_player_surface(self, main_window, coordinates_tuple, players_list):
        main_window.blit(self.surface,(coordinates_tuple[0],coordinates_tuple[1]))
        self.surface.fill((50,50,50))
        pygame.draw.rect(self.surface, (255, 255, 255), self.surface.get_rect(), 3)
        pygame.draw.line(self.surface,(255,255,255),[0,self.surface.get_height()*0.85],[self.surface.get_width(),self.surface.get_height()*0.85],3)
        if self.ingame:
            self.surface.blit(self.hand[0].draw_card(), (10, 10))
            self.surface.blit(self.hand[1].draw_card(), (20 + 128 // 3, 10))

        f1 = pygame.font.Font(None,16)
        if self.ingame:
            line_1 = f1.render("Player {0}".format(self.name), 1, (255, 255, 255))
            line_2 = f1.render("Chips: {0}".format(self.chip_amount), 1, (255, 255, 255))
            line_3 = f1.render("{0} of {1}".format(self.comb_names[self.combination[0]], self.combination[1]),1,(255,255,255))

            line_5 = f1.render("Current bet:{0}".format(self.current_bet),1, (150,255,150))
        
            self.surface.blit(line_1, (10, 10 * 2 + 178 // 3))
            self.surface.blit(line_2, (10, 10 * 4 + 178 // 3))
            self.surface.blit(line_3, (10, 10 * 6 + 178 // 3))
            
            self.surface.blit(line_5, (10,self.surface.get_height()-20))
        if not self.ingame:
            fold_text =  line_5 = f1.render("Player folded",0, (225,20,20))
            self.surface.blit(fold_text, (10,self.surface.get_height()-23))


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
            if len(self.val_list) >= 5:
                self.kicker[0] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-1]
                self.kicker[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-2]
                self.kicker[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-3]
        
            #1 - High Card
        else:
            self.combination[0] = 1
            self.combination[1] = max(self.val_list)
            if len(self.val_list) >= 5:
                self.kicker[0] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-1]
                self.kicker[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-2]
                self.kicker[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-3]

    def bet(self, bet_amount, board):
        self.chip_amount -= bet_amount
        self.current_bet += bet_amount
        board.bank += bet_amount

    # input is a number where:
    # N = (max(all current bets)-you.current bet)
    # 0 - fold
    # 1 - bet 0 (check)
    # 2 - bet N (call)
    # 3 - bet > N (raise)
    def decision(self, action,players,board):
        if action == "fold":
            self.ingame = False
            self.current_bet = 0
            #self.hand = None
            print(self,"folded")
        elif action == "call":
            print(self,"calls for {0} chips".format(max([x.current_bet for x in players])-self.current_bet))
            self.bet(max([x.current_bet for x in players])-self.current_bet,board)
            self.made_action = True
        elif action == "raise":
            raise_amount = int(input("Raise for:"))
            self.bet(raise_amount,board)
            print(self,"raises for {0} chips".format(raise_amount))
            self.made_action = True
        else:
            print("Enter valid action!")
   
class StandardBoard(list):
    def __init__(self):
        self.bank = 0
        self.game_round = -1
        self.street = "preflop"

        # GUI variables and functions
        self.surface = pygame.Surface((270,140))

    def draw_board_surface(self, main_window):
        main_window.blit(self.surface,((800-self.surface.get_width())//2,230))
        self.surface.fill((15,45,45))
        pygame.draw.rect(self.surface, (50, 50, 190), self.surface.get_rect(), 3)
        if len(self) == 3:
            self.surface.blit(self[0].draw_card(), (10, 70))
            self.surface.blit(self[1].draw_card(), (20 + (128 // 3), 70))
            self.surface.blit(self[2].draw_card(), (30 + 2*(128 // 3), 70))
        if len(self) == 4:
            self.surface.blit(self[0].draw_card(), (10, 70))
            self.surface.blit(self[1].draw_card(), (20 + (128 // 3), 70))
            self.surface.blit(self[2].draw_card(), (30 + 2*(128 // 3), 70))            
            self.surface.blit(self[3].draw_card(), (40 + 3*(128 // 3), 70))
        if len(self) == 5:
            self.surface.blit(self[0].draw_card(), (10, 70))
            self.surface.blit(self[1].draw_card(), (20 + (128 // 3), 70))
            self.surface.blit(self[2].draw_card(), (30 + 2*(128 // 3), 70))            
            self.surface.blit(self[3].draw_card(), (40 + 3*(128 // 3), 70))
            self.surface.blit(self[4].draw_card(), (50 + 4*(128 // 3), 70))

        f1 = pygame.font.Font(None, 35)
        line_1 = f1.render("Current bank: {0}".format(self.bank), 0, (50, 215, 50))

        self.surface.blit(line_1, ((self.surface.get_width()-line_1.get_width())//2,10))



    def blind_bet(self, players, big_blind):
        bb = players[0]
        sb = players[1]
        bb.bet(big_blind,self)
        sb.bet(big_blind//2,self)


