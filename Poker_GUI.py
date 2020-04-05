from random import randint
from tkinter import *
from PIL import Image, ImageTk
from poker_main import StandardDeck, StandardBoard, Player

#THIS FILE CONTAINS GUI EXPANSIONS FOR CLASSES FROM poker_main

class Player_GUI(Player):
	def __init__(self, name, root):
		super().__init__(name)
		self.root = root

		self.frame = LabelFrame(root,text=self.name)
