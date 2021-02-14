import exception
import settings
import json


scores_file = settings.SCORES_FILE


def check_for_file():
    try:
        with open(scores_file, "r+") as f:
            char = f.read(1)
            if not char:
                f.write("{}")
    except FileNotFoundError:
        with open(scores_file, "w") as f:
            f.write("{}")


def top_ten():
    check_for_file()
    with open(scores_file, "r") as f:
        scores = json.load(f)
    res = []
    for key, val in scores.items():
        res.append((key, val))
    res.sort(key=lambda x: x[1], reverse=True)
    for elem in res:
        print(f"{elem[0]}: {elem[1]}")


def save_score(player_name, score):
    check_for_file()
    with open(scores_file, "r") as f:
        scores = json.load(f)
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
    with open(scores_file, "w") as f:
        json.dump(scores, f)


def check_commands(n):
    if n == "exit":
        raise exception.ExitGame("Exit game")
    elif n == "help":
        settings.game_help()
    elif n == "show_scores":
        top_ten()
