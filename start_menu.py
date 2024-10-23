QUESTION_TYPES = ("complex arithmetic",
            "general eq",
            "system of eq",
            "second deg polynomials",
            "polynomial div",
            "inverse trig")

def start_menu() -> dict[str]:
    options = {}
    options.update({"types":choose_question_types(QUESTION_TYPES)})
    options.update({"sleep_time":duration_input()})
    return options

def duration_input():
    while True:
        try:
            i = int(input("\nChoose duration between questions(in seconds): "))
            if i >= 0:
                return(i)
            else:
                print("Duration cannot be negative")
        except ValueError:
            pass
    
def choose_question_types(questions: tuple[str]) -> tuple[str]:
    chosen_questions = []
    print("\nChoose question types\n")
    for index, question_type in enumerate(questions, 0):
            print(f"{index}) {question_type}")
    while True:
        if len(chosen_questions) > 0:
            print("\nYour chosen question types")
            for question_type in chosen_questions:
                print(f"\t{question_type}")
                
        chosen_option = input("\nChoose question type: ")
        if chosen_option == "":
            if len(chosen_questions) > 0:
                return tuple(chosen_questions)
            else:
                print("\nMust choose atleast one question type!")
        else:
            try:
                i = int(chosen_option)
                if questions[i] not in chosen_questions:
                    chosen_questions.append(questions[i])
            except:
                pass
