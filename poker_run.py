'''
TO DO LIST:
- Low Straight flush combination (SOLVED)
- Kickers
- Second hgh card for Two pairs and Full House

KNOWN BUGS:
- max([x for x,y in zip(self.val_list,self.count_list) if y == 1])
will be empty sequence if none of y == 1
- Full house error if two sets
'''
from poker_main import Card, Player, StandardDeck, StandardBoard
from random import randint

deck = StandardDeck()
board = StandardBoard()
player1 = Player("One")
player2 = Player("Two")

deck.shuffle()

player1.hand.append(deck.pop(randint(0, len(deck)-1)))
player1.hand.append(deck.pop(randint(0, len(deck)-1)))
player2.hand.append(deck.pop(randint(0, len(deck)-1)))
player2.hand.append(deck.pop(randint(0, len(deck)-1)))


[board.append(deck.pop(randint(0, len(deck)-1))) for x in range(5)]

print("Player1: ",player1.hand)
print("Player2: ",player2.hand)
print(board)
player1.evaluate(board)
player2.evaluate(board)
print("-------------------------")
print(player1.combination,player1.kicker)
print(player2.combination,player2.kicker)
