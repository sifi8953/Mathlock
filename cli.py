from collections.abc import Callable

# (question, grading function)
type Question = tuple[str, Callable[[str], bool]]


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
