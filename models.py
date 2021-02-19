"""
Module, which contains models for game
"""


from enum import Enum
from random import choice
import settings
from exception import EnemyDown, ExitGame, GameOver
from misc import check_commands, if_command


class Attacks(Enum):
    """
    Class-enum, which represents attack types
    """
    MAGE = "mage"
    WARRIOR = "warrior"
    ROGUE = "rogue"
    CHOICES = (MAGE, WARRIOR, ROGUE)
    WINS = {MAGE: WARRIOR, WARRIOR: ROGUE, ROGUE: MAGE}

    @staticmethod
    def make_decision(inst1, inst2):
        """
        Method for resolving whether inst1 attack defeats inst2 attack
        :param inst1: string
        :param inst2: string
        :return: Result
        """
        if inst1 not in Attacks.CHOICES.value or inst2 not in Attacks.CHOICES.value:
            raise TypeError("Not an attack")
        if inst1 == inst2:
            return Result.DRAW
        elif Attacks.WINS.value[inst1] == inst2:
            return Result.WIN
        else:
            return Result.LOSE


class Result(Enum):
    """
    Class-enum, which represents results of rounds
    """
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


class Alive(object):
    """
    Class, which represents object with hp
    """
    def __init__(self, lives):
        self.lives = lives

    def decrease_life(self):
        """Function, which must be impelemented in child classes"""
        raise NotImplementedError

    def is_alive(self):
        """Function, which returns, whether object is alive or not"""
        return self.lives > 0


class MoveMixin:
    """Class, which represents object, which can make moves"""
    @staticmethod
    def attack(**kwargs):
        """Function, which must be impelemented in child classes"""
        raise NotImplementedError

    @staticmethod
    def defence(**kwargs):
        """Function, which must be impelemented in child classes"""
        raise NotImplementedError


class Enemy(Alive, MoveMixin):
    """Class, for representing enemy AI"""
    def __init__(self, lives_level):
        super().__init__(lives_level)
        self.level = lives_level

    @staticmethod
    def attack():
        """Function, for returning random attack of an enemy"""
        return choice(Attacks.CHOICES.value)

    @staticmethod
    def defence():
        """Function, for returning random defence of an enemy"""
        return choice(Attacks.CHOICES.value)

    def decrease_life(self):
        "Function, for decreasing enemy hp"
        self.lives -= 1
        if self.lives <= 0:
            raise EnemyDown("Enemy is dead")


def player_choice():
    """Function, for representing player move, by accepting input"""
    user_input = ""
    while True:
        user_input = input()
        if if_command(user_input):
            check_commands(user_input)
        else:
            try:
                user_input = int(user_input)
            except ValueError:
                print("Invalid input")
            else:
                if user_input not in (1, 2, 3):
                    print("Invalid number")
                    continue
                else:
                    break
    if user_input == 1:
        return Attacks.MAGE.value
    elif user_input == 2:
        return Attacks.WARRIOR.value
    elif user_input == 3:
        return Attacks.ROGUE.value


class Player(Alive, MoveMixin):
    """Class, for representing player"""
    def __init__(self, name):
        super().__init__(settings.PLAYER_LIVES)
        self.name = name
        self.score = 0

    @staticmethod
    def fight(attack, defence):
        """Function, which decides whether player is attacking or defending"""
        if isinstance(attack, Player):
            attack.attack(defence)
        elif isinstance(attack, Enemy):
            defence.defence(attack)

    def attack(self, enemy_object):
        """Function, which implements player's attack"""
        try:
            player_move = player_choice()
        except ExitGame as error:
            raise error
        enemy_move = enemy_object.defence()
        result = Attacks.make_decision(player_move, enemy_move)
        print(f"Your choice {player_move}")
        print(f"Enemy choice {enemy_move}")
        if result == Result.WIN:
            enemy_object.decrease_life()
            print(f"You attacked successfully! Enemy now has {enemy_object.lives} hp.")
        elif result == Result.DRAW:
            print("Draw round!")
        elif result == Result.LOSE:
            print("You missed!")

    def defence(self, enemy_object):
        """Function, which represents player's defence"""
        try:
            player_move = player_choice()
        except ExitGame as error:
            raise error
        enemy_move = enemy_object.defence()
        result = Attacks.make_decision(player_move, enemy_move)
        print(f"Your choice {player_move}")
        print(f"Enemy choice {enemy_move}")
        if result == Result.WIN:
            print("You protected yourself successfully!")
        elif result == Result.DRAW:
            print("Draw round!")
        elif result == Result.LOSE:
            self.decrease_life()
            print(f"You lost defence! You now have {self.lives} hp.")

    def decrease_life(self):
        """Function for decreasing player's lives"""
        self.lives -= 1
        if self.lives <= 0:
            raise GameOver(self.name, self.score)
