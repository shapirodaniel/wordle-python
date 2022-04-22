from words import words
from random import random


class bcolors:
    YELLOW = "\33[93m"
    GREEN = "\033[92m"
    ENDC = "\033[0m"


"""
todo

prompt for guess
if word not in dictionary, prompt for retry

else, evaluate input against word
if letter in right spot, show green letter on guess and keyboard
if letter in word and not in right spot, show yellow letter on guess and keyboard
if letter not in word, show grey letter on keyboard

print current word

if all letters correct, show win dialog and prompt to restart
else loop to start
"""


def select_random_word(words):
    return words[int(len(words) * random())]


def initialize_game():
    return {
        "answer": select_random_word(words),
        "num_guesses": 0,
        "guesses": [
            [
                {"value": "_", "color": None},
                {"value": "_", "color": None},
                {"value": "_", "color": None},
                {"value": "_", "color": None},
                {"value": "_", "color": None},
            ]
        ],
        "won": False,
        "playing": True,
    }


def evaluate_guess(game_state, guess):
    result = []
    for idx, char in enumerate(list(guess.upper())):
        if game_state["answer"][idx] == char:
            result.append({"value": char.upper(), "color": bcolors.GREEN})
            continue
        if char in game_state["answer"]:
            result.append({"value": char.upper(), "color": bcolors.YELLOW})
            continue
        else:
            result.append({"value": char.upper(), "color": None})
    return result


def get_current_guess(game_state):
    current_guess = game_state["guesses"][len(game_state["guesses"]) - 1]
    result = ""
    for idx, obj in enumerate(current_guess):
        if obj["color"] is not None:
            result += obj["color"]
        result += obj["value"]
        if obj["color"] is not None:
            result += bcolors.ENDC
        if idx < len(current_guess):
            result += " "
    print(current_guess)
    return result


def game_loop():
    game_state = initialize_game()
    print(f"welcome to {bcolors.GREEN}python wordle!{bcolors.ENDC}\n")
    while game_state["playing"] == True:
        print(f"current guess: {get_current_guess(game_state)}\n")
        guess = input()
        result = evaluate_guess(game_state, guess)
        game_state["guesses"].append(result)
        if all([x["color"] == bcolors.GREEN for x in result]):
            game_state["won"] = True
            print(f"you win, the word was {get_current_guess(game_state)}!")
            exit(0)
        elif len(game_state["guesses"]) > 6:
            print("you lose :/ play again? type 1 for yes, 0 for no...")
            play_again = input()
    while play_again != "0" and play_again != "1":
        print("type 1 to play again or 0 to exit wordle...")
        play_again = input()
    if play_again == 1:
        game_state = initialize_game()
    else:
        game_state["playing"] = False
        print("thanks for playing wordle!")
        exit(0)


game_loop()
