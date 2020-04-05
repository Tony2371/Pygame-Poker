from random import randint
from tkinter import *
from PIL import Image, ImageTk
from poker_main import StandardDeck, StandardBoard

root = Tk()
root.geometry("640x480")
deck = StandardDeck()
board = StandardBoard()

def load_card_images():
	suit_list = ["c","d","h","s"]
	card_img_dict = {}
	for value in range(2,15):
		for suit in suit_list:
			load = Image.open("D:/pkr_face/deck_images_jpg/{0}{1}.jpg".format(value,suit))
			resize = load.resize((int(128/3),int(178/3)))
			render = ImageTk.PhotoImage(resize)
			card_img_dict.update({"{0}{1}".format(value,suit) : render})

	return card_img_dict

img_dict = load_card_images()
frame = LabelFrame(root,text="Board cards")
frame.grid()

def add_card():
    global deck
    global board
    for c in deck:
        c.showing = True
    if len(board) < 5:
        board.append(deck.pop(randint(0,len(deck)-1)))
    print(board)
    print(deck)
    board_card_1 = Label(frame,image=img_dict["{0}{1}".format(board[-1].value,board[-1].suit)])
    board_card_1.grid(row=0,column=len(board))


def reset_board():
    global board
    global deck
    board.clear()
    deck.reset()
    print("The game is back on!")
    for widget in frame.winfo_children():
        widget.destroy()



button = Button(root,text="Add card",width=25,command=add_card)
button.grid(row=1,columnspan=5)
button_1 = Button(root,text="Clear",width=25,command=reset_board)
button_1.grid(row=2,columnspan=5)

columns = 0

for card in board:
    columns += 1
    card_0 = Label(root,text=deck[0])
    card_0.grid(column=columns)

for wid in root.winfo_children():
    print (wid)

if len(board) >= 5:
    button.state = DISABLED

root.mainloop()
