import time
import random
from collections.abc import Callable

# (question, [answers])
type Question = tuple[str, list[float]]

questions: list[Question] = [
    ("Solve for x:\n\tx = 1 + 1\nx = ", [2]),
    ("Solve for x:\n\tx * 2 = 3\nx = ", [1.5]),
]

SLEEP_TIME: float = 60  # time in seconds between questions


def give_question(q: Question) -> None:
    while True:
        s = input(q[0])
        try:
            x = float(s)
        except ValueError:
            print(f"Error: '{s}' is not a number.\n")
        else:
            if x in q[1]:
                print("Correct!\n")
                break
            else:
                print("Incorrect, try again.\n")


def run_periodically(f: Callable[[], None], T: float):
    while True:
        f()
        time.sleep(T)


def main() -> None:
    run_periodically(lambda: give_question(random.choice(questions)), SLEEP_TIME)


if __name__ == "__main__":
    main()
