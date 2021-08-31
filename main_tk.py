import tkinter as tk
from tkinter import *
from tkinter import ttk
import numpy as np


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry('500x400')
        self.root.resizable(False, False)
        self.root.title('Ticer\'s Apportionment Calculator 0.1.0')

        frame_main = tk.Frame(self.root)
        frame_main.grid(sticky='news')

        # title
        Label(frame_main, text='Ticer\'s Apportionment Calculator 0.1.0').place(relx=.5, y=20,
                                                                                anchor=CENTER)

        # select method
        options = [
            'Hamilton',
            'Jefferson',
            'Adam',
            'Webster'
        ]
        clicked = StringVar()
        clicked.set('Hamilton')
        self.drop_down = OptionMenu(frame_main, clicked, *options).place(relx=.5, y=50, anchor=CENTER)

        # add seats
        Label(frame_main, text='seats: ').place(relx=.45, y=85, anchor=CENTER)
        self.input_seats = Entry(self.root, width=7).place(relx=.54, y=85, anchor=CENTER)

        # add, remove, clear, and calculate
        self.button_add = Button(self.root, text='+', width=5, command=self.add_state).place(relx=.35, y=120,
                                                                                             anchor=CENTER)
        self.button_remove = Button(self.root, text='-', width=5).place(relx=.45, y=120, anchor=CENTER)
        self.button_clear = Button(self.root, text='CLEAR', width=5).place(relx=.55, y=120, anchor=CENTER)
        self.button_calculate = Button(self.root, text='=', width=5).place(relx=.65, y=120, anchor=CENTER)

        # Create a frame for the canvas with non-zero row&column weights
        self.frame_canvas = tk.Frame(frame_main)
        self.frame_canvas.place(relx=.5, y=240, anchor=CENTER)
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        self.canvas = tk.Canvas(self.frame_canvas)
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Create a frame to contain the buttons
        self.frame_buttons = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')

        # Add 9-by-5 buttons to the frame
        self.rows = 2
        self.columns = 5
        # self.grid = np.empty(shape=(self.rows, self.columns), dtype=list_temp)
        self.grid = []

        list_temp = []

        list_temp.append(Label(self.frame_buttons, text='state', width=9))
        list_temp.append(Label(self.frame_buttons, text='population', width=9))
        list_temp.append(Label(self.frame_buttons, text='quota', width=9))
        list_temp.append(Label(self.frame_buttons, text='initial FS', width=9))
        list_temp.append(Label(self.frame_buttons, text='final FS', width=9))

        self.grid.append(list_temp)

        self.grid[0][0].grid(row=0, column=0, sticky='news')
        self.grid[0][1].grid(row=0, column=1, sticky='news')
        self.grid[0][2].grid(row=0, column=2, sticky='news')
        self.grid[0][3].grid(row=0, column=3, sticky='news')
        self.grid[0][4].grid(row=0, column=4, sticky='news')

        list_temp = []
        list_temp.append(Label(self.frame_buttons, text='1', width=9))
        list_temp.append(Entry(self.frame_buttons, width=7))
        list_temp.append(Label(self.frame_buttons, text='-', width=7))
        list_temp.append(Label(self.frame_buttons, text='-', width=7))
        list_temp.append(Label(self.frame_buttons, text='-', width=7))

        self.grid.append(list_temp)

        self.grid[1][0].grid(row=1, column=0, sticky='news', padx=10)
        self.grid[1][1].grid(row=1, column=1, sticky='news', padx=10)
        self.grid[1][2].grid(row=1, column=2, sticky='news', padx=10)
        self.grid[1][3].grid(row=1, column=3, sticky='news', padx=10)
        self.grid[1][4].grid(row=1, column=4, sticky='news', padx=10)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns))
        # first5rows_height = sum([self.grid[i][0].winfo_height() for i in range(0, self.rows)])
        first5rows_height = 190

        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                 height=first5rows_height)

        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Launch the GUI
        self.root.mainloop()

    def add_state(self):
        self.rows += 1
        print(self.rows)

        list_temp = []
        list_temp.append(Label(self.frame_buttons, text=self.rows - 1, width=9))
        list_temp.append(Entry(self.frame_buttons, width=7))
        list_temp.append(Label(self.frame_buttons, text='-', width=7))
        list_temp.append(Label(self.frame_buttons, text='-', width=7))
        list_temp.append(Label(self.frame_buttons, text='-', width=7))

        self.grid.append(list_temp)

        self.grid[self.rows - 1][0].grid(row=self.rows - 1, column=0, sticky='news', padx=10)
        self.grid[self.rows - 1][1].grid(row=self.rows - 1, column=1, sticky='news', padx=10)
        self.grid[self.rows - 1][2].grid(row=self.rows - 1, column=2, sticky='news', padx=10)
        self.grid[self.rows - 1][3].grid(row=self.rows - 1, column=3, sticky='news', padx=10)
        self.grid[self.rows - 1][4].grid(row=self.rows - 1, column=4, sticky='news', padx=10)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns))
        # first5rows_height = sum([self.grid[i][0].winfo_height() for i in range(0, self.rows)])
        first5rows_height = 190

        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                 height=first5rows_height)

        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


if __name__ == '__main__':
    App()
