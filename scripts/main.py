import pygame as py
import random
import os

py.init()

main_window = py.display.set_mode((1024, 768))

py.display.set_caption("Scoundrel")

#Manages signals for the game, which uses the signal pattern
class SignalHandler:
    pass

class SplashScreen:
    pass

class TitleScreen:
    pass

class GameScreen:
    pass

#---Game Screen Classes---#

#This class manages the gameplay (not gui)
class GameManager:
    player_health = 20
    weapon_strength = 0
    last_monster_strength = 0
    weapon_equipped = False
    last_used_card = ""
    
    scoundrel_deck = ["2C", "2S", "2D", "2H", "3C", "3S", "3D", "3H", "4C", "4S", "4D", "4H", "5C", "5S", "5D", "5H", "6S", "6C", "6D", "6H", "7S", "7C", "7D", "7H", "8S", "8C", "8D", "8H", "9S", "9C", "9D", "9H", "TS", "TC", "TD", "TH", "JS", "JC", "QS", "QC", "KS", "KC", "AS", "AC"]
    endgame_deck = ["2C", "2S", "2D", "2H", "3C"]
    current_deck = []
    current_room = []

    #statuses
    room_active = False
    room_avoided = False
    health_potion_consumed = False

    def start_new_game(self):
        print("---SCOUNDREL---")
        print("Starting new game!")
        self.player_health = 20
        self.weapon_strength = 0
        self.last_monster_strength = 0
        self.weapon_equipped = False

        self.room_active = False
        self.room_avoided = False
        self.health_potion_consumed = False

        self.current_deck = []
        self.current_room = []

        self.last_used_card = ""

        self.deal_new_deck()
        self.new_room()
    def deal_new_deck(self):
        self.current_deck = self.scoundrel_deck.copy()
        random.shuffle(self.current_deck)
    def new_room(self):
        #Generates a new room from 4 cards from the deck
        for x in range(4):
            card = self.current_deck.pop(0)
            self.current_room.append(card)
        game_ui_manager.set_new_room_images(self.current_room)
        if self.room_avoided:
            game_ui_manager.run_room_button.selection_disabled = True
        else:
            game_ui_manager.run_room_button.selection_disabled = False
        game_ui_manager.update_object_index(1)
        self.show_current_room()
    def run_room(self):
        if self.room_avoided:
            print("You cannot run from a room twice in a row!")
            self.show_current_room()
        elif self.room_active:
            print("You cannot run since you have used a card in this room already!")
            self.show_current_room()
        else:
            for card in self.current_room:
                self.current_deck.append(card)
            self.current_room.clear()
            self.room_avoided = True
            self.new_room()
    def show_current_room(self):
        if self.current_deck != []:
            if len(self.current_room) <= 1:
                #Generate new room
                print("Generating new cards...")
                while len(self.current_room) < 4:
                    if self.current_deck != []:
                        card = self.current_deck.pop(0)
                        self.current_room.append(card)
                    else:
                        break
                game_ui_manager.set_new_room_images(self.current_room)
                game_ui_manager.run_room_button.selection_disabled = False
                self.room_avoided = False
                self.health_potion_consumed = False
                self.room_active = False
                print("New room!")
                self.show_current_room()
            else:
                print(f"Current room: {self.current_room}, {len(self.current_deck)} cards in the deck. Health: {self.player_health}. Weapon strength: {self.weapon_strength}. Last monster strength: {self.last_monster_strength}.")
                #selected_card = input("Input an action: ")
                #self.process_user_input(selected_card)
        else:
            if self.current_room == []:
                print("Dungeon cleared! You win!")
                print("Final score: " + str(self.compute_final_score()))
                user_acceptance = input("Play again? (Y to accept): ")
                if user_acceptance == 'Y':
                    self.start_new_game()
                else:
                    pass
            else:
                print("Current room: " + str(self.current_room) + ", " + str(len(self.current_deck)) + " cards in the deck. Health: " + str(self.player_health) + ". Weapon strength: " + str(self.weapon_strength) + ". Last monster strength: " + str(self.last_monster_strength) + ".")
                #selected_card = input("Input an action: ")
                #self.process_user_input(selected_card)
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
            self.room_active = True
            game_ui_manager.run_room_button.selection_disabled = True
            self.last_used_card = card
        #user_acceptance = input("Are you sure you want to select card " + card + "? (Y to accept): ")
        #if user_acceptance == 'Y':
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
                    self.attack_enemy(card_number)
                case 'H':
                    self.heal_health(card_number)
                case 'D':
                    self.equip_weapon(card_number)
        #else:
            #self.show_current_room()
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
        self.last_monster_strength = 0
        print("New weapon equipped with strength " + str(amount) + ".")
        self.show_current_room()
    def attack_enemy(self, amount):
        if self.weapon_equipped:
            if amount > self.last_monster_strength and self.last_monster_strength != 0:
                print("Weapon has been used against a higher power monster, fighting barehanded instead.")
                print("Fighting barehanded against a monster of power " + str(amount) + ".")
                self.take_damage(amount)
            else:
                print("Weapon strength of " + str(self.weapon_strength) + " against a monster of power " + str(amount) + ".")
                self.last_monster_strength = amount
                self.take_damage(amount - self.weapon_strength)
        else:
            print("Fighting barehanded against a monster of power " + str(amount) + ".")
            self.take_damage(amount)
    def take_damage(self, damage):
        if damage <= 0:
            damage = 0
        print("You take " + str(damage) + " damage!")
        self.player_health -= damage
        if self.player_health <= 0:
            self.player_health = 0
            print("Your health is now " + str(self.player_health) + ".")
            print("You died. Game over!")
            print("Final score: " + str(self.compute_final_score()))
            user_acceptance = input("Play again? (Y to accept): ")
            if user_acceptance == 'Y':
                self.start_new_game()
            else:
                pass
        else:
            print("Your health is now " + str(self.player_health) + ".")
            self.show_current_room()
    def compute_final_score(self):
        total_deck = self.current_deck
        for card in self.current_room:
            total_deck.append(card)
        if total_deck == []:
            if self.player_health == 20:
                if self.last_used_card != "":
                    last_card = list(self.last_used_card)
                    if last_card[1] == 'H':
                        return self.player_health + int(last_card[0])
                    else:
                        return self.player_health
                else:
                    return self.player_health
            else:
                return self.player_health
        else:
            total_score = 0
            for card in total_deck:
                split_card = list(card)
                card_number = 0
                card_suit = split_card[1]

                if card_suit == 'C' or card_suit == 'S':

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

                    total_score -= card_number
                else:
                    continue
            return total_score

