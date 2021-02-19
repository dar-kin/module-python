import logging
import models
import exception
from misc import check_commands, save_score


logging.basicConfig(filename="logs.txt")


def play():
    player_name = ""
    while len(player_name) < 5 or player_name in ("help", "show_scores"):
        player_name = input("Input your name. It must be at least 5 characters "
                            "(not 'help', 'exit', 'show_scores').\n")
        if player_name == 'help':
            continue
        check_commands(player_name)
    if player_name == "exit":
        raise exception.ExitGame
    player = models.Player(name=player_name)
    level = 1
    enemy = models.Enemy(1)
    print(f"Starting the game. You have {player.lives} hp.")
    print(f"Generating an enemy of level {level}")
    while True:
        try:
            print("You are attacking.")
            models.Player.fight(player, enemy)
            print("You are defending.")
            models.Player.fight(enemy, player)
        except exception.EnemyDown:
            level += 1
            player.score += 5
            print(f"Enemy down. You got 5 points. You now have {player.score} points. "
                  f"Generating a new one of level {level}.")
            enemy = models.Enemy(level)


if __name__ == "__main__":
    try:
        play()
    except exception.ExitGame as error:
        print("Game was stopped manually. Score is not recorded.")
        logging.exception(error)
    except KeyboardInterrupt as error:
        logging.exception(error)
    except exception.GameOver as error:
        print("Your game is over. Your score has been recorded.")
        save_score(error.player_name, error.score)
        logging.exception(error)
    finally:
        print("Goodbye!")
