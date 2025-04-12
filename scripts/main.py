import tkinter as tk
import random

main = tk.Tk()

#Manages signals for the game, which uses the signal pattern
class SignalHandler:
    pass

#Displays inital splash sceen on startup
class SplashScreen:
    pass

#Displays title screen
class TitleScreen:
    def __init__(self):
        pass

#Displays game screen
class GameScreen:
    def __init__(self):
        pass

#This class manages the gameplay
class GameManager:
    player_health = 20
    weapon_strength = 0
    weapon_equipped = False
    
    scoundrel_deck = ["2C", "2S", "2D", "2H", "3C", "3S", "3D", "3H", "4C", "4S", "4D", "4H", "5C", "5S", "5D", "5H", "6S", "6C", "6D", "6H", "7S", "7C", "7D", "7H", "8S", "8C", "8D", "8H", "9S", "9C", "9D", "9H", "TS", "TC", "TD", "TH", "JS", "JC", "QS", "QC", "KS", "KC", "AS", "AC"]
    current_deck = []
    current_room = []

    #statuses
    room_avoided = False
    health_potion_consumed = False

    def __init__(self):
        pass
    def start_new_game(self):
        self.deal_new_deck()
        self.new_room()
    def deal_new_deck(self):
        self.current_deck = self.scoundrel_deck
        random.shuffle(self.current_deck)
    def new_room(self):
        #Generates a new room from 4 cards from the deck
        ##TODO: fix possible bug in the endgame (<4 cards)
        for x in range(4):
            card = self.current_deck.pop(0)
            self.current_room.append(card)
        self.show_current_room()
    def run_room(self):
        if self.room_avoided:
            print("You cannot run from a room twice in a row!")
            self.show_current_room()
        else:
            for card in self.current_room:
                self.current_deck.append(card)
            self.current_room.clear()
            self.room_avoided = True
            self.new_room()
    def show_current_room(self):
        if len(self.current_room) <= 1:
            print("Generating new cards...")
        else:
            print("Current room: " + str(self.current_room) + ", " + str(len(self.current_deck)) + " cards in the deck. Health: " + str(self.player_health) + ". Weapon strength: " + str(self.weapon_strength) + ".")
            selected_card = input("Input an action: ")
            self.process_user_input(selected_card)
    def process_user_input(self, user_input):
        #checks if card exists in the room
        for card in self.current_room:
            if user_input == card:
                self.card_selected(user_input)
                break
            elif user_input == "run":
                self.run_room()
                self.room_avoided = True
                break
        else:
            print("Invalid card or command!")
            selected_card = input("Enter an action: ")
            self.process_user_input(selected_card)
    def card_selected(self, card):
        user_acceptance = input("Are you sure you want to select card " + card + "? (Y to accept): ")
        if user_acceptance == 'Y':
            self.current_room.remove(card)
            split_card = list(card)
            card_number = 0
            card_suit = split_card[1]

            #converts face cards to values
            match split_card[0]:
                case 'T':
                    card_number = 10
                case 'J':
                    card_number = 11
                case 'Q':
                    card_number = 12
                case 'K':
                    card_number = 13
                case 'A':
                    card_number = 14
                case _:
                    card_number = int(split_card[0])

            match card_suit:
                case 'S' | 'C':
                    print("Monster card.")
                case 'H':
                    self.heal_health(card_number)
                case 'D':
                    self.equip_weapon(card_number)
        else:
            self.show_current_room()
    def heal_health(self, amount):
        if self.health_potion_consumed:
            print("You have already used a health potion in this room. No effect.")
        else:
            self.player_health += amount
            if self.player_health >= 20:
                self.player_health = 20
            print("You heal " + str(amount) + " health. Your health is now " + str(self.player_health) + ".")
            self.health_potion_consumed = True
        self.show_current_room()
    def equip_weapon(self, amount):
        self.weapon_strength = amount
        self.weapon_equipped = True
        print("New weapon equipped with strength " + str(amount) + ".")
        self.show_current_room()
    def attack_enemy(self):
        pass
    def take_damage(self, damage):
        pass

#This class controls the program itself
class ProgramManager(tk.Tk):
    def __init__(self):
        pass
    def change_screen():
        pass
    def quit_game():
        pass

def show_title_screen():
    scoundrel_title = tk.Label(main, text="Scoundrel", font=('Arial', 60, 'bold'))
    scoundrel_title.place(x=50, y=100)

    play_button = tk.Button(main, text="Play")
    play_button.place(x=150, y=500)

    quit_button = tk.Button(main, text="Quit", command=main.destroy)
    quit_button.place(x=150, y=550)

def show_game_screen():
    pass

def initialize_game():
    #Creates the main window
    main.geometry("1024x768")
    main.resizable(width=False, height=False)
    main.title("Scoundrel - A Rogue-like Card Game in Python")

    main.config(background="white")

    show_title_screen()

    main.mainloop()

initialize_game()
game_manager = GameManager()
game_manager.start_new_game()
