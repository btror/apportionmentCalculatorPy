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
        self.button_add = Button(self.root, text='+', width=5).place(relx=.35, y=120, anchor=CENTER)
        self.button_remove = Button(self.root, text='-', width=5).place(relx=.45, y=120, anchor=CENTER)
        self.button_clear = Button(self.root, text='CLEAR', width=5).place(relx=.55, y=120, anchor=CENTER)
        self.button_calculate = Button(self.root, text='=', width=5).place(relx=.65, y=120, anchor=CENTER)

        # Create a frame for the canvas with non-zero row&column weights
        frame_canvas = tk.Frame(frame_main)
        frame_canvas.place(relx=.5, y=210, anchor=CENTER)
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        # Create a frame to contain the buttons
        frame_buttons = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

        # Add 9-by-5 buttons to the frame
        self.rows = 5
        self.columns = 5
        self.grid = np.empty(shape=(self.rows, self.columns), dtype=list)

        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if i == 0:
                    self.grid[i][0] = Label(frame_buttons, text='state', width=9)
                    self.grid[i][0].grid(row=0, column=0, sticky='news')

                    self.grid[i][1] = Label(frame_buttons, text='population', width=9)
                    self.grid[i][1].grid(row=0, column=1, sticky='news')

                    self.grid[i][2] = Label(frame_buttons, text='quota', width=9)
                    self.grid[i][2].grid(row=0, column=2, sticky='news')

                    self.grid[i][3] = Label(frame_buttons, text='initial FS', width=9)
                    self.grid[i][3].grid(row=0, column=3, sticky='news')

                    self.grid[i][4] = Label(frame_buttons, text='final FS', width=9)
                    self.grid[i][4].grid(row=0, column=4, sticky='news')

                else:
                    if j == 0:
                        self.grid[i][j] = Label(frame_buttons, text=i, width=7)
                        self.grid[i][j].grid(row=i, column=j, sticky='news', padx=10)
                    elif j == 1:
                        self.grid[i][j] = Entry(frame_buttons, text='-', width=7)
                        self.grid[i][j].grid(row=i, column=j, sticky='news', padx=10)
                    else:
                        self.grid[i][j] = Label(frame_buttons, text='-', width=7)
                        self.grid[i][j].grid(row=i, column=j, sticky='news', padx=10)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns))
        first5rows_height = sum([self.grid[i][0].winfo_height() for i in range(0, self.rows)])

        frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                            height=first5rows_height)

        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))

        # Launch the GUI
        self.root.mainloop()


if __name__ == '__main__':
    App()

