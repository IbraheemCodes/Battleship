from google.oauth2.service_account import Credentials
from enum import Enum
import random
import os
import sys
import subprocess
import gspread


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)

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