from words import words
from random import random
from copy import deepcopy


class bcolors:
    YELLOW = "\33[93m"
    GREEN = "\033[92m"
    ENDC = "\033[0m"


def select_random_word(words):
    return words[int(len(words) * random())]


def get_letter_distribution(word):
    result = {}
    char_array = list(word)
    for char in char_array:
        try:
            result[char] += 1
        except KeyError:
            result[char] = 1
    return result


def initialize_game():
    answer = select_random_word(words)
    letter_distribution = get_letter_distribution(answer)
    print(letter_distribution)
    return {
        "answer": answer,
        "letter_distribution": letter_distribution,
        "guesses": [
            [
                {"value": "_", "color": None},
                {"value": "_", "color": None},
                {"value": "_", "color": None},
                {"value": "_", "color": None},
                {"value": "_", "color": None},
            ]
        ],
    }


def evaluate_guess(game_state, guess):
    result = []
    letter_distribution = deepcopy(game_state["letter_distribution"])
    for idx, char in enumerate(list(guess.upper())):
        if game_state["answer"][idx] == char:
            result.append({"value": char.upper(), "color": bcolors.GREEN})
            letter_distribution[char] -= 1
            continue
        elif char in game_state["answer"] and letter_distribution[char] > 0:
            result.append({"value": char.upper(), "color": bcolors.YELLOW})
            letter_distribution[char] -= 1
            continue
        else:
            result.append({"value": char.upper(), "color": None})
    return result


def get_current_guess(game_state):
    current_guess = game_state["guesses"][len(game_state["guesses"]) - 1]
    result = ""
    for obj in current_guess:
        if obj["color"] is not None:
            result += obj["color"]
        result += obj["value"]
        if obj["color"] is not None:
            result += bcolors.ENDC
        result += " "
    return result


# todo:
# print alphabet with letter distribution and colors after each guess
def game_loop():
    print(f"welcome to {bcolors.GREEN}python wordle!{bcolors.ENDC}\n")
    game_state = initialize_game()
    while True:
        print(f"current guess: {get_current_guess(game_state)}\n")
        guess = input()
        while len(guess) != 5:
            print("all wordle words are 5 letters! try again...\n")
            guess = input()
        result = evaluate_guess(game_state, guess)
        game_state["guesses"].append(result)
        if all([x["color"] == bcolors.GREEN for x in result]):
            print(f"you win, the word was {get_current_guess(game_state)}!\n")
            print("play again? type 1 for yes, 0 for no ...\n")
            play_again = input()
            while play_again != "0" and play_again != "1":
                print("type 1 to play again or 0 to exit wordle...\n")
                play_again = input()
            if play_again == "1":
                game_state = initialize_game()
                continue
            else:
                print("thanks for playing wordle!")
                exit(0)
        elif len(game_state["guesses"]) > 6:
            print("you lose :/ play again? type 1 for yes, 0 for no...\n")
            play_again = input()
            while play_again != "0" and play_again != "1":
                print("type 1 to play again or 0 to exit wordle...\n")
                play_again = input()
            if play_again == "1":
                game_state = initialize_game()
                continue
            else:
                print("thanks for playing wordle!")
                exit(0)


game_loop()
