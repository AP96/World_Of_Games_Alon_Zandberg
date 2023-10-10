import random
import time
import utils

WELCOME_PROMPT = '\n------------------ Welcome to the Memory Game ! Are you a memory magician ? ' \
                 '------------------ \n'
INPUT_PROMPT = '\nHello User ! \nPlease guess the value of a new generated random number (between 1 to 100) : '


def welcome():
    print(WELCOME_PROMPT)


def play(level):
    welcome()
    sequence = generate_sequence(level)
    guess_list = get_list_from_user(INPUT_PROMPT, level)
    comparison = is_list_equal(sequence, guess_list)
    result = "Won" if comparison == 1 else "Lost"
    print(f'\n\nYou have {result} Memory Guess Game !')
    return result


def generate_sequence(level):
    generated_seq = []
    for i in range(level):
        generated_seq.append(random.randint(0, 101))
    for num in generated_seq:
        print(num, end=' ', flush=True)
    time.sleep(0.7)
    utils.screen_cleaner()
    return generated_seq


def get_list_from_user(prompt, length):
    guess_list = []
    i = 0
    while i < length:
        choice = input(prompt)
        if choice.isdigit() and 1 <= int(choice) <= 100:
            guess_list.append(int(choice))
            i += 1
        else:
            print(f"Illegal Input! Please enter a valid Integer number between 1 and 100.")
    return guess_list


def is_list_equal(guess_list, generated_lists):
    return sorted(guess_list) == sorted(generated_lists)
