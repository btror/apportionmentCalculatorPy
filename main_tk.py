import tkinter as tk
from tkinter import *
from methods.hamilton import Hamilton
from methods.jefferson import Jefferson
from methods.adam import Adam
from methods.webster import Webster


class App:
    def __init__(self):
        """
        init - initialize variables
        """

        self.root = tk.Tk()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry('500x400')
        self.root.resizable(False, False)
        self.root.title('Ticer\'s Apportionment Calculator 0.1.0')

        frame_main = tk.Frame(self.root)
        frame_main.grid(sticky='news')

        # top label (title)
        Label(frame_main, text='Ticer\'s Apportionment Calculator 0.1.0').place(relx=.5, y=20,
                                                                                anchor=CENTER)

        # select apportionment method
        options = [
            'Hamilton',
            'Jefferson',
            'Adam',
            'Webster'
        ]
        self.clicked = StringVar()
        self.clicked.set('Hamilton')
        self.drop_down = OptionMenu(frame_main, self.clicked, *options).place(relx=.5, y=50, anchor=CENTER)

        # entry for amount of seats
        Label(frame_main, text='seats: ').place(relx=.45, y=85, anchor=CENTER)
        self.input_seats = Entry(self.root, width=7).place(relx=.54, y=85, anchor=CENTER)

        # add, remove, clear, and calculate buttons
        self.button_add = Button(self.root, text='+', width=5, command=self.add_state).place(relx=.35, y=120,
                                                                                             anchor=CENTER)
        self.button_remove = Button(self.root, text='-', width=5, command=self.remove_state).place(relx=.45, y=120,
                                                                                                   anchor=CENTER)
        self.button_clear = Button(self.root, text='CLEAR', width=5, command=self.clear_states).place(relx=.55, y=120,
                                                                                                      anchor=CENTER)
        self.button_calculate = Button(self.root, text='=', width=5, command=self.calculate).place(relx=.65, y=120,
                                                                                                   anchor=CENTER)

        # create a frame for the canvas
        self.frame_canvas = tk.Frame(frame_main)
        self.frame_canvas.place(relx=.5, y=240, anchor=CENTER)
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)

        # allows widget resizing later
        self.frame_canvas.grid_propagate(False)

        # add a canvas to the frame
        self.canvas = tk.Canvas(self.frame_canvas)
        self.canvas.grid(row=0, column=0, sticky="news")

        # add a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # create a frame to contain the widgets
        self.frame_buttons = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')

        # initialize a default number of rows and columns (cols is ALWAYS 5 and rows is dynamic, but starts as 2)
        self.rows = 2
        self.columns = 5

        # create a list to hold the widgets
        self.grid = []

        # add the first row of widgets (all labels)
        list_temp = [Label(self.frame_buttons, text='state', width=9),
                     Label(self.frame_buttons, text='population', width=9),
                     Label(self.frame_buttons, text='quota', width=9),
                     Label(self.frame_buttons, text='initial FS', width=9),
                     Label(self.frame_buttons, text='final FS', width=9)]

        self.grid.append(list_temp)

        self.grid[0][0].grid(row=0, column=0, sticky='news')
        self.grid[0][1].grid(row=0, column=1, sticky='news')
        self.grid[0][2].grid(row=0, column=2, sticky='news')
        self.grid[0][3].grid(row=0, column=3, sticky='news')
        self.grid[0][4].grid(row=0, column=4, sticky='news')

        # add the second row of widgets (all labels and one entry)
        list_temp = [Label(self.frame_buttons, text='1', width=9), Entry(self.frame_buttons, width=7),
                     Label(self.frame_buttons, text='-', width=7), Label(self.frame_buttons, text='-', width=7),
                     Label(self.frame_buttons, text='-', width=7)]

        self.grid.append(list_temp)

        self.grid[1][0].grid(row=1, column=0, sticky='news', padx=10)
        self.grid[1][1].grid(row=1, column=1, sticky='news', padx=10)
        self.grid[1][2].grid(row=1, column=2, sticky='news', padx=10)
        self.grid[1][3].grid(row=1, column=3, sticky='news', padx=10)
        self.grid[1][4].grid(row=1, column=4, sticky='news', padx=10)

        # update widget frames idle tasks to let tkinter calculate widget sizes
        self.frame_buttons.update_idletasks()

        # resize the canvas frame (width fits depending on input, height is static)
        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns))
        first5rows_height = 190

        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                 height=first5rows_height)

        # set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # launch
        self.root.mainloop()

    def add_state(self):
        """
        add_state - adds a new row to the grid (4 labels and 1 entry)
        """

        # increment rows
        self.rows += 1

        # add a new row of widgets to the grid
        list_temp = [Label(self.frame_buttons, text=self.rows - 1, width=9), Entry(self.frame_buttons, width=7),
                     Label(self.frame_buttons, text='-', width=7), Label(self.frame_buttons, text='-', width=7),
                     Label(self.frame_buttons, text='-', width=7)]

        self.grid.append(list_temp)

        self.grid[self.rows - 1][0].grid(row=self.rows - 1, column=0, sticky='news', padx=10)
        self.grid[self.rows - 1][1].grid(row=self.rows - 1, column=1, sticky='news', padx=10)
        self.grid[self.rows - 1][2].grid(row=self.rows - 1, column=2, sticky='news', padx=10)
        self.grid[self.rows - 1][3].grid(row=self.rows - 1, column=3, sticky='news', padx=10)
        self.grid[self.rows - 1][4].grid(row=self.rows - 1, column=4, sticky='news', padx=10)

        # update widget frames idle tasks to calculate widget sizes
        self.frame_buttons.update_idletasks()

        # resize the canvas frame (width fits depending on input, height is static)
        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns))
        first5rows_height = 190

        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                 height=first5rows_height)

        # set canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def remove_state(self):
        """
        remove_state - removes the last row from the grid (4 labels and 1 entry)
        """

        # always keep the first two default rows
        if self.rows > 2:
            # decrement rows
            self.rows -= 1

            # remove the widget from the grid
            for i, widget in enumerate(self.grid[len(self.grid) - 1]):
                widget.grid_forget()

            self.grid.pop(len(self.grid) - 1)

            # update widget frames idle tasks to calculate widget sizes
            self.frame_buttons.update_idletasks()

            # resize the canvas frame (width fits depending on input, height is static)
            first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns))
            first5rows_height = 190

            self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                     height=first5rows_height)

            # set canvas scrolling region
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def clear_states(self):
        """
        clear_states - removes the all rows from the grid except for the first two default rows (4 labels and 1 entry)
        """

        # always keep the first two default rows
        if self.rows > 2:
            for i in range(self.rows - 2):
                self.remove_state()

    def calculate(self):
        """
        calculate - calculates the results for the selected method
        """

        # TODO: gather input data (seats, populations, number of states)
        # --------------------

        # pass data into desired method
        selected = self.clicked.get()
        method = None

        # TODO: add parameters
        if selected == 'Hamilton':
            method = Hamilton()
        elif selected == 'Jefferson':
            method = Jefferson()
        elif selected == 'Adam':
            method = Adam()
        elif selected == 'Webster':
            method = Webster()
        else:
            print('ERROR - calculate: method selection')


if __name__ == '__main__':
    App()
