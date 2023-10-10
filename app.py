# Constants
import currency_roulette_game
import guess_game
import memory_game
import score
import utils

GAME_INPUT_CHOICES = [1, 2, 3, 4]
DIFFICULTY_INPUT_CHOICES = [1, 2, 3, 4, 5]
GAMES_DESCRIPTION_CHOICES = [
    "Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back.",
    "Guess Game - guess a number and see if you chose like the computer.",
    "Currency Roulette - try and guess the value of a random amount of USD in ILS."
]


def welcome(username):
    print(f'Hi {username} and welcome to the World of Games: The Epic Journey')


def start_play():
    while True:
        print("\nPlease choose a game to play:")
        # index enumerator starts at index 1
        for index, description in enumerate(GAMES_DESCRIPTION_CHOICES, 1):
            print(f"{index}. {description}")

        # Adding an exit option
        print(f"{len(GAMES_DESCRIPTION_CHOICES) + 1}. Exit")

        game = get_user_choice("User selected choice : ", GAME_INPUT_CHOICES, "Game")

        if game == len(GAMES_DESCRIPTION_CHOICES) + 1:
            print("\nThank you for playing !\n")
            break

        level = get_user_choice("Please select a difficulty level between 1 and 5: ", DIFFICULTY_INPUT_CHOICES,
                                "Difficulty level")
        print(f'\nGame number {game} has been selected with difficulty level {level} ! \n')
        play(game, level)
        utils.screen_cleaner()


def play(game, level):
    result = None
    if game == 1:
        result = memory_game.play(level)
    elif game == 2:
        result = guess_game.play(level)
    else:
        result = currency_roulette_game.play(level)
    if result == 'Won':
        score.add_score(level)

def get_user_choice(prompt, valid_choices, mode):
    while True:
        choice = input(prompt)
        if choice.isdigit():
            if int(choice) in valid_choices:
                return int(choice)
            else:
                print(f"Invalid {mode} choice. Please select a choice in {valid_choices}.")
        else:
            print(f"Illegal Input! Please enter a valid Integer number for the {mode} choice.")
