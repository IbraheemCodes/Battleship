from enum import Enum
import random
import os
import sys
import subprocess


# Constants
COLUMNS = 5
ROWS = 6

ICONS = {
    "Ship": "🚢",
    "Flame": "🔥",
    "Water": "🌊",
    "Robot": "🤖",
    "Cool": "😎",
    "Explosion": "💥",
    "Barrel": "🛢️",
    "Barrels": "🛢️🛢️🛢️🛢️🛢️",
    "Telescope": "🔭",  # replacement for binoculars
    "Gun": "🔫",
    "WomanSmoking": "🚬👩"
}


class Difficulty(Enum):
    STANDARD = 1
    VETERAN = 2
    NEAR_IMPOSSIBLE = 3


class State(Enum):
    INITIALISING = 1
    ACTIVE = 2
    AWAITING_END_ACTION = 3


# Set this to True if you wish to see opponent's ships
show_opponents_ships = False


# Game class
class Game:
    def __init__(self, opponent_difficulty, game_state):
        self.opponent_difficulty = opponent_difficulty
        self.game_state = game_state

    def set_difficulty(self, difficulty):
        self.opponent_difficulty = difficulty

    def set_state(self, state):
        self.game_state = state

    def get_difficulty(self):
        return self.opponent_difficulty

# Player class


class Player:
    def __init__(self, username, ship):
        self.username = username
        self.ship = ship

    def set_username(self, uname):
        self.username = uname

    def set_ship(self, ship):
        self.ship = ship

    def get_ship(self, show_ship, as_array):
        if show_ship:
            output = ""
            temp = self.ship
            for row in temp:
                for col in row:
                    output += str(col[0])
                output += "\n"
            return temp if as_array else output
        else:
            output = ""
            temp = self.ship
            for row in temp:
                for col in row:
                    if col == ICONS["Ship"]:
                        output += ICONS["Water"]
                    else:
                        output += str(col[0])
                output += "\n"
            return temp if as_array else output

    def get_username(self):
        return self.username

    def has_ships_remaining(self):
        result = False
        temp = self.ship
        for row in temp:
            for col in row:
                if col == ICONS["Ship"]:
                    result = True
                    break
        return result


# Validator class


class Validator:
    @staticmethod
    def is_input_int(i):
        try:
            int(i)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_selected_difficulty_valid(i):
        if Validator.is_input_int(i):
            if int(i) in [member.value for member in Difficulty]:
                return True
        return False

    @staticmethod
    def is_row_attack_valid(i):
        if Validator.is_input_int(i):
            attack_loc = int(i) - 1
            if attack_loc < 0 or attack_loc >= ROWS:
                print("Attack is out of range.\nTry again:")
                return False
            else:
                row_all_used = True
                temp_bot_ship = bot.get_ship(False, True)

                for i in temp_bot_ship[attack_loc]:
                    if i == ICONS["Water"] or i == ICONS["Ship"]:
                        row_all_used = False
                if row_all_used:
                    print("This entire row is already destroyed\nTry again:\n")
                    return False
                else:
                    return True
        else:
            print(f"Row must be numerical (1-{ROWS})\nTry again:\n")
            return False

    @staticmethod
    def is_overall_attack_valid(row_input, column_input):
        if Validator.is_input_int(column_input):
            row_input = int(row_input) - 1
            column_input = int(column_input) - 1

            if column_input < 0 or column_input >= COLUMNS:
                print("Column is out of range.\nTry again:")
                return False
            else:
                temp_bot_ship = bot.get_ship(False, True)
                target_loc = temp_bot_ship[row_input][column_input]
                if target_loc == ICONS["Flame"] or target_loc == ICONS["Explosion"]:
                    print_results()
                    print("You cannot attack the same location twice\nTry again\n")
                    return False
                else:
                    return True
        else:
            print("Column needs to be numerical\nTry again:\n")
            return False


# Reset the board

def reset_board(columns, rows):

    board = [[ICONS["Water"] for _ in range(columns)] for _ in range(rows)]
    ships_placed = 0

    while ships_placed < rows:
        row = random.randint(0, rows - 1)
        col = random.randint(0, columns - 1)
        if board[row][col] == ICONS["Water"]:
            board[row][col] = ICONS["Ship"]
            ships_placed += 1
    return board


# Instantiate players
game = Game(Difficulty.STANDARD, State.INITIALISING)
human = Player(ICONS["Cool"], reset_board(COLUMNS, ROWS))
bot = Player(ICONS["Telescope"] + ICONS["Robot"] + ICONS["Gun"] + " (Opponent)", reset_board(COLUMNS, ROWS))

# Initialise the game


def initialise_game():

    is_username_valid = False
    is_difficulty_valid = False

    while game.game_state == State.INITIALISING:
        while not is_username_valid:
            username = input("**Enter your username...**\n")
            if len(username) > 0:
                is_username_valid = True
                human.set_username(ICONS["Telescope"] + " " + ICONS["Cool"] + " " + ICONS["Gun"] + " (" + username + ")")

        while not is_difficulty_valid:
            difficulty = input("\n**Choose the difficulty:**\n1. Standard\n2. Veteran\n3. Near Impossible\n")
            difficulty = difficulty.strip()
            if Validator.is_selected_difficulty_valid(difficulty):
                difficulty = int(difficulty)
                if difficulty in [member.value for member in Difficulty]:
                    game.set_difficulty(Difficulty(difficulty))
                    human.set_ship(reset_board(COLUMNS, ROWS))
                    bot.set_ship(reset_board(COLUMNS, ROWS))
                    is_difficulty_valid = True
                    game.set_state(State.ACTIVE)
                    break

            else:
                print("**Invalid difficulty chosen!**")

