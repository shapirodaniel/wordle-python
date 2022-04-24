from words import words
from random import random
import copy, string, os


class bcolors:
    DARK_GRAY = "\033[90m"
    RED = "\33[91m"
    GREEN = "\033[92m"
    YELLOW = "\33[93m"
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
    return {
        "answer": answer,
        "letter_distribution": letter_distribution,
        "guesses": [],
        # { 'A': None, 'B': None, ... }
        # will be updated whenever a char match is found
        "alphabet": dict.fromkeys(string.ascii_uppercase, None),
    }


def evaluate_guess(game_state, guess):
    # initialize empty list with 5 spots for direct index assignment
    result = [None] * 5
    guess_charlist = list(guess)
    answer_charlist = list(game_state["answer"])
    letters_ht = copy.deepcopy(game_state["letter_distribution"])
    # first pass, convert all exact matches and update ht
    for i, char in enumerate(guess_charlist):
        if guess_charlist[i] == answer_charlist[i]:
            result[i] = {"value": char, "color": bcolors.GREEN}
            game_state["alphabet"][char] = bcolors.GREEN
            letters_ht[char] -= 1
    # second pass with ht
    for i, char in enumerate(guess_charlist):
        # skip exact matches we've already found
        if result[i] is not None:
            continue
        elif char in game_state["answer"] and letters_ht[char] > 0:
            result[i] = {"value": char, "color": bcolors.YELLOW}
            game_state["alphabet"][char] = bcolors.YELLOW
            letters_ht[char] -= 1
        else:
            result[i] = {"value": char, "color": None}
            game_state["alphabet"][char] = bcolors.DARK_GRAY
    return result


def latest_guess(guesses):
    return guesses[len(guesses) - 1]


def build_guess(guess):
    result = ""
    for obj in guess:
        if obj["color"] is not None:
            result += obj["color"]
        result += obj["value"]
        if obj["color"] is not None:
            result += bcolors.ENDC
        result += " "
    return result


def get_current_guess(game_state):
    current_guess = latest_guess(game_state["guesses"])
    return build_guess(current_guess)


def get_all_guesses(game_state):
    result = ""
    for guess in game_state["guesses"]:
        result += build_guess(guess) + "\n"
    return result


def get_current_alphabet(alphabet_dict):
    result = bcolors.ENDC
    for (letter, color) in alphabet_dict.items():
        if color is not None:
            result += f"{color}{letter}{bcolors.ENDC}"
        else:
            result += letter
        result += " "
    return result


def already_guessed(game_state, guess):
    count = 0
    for previous_guess in game_state["guesses"]:
        for i, char_dict in enumerate(previous_guess):
            if char_dict["value"] == guess[i]:
                count += 1
        if count == 5:
            return True
        else:
            count = 0
    return False


def game_loop():
    game_title = f"{bcolors.GREEN}python wordle{bcolors.ENDC}"
    game_state = initialize_game()

    while True:
        os.system("clear")
        print(f"welcome to {game_title}!\n")
        print(get_all_guesses(game_state))
        print(get_current_alphabet(game_state["alphabet"]))

        guess = input("> ").strip().upper()

        while len(guess) != 5:
            print("all wordle words are 5 letters! try again...\n")
            guess = input("> ").strip().upper()
        while guess not in words:
            print(f"{guess} is not in the wordle dictionary! try again...\n")
            guess = input("> ").strip().upper()
        while already_guessed(game_state, guess):
            print(f"{guess} was already guessed! try again...\n")
            guess = input("> ").strip().upper()

        result = evaluate_guess(game_state, guess)
        game_state["guesses"].append(result)
        won = all([x["color"] == bcolors.GREEN for x in result])
        lost = len(game_state["guesses"]) == 6 and not won

        if not won and not lost:
            continue
        elif won:
            winning_word = get_current_guess(game_state).replace(" ", "")
            print(f"you win, the word was {winning_word}!\n")
        elif lost:
            print(f"you lose :/ the word was {bcolors.RED}{game_state['answer']}{bcolors.ENDC}")

        print("play again? type 1 for yes, 0 for no...\n")
        play_again = input("> ").strip()

        while play_again != "0" and play_again != "1":
            print("type 1 to play again or 0 to exit wordle...\n")
            play_again = input("> ").strip()

        if play_again == "1":
            game_state = initialize_game()
            continue
        else:
            print(f"thanks for playing {game_title}!")
            exit(0)


game_loop()