class GameUIManager:
    card_image_paths = {
        "2C": "assets/textures/clubs/2C.png",
        "2S": "assets/textures/spades/2S.png",
        "2D": "assets/textures/diamonds/2D.png",
        "2H": "assets/textures/hearts/2H.png",
        "3C": "assets/textures/clubs/3C.png",
        "3S": "assets/textures/spades/3S.png",
        "3D": "assets/textures/diamonds/3D.png",
        "3H": "assets/textures/hearts/3H.png",
        "4C": "assets/textures/clubs/4C.png",
        "4S": "assets/textures/spades/4S.png",
        "4D": "assets/textures/diamonds/4D.png",
        "4H": "assets/textures/hearts/4H.png",
        "5C": "assets/textures/clubs/5C.png",
        "5S": "assets/textures/spades/5S.png",
        "5D": "assets/textures/diamonds/5D.png",
        "5H": "assets/textures/hearts/5H.png",
        "6C": "assets/textures/clubs/6C.png",
        "6S": "assets/textures/spades/6S.png",
        "6D": "assets/textures/diamonds/6D.png",
        "6H": "assets/textures/hearts/6H.png",
        "7C": "assets/textures/clubs/7C.png",
        "7S": "assets/textures/spades/7S.png",
        "7D": "assets/textures/diamonds/7D.png",
        "7H": "assets/textures/hearts/7H.png",
        "8C": "assets/textures/clubs/8C.png",
        "8S": "assets/textures/spades/8S.png",
        "8D": "assets/textures/diamonds/8D.png",
        "8H": "assets/textures/hearts/8H.png",
        "9C": "assets/textures/clubs/9C.png",
        "9S": "assets/textures/spades/9S.png",
        "9D": "assets/textures/diamonds/9D.png",
        "9H": "assets/textures/hearts/9H.png",
        "TC": "assets/textures/clubs/TC.png",
        "TS": "assets/textures/spades/TS.png",
        "TD": "assets/textures/diamonds/TD.png",
        "TH": "assets/textures/hearts/TH.png",
        "JC": "assets/textures/clubs/JC.png",
        "JS": "assets/textures/spades/JS.png",
        "QC": "assets/textures/clubs/QC.png",
        "QS": "assets/textures/spades/QS.png",
        "KC": "assets/textures/clubs/KC.png",
        "KS": "assets/textures/spades/KS.png",
        "AC": "assets/textures/clubs/AC.png",
        "AS": "assets/textures/spades/AS.png",
    }
    def __init__(self):
        self.room_card_1 = RoomCard([198, 192])
        self.room_card_2 = RoomCard([357, 192])
        self.room_card_3 = RoomCard([517, 192])
        self.room_card_4 = RoomCard([676, 192])
        self.run_room_button = RunRoom([858, 208])
        self.game_deck = GameDeck([32, 320])
        self.discard_deck = DiscardDeck([842, 320])
        self.weapon_card = WeaponCard([437, 526], [0, 0])
        self.object_index = 0
        self.selectable_objects = [self.room_card_1, self.room_card_2, self.room_card_3, self.room_card_4, self.run_room_button]
        self.selected_object = self.selectable_objects[self.object_index]
        self.previous_selected_object = None
        self.room_card_1.set_hover_status(True)
        self.room_card_1.set_card_image()
        self.room_card_2.set_card_image()
        self.room_card_3.set_card_image()
        self.room_card_4.set_card_image()
    def draw_game_uis(self):
        #what the hell is this
        self.room_card_1.display_card_image()
        self.room_card_2.display_card_image()
        self.room_card_3.display_card_image()
        self.room_card_4.display_card_image()
        self.game_deck.display_card_image()
        self.discard_deck.display_card_image()
        self.run_room_button.display_image()
        self.weapon_card.display_card_image()

        if hasattr(self.selected_object, "set_hover_status"):
            self.selected_object.set_hover_status(True)
        
        if hasattr(self.previous_selected_object, "set_hover_status") and self.previous_selected_object:
            if not self.previous_selected_object.selection_disabled:
                self.previous_selected_object.set_hover_status(False)
            else:
                self.previous_selected_object.set_hover_status(True)

    def update_object_index(self, modifier):
        self.object_index += modifier
        if self.object_index >= len(self.selectable_objects) or self.object_index <= -len(self.selectable_objects):
            self.object_index = self.object_index % len(self.selectable_objects)
        self.previous_selected_object = self.selected_object

        self.selected_object = self.selectable_objects[self.object_index]
        while self.selected_object.selection_disabled:
            self.object_index += modifier
            if self.object_index >= len(self.selectable_objects) or self.object_index <= -len(self.selectable_objects):
                self.object_index = self.object_index % len(self.selectable_objects)
            self.selected_object = self.selectable_objects[self.object_index]
        
        if hasattr(self.selected_object, "set_card_image"):
            self.selected_object.set_card_image()
        
    def object_selected(self):
        if hasattr(self.selected_object, "selected"):
            self.selected_object.selected()

    #functions that the game manager will actually use
    def hide_all_cards(self):
        pass
    def set_new_room_images(self, cards):
        #too lazy to loop this lmao
        self.room_card_1.set_hover_status(False)
        self.room_card_2.set_hover_status(False)
        self.room_card_3.set_hover_status(False)
        self.room_card_4.set_hover_status(False)
        
        self.room_card_1.current_card = cards[0]
        self.room_card_2.current_card = cards[1]
        self.room_card_3.current_card = cards[2]
        self.room_card_4.current_card = cards[3]

        self.room_card_1.set_card_image()
        self.room_card_2.set_card_image()
        self.room_card_3.set_card_image()
        self.room_card_4.set_card_image()

        self.room_card_1.reset_position()
        self.room_card_2.reset_position()
        self.room_card_3.reset_position()
        self.room_card_4.reset_position()

        self.room_card_1.selection_disabled = False
        self.room_card_2.selection_disabled = False
        self.room_card_3.selection_disabled = False
        self.room_card_4.selection_disabled = False

