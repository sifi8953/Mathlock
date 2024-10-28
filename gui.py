import tkinter as tk
from tkinter import ttk

from collections.abc import Callable

# (question, grading function)
type Question = tuple[str, Callable[[str], bool]]


def validate(grade: Callable[[str], bool], error: ttk.Label, root: tk.Tk):
    def f(event: tk.Event):
        entry: ttk.Entry = event.widget
        ans = entry.get()

        # make sure it can be closed still
        if ans == "q":
            quit()

        try:
            correct = grade(ans)
        except ValueError as e:
            error.config(text=f"Error: {e}")
        else:
            if correct:
                # close window
                root.destroy()
                root.quit()
            else:
                error.config(text=f"Incorrect, try again.")
    return f


def give_question(q: Question, i: int) -> None:
    '''notify and give user question until they get it right'''
    win = tk.Tk()  # new window
    win.title("MathLock")  # rename window
    win.resizable(False, False)  # disable resizing
    win.attributes("-topmost", True)  # always on top
    # win.attributes("-type", "toolbar")  # disable minimizing and closing

    win_width = 500  # window width
    win_height = 500  # window height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_cord = (screen_width - win_width) // 2  # horizontal offset
    y_cord = (screen_height - win_height) // 2  # vertical offset
    win.geometry(f"{win_width}x{win_height}+{x_cord}+{y_cord}")  # resize and reposition

    # create widgets
    center = ttk.Frame(win)
    number = ttk.Label(center, text=f"Question #{i+1}")
    seperator = ttk.Separator(center)
    label = ttk.Label(center, text=q[0], wraplength=int(win_width * 0.9))
    entry = ttk.Entry(center)
    error = ttk.Label(center)

    # bind enter to submit
    entry.bind("<Return>", validate(q[1], error, win))
    entry.focus()  # focus on text box, doesn't seem to work on Ubuntu at least

    # add widgets
    number.pack()
    seperator.pack(fill="x")
    label.pack()
    entry.pack()
    error.pack()
    center.place(relx=0.5, rely=0.5, anchor="center")

    win.mainloop()  # show window


if __name__ == "__main__":
    give_question(("Question\nx = ", lambda x: False))
