"""
Settings module for constants
"""


PLAYER_LIVES = 3
SCORES_FILE = "scores.json"
COMMANDS = ("exit", "help", "show_scores")


# Method for showing possible commands
def game_help():
    print("""
1. Mage
2. Warrior
3. Rogue
exit - exits game
show_scores - top ten scores
help - game commands
""")