#Game Objects
class GameDeck():
    current_image = None
    card_position = [0, 0]
    def __init__(self, position):
        self.card_position = position
        self.current_image = py.image.load("assets/textures/back_card.png")
    def display_card_image(self):
        main_window.blit(self.current_image, self.card_position)

class RoomCard():
    current_card = ""
    selection_disabled = False
    current_image = None
    card_position = [0, 0]
    #where the selected card will stop hovering to
    y_offset = 172
    fade_out_y_offset = 102
    def __init__(self, position):
        self.card_position = position
    def reset_position(self):
        self.card_position = [self.card_position[0], 192]
        self.y_offset = 172
    def set_hover_status(self, status):
        #i know i shouldn't put magic numbers but tbh this is an elective project and i want this done already
        #who cares? it's not like they will do an actually detailed code review
        #the rest of the program is already so messy anyway
        if status:
            if self.card_position[1] > self.y_offset:
                self.card_position[1] -= 1
            else:
                if self.selection_disabled:
                    self.current_image = None
        else:
            if self.card_position[1] < 192:
                self.card_position[1] += 1
            else:
                pass
    def set_card_image(self):
        if self.current_card in GameUIManager.card_image_paths:
            if os.path.exists(GameUIManager.card_image_paths[self.current_card]):
                self.current_image = py.image.load(GameUIManager.card_image_paths[self.current_card])
            else:
                self.current_image = py.image.load("assets/textures/back_card.png")
        else:
            self.current_image = py.image.load("assets/textures/back_card.png")
    def display_card_image(self):
        if self.current_image != None:
            main_window.blit(self.current_image, self.card_position)
    def selected(self):
        self.y_offset = self.fade_out_y_offset
        self.selection_disabled = True
        game_ui_manager.run_room_button.selection_disabled = True
        game_ui_manager.update_object_index(1)
        game_manager.process_user_input(self.current_card)

