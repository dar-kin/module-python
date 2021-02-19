"""
Module, containing exceptions
"""


class GameOver(Exception):
    def __init__(self, player_name, score):
        self.player_name = player_name
        self.score = score


class EnemyDown(Exception):
    pass


class ExitGame(Exception):
    pass

