from c_arithmetic import get_complex
import time
import random
from collections.abc import Callable

# (question, [answers])
type Question = tuple[str, Callable[[str], bool]]


def parse_float(x: str) -> float:
    try:
        return float(x)
    except ValueError:
        raise ValueError("please input a number")


questions: list[Question] = [
    ("Solve for x:\n\tx = 1 + 1\nx = ", lambda x: parse_float(x) == 2),
    ("Solve for x:\n\tx * 2 = 3\nx = ", lambda x: parse_float(x) == 1.5),
]

EQ_TYPES: list[str] = [
    "complex arithmetic",  # working
    "general eq",
    "system of eq",
    "second deg polynomials",
    "polynomial div",
    "inverse trig",
]

SLEEP_TIME: float = 60  # time in seconds between questions


def get_question(types: list[str]) -> Question:
    type = random.choice(types)

    match type:
        # case "complex arithmetic":
        case _:
            return get_complex(0)


def give_question(q: Question) -> None:
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
    # run_periodically(lambda: give_question(random.choice(questions)), SLEEP_TIME)
    run_periodically(lambda: give_question(get_question(EQ_TYPES)), SLEEP_TIME)


if __name__ == "__main__":
    main()
