import gspread
from google.oauth2.service account import Credentials
from enum import Enum
import random



SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)

# Battleship

# Variables and enums
class Icons(Enum):
    SHIP = "🚢"
    FLAME = "🔥"
    WATER = "🌊"
    ROBOT = "🤖"
    COOL = "😎"
    EXPLOSION = "💥"
    BARREL = "🛢️"
    BARRELS = "🛢️🛢️🛢️🛢️🛢️"
    TELESCOPE = "🔭"
    GUN = "🔫"
    WOMAN_SMOKING = "🚬👩"


class Difficulty(Enum):
    STANDARD = 1  # Default
    VETERAN = 2
    NEAR_IMPOSSIBLE = 3
    
  
class State(Enum):
    INITIALISING = 1
    ACTIVE = 2
    AWAITING_END_ACTION = 3


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