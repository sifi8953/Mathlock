import tkinter as tk
from tkinter import ttk

class Checkboxes(ttk.Frame):
   def __init__(self, parent=None, options=[], side=tk.BOTTOM, anchor=tk.W):
      ttk.Frame.__init__(self, parent)
      self.states = []
      self.options = options
      for i, pick in enumerate(options):
         state = tk.IntVar()
         chk = ttk.Checkbutton(self, text=pick, variable=state)
         chk.pack(side=side, anchor=anchor, expand=tk.YES)
         self.states.append(state)

   def active_boxes(self) -> tuple[str]:
      active_types = []
      for i, state in enumerate(self.states, 0):
         if state.get() == 1:
            active_types.append(self.options[i])

      if len(active_types) == 0: #if no box is selected, return all 
         active_types = self.options
      return tuple(active_types)      
   

class Slider(ttk.Frame):
   def __init__(self, parent=None, orient="horizontal", max = 5, min = 1):
      ttk.Frame.__init__(self, parent)
      self.var = tk.IntVar()
      slider = tk.Scale(self, from_=min, to=max, variable=self.var, orient=orient)
      slider.pack()

   def value(self) -> int:
      return self.var.get()
   
   
def start_menu(eq_types: tuple[str]) -> dict[str]:
    exit = False
    win = tk.Tk()  # new window
    win.title("MathLock Settings")  # rename window
    win_width = 500  # window width
    win_height = 500  # window height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_cord = (screen_width - win_width) // 2  # horizontal offset
    y_cord = (screen_height - win_height) // 2  # vertical offset
    win.geometry(f"{win_width}x{win_height}+{x_cord}+{y_cord}")  # resize and reposition
    win.resizable(False, False) # disable resizing

    
    # create widgets
    eq_options = ttk.Frame(win)
    eq_text = ttk.Label(eq_options, text="Equation types")
    eq_checkbar = Checkboxes(eq_options, eq_types)

    diff = ttk.Frame(win)
    diff_text = ttk.Label(diff, text="Difficulty")
    diff_slider = Slider(diff)

    sleep = ttk.Frame(win)
    sleep_text = ttk.Label(sleep, text="Sleep Time")
    sleep_slider = Slider(sleep, max=256, min=0)

    start = ttk.Button(win, text="Start", command = win.destroy)

    #set grid row and column size
    for col in range(4):
        win.grid_columnconfigure(col, minsize=250)
    for row in range(4):
        win.grid_rowconfigure(row, minsize=250)

    #grid elements
    eq_options.grid(row = 0, column = 0)
    diff.grid(row = 0, column = 1)
    sleep.grid(row = 1, column = 0)
    start.grid(row = 1, column = 1)
  
    #add widgets
    eq_text.pack(side="top")
    eq_checkbar.pack(side="top")

    diff_text.pack(side="top")
    diff_slider.pack()

    sleep_text.pack(side="top")
    sleep_slider.pack(side="top")

    win.mainloop() # show window

    return {
          "types":eq_checkbar.active_boxes(),
          "difficulty":diff_slider.value(),
          "sleep_time":sleep_slider.value()
       } 