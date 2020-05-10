from tkinter import *
from PIL import Image, ImageTk
from poker_main import StandardDeck, StandardBoard
from Poker_GUI import Player_GUI, Board_GUI
from random import randint
import time

root=Tk()
root.title("Texas Hold'em")
def load_card_images():
	suit_list = ["c","d","h","s"]
	card_img_dict = {}
	for value in range(2,15):
		for suit in suit_list:
			load = Image.open("D:/pkr_face/deck_images/{0}{1}.jpg".format(value,suit))
			resize = load.resize((int(128/3),int(178/3)))
			render = ImageTk.PhotoImage(resize)
			card_img_dict.update({"{0}{1}".format(value,suit) : render})
	return card_img_dict
img_dict = load_card_images()

deck = StandardDeck()
board = Board_GUI(root)
player_1 = Player_GUI("One", root)
player_2 = Player_GUI("Two", root)
player_3 = Player_GUI("Three", root)
player_4 = Player_GUI("Four", root)

# --------------------------PREFLOP-----------------------------------
players_in_game = [player_1,player_2,player_3,player_4]

while True:
	deck.shuffle()
	board.append(deck.pop(0))
	board.append(deck.pop(0))
	board.append(deck.pop(0))
	board.reset_frame()
	board.update_frame([img_dict["{0}{1}".format(card.value,card.suit)] for card in board])

	player_1.hand.append(deck.pop(0))
	player_1.hand.append(deck.pop(0))

	root.update()
	input("Action:")
	board.append(deck.pop(0))
	board.reset_frame()
	board.update_frame([img_dict["{0}{1}".format(card.value,card.suit)] for card in board])

	if len(board) == 5:
		break
