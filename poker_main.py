from random import shuffle

class Card(object):
    def __init__(self, name, value, suit):
        self.value = value
        self.suit = suit
        self.name = name
        self.showing = True
    def __repr__(self):
        if self.showing and self.value <= 10:
            return str(self.value)+" of "+self.suit
        elif self.showing:
            return str(self.name)+" of "+self.suit
        else:
            return "Card"


class StandardDeck(list):
    def __init__(self):
        self.shuffled = False
        #suits = ["\u2660", "\u2665", "\u2666", "\u2663"]
        suits = ["c","d","h","s"]
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
        [shuffle(self) for x in range(7)]
        print("Deck shuffled")
        self.shuffled = True

    def reset(self):
        self.clear()
        self.__init__()

class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.val_list = []
        self.count_list = []
        self.suit_list = []

        self.ingame = True
        self.chip_amount = 1000
        self.current_bet = 0
        self.answered = False
        self.winner = False

        self.combination = [0,0,0,0,0,0]
        # combination takes 6 arguments where:
        # 0 - combination index
        # 1 - highest card value in combination
        # 2 - second high card (for two pairs and Full house)
        # 3-5 - kickers
        self.comb_names = {
            0: "None",
        	1: "High Card",
        	2: "Pair",
        	3: "Two pairs",
        	4: "Three of a kind",
        	5: "Straight",
        	6: "Flush",
        	7: "Full house",
        	8: "Four of a kind",
        	9: "Straight flush"}

    def __repr__(self):
        return str("Player "+self.name)

    def reset(self):
        self.hand.clear()
        self.ingame = True
        self.answered = False
        self.winner = False
        self.current_bet = 0
        self.combination = [0,0,0,0,0,0]

    def straight_eval(self,input_list):
        card_list = sorted(input_list)
        if len(card_list) == 7:
            if card_list[4] == card_list[3]+1 and card_list[3] == card_list[2]+1 and card_list[2] == card_list[1]+1 and card_list[1] == card_list[0]+1:
                return card_list[4]
            elif card_list[5] == card_list[4]+1 and card_list[4] == card_list[3]+1 and card_list[3] == card_list[2]+1 and card_list[2] == card_list[1]+1:
                return card_list[5]
            elif card_list[6] == card_list[5]+1 and card_list[5] == card_list[4]+1 and card_list[4] == card_list[3]+1 and card_list[3] == card_list[2]+1:
                return card_list[6]
            else:
                return 0
        elif len(card_list) == 6:
            if card_list[4] == card_list[3]+1 and card_list[3] == card_list[2]+1 and card_list[2] == card_list[1]+1 and card_list[1] == card_list[0]+1:
                return card_list[4]
            elif card_list[5] == card_list[4]+1 and card_list[4] == card_list[3]+1 and card_list[3] == card_list[2]+1 and card_list[2] == card_list[1]+1:
                return card_list[5]
            else:
                return 0
        elif len(card_list) == 5:
            if card_list[4] == card_list[3]+1 and card_list[3] == card_list[2]+1 and card_list[2] == card_list[1]+1 and card_list[1] == card_list[0]+1:
                return card_list[4]
            else:
                return 0
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
            self.combination = [9,self.straight_eval(self.val_list),0,0,0,0]

            #9.1 - Low straight flush
        elif self.low_straight_flush_eval(self.val_list, self.suit_list) == 5:
            self.combination = [9,5,0,0,0,0]

            #8 - Four of a kind
        elif 4 in self.count_list:
            self.combination = [8,self.val_list[self.count_list.index(4)],0,0,0,0]

            #7 - Full House
        elif self.count_list.count(3) == 6: # this handles two "three of a kind" problem
            self.combination[0] = 7
            self.combination[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 3])[-1]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 3])[-4]
            self.combination[3] = 0
            self.combination[4] = 0
            self.combination[5] = 0
        elif 3 in self.count_list and 2 in self.count_list:
            self.combination[0] = 7
            self.combination[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 3])[-1]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2])[0]
            self.combination[3] = 0
            self.combination[4] = 0
            self.combination[5] = 0

            #6 - Flush
        elif 5 in [self.suit_list.count(x) for x in self.suit_list] or 6 in [self.suit_list.count(x) for x in self.suit_list] or 7 in [self.suit_list.count(x) for x in self.suit_list]:
            self.combination[0] = 6
            self.combination[1] = sorted([x for x,y in zip(self.val_list,self.suit_count_list) if y >= 5])[-1]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.suit_count_list) if y >= 5])[-2]
            self.combination[3] = sorted([x for x,y in zip(self.val_list,self.suit_count_list) if y >= 5])[-3]
            self.combination[4] = sorted([x for x,y in zip(self.val_list,self.suit_count_list) if y >= 5])[-4]
            self.combination[5] = sorted([x for x,y in zip(self.val_list,self.suit_count_list) if y >= 5])[-5]

            #5 - Straight
        elif self.straight_eval(self.val_list) != 0:
            self.combination = [5,self.straight_eval(self.val_list),0,0,0,0]

            #5.1 - Low Straight
        elif sum([1 for x in set(self.val_list) if x in [2,3,4,5,14]]) == 5:
            self.combination = [5,5,0,0,0,0]

            #4 - Three of a kind (Set)
        elif 3 in self.count_list:
            self.combination[0] = 4
            self.combination[1] = self.val_list[self.count_list.index(3)]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-1]
            self.combination[3] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-2]
            self.combination[4] = 0
            self.combination[5] = 0

            #3 - Two Pairs
        elif self.count_list.count(2) == 6: # this handles three "Pairs" problem
            self.combination[0] = 3
            self.combination[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2])[-1]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2])[-3]
            self.combination[3] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2])[-5]
            self.combination[4] = 0
            self.combination[5] = 0
        elif self.count_list.count(2) == 4:
            self.combination[0] = 3
            self.combination[1] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2])[-1]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 2])[-3]
            self.combination[3] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-1]
            self.combination[4] = 0
            self.combination[5] = 0

            #2 - One Pair
        elif len(self.val_list) != len(set(self.val_list)):
            self.combination[0] = 2
            self.combination[1] = self.val_list[self.count_list.index(2)]
            self.combination[2] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-1]
            self.combination[3] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-2]
            self.combination[4] = sorted([x for x,y in zip(self.val_list,self.count_list) if y == 1])[-3]
            self.combination[5] = 0

            #1 - High Card
        else:
            self.combination[0] = 1
            self.combination[1] = sorted(self.val_list)[-1]
            self.combination[2] = sorted(self.val_list)[-2]
            self.combination[3] = sorted(self.val_list)[-3]
            self.combination[4] = sorted(self.val_list)[-4]
            self.combination[5] = sorted(self.val_list)[-5]

    def bet(self, bet_amount, board):
        if bet_amount > self.chip_amount:
            print("You can't bet more than {0}".format(self.chip_amount))
            bet_amount = self.chip_amount
        self.chip_amount -= bet_amount
        self.current_bet += bet_amount
        board.pot += bet_amount

    # input numbers where:
    # 0 - fold
    # 1 - call/check
    # 2 - raise
    def decision(self,action,players,board):
        if action == "fold":
            self.hand = None
            self.ingame = False
            print(self,"folded")
        elif action == "call":
            print(self,"calls for {0} chips".format(max(x.current_bet for x in players)-self.current_bet))
            self.bet(max(x.current_bet for x in players)-self.current_bet,board)
            self.answered = True
        elif "raise" in action:
            raise_amount = int(action.split("raise")[-1])
            self.bet(raise_amount,board)
            print(self,"raises for {0} chips".format(raise_amount))
            for player in players:
                player.answered = False
            self.answered = True
        else:
            print("Enter valid action!")

    def print_player_status(self):
        print("--------------------")
        print(self.name,":",self.hand)
        print(self.chip_amount)
        print(self.current_bet)
        print(self.comb_names[self.combination[0]],"of",self.combination[1])
        print("--------------------")

