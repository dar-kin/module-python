import json
import exception
import settings


SCORES_FILE = settings.SCORES_FILE


def check_for_file():
    try:
        with open(SCORES_FILE, "r+") as file:
            char = file.read(1)
            if not char:
                file.write("{}")
    except FileNotFoundError:
        with open(SCORES_FILE, "w") as file:
            file.write("{}")


def top_ten():
    check_for_file()
    with open(SCORES_FILE, "r") as file:
        scores = json.load(file)
    res = []
    for key, val in scores.items():
        res.append((key, val))
    res.sort(key=lambda x: x[1], reverse=True)
    for elem in res:
        print(f"{elem[0]}: {elem[1]}")


def save_score(player_name, score):
    check_for_file()
    with open(SCORES_FILE, "r") as file:
        scores = json.load(file)
    if player_name in scores.keys():
        if scores[player_name] < score:
            scores[player_name] = score
    elif len(scores) < 10:
        scores[player_name] = score
    elif len(scores) >= 10:
        min_score = 10000
        min_key = ""
        for key, val in scores.items():
            if val < min_score:
                min_score = val
                min_key = key
        if score > min_score:
            del scores[min_key]
            scores[player_name] = score
    with open(SCORES_FILE, "w") as file:
        json.dump(scores, file)


def check_commands(user_input):
    if user_input == "exit":
        raise exception.ExitGame("Exit game")
    elif user_input == "help":
        settings.game_help()
    elif user_input == "show_scores":
        top_ten()


def if_command(suer_input):
    return suer_input in settings.COMMANDS
