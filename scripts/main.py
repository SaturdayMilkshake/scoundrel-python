import tkinter as tk

window = tk.Tk()

#Displays title screen
class TitleScreen:
    def __init__(self):
        pass

#This class manages the gameplay
class GameManager:
    scoundrel_deck = []
    current_deck = []
    def __init__(self):
        pass

#This class controls the program itself
class ProgramManager:
    def __init__(self):
        pass

def show_title_screen():
    scoundrel_title = tk.Label(window, text="Scoundrel",font=('Arial', 60, 'bold'))
    scoundrel_title.place(x=50,y=100)

    author_label = tk.Label(window, text="A game by SaturdayMilkshake",font=('Arial',20))
    author_label.place(x=250,y=190)

def initialize_game():
    #Creates the main window
    window.geometry("1024x768")
    window.title("Scoundrel - A Rogue-like Card Game in Python")

    window.config(background="white")

    show_title_screen()

    window.mainloop()

initialize_game()

