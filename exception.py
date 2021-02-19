"""
Module, containing exceptions
"""


class GameOver(Exception):
    """
    Class, which represents game ending exception
    """
    def __init__(self, player_name, score):
        super().__init__()
        self.player_name = player_name
        self.score = score


class EnemyDown(Exception):
    """
    Class, which represents enemy down
    """


class ExitGame(Exception):
    """
    Class, which represents game ending exception by user
    """