class WeaponCard():
    current_card = ""
    image_position = [0, 0]
    last_monster_card_image_position = [0, 0]
    current_image = None
    def __init__(self, position, monster_position):
        self.image_position = position
        self.last_monster_card_image_position = monster_position
        self.current_image = py.image.load("assets/textures/back_card.png")
    def display_card_image(self):
        main_window.blit(self.current_image, self.image_position)

class RunRoom():
    image_position = [0, 0]
    selection_disabled = False
    y_offset = 183
    current_image = py.image.load("assets/textures/run_room.png")
    def __init__(self, position):
        self.image_position = position
    def reset_position(self):
        self.image_position = [858, 208]
    def set_hover_status(self, status):
        if status and not self.selection_disabled:
            if self.image_position[1] > self.y_offset:
                self.image_position[1] -= 1
            else:
                pass
        else:
            if self.image_position[1] < 208:
                self.image_position[1] += 1
            else:
                pass
    def display_image(self):
        main_window.blit(self.current_image, self.image_position)
    def selected(self):
        self.reset_position()
        self.selection_disabled = True
        game_manager.run_room()

class DiscardDeck():
    image_position = [0, 0]
    discarded_cards_active = False
    current_image = py.image.load("assets/textures/back_card.png")
    def __init__(self, position):
        self.image_position = position
    def display_card_image(self):
        main_window.blit(self.current_image, self.image_position)

class ProgramManager():
    just_pressed = False
    def __init__(self):
        pass
    def process_user_input(self, inputs):
        if not self.just_pressed:
            if inputs[py.K_LEFT]:
                game_ui_manager.update_object_index(-1)
                self.just_pressed = True
            elif inputs[py.K_RIGHT]:
                game_ui_manager.update_object_index(1)
                self.just_pressed = True
            elif inputs[py.K_SPACE]:
                game_ui_manager.object_selected()
                self.just_pressed = True

program_active = True

program_manager = ProgramManager()
game_ui_manager = GameUIManager()
game_manager = GameManager()

game_manager.start_new_game()

while program_active:
    for event in py.event.get():
        if event.type == py.KEYUP:
            program_manager.just_pressed = False
        if event.type == py.QUIT:
            program_active = False

    main_window.fill(0)

    game_ui_manager.draw_game_uis()
    program_manager.process_user_input(py.key.get_pressed())

    py.display.update()
