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
        self.root.title('Ticer\'s Apportionment Calculator 0.4.5')

        # create lists to hold populations
        self.populations = []
        self.initial_quotas = []
        self.final_quotas = []
        self.initial_fair_shares = []
        self.final_fair_shares = []
        self.calculate_pressed = False

        frame_main = tk.Frame(self.root)
        frame_main.grid(sticky='news')

        # top label (title)
        Label(frame_main, text='Ticer\'s Apportionment Calculator 0.4.5').place(relx=.5, y=20,
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
        self.num_seats = StringVar()
        self.input_seats = Entry(frame_main, textvariable=self.num_seats, width=7).place(relx=.54, y=85, anchor=CENTER)

        # add, remove, clear, and calculate buttons
        self.button_add = Button(frame_main, text='+', width=5, command=self.add_state).place(relx=.35, y=120,
                                                                                              anchor=CENTER)
        self.button_remove = Button(frame_main, text='-', width=5, command=self.remove_state).place(relx=.45, y=120,
                                                                                                    anchor=CENTER)
        self.button_clear = Button(frame_main, text='CLEAR', width=5, command=self.clear_states).place(relx=.55, y=120,
                                                                                                       anchor=CENTER)
        self.button_calculate = Button(frame_main, text='=', width=5, command=self.calculate).place(relx=.65, y=120,
                                                                                                    anchor=CENTER)

        # create labels for original and modified divisor
        self.message_variable = StringVar()

        Label(frame_main, textvariable=self.message_variable, width=50).place(
            relx=.5, y=365, anchor=CENTER)

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

        # initialize a default number of rows and columns (cols is ALWAYS 6 and rows is dynamic, but starts as 2)
        self.rows = 2
        self.columns = 6

        # create a list to hold the widgets
        self.grid = []

        # add the first row of widgets (all labels)
        list_temp = [Label(self.frame_buttons, text='\nstate', width=9),
                     Label(self.frame_buttons, text='state\npopulation', width=9),
                     Label(self.frame_buttons, text='initial\nquotas', width=9),
                     Label(self.frame_buttons, text='final\nquotas', width=9),
                     Label(self.frame_buttons, text='initial\nfair share', width=9),
                     Label(self.frame_buttons, text='final\nfair share', width=9)]

        self.grid.append(list_temp)

        self.grid[0][0].grid(row=0, column=0, sticky='news')
        self.grid[0][1].grid(row=0, column=1, sticky='news')
        self.grid[0][2].grid(row=0, column=2, sticky='news')
        self.grid[0][3].grid(row=0, column=3, sticky='news')
        self.grid[0][4].grid(row=0, column=4, sticky='news')
        self.grid[0][5].grid(row=0, column=5, sticky='news')

        self.default_entry_value = StringVar()
        self.temp_1 = StringVar()
        self.temp_2 = StringVar()
        self.temp_3 = StringVar()
        self.temp_4 = StringVar()

        self.temp_1.set('-')
        self.temp_2.set('-')
        self.temp_3.set('-')
        self.temp_4.set('-')

        # add the second row of widgets (all labels and one entry)
        list_temp = [Label(self.frame_buttons, text='1', width=9),
                     Entry(self.frame_buttons, textvariable=self.default_entry_value, width=7),
                     Label(self.frame_buttons, text='-', textvariable=self.temp_1, width=7),
                     Label(self.frame_buttons, text='-', textvariable=self.temp_2, width=7),
                     Label(self.frame_buttons, text='-', textvariable=self.temp_3, width=7),
                     Label(self.frame_buttons, text='-', textvariable=self.temp_4, width=7)]

        self.grid.append(list_temp)
        self.populations.append(self.default_entry_value)

        self.initial_quotas.append(self.temp_1)
        self.final_quotas.append(self.temp_2)
        self.initial_fair_shares.append(self.temp_3)
        self.final_fair_shares.append(self.temp_4)

        self.grid[1][0].grid(row=1, column=0, sticky='news', padx=10)
        self.grid[1][1].grid(row=1, column=1, sticky='news', padx=10)
        self.grid[1][2].grid(row=1, column=2, sticky='news', padx=10)
        self.grid[1][3].grid(row=1, column=3, sticky='news', padx=10)
        self.grid[1][4].grid(row=1, column=4, sticky='news', padx=10)
        self.grid[1][5].grid(row=1, column=5, sticky='news', padx=10)

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

        # if the row displaying the totals is present, remove it
        if self.calculate_pressed:
            self.rows -= 1
            for i, widget in enumerate(self.grid[len(self.grid) - 1]):
                widget.grid_forget()

            self.message_variable.set('')
            self.grid.pop(len(self.grid) - 1)
            self.calculate_pressed = False

        # increment rows
        self.rows += 1

        # remove calculation values
        for i in range(len(self.populations)):
            self.initial_quotas[i].set('-')
            self.final_quotas[i].set('-')
            self.initial_fair_shares[i].set('-')
            self.final_fair_shares[i].set('-')

        value = StringVar()
        temp_1 = StringVar()
        temp_2 = StringVar()
        temp_3 = StringVar()
        temp_4 = StringVar()

        temp_1.set('-')
        temp_2.set('-')
        temp_3.set('-')
        temp_4.set('-')

        # add a new row of widgets to the grid
        list_temp = [Label(self.frame_buttons, text=self.rows - 1, width=9),
                     Entry(self.frame_buttons, textvariable=value, width=7),
                     Label(self.frame_buttons, textvariable=temp_1, width=7),
                     Label(self.frame_buttons, textvariable=temp_2, width=7),
                     Label(self.frame_buttons, textvariable=temp_3, width=7),
                     Label(self.frame_buttons, textvariable=temp_4, width=7)]

        self.initial_quotas.append(temp_1)
        self.final_quotas.append(temp_2)
        self.initial_fair_shares.append(temp_3)
        self.final_fair_shares.append(temp_4)

        self.grid.append(list_temp)
        self.populations.append(value)

        self.grid[self.rows - 1][0].grid(row=self.rows - 1, column=0, sticky='news', padx=10)
        self.grid[self.rows - 1][1].grid(row=self.rows - 1, column=1, sticky='news', padx=10)
        self.grid[self.rows - 1][2].grid(row=self.rows - 1, column=2, sticky='news', padx=10)
        self.grid[self.rows - 1][3].grid(row=self.rows - 1, column=3, sticky='news', padx=10)
        self.grid[self.rows - 1][4].grid(row=self.rows - 1, column=4, sticky='news', padx=10)
        self.grid[self.rows - 1][5].grid(row=self.rows - 1, column=5, sticky='news', padx=10)

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

        # if the row displaying the totals is present, remove it
        if self.calculate_pressed:
            self.rows -= 1
            for i, widget in enumerate(self.grid[len(self.grid) - 1]):
                widget.grid_forget()
            self.message_variable.set('')
            self.grid.pop(len(self.grid) - 1)
            self.calculate_pressed = False

        # always keep the first two default rows
        if self.rows > 2:
            # decrement rows
            self.rows -= 1

            # remove the widget from the grid
            for i, widget in enumerate(self.grid[len(self.grid) - 1]):
                widget.grid_forget()

            # remove calculation values
            for i in range(len(self.populations) - 1):
                self.initial_quotas[i].set('-')
                self.final_quotas[i].set('-')
                self.initial_fair_shares[i].set('-')
                self.final_fair_shares[i].set('-')

            self.grid.pop(len(self.grid) - 1)
            self.initial_quotas.pop(len(self.initial_fair_shares) - 1)
            self.final_quotas.pop(len(self.final_quotas) - 1)
            self.initial_fair_shares.pop(len(self.initial_fair_shares) - 1)
            self.final_fair_shares.pop(len(self.final_fair_shares) - 1)

            self.populations.pop(len(self.populations) - 1)

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

        # if the row displaying the totals is present, remove it
        if self.calculate_pressed:
            self.rows -= 1
            for i, widget in enumerate(self.grid[len(self.grid) - 1]):
                widget.grid_forget()
            self.grid.pop(len(self.grid) - 1)
            self.message_variable.set('')
            self.calculate_pressed = False

        # always keep the first two default rows
        if self.rows > 2:
            for i in range(self.rows - 2):
                self.remove_state()

            # clear default label entry
            self.initial_quotas[0].set('-')
            self.final_quotas[0].set('-')
            self.initial_fair_shares[0].set('-')
            self.final_fair_shares[0].set('-')
            self.populations[0].set('')

    def calculate(self):
        """
        calculate - calculates the results for the selected method
        """

        # if the row displaying the totals is present, remove it
        if self.calculate_pressed:
            self.rows -= 1
            for i, widget in enumerate(self.grid[len(self.grid) - 1]):
                widget.grid_forget()
            self.grid.pop(len(self.grid) - 1)
            self.calculate_pressed = False

        # gather input data (num_seats, list of populations, num_states)
        if self.num_seats.get() == '':
            self.message_variable.set('A number for the amount of seats is required.')
        else:
            valid_input = True
            if self.num_seats.get() == '':
                valid_input = False
            if not valid_input:
                self.message_variable.set("Invalid input type for amount of seats. Make sure there are\n"
                                          "not any letters in the textbox for the amount of seats.")
            else:
                num_seats = float(self.num_seats.get())
                populations = []
                for i, x in enumerate(self.populations):
                    if x.get() == '':
                        valid_input = False
                        break
                    populations.append(float(x.get()))

                if not valid_input:
                    self.message_variable.set("At least one population textfield is empty. Remove it\n"
                                              "or enter a value.")
                else:
                    num_states = self.rows - 1

                    # pass data into desired method
                    selected = self.clicked.get()
                    method = None

                    if selected == 'Hamilton':
                        method = Hamilton(num_seats, num_states, populations)
                    elif selected == 'Jefferson':
                        method = Jefferson(num_seats, num_states, populations)
                    elif selected == 'Adam':
                        method = Adam(num_seats, num_states, populations)
                    elif selected == 'Webster':
                        method = Webster(num_seats, num_states, populations)
                    else:
                        self.message_variable.set('drop-down menu error!')

                    # gather filtered results
                    original_divisor, modified_divisor, initial_quotas, final_quotas, initial_fair_shares, \
                    final_fair_shares, total_initial_fair_shares = method.calculate()

                    if original_divisor is None:
                        self.message_variable.set(f'Warning: results could not be calculated. This can sometimes\n'
                                                  f'happen using {selected}\'s method with very specific number\n'
                                                  f'combinations and is rare. Make sure the correct values are entered.')

                        # remove calculation values
                        for i in range(len(self.populations)):
                            self.initial_quotas[i].set('-')
                            self.final_quotas[i].set('-')
                            self.initial_fair_shares[i].set('-')
                            self.final_fair_shares[i].set('-')
                    else:
                        # update values in grid
                        for i, initial_quota in enumerate(initial_quotas):
                            self.initial_quotas[i].set(round(initial_quota, 4))
                        for i, final_quota in enumerate(final_quotas):
                            self.final_quotas[i].set(round(final_quota, 4))
                        for i, initial_fair_share in enumerate(initial_fair_shares):
                            self.initial_fair_shares[i].set(round(initial_fair_share, 4))
                        for i, final_fair_share in enumerate(final_fair_shares):
                            self.final_fair_shares[i].set(round(final_fair_share, 4))

                        # create a new row for total values
                        self.rows += 1

                        # add a new row of widgets to the grid
                        list_temp = [Label(self.frame_buttons, text='total', width=9),
                                     Label(self.frame_buttons, text=sum(populations), width=7),
                                     Label(self.frame_buttons, text=f'~{round(sum(initial_quotas), 4)}', width=7),
                                     Label(self.frame_buttons, text=f'~{round(sum(final_quotas), 4)}', width=7),
                                     Label(self.frame_buttons, text=sum(initial_fair_shares), width=7),
                                     Label(self.frame_buttons, text=sum(final_fair_shares), width=7)]

                        self.grid.append(list_temp)

                        self.message_variable.set(
                            f'original divisor: {round(original_divisor, 4)}\tmodified divisor: {round(modified_divisor, 4)}')

                        self.grid[self.rows - 1][0].grid(row=self.rows - 1, column=0, sticky='news', padx=10)
                        self.grid[self.rows - 1][1].grid(row=self.rows - 1, column=1, sticky='news', padx=10)
                        self.grid[self.rows - 1][2].grid(row=self.rows - 1, column=2, sticky='news', padx=10)
                        self.grid[self.rows - 1][3].grid(row=self.rows - 1, column=3, sticky='news', padx=10)
                        self.grid[self.rows - 1][4].grid(row=self.rows - 1, column=4, sticky='news', padx=10)
                        self.grid[self.rows - 1][5].grid(row=self.rows - 1, column=5, sticky='news', padx=10)

                        # update widget frames idle tasks to calculate widget sizes
                        self.frame_buttons.update_idletasks()

                        # resize the canvas frame (width fits depending on input, height is static)
                        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns))
                        first5rows_height = 190

                        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                                 height=first5rows_height)

                        # set canvas scrolling region
                        self.canvas.config(scrollregion=self.canvas.bbox("all"))

                        # set calculate pressed to true
                        self.calculate_pressed = True


if __name__ == '__main__':
    App()
