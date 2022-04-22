from words import words
from random import random


class bcolors:
    YELLOW = "\33[33m"
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
    }


def evaluate_guess(game_state, guess):
    result = []
    for idx, char in enumerate(guess.upper().split("")):
        if game_state.answer[idx] == char:
            result.append({"value": char, "color": bcolors.GREEN})
            continue
        if char in game_state.answer:
            result.append({"value": char, "color": bcolors.YELLOW})
            continue
        else:
            result.append({"value": char, "color": None})
    return result


def get_current_guess(game_state):
    current_guess = game_state["guesses"][len(game_state["guesses"]) - 1]
    result = ""
    for idx, obj in enumerate(current_guess):
        result += obj["value"]
        if idx < len(current_guess):
            result += " "
    return result


def game_loop():
    game_state = initialize_game()
    print(game_state)

    print("welcome to python wordle!\n")
    print(f"current guess: {get_current_guess(game_state)}\n")

    while game_state.playing == True:
        guess = input()
        result = evaluate_guess(game_state, guess)
        game_state.guesses.append(result)
        for char_obj in result:
            if all(char_obj.color == bcolors.GREEN):
                game_state.won = True
                print("you win!")
                print(game_state.guesses[len(game_state.guesses) - 1])
            elif len(game_state.guesses) == 6:
                print("you lose :/ play again? type 1 for yes, 0 for no...")
                play_again = input()
                while play_again != 0 or play_again != 1:
                    print("type 1 to play again or 0 to exit wordle...")
                if play_again == 1:
                    game_state = initialize_game()
                else:
                    game_state.playing = False

    print("thanks for playing wordle!")
    exit(0)


game_loop()