# used to print the results every time an attack is done


def print_results():

    os.system('cls' if os.name == 'nt' else 'clear')
    subprocess.call("clear" if os.name != "nt" else "cls", shell=True)
    print("-------------")
    print(bot.get_username())
    print("-------------")
    print(bot.get_ship(show_opponents_ships, False))
    print(ICONS["Barrels"])
    print("")
    print(human.get_ship(True, False) + "-------------")
    print(human.get_username())
    print("-------------")


# function to attack bot with specified coords
def player_attack_bot(column, row):
    temp = bot.get_ship(True, True)

    if temp[column][row] == ICONS["Ship"]:
        print(ICONS["WomanSmoking"] + " Good shot chief!")
        temp[column][row] = ICONS["Explosion"]
    else:
        print(ICONS["WomanSmoking"] + " Nice try chief!")
        temp[column][row] = ICONS["Flame"]

    bot.set_ship(temp)


# function to attack player after an attack is done. No parameters are required
def bot_attack_player():

    temp = human.get_ship(True, True)
    difficulty = game.get_difficulty()

    column_len = len(temp) - 1
    row_len = len(temp[0]) - 1

    attack_valid = False
    chosen_column = random.randint(0, column_len)
    chosen_row = random.randint(0, row_len)
    attack_loc = temp[chosen_column][chosen_row]

    if difficulty == Difficulty.STANDARD:
        if attack_loc == ICONS["Ship"] or attack_loc == ICONS["Water"]:
            attack_valid = True

        while not attack_valid:
            chosen_column = random.randint(0, column_len)
            chosen_row = random.randint(0, row_len)
            attack_loc = temp[chosen_column][chosen_row]

            if attack_loc == ICONS["Ship"] or attack_loc == ICONS["Water"]:
                attack_valid = True

    if difficulty == Difficulty.VETERAN:
        force_winning_gamble = random.randint(0, 8)
        if force_winning_gamble > 3:
            attack_valid = False
            for column_idx, column in enumerate(temp):
                for row_idx, row in enumerate(column):
                    if row == ICONS["Ship"]:
                        chosen_column = column_idx
                        chosen_row = row_idx
                        attack_loc = temp[chosen_column][chosen_row]
                        attack_valid = True
                        break
                    if not attack_valid:
                        chosen_column = -1
                        chosen_row = -1
        else:
            while not attack_valid:
                chosen_column = random.randint(0, column_len)
                chosen_row = random.randint(0, row_len)
                attack_loc = temp[chosen_column][chosen_row]

                if attack_loc == ICONS["Ship"] or attack_loc == ICONS["Water"]:
                    attack_valid = True

    if difficulty == Difficulty.NEAR_IMPOSSIBLE:
        force_winning_gamble = random.randint(0, 1)
        if force_winning_gamble == 0:
            attack_valid = False  # Reset the flag
            for column_idx, column in enumerate(temp):
                for row_idx, row in enumerate(column):
                    if row == ICONS["Ship"]:
                        chosen_column = column_idx
                        chosen_row = row_idx
                        attack_loc = temp[chosen_column][chosen_row]
                        attack_valid = True
                    break
                if not attack_valid:
                    chosen_column = -1
                    chosen_row = -1
        else:
            while not attack_valid:
                chosen_column = random.randint(0, column_len)
                chosen_row = random.randint(0, row_len)
                attack_loc = temp[chosen_column][chosen_row]

                if attack_loc == ICONS["Ship"] or attack_loc == ICONS["Water"]:
                    attack_valid = True

    print("code reach test")
    if attack_loc == ICONS["Ship"]:
        print(ICONS["WomanSmoking"] + " Ahh we lost a ship!")
        temp[chosen_column][chosen_row] = ICONS["Explosion"]
    else:
        print(ICONS["WomanSmoking"] + " Haha, they missed. Let's strike back!")
        temp[chosen_column][chosen_row] = ICONS["Flame"]

    human.set_ship(temp)


# Play the game
def play_game():
    is_row_valid = False
    is_column_valid = False
    target_column = 0
    target_row = 0

    while game.game_state == State.ACTIVE:
        print_results()
        while not is_row_valid:
            row = input(f"Enter Row (1-{ROWS}):\n")
            is_row_valid = Validator.is_row_attack_valid(row)
            target_row = row

        while not is_column_valid:
            column = input(f"Enter Column (1-{COLUMNS}):\n")
            is_column_valid = Validator.is_overall_attack_valid(target_row, column)
            target_column = column

        player_attack_bot(int(target_row) - 1, int(target_column) - 1)
        if not bot.has_ships_remaining():
            game.set_state(State.AWAITING_END_ACTION)
            break

        bot_attack_player()
        if not human.has_ships_remaining():
            game.set_state(State.AWAITING_END_ACTION)
            break

        is_row_valid = False
        is_column_valid = False

    # End game actions


def end_game_actions():

    did_human_win = human.has_ships_remaining()
    while game.game_state == State.AWAITING_END_ACTION:
        if did_human_win:
            print_results()
            print("Well done " + human.get_username()[4::] + "!")
        else:
            print_results()
            print("Good battle! But let's not give up")
        next_action = input("Would you like to go again? (Y/N)")
        if next_action.upper() == "Y":
            game.set_state(State.INITIALISING)
            initialise_game()
        elif next_action.upper() == "N":
            sys.exit()


# Called functions. Each function repeatedly executes depending on game's state
initialise_game()
play_game()
end_game_actions()
