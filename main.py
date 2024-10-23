from c_arithmetic import get_complex
from general_eq import get_eq

import time
import random
from collections.abc import Callable
from typing import Any

# (question, [answers])
type Question = tuple[str, Callable[[str], bool]]

EQ_TYPES: dict[str, Callable[[str], Question]] = {
    "complex arithmetic": get_complex,  # working
    "general eq": get_eq,  # working
    "system of eq": NotImplemented,
    "second deg polynomials": NotImplemented,
    "polynomial div": NotImplemented,
    "inverse trig": NotImplemented,
}

OPTIONS: dict[Any] = {
    "difficulty": 4,
}

SLEEP_TIME: float = 60  # time in seconds between questions


def get_question(types: tuple[str], options: dict[Any]) -> Question:
    return EQ_TYPES[random.choice(types)](**options)


def give_question(q: Question) -> None:
    print(end="\007")  # play notification sound

    while True:
        try:
            correct = q[1](input(q[0]))
        except ValueError as e:
            print(f"Error: {e}\n")
        else:
            if correct:
                print("Correct!\n")
                break
            else:
                print("Incorrect, try again.\n")


def run_periodically(f: Callable[[], None], T: float):
    while True:
        f()
        time.sleep(T)


def main() -> None:
    types = ("complex arithmetic", "general eq")

    # run_periodically(lambda: give_question(random.choice(questions)), SLEEP_TIME)
    run_periodically(lambda: give_question(get_question(types, OPTIONS)), SLEEP_TIME)


if __name__ == "__main__":
    main()
