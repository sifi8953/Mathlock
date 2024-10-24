from start_menu import start_menu
from c_arithmetic import get_complex
from eq_system import get_eq
from poly_eq import get_poly

import time
import random
from collections.abc import Callable
from typing import Any

# (question, grading function)
type Question = tuple[str, Callable[[str], bool]]

# (name, function to question)
EQ_TYPES: dict[str, Callable[[], Question]] = {
    "complex arithmetic": get_complex,  # working
    "general eq": get_eq,  # working
    "system of eq": NotImplemented,  # started
    "second deg polynomials": get_poly,  # working
    "polynomial div": NotImplemented,
    "inverse trig": NotImplemented,
}

# arguments to get_{equation type} functions
OPTIONS: dict[Any] = {
    "difficulty": 2,
    "degree": 2
}


def get_question(types: tuple[str], options: dict[Any]) -> Question:
    '''generate and return a random question from among the types'''
    return EQ_TYPES[random.choice(types)](**options)


def give_question(q: Question) -> None:
    '''notify and give user question until they get it right'''
    print(end="\007")  # play notification sound

    while True:
        try:
            # call grading function of question with user inputted answer
            correct = q[1](input(q[0]))
        except ValueError as e:
            # grading function failed
            print(f"Error: {e}\n")
        else:
            # grading successfull
            if correct:
                print("Correct!\n")
                break  # done with question
            else:
                print("Incorrect, try again.\n")


def run_periodically(f: Callable[[], None], T: float):
    while True:
        f()  # run
        time.sleep(T)  # wait one period


def main() -> None:
    options = start_menu()
    types = options["types"]  # types = ("complex arithmetic", "general eq")
    sleep_time = options["sleep_time"]
    # run_periodically(lambda: give_question(random.choice(questions)), SLEEP_TIME)
    run_periodically(lambda: give_question(get_question(types, OPTIONS)), sleep_time)


if __name__ == "__main__":
    main()
