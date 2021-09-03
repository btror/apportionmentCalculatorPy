import tkinter as tk
import tkinter.font as font
import csv
import pandas as pd
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
        self.root.geometry('685x430')
        self.root.resizable(False, False)
        self.root.title('Ticer\'s Apportionment Calculator')

        # colors
        self.frame_background = 'gray23'
        self.widget_foreground = 'ghost white'

        # fonts
        self.font = font.Font(family='Helvetica', size=12, weight='bold')
        self.tiny_font = font.Font(family='Helvetica', size=10, weight='bold')
        self.seats_font = font.Font(family='Helvetica', size=15, weight='bold')

        # create lists to hold populations
        self.populations = []
        self.initial_quotas = []
        self.final_quotas = []
        self.initial_fair_shares = []
        self.final_fair_shares = []
        self.calculate_pressed = False
        self.original_divisor = None
        self.modified_divisor = None

        frame_main = tk.Frame(self.root)
        frame_main.grid(sticky='news')
        frame_main.configure(bg=self.frame_background)

        # top label (title)
        Label(frame_main, text='Desktop 0.8.2', bg=self.frame_background, fg=self.widget_foreground).place(x=55, y=20,
                                                                                                           anchor=CENTER)

        # select apportionment method

        self.clicked = StringVar()
        self.clicked.set('Hamilton')
        self.button_hamilton = Button(frame_main, text='Hamilton', width=8, height=1, bg=self.frame_background,
                                      fg=self.widget_foreground, relief='groove',
                                      borderwidth=2, font=self.font,
                                      command=self.change_method_hamilton)
        self.button_hamilton.place(x=365,
                                   y=70,
                                   anchor=CENTER)

        self.button_jefferson = Button(frame_main, text='Jefferson', width=8, height=1, bg=self.frame_background,
                                       fg=self.widget_foreground, relief='groove',
                                       borderwidth=2, font=self.font,
                                       command=self.change_method_jefferson)
        self.button_jefferson.place(x=456,
                                    y=70,
                                    anchor=CENTER)

        self.button_adam = Button(frame_main, text='Adam', width=5, height=1, bg=self.frame_background,
                                  fg=self.widget_foreground, relief='groove',
                                  borderwidth=2, font=self.font,
                                  command=self.change_method_adam)
        self.button_adam.place(x=532,
                               y=70,
                               anchor=CENTER)

        self.button_webster = Button(frame_main, text='Webster', width=7, height=1, bg=self.frame_background,
                                     fg=self.widget_foreground, relief='groove',
                                     borderwidth=2, font=self.font,
                                     command=self.change_method_webster)
        self.button_webster.place(x=603,
                                  y=70,
                                  anchor=CENTER)

        self.change_method_hamilton()

        # entry for amount of seats
        Label(frame_main, text='seats: ', bg=self.frame_background, fg=self.widget_foreground,
              font=self.font).place(
            x=45, y=69,
            anchor=CENTER)
        self.num_seats = StringVar()
        self.input_seats = Entry(frame_main, textvariable=self.num_seats, width=6, bg=self.frame_background,
                                 fg=self.widget_foreground, relief='solid', highlightthickness=1,
                                 highlightbackground=self.widget_foreground, font=self.seats_font).place(x=108, y=70,
                                                                                                         anchor=CENTER)

        # add, remove, clear, and calculate buttons
        self.button_remove = Button(frame_main, text='-', width=3, height=1, bg=self.frame_background,
                                    fg=self.widget_foreground, relief='groove',
                                    borderwidth=2, font=self.font,
                                    command=self.remove_state).place(x=190,
                                                                     y=70,
                                                                     anchor=CENTER)

        self.button_add = Button(frame_main, text='+', width=3, height=1, bg=self.frame_background,
                                 fg=self.widget_foreground, relief='groove',
                                 borderwidth=2, font=self.font, command=self.add_state).place(x=231, y=70,
                                                                                              anchor=CENTER)

        self.button_calculate = Button(frame_main, text='=', width=3, height=1, bg=self.frame_background,
                                       fg=self.widget_foreground,
                                       relief='groove', borderwidth=2, font=self.font, command=self.calculate).place(
            x=272,
            y=70,
            anchor=CENTER)

        self.button_clear = Button(frame_main, text='CLEAR', width=7, height=1, bg=self.frame_background,
                                   fg=self.widget_foreground,
                                   relief='groove', borderwidth=2, font=self.font, command=self.clear_states).place(
            x=210, y=105,
            anchor=CENTER)

        # create labels for original and modified divisor
        self.message_variable = StringVar()

        Label(frame_main, textvariable=self.message_variable, bg=self.frame_background,
              fg=self.widget_foreground, font=self.tiny_font).place(
            x=15, y=377, anchor='w')

        # create a frame for the canvas
        self.frame_canvas = tk.Frame(frame_main)
        self.frame_canvas.place(x=341, y=240, anchor=CENTER)
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)

        # allows widget resizing later
        self.frame_canvas.grid_propagate(False)

        # add a canvas to the frame
        self.canvas = tk.Canvas(self.frame_canvas, bg=self.frame_background,
                                relief='flat')  # ---------------------------------------
        self.canvas.grid(row=0, column=0, sticky="news")

        # add a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # create a frame to contain the widgets
        self.frame_buttons = tk.Frame(self.canvas, bg=self.frame_background)
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')

        # initialize a default number of rows and columns (cols is ALWAYS 6 and rows is dynamic, but starts as 2)
        self.rows = 2
        self.columns = 6

        # create a list to hold the widgets
        self.grid = []

        # add the first row of widgets (all labels)
        list_temp = [Label(self.frame_buttons, text='\nstate', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_buttons, text='state\npopulation', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_buttons, text='initial\nquotas', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_buttons, text='final\nquotas', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_buttons, text='initial\nfair share', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_buttons, text='final\nfair share', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10)]

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
        list_temp = [Label(self.frame_buttons, text='1', width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Entry(self.frame_buttons, textvariable=self.default_entry_value, width=10,
                           bg=self.frame_background,
                           fg=self.widget_foreground, relief='solid', highlightthickness=1,
                           highlightbackground=self.widget_foreground),
                     Label(self.frame_buttons, text='-', textvariable=self.temp_1, width=10, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat'),
                     Label(self.frame_buttons, text='-', textvariable=self.temp_2, width=10, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat'),
                     Label(self.frame_buttons, text='-', textvariable=self.temp_3, width=10, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat'),
                     Label(self.frame_buttons, text='-', textvariable=self.temp_4, width=10, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat')]

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
        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns)) + 4
        first5rows_height = 190

        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                 height=first5rows_height)

        # set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # create menu bar
        menu_bar = Menu(self.root)

        file = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file)
        file.add_command(label='New', command=None)
        file.add_command(label='Open...', command=None)
        file.add_command(label='Save', command=self.save_data)
        file.add_command(label='Save as', command=self.save_data)
        file.add_separator()
        file.add_command(label='Exit', command=self.root.destroy)

        view = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='View', menu=view)
        view.add_command(label='Theme', command=None)

        help_ = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Guide', command=None)
        help_.add_command(label='Demo', command=None)
        help_.add_separator()
        help_.add_command(label='About', command=None)

        self.root.config(menu=menu_bar)

        # launch
        self.root.mainloop()

    def save_data(self):
        file = open('data/data.csv', 'w', newline='')

        with file:
            headers = ['method', 'seats', 'original_divisor', 'modified_divisor', 'state_number', 'population',
                       'initial_quota', 'final_quota', 'initial_fair_share',
                       'final_fair_share']
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            method = self.clicked.get()
            seats = self.num_seats.get()

            if seats == '':
                seats = '-'

            original_divisor = self.original_divisor
            modified_divisor = self.modified_divisor

            if self.original_divisor is None:
                original_divisor = '-'

            if self.modified_divisor is None:
                modified_divisor = '-'

            list_state_numbers = []
            for i in range(len(self.populations)):
                list_state_numbers.append(i + 1)

            list_populations = []
            for i in range(len(self.populations)):
                list_populations.append(self.populations[i].get())

            list_initial_quotas = []
            for i in range(len(self.initial_quotas)):
                list_initial_quotas.append(self.initial_quotas[i].get())

            list_final_quotas = []
            for i in range(len(self.final_quotas)):
                list_final_quotas.append(self.final_quotas[i].get())

            list_initial_fair_shares = []
            for i in range(len(self.initial_fair_shares)):
                list_initial_fair_shares.append(self.initial_fair_shares[i].get())

            list_final_fair_shares = []
            for i in range(len(self.final_fair_shares)):
                list_final_fair_shares.append(self.final_fair_shares[i].get())

            for i in range(len(list_state_numbers)):
                writer.writerow({headers[0]: method,
                                 headers[1]: seats,
                                 headers[2]: original_divisor,
                                 headers[3]: modified_divisor,
                                 headers[4]: list_state_numbers[i],
                                 headers[5]: list_populations[i],
                                 headers[6]: list_initial_quotas[i],
                                 headers[7]: list_final_quotas[i],
                                 headers[8]: list_initial_fair_shares[i],
                                 headers[9]: list_final_fair_shares[i]})

        # data = pd.read_csv(r'data/data.csv')
        # data.to_excel(r'data/data.xlsx', index=None, header=True)

    def change_method_hamilton(self):
        self.clicked.set('Hamilton')
        self.button_hamilton.config(background=self.widget_foreground, foreground=self.frame_background)

        self.button_jefferson.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_adam.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_webster.config(background=self.frame_background, foreground=self.widget_foreground)

    def change_method_jefferson(self):
        self.clicked.set('Jefferson')
        self.button_jefferson.config(background=self.widget_foreground, foreground=self.frame_background)

        self.button_hamilton.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_adam.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_webster.config(background=self.frame_background, foreground=self.widget_foreground)

    def change_method_adam(self):
        self.clicked.set('Adam')
        self.button_adam.config(background=self.widget_foreground, foreground=self.frame_background)

        self.button_jefferson.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_hamilton.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_webster.config(background=self.frame_background, foreground=self.widget_foreground)

    def change_method_webster(self):
        self.clicked.set('Webster')
        self.button_webster.config(background=self.widget_foreground, foreground=self.frame_background)

        self.button_jefferson.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_adam.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_hamilton.config(background=self.frame_background, foreground=self.widget_foreground)

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
        list_temp = [Label(self.frame_buttons, text=self.rows - 1, width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Entry(self.frame_buttons, textvariable=value, width=10, bg=self.frame_background,
                           fg=self.widget_foreground, relief='solid', highlightthickness=1,
                           highlightbackground=self.widget_foreground),
                     Label(self.frame_buttons, textvariable=temp_1, width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Label(self.frame_buttons, textvariable=temp_2, width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Label(self.frame_buttons, textvariable=temp_3, width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Label(self.frame_buttons, textvariable=temp_4, width=10, bg=self.frame_background,
                           fg=self.widget_foreground)]

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
        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns)) + 4
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
            first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns)) + 4
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
        if self.rows > 1:
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
                self.message_variable.set(
                    "Invalid input type for amount of seats. Make sure there are not any letters in the textbox for the\n"
                    "amount of seats. not any letters in the textbox for the amount of seats.")
            else:
                num_seats = 0
                try:
                    num_seats = float(self.num_seats.get())
                except ValueError as e:
                    valid_input = False

                if not valid_input:
                    self.message_variable.set(
                        'Invalid character type detected in seats textbox. Make sure the seats field doesn\'t contain letters.')
                else:
                    populations = []
                    for i, x in enumerate(self.populations):
                        if x.get() == '':
                            valid_input = False
                            break
                        try:
                            populations.append(float(x.get()))
                        except ValueError as e:
                            valid_input = False
                            break

                    if not valid_input:
                        self.message_variable.set(
                            "At least one population textfield is empty or contains invalid characters. Remove the state or enter\n"
                            "a valid population value.")
                    else:
                        num_states = self.rows - 1

                        # pass data into desired method
                        selected = self.clicked.get()
                        method = None

                        if num_seats < 1:
                            self.message_variable.set("Number of seats must be greater than 0.")
                            valid_input = False

                        if valid_input:
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
                                self.message_variable.set(
                                    f'Warning: results could not be calculated. This can sometimes happen using {selected}\'s method\n'
                                    f'with very specific number combinations and is rare. Make sure the correct values are entered.\n')

                                # remove calculation values
                                for i in range(len(self.populations)):
                                    self.initial_quotas[i].set('-')
                                    self.final_quotas[i].set('-')
                                    self.initial_fair_shares[i].set('-')
                                    self.final_fair_shares[i].set('-')
                            else:
                                self.original_divisor = original_divisor
                                self.modified_divisor = modified_divisor

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
                                list_temp = [Label(self.frame_buttons, text='total', width=10, bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_buttons, text=sum(populations), width=10,
                                                   bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_buttons, text=f'~{round(sum(initial_quotas), 4)}',
                                                   width=10, bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_buttons, text=f'~{round(sum(final_quotas), 4)}', width=10,
                                                   bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_buttons, text=sum(initial_fair_shares), width=10,
                                                   bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_buttons, text=sum(final_fair_shares), width=10,
                                                   bg=self.frame_background,
                                                   fg=self.widget_foreground)]

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
                                first5columns_width = sum(
                                    self.grid[0][j].winfo_width() for j in range(0, self.columns)) + 4
                                first5rows_height = 190

                                self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                                         height=first5rows_height)

                                # set canvas scrolling region
                                self.canvas.config(scrollregion=self.canvas.bbox("all"))

                                # set calculate pressed to true
                                self.calculate_pressed = True


if __name__ == '__main__':
    App()
