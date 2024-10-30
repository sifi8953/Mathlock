from c_arithmetic import get_complex
from eq_system import get_eq, get_eq_sys
from poly_eq import get_poly, get_poly_div
from inv_trig import get_inv_trig

import time
import random
from collections.abc import Callable
from typing import Any

from start_menu_gui import start_menu
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
    i = 0
    while True:
        time.sleep(T)  # wait one period
        f(i)  # run
        i += 1  # advance counter


def main() -> None:
    options = start_menu(tuple(EQ_TYPES.keys()))
    if "difficulty" in options.keys():
        OPTIONS["difficulty"] = options["difficulty"] 

    print()
    run_periodically(lambda i: give_question(get_question(options["types"], OPTIONS), i), options["sleep_time"])


if __name__ == "__main__":
    main()
