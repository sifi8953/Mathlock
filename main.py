from start_menu import start_menu
from c_arithmetic import get_complex
from eq_system import get_eq, get_eq_sys
from poly_eq import get_poly, get_poly_div
from inv_trig import get_inv_trig

import time
import random
from collections.abc import Callable
from typing import Any

from gui import give_question

# (question, grading function)
type Question = tuple[str, Callable[[str], bool]]

# (name, function to question)
EQ_TYPES: dict[str, Callable[[], Question]] = {
    "complex arithmetic": get_complex,  # working
    "general eq": get_eq,  # working
    "system of eq": get_eq_sys,  # working
    "second deg polynomials": get_poly,  # working
    "polynomial div": get_poly_div,  # working
    "inverse trig": get_inv_trig,  # working
}

# arguments to get_{equation type} functions
OPTIONS: dict[Any] = {
    "difficulty": 3,
    "degree": 2,
    "var_count": 3
}


def get_question(types: tuple[str], options: dict[Any]) -> Question:
    '''generate and return a random question from among the types'''
    return EQ_TYPES[random.choice(types)](**options)


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
