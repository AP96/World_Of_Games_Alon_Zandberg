from currency_converter import CurrencyConverter
import random

VALID_USER_USD_INPUT_CHOICES = list(range(1, 101))
WELCOME_PROMPT = '\n------------------ Welcome to the Currency Roulette Game ! Enjoy guessing the secret roulette ' \
                 'number :) ------------------ \n'
INPUT_PROMPT = 'Hello User ! \n Please guess the value of a new generated random number (between 1 to 100) in USD : '


def welcome():
    print(WELCOME_PROMPT)


def play(level):
    welcome()
    converter = CurrencyConverter()
    money_interval = get_money_interval(level, random.randint(0, 101), converter)
    guess = get_guess_from_user(INPUT_PROMPT, VALID_USER_USD_INPUT_CHOICES, converter)
    comparison = compare_results(guess, money_interval)
    result = "Won" if comparison == 1 else "Lost"
    print(f'You have {result} Currency Roulette Guess Game !')
    return result


# The get_money_interval function will calculate an interval of possible values
# in ILS that the player needs to guess within.
# The size of this interval is influenced by the game's difficulty level
def get_money_interval(level, generated, converter):
    exchanged = round(converter.convert(generated, 'USD', 'ILS'))
    interval = range(exchanged - level, exchanged + level + 1)
    return interval


# The function prompts the user to guess the amount of money in USD
# which is then converted to ILS using the converter. Final User's guess returned will be in ILS
# and it will be compared to the valid_money_interval range also which is also in the converted ILS.
def get_guess_from_user(prompt, valid_choices, converter):
    while True:
        choice = input(prompt)
        if choice.isdigit():
            if int(choice) in valid_choices:
                exchanged = round(converter.convert(int(choice), 'USD', 'ILS'))
                return exchanged
            else:
                print(f"Invalid choice. Please select a choice in {valid_choices}.")
        else:
            print(f"Illegal Input! Please enter a valid Integer number for the {valid_choices} choice.")


# An interval of possible values in ILS is compared against a user_guess in ILS
def compare_results(user_guess, range_options):
    return True if user_guess in list(range_options) else False
