from enum import Enum
from random import choice
import settings
from exception import EnemyDown, ExitGame, GameOver
from misc import check_commands, if_command

class Attacks(Enum):
    MAGE = "mage"
    WARRIOR = "warrior"
    ROGUE = "rogue"
    CHOICES = (MAGE, WARRIOR, ROGUE)
    WINS = {MAGE: WARRIOR, WARRIOR: ROGUE, ROGUE: MAGE}

    @staticmethod
    def make_decision(inst1, inst2):
        if inst1 not in Attacks.CHOICES.value or inst2 not in Attacks.CHOICES.value:
            raise TypeError("Not an attack")
        if inst1 == inst2:
            return Result.DRAW
        elif Attacks.WINS.value[inst1] == inst2:
            return Result.WIN
        else:
            return Result.LOSE


class Result(Enum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


class Alive(object):
    def __init__(self, lives):
        self.lives = lives

    def decrease_life(self):
        raise NotImplementedError

    def is_alive(self):
        return self.lives > 0


class MoveMixin(object):
    @staticmethod
    def attack(**kwargs):
        raise NotImplementedError

    @staticmethod
    def defence(**kwargs):
        raise NotImplementedError


class Enemy(Alive, MoveMixin):
    def __init__(self, lives_level):
        super().__init__(lives_level)
        self.level = lives_level

    @staticmethod
    def attack():
        return choice(Attacks.CHOICES.value)

    @staticmethod
    def defence():
        return choice(Attacks.CHOICES.value)

    def decrease_life(self):
        self.lives -= 1
        if self.lives <= 0:
            raise EnemyDown("Enemy is dead")


def player_choice():
    n = ""
    while True:
        n = input()
        if if_command(n):
            check_commands(n)
        else:
            try:
                n = int(n)
            except ValueError:
                print("Invalid input")
            else:
                if n not in (1, 2, 3):
                    print("Invalid number")
                    continue
                else:
                    break
    if n == 1:
        return Attacks.MAGE.value
    elif n == 2:
        return Attacks.WARRIOR.value
    elif n == 3:
        return Attacks.ROGUE.value


class Player(Alive, MoveMixin):
    def __init__(self, name):
        super().__init__(settings.PLAYER_LIVES)
        self.name = name
        self.score = 0

    @staticmethod
    def fight(attack, defence):
        if isinstance(attack, Player):
            attack.attack(defence)
        elif isinstance(attack, Enemy):
            defence.defence(attack)

    def attack(self, enemy_object):
        try:
            player_move = player_choice()
        except ExitGame as e:
            raise e
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
        try:
            player_move = player_choice()
        except ExitGame as e:
            raise e
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
        self.lives -= 1
        if self.lives <= 0:
            raise GameOver(self.name, self.score)