class StandardBoard(list):
    def __init__(self):
        self.pot = 0
        self.game_round = 0
        self.blinds_list = [20,50,100,200,400,800,1600]

    def reset(self):
        self.pot = 0
        self.clear()

    def blind_bet(self, players):
        if self.game_round % 10 == 0 and self.game_round != 0 and len(self.blinds_list) != 1:
            self.blinds_list.pop(0)
        bb = players[-1]
        sb = players[-2]
        bb.bet(self.blinds_list[0],self)
        sb.bet(self.blinds_list[0]//2,self)

    def check_bets(self, players):
        while True:
            for player in players:
                if len(self) > 1 and player.ingame:
                    player.evaluate(self)
                if player.ingame and not player.answered:
                    player.print_player_status()
                    #player.decision(input("{0}'s decision:".format(player)), players, board)
                    player.decision("call", players, self)
            if all([player.answered for player in players if player.ingame]):
                break
        print("Bets done!!!")

        for player in players:
            player.answered = False
            player.current_bet = 0

    def check_winner(self, players):
        status_list = [player.ingame for player in players]
        if status_list.count(True) == 1:
            for player, status in zip(players, status_list):
                if status:
                    player.winner = True

        if len(self) == 5:
            comb_list = [player.combination for player in players]
            winner_combination = sorted(comb_list)[-1]
            for player in players:
                if player.combination == winner_combination:
                    print(player, "is the winner!!!")
                    player.winner = True

        for player in players:
            if player.winner == True and comb_list.count(winner_combination) == 1:
                player.chip_amount += self.pot
                print(player, "wins {0} chips!".format(self.pot))
                return True

            elif player.winner == True and comb_list.count(winner_combination) > 1:
                player.chip_amount += self.pot//len([player for player in players if player.winner])
                print("pot {0} will be split between {1} players".format(self.pot,len([player for player in players if player.winner])))

        self.game_round += 1
