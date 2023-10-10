import random
import app

WELCOME_PROMPT = '\n------------------ Welcome to the Guess Game ! Enjoy guessing the magic number :) ' \
                 '------------------ \n'


def welcome():
    print(WELCOME_PROMPT)


def play(level):
    welcome()
    secret_number = generate_number(level)
    comparison = compare_results(secret_number, get_guess_from_user(level))
    result = "Won" if comparison == 1 else "Lost"
    print(f'You have {result} Guess Game !')
    return result


def generate_number(level):
    return random.randint(0, level + 1)


def get_guess_from_user(level):
    guess = app.get_user_choice(f'Please select a difficulty level between 0 and {level}: ', list(range(0, level + 1)),
                                "Difficulty level")
    return guess


def compare_results(secret_number, guess):
    return secret_number == guess
