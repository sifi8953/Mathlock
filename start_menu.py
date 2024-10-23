QUESTION_TYPES = ("complex arithmetic",
            "general eq",
            "system of eq",
            "second deg polynomials",
            "polynomial div",
            "inverse trig")

def start_menu() -> dict[str]:
    options = {}
    options.update({"types":choose_question_types(QUESTION_TYPES)})
    options.update({"sleep_time":choose_interval()})
    return options

def choose_interval():
    while True:
        try:
            interval = int(input("\nChoose interval between questions(in seconds): "))
            return(interval)
        except ValueError:
            pass
    
def choose_question_types(questions: tuple[str]) -> tuple[str]:
    chosen_questions = []
    print("\nChoose question types\n")
    for index, question_type in enumerate(questions, 0):
            print(f"{index}) {question_type}")
    while True:
        print("\nYour chosen question types\n")
        if len(chosen_questions) > 0:
            for question_type in chosen_questions:
                print(f"--{question_type}")
            print()
                
        chosen_option = input("Add question type: ")
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
