CARD_NAME = "Card"
CARD_DESC = "A card."
CARD_SYMBOL = "C"
SHIELD_NAME = "Shield"
SHIELD_DESC = "Cast a protective shield that can absorb 5 damage."
SHIELD_SYMBOL = "S"
HEAL_NAME = "Heal"
HEAL_DESC = "Cast an aura on target. It recovers 2 health."
HEAL_SYMBOL = "H"
FIREBALL_NAME = "Fireball"
FIREBALL_DESC = "FIREBALL! Deals 3 + [turns in hand] damage."

MINION_NAME = "Minion"
MINION_DESC = "Summon a minion."
MINION_SYMBOL = "M"
RAPTOR_NAME = "Raptor"
RAPTOR_DESC = "Summon a Bloodfen Raptor to fight for you."
RAPTOR_SYMBOL = "R"
WYRM_NAME = "Wyrm"
WYRM_DESC = "Summon a Mana Wyrm to buff your minions."
WYRM_SYMBOL = "W"

DAMAGE = "damage"
SHIELD = "shield"
HEALTH = "health"

MAX_HAND = 5
MAX_MINIONS = 5
SAVE_LOC = "autosave.txt"

PLAYER_SELECT = "M"
ENEMY_SELECT = "O"

CONTROLLER_DESC = "A game of HearthStone using: "

HELP_COMMAND = "help"
END_TURN_COMMAND = "end turn"
PLAY_COMMAND = "play"
DISCARD_COMMAND = "discard"
LOAD_COMMAND = "load"

COMMAND_PROMPT = "Please enter command (or Help to see valid commands): "
ENTITY_PROMPT = ("Please enter target Minion number, 'M' for yourself, or " +
                    "'O' for your opponent: ")


INVALID_COMMAND = ("Invalid command! Enter 'Help' to see a list of valid"
                   " commands.")
INVALID_ENTITY = "Invalid target."

WELCOME_MESSAGE = "Welcome to HearthStone!"

PLAY_MESSAGE = "Played "
ENERGY_MESSAGE = "Insufficient Energy!"
ENEMY_PLAY_MESSAGE = "Opponent played "
DISCARD_MESSAGE = "Discarded "

HELP_MESSAGES = ["Commands:",
                 "  - Help: See possible commands.",
                 "  - Play X: Plays Card at position X in hand.",
                 "  - Discard X: Discards Card at position X in hand.",
                 "  - End turn: end your turn and let the enemy move.",
                 "  - load FILE: loads game state from FILE."
                 ] 

GAME_SAVE_MESSAGE = "Game Saved."
GAME_LOAD_MESSAGE = "Loaded "
BAD_FILE_MESSAGE = "Malformed File: "
NO_FILE_MESSAGE = " not found." 

WIN_MESSAGE = "You have defeated your opponent, Congratulations!"
LOSS_MESSAGE = "You have been defeated. Better luck next time!"
