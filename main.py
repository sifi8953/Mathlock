# (question, [answers])
type Question = tuple[str, list[float]]

questions: list[Question] = [
    ("Solve for x:\n\tx = 1 + 1\nx = ", [2])
]


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


def main() -> None:
    for q in questions:
        give_question(q)


if __name__ == "__main__":
    main()
