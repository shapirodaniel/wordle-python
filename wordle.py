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
    # initialize empty list with 5 spots for direct index assignment
    result = [None] * 5
    guess_charlist = list(guess.upper())
    answer_charlist = list(game_state["answer"])
    letters_ht = deepcopy(game_state["letter_distribution"])

    # first pass, convert all exact matches and update ht
    for i, char in enumerate(guess_charlist):
        if guess_charlist[i] == answer_charlist[i]:
            result[i] = {"value": char, "color": bcolors.GREEN}
            letters_ht[char] -= 1

    # second pass with ht
    for i, char in enumerate(guess_charlist):
        # skip exact matches we've already found
        if result[i] is not None:
            continue
        elif char in game_state["answer"] and letters_ht[char] > 0:
            result[i] = {"value": char, "color": bcolors.YELLOW}
            letters_ht[char] -= 1
        else:
            result[i] = {"value": char, "color": None}

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
            print(f"you lose :/ the word was {game_state['answer']}")
            print("play again? type 1 for yes, 0 for no...\n")
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
