import tkinter as tk
import tkinter.font as font
from tkinter import ttk
import csv
import xlsxwriter
import webbrowser
from tkinter import *
from tkinter.filedialog import asksaveasfile
from main.main_plots import Plot
from main.methods.hamilton import Hamilton
from main.methods.jefferson import Jefferson
from main.methods.adam import Adam
from main.methods.webster import Webster


class App:
    def __init__(self):
        """
        init - initialize variables
        """

        # tkinter gui
        self.root = tk.Tk()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry('685x430')
        self.root.resizable(False, False)
        self.root.title('TICERAPPS Apportionment Calculator')

        # set gui icon
        icon = PhotoImage(file='../res/apportionmentimage.png')
        self.root.iconphoto(False, icon)

        self.frame_background = None
        self.widget_foreground = None

        # default colors
        with open('../data/settings.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            rows = []
            for row in csv_reader:
                rows.append(row)

            for row in rows:
                i = 0
                for col in row:
                    if i == 0:
                        self.selected_theme = col
                    elif i == 1:
                        self.widget_foreground = col
                    elif i == 2:
                        self.frame_background = col
                    i += 1

        # track chart and graph settings
        self.show_chart = IntVar()
        self.show_graph = IntVar()

        # default fonts
        self.font = font.Font(family='Helvetica', size=12, weight='bold')
        self.tiny_font = font.Font(family='Helvetica', size=10, weight='bold')
        self.seats_font = font.Font(family='Helvetica', size=15, weight='bold')

        # lists to keep track of table (values)
        self.original_quota_values = []
        self.original_fair_share_values = []
        self.final_quota_values = []
        self.final_fair_share_values = []
        self.divisor_estimations_history = []
        self.method = None

        # lists to keep track of table (objects)
        self.populations = []
        self.initial_quotas = []
        self.final_quotas = []
        self.initial_fair_shares = []
        self.final_fair_shares = []

        # track if calculate button is pressed
        self.calculate_pressed = False

        # initialize original/modified divisors and lower/upper boundaries (boundaries are referring to lowest and
        # highest estimated divisors possible)
        self.original_divisor = None
        self.modified_divisor = None
        self.lower_boundary = None
        self.upper_boundary = None

        # create a frame to put objects in
        frame_main = tk.Frame(self.root)
        frame_main.grid(sticky='news')
        frame_main.configure(bg=self.frame_background)

        # desktop version label
        Label(frame_main, text='Desktop 1.1.0', bg=self.frame_background, fg=self.widget_foreground).place(x=55, y=20,
                                                                                                           anchor=CENTER)

        # track selected method (default is hamilton)
        self.clicked = StringVar()
        self.clicked.set('Hamilton')
        self.last_calculation = StringVar()
        self.last_calculation.set('Hamilton')

        # initialize buttons for choosing methods
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

        # initialize entry widget for getting the number of seats
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

        # create a message variable for results output
        self.message_variable = StringVar()

        # create a label to display message variable
        Label(frame_main, textvariable=self.message_variable, bg=self.frame_background,
              fg=self.widget_foreground, font=self.tiny_font, width=40).place(
            relx=.5, y=380, anchor=CENTER)

        # create a slider for changing the divisor (only applies to jefferson, adam, and webster)
        self.slider_value = StringVar()
        style = ttk.Style()
        style.configure('scale.Horizontal.TScale', background=self.frame_background)
        self.slider = ttk.Scale(frame_main, from_=0, to=10, orient=HORIZONTAL, style='scale.Horizontal.TScale',
                                command=self.slider_changed)
        self.slider.place(y=368, x=20)

        # disable the slider by default
        self.slider['state'] = DISABLED

        # configure slider settings
        self.slider_label_title = Label(frame_main, bg=self.frame_background, fg=self.widget_foreground,
                                        font=self.tiny_font, text='')
        self.slider_label_title.place(x=18, y=345)
        self.slider.configure(state='disabled')

        # create a label letting the user know what the slider is for (modifying the modified divisor when applicable)
        self.slider_label = Label(frame_main, bg=self.frame_background, fg=self.widget_foreground,
                                  font=self.tiny_font)
        self.slider_label.place(x=18, y=395)

        # create a label displaying the changed modified divisor based on slider usage
        self.original_divisor_label = Label(frame_main, bg=self.frame_background, fg=self.widget_foreground,
                                            font=self.tiny_font)
        self.original_divisor_label.place(x=130, y=370)

        # create a frame for the canvas
        self.frame_canvas = tk.Frame(frame_main)
        self.frame_canvas.place(x=341, y=240, anchor=CENTER)
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)

        # allows widget resizing later
        self.frame_canvas.grid_propagate(False)

        # add a canvas to the frame
        self.canvas = tk.Canvas(self.frame_canvas, bg=self.frame_background,
                                relief='flat')
        self.canvas.grid(row=0, column=0, sticky="news")

        # add a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # create a frame to contain the widgets
        self.frame_widgets = tk.Frame(self.canvas, bg=self.frame_background)
        self.canvas.create_window((0, 0), window=self.frame_widgets, anchor='nw')

        # initialize a default number of rows and columns (cols is ALWAYS 6 and rows is dynamic, but starts as 2)
        self.rows = 2
        self.columns = 6

        # create a list to hold the widgets
        self.grid = []

        # add the first row of widgets (all labels)
        list_temp = [Label(self.frame_widgets, text='\nstate', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_widgets, text='state\npopulation', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_widgets, text='initial\nquotas', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_widgets, text='final\nquotas', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_widgets, text='initial\nfair share', width=14, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat', pady=10),
                     Label(self.frame_widgets, text='final\nfair share', width=14, bg=self.frame_background,
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
        list_temp = [Label(self.frame_widgets, text='1', width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Entry(self.frame_widgets, textvariable=self.default_entry_value, width=10,
                           bg=self.frame_background,
                           fg=self.widget_foreground, relief='solid', highlightthickness=1,
                           highlightbackground=self.widget_foreground),
                     Label(self.frame_widgets, text='-', textvariable=self.temp_1, width=10, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat'),
                     Label(self.frame_widgets, text='-', textvariable=self.temp_2, width=10, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat'),
                     Label(self.frame_widgets, text='-', textvariable=self.temp_3, width=10, bg=self.frame_background,
                           fg=self.widget_foreground,
                           relief='flat'),
                     Label(self.frame_widgets, text='-', textvariable=self.temp_4, width=10, bg=self.frame_background,
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
        self.frame_widgets.update_idletasks()

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
        # file.add_command(label='Import', command=None)
        submenu_1 = Menu(file, tearoff=0)
        submenu_1.add_command(label='.csv file', command=self.save_csv)
        submenu_1.add_command(label='.xlsx file', command=self.save_xlsx)
        file.add_cascade(label='Export', menu=submenu_1)

        file.add_separator()
        file.add_command(label='Exit', command=self.root.destroy)

        view = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='View', menu=view)

        # submenu for charts
        submenu_2 = Menu(view, tearoff=0)
        submenu_2.add_checkbutton(label='Show fair share chart', variable=self.show_chart)
        submenu_2.add_checkbutton(label='Show estimated divisor graph', variable=self.show_graph)
        view.add_cascade(label='Chart settings', menu=submenu_2)

        # submenu for themes
        submenu_3 = Menu(view, tearoff=0)
        submenu_3.add_command(label='Light theme', command=self.change_theme_light)
        submenu_3.add_command(label='Dark theme', command=self.change_theme_dark)
        submenu_3.add_separator()
        submenu_3.add_command(label='Clt green', command=self.change_theme_clt_green)
        submenu_3.add_command(label='Tarheel blue', command=self.change_theme_tarheel_blue)
        submenu_3.add_command(label='Wolfpack red', command=self.change_theme_wolfpack_red)
        view.add_cascade(label="Themes", menu=submenu_3)

        help_ = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Guide', command=self.show_guide)
        # help_.add_command(label='Demo', command=None)
        help_.add_separator()
        help_.add_command(label='About', command=self.show_about)

        self.root.config(menu=menu_bar)

        self.load_saved_table_data()

        # launch
        self.root.mainloop()

    def save_recent_data(self):
        """
        save_recent_data - saves recent table entries
        """

        # clear data
        data = open('../data/recent_table_data.csv', 'r+')
        data.truncate(0)
        data.close()

        # write new data
        with open('../data/recent_table_data.csv', 'w', newline='') as file:
            headers = ['method', 'seats', 'original_divisor', 'modified_divisor', 'lowest_possible_estimated_divisor',
                       'highest_possible_estimated_divisor', 'state_number', 'population',
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
                if i == 0:
                    writer.writerow({headers[0]: method,
                                     headers[1]: seats,
                                     headers[2]: original_divisor,
                                     headers[3]: modified_divisor,
                                     headers[4]: self.lower_boundary,
                                     headers[5]: self.upper_boundary,
                                     headers[6]: list_state_numbers[i],
                                     headers[7]: list_populations[i],
                                     headers[8]: list_initial_quotas[i],
                                     headers[9]: list_final_quotas[i],
                                     headers[10]: list_initial_fair_shares[i],
                                     headers[11]: list_final_fair_shares[i]})
                else:
                    writer.writerow({headers[0]: '',
                                     headers[1]: '',
                                     headers[2]: '',
                                     headers[3]: '',
                                     headers[4]: '',
                                     headers[5]: '',
                                     headers[6]: list_state_numbers[i],
                                     headers[7]: list_populations[i],
                                     headers[8]: list_initial_quotas[i],
                                     headers[9]: list_final_quotas[i],
                                     headers[10]: list_initial_fair_shares[i],
                                     headers[11]: list_final_fair_shares[i]})

    def load_saved_table_data(self):
        # TODO: when the software starts, load recent data into the table
        with open('../data/recent_table_data.csv', newline='') as file:
            reader = csv.reader(file, delimiter=',')

            line_count = 0
            for row in reader:
                if line_count == 1:
                    self.method = row[0]
                    self.num_seats.set(row[1])
                    self.original_divisor = float(row[2])
                    self.modified_divisor = float(row[3])
                    self.lower_boundary = float(row[4])
                    self.upper_boundary = float(row[5])
                    self.populations[line_count - 1].set(float(row[7]))
                if line_count > 1:
                    x = 1
                    self.add_state()
                    self.populations[line_count - 1].set(float(row[7]))
                line_count += 1
            if self.method == 'Hamilton':
                self.change_method_hamilton()
            elif self.method == 'Jefferson':
                self.change_method_jefferson()
            elif self.method == 'Adam':
                self.change_method_adam()
            elif self.method == 'Webster':
                self.change_method_webster()

    def save_csv(self):
        """
        save_csv - save csv data of what is in the table. Creates a CSV file and saves it to system.
        """

        # only allow users to save csv file type
        new_file = asksaveasfile(defaultextension='*.*', filetypes=[('csv file', '.csv')])

        # create headers and append data
        with new_file:
            headers = ['method', 'seats', 'original_divisor', 'modified_divisor', 'lowest_possible_estimated_divisor',
                       'highest_possible_estimated_divisor', 'state_number', 'population',
                       'initial_quota', 'final_quota', 'initial_fair_share',
                       'final_fair_share']
            writer = csv.DictWriter(new_file, fieldnames=headers)
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
                if i == 0:
                    writer.writerow({headers[0]: method,
                                     headers[1]: seats,
                                     headers[2]: original_divisor,
                                     headers[3]: modified_divisor,
                                     headers[4]: self.lower_boundary,
                                     headers[5]: self.upper_boundary,
                                     headers[6]: list_state_numbers[i],
                                     headers[7]: list_populations[i],
                                     headers[8]: list_initial_quotas[i],
                                     headers[9]: list_final_quotas[i],
                                     headers[10]: list_initial_fair_shares[i],
                                     headers[11]: list_final_fair_shares[i]})
                else:
                    writer.writerow({headers[0]: '',
                                     headers[1]: '',
                                     headers[2]: '',
                                     headers[3]: '',
                                     headers[4]: '',
                                     headers[5]: '',
                                     headers[6]: list_state_numbers[i],
                                     headers[7]: list_populations[i],
                                     headers[8]: list_initial_quotas[i],
                                     headers[9]: list_final_quotas[i],
                                     headers[10]: list_initial_fair_shares[i],
                                     headers[11]: list_final_fair_shares[i]})

    def save_xlsx(self):
        """
        save_xlsx - save xlsx data of what is in the table. Creates a xlsx file and saves it to system.
        """

        # only allow users to save csv file type
        new_file = asksaveasfile(defaultextension='*.*', filetypes=[('xlsx file', '.xlsx')])

        workbook = xlsxwriter.Workbook(new_file.name)
        worksheet = workbook.add_worksheet("Data Sheet")

        # create headers
        headers = ['method', 'seats', 'original_divisor', 'modified_divisor', 'lowest_possible_estimated_divisor',
                   'highest_possible_estimated_divisor', 'state_number', 'population',
                   'initial_quota', 'final_quota', 'initial_fair_share',
                   'final_fair_share']

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

        list_method = [headers[0]]
        for i in range(len(self.populations)):
            if i == 0:
                list_method.append(method)
            else:
                list_method.append('')

        list_seats = [headers[1]]
        for i in range(len(self.populations)):
            if i == 0:
                list_seats.append(seats)
            else:
                list_seats.append('')

        list_original_divisor = [headers[2]]
        for i in range(len(self.populations)):
            if i == 0:
                list_original_divisor.append(original_divisor)
            else:
                list_original_divisor.append('')

        list_modified_divisor = [headers[3]]
        for i in range(len(self.populations)):
            if i == 0:
                list_modified_divisor.append(modified_divisor)
            else:
                list_modified_divisor.append('')

        list_lowest_boundary = [headers[4]]
        for i in range(len(self.populations)):
            if i == 0:
                list_lowest_boundary.append(self.lower_boundary)
            else:
                list_lowest_boundary.append('')

        list_upper_boundary = [headers[5]]
        for i in range(len(self.populations)):
            if i == 0:
                list_upper_boundary.append(self.upper_boundary)
            else:
                list_upper_boundary.append('')

        list_state_numbers = [headers[6]]
        for i in range(len(self.populations)):
            list_state_numbers.append(i + 1)

        list_populations = [headers[7]]
        for i in range(len(self.populations)):
            list_populations.append(self.populations[i].get())

        list_initial_quotas = [headers[8]]
        for i in range(len(self.initial_quotas)):
            list_initial_quotas.append(self.initial_quotas[i].get())

        list_final_quotas = [headers[9]]
        for i in range(len(self.final_quotas)):
            list_final_quotas.append(self.final_quotas[i].get())

        list_initial_fair_shares = [headers[10]]
        for i in range(len(self.initial_fair_shares)):
            list_initial_fair_shares.append(self.initial_fair_shares[i].get())

        list_final_fair_shares = [headers[11]]
        for i in range(len(self.final_fair_shares)):
            list_final_fair_shares.append(self.final_fair_shares[i].get())

        data = (
            list_method,
            list_seats,
            list_original_divisor,
            list_modified_divisor,
            list_lowest_boundary,
            list_upper_boundary,
            list_state_numbers,
            list_populations,
            list_initial_quotas,
            list_final_quotas,
            list_initial_fair_shares,
            list_final_fair_shares
        )

        for i, d in enumerate(data):
            for j in range(len(d)):
                worksheet.write(j, i, d[j])

        workbook.close()

    def change_method_hamilton(self):
        """
        change_method_hamilton - updates method tracker variable, updates method button colors
        """

        self.method = 'Hamilton'
        self.clicked.set('Hamilton')
        self.button_hamilton.config(background=self.widget_foreground, foreground=self.frame_background)

        self.button_jefferson.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_adam.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_webster.config(background=self.frame_background, foreground=self.widget_foreground)

    def change_method_jefferson(self):
        """
        change_method_hamilton - updates method tracker variable, updates method button colors
        """

        self.method = 'Jefferson'
        self.clicked.set('Jefferson')
        self.button_jefferson.config(background=self.widget_foreground, foreground=self.frame_background)

        self.button_hamilton.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_adam.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_webster.config(background=self.frame_background, foreground=self.widget_foreground)

    def change_method_adam(self):
        """
        change_method_hamilton - updates method tracker variable, updates method button colors
        """

        self.method = 'Adam'
        self.clicked.set('Adam')
        self.button_adam.config(background=self.widget_foreground, foreground=self.frame_background)

        self.button_jefferson.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_hamilton.config(background=self.frame_background, foreground=self.widget_foreground)
        self.button_webster.config(background=self.frame_background, foreground=self.widget_foreground)

    def change_method_webster(self):
        """
        change_method_hamilton - updates method tracker variable, updates method button colors
        """

        self.method = 'Webster'
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
        list_temp = [Label(self.frame_widgets, text=self.rows - 1, width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Entry(self.frame_widgets, textvariable=value, width=10, bg=self.frame_background,
                           fg=self.widget_foreground, relief='solid', highlightthickness=1,
                           highlightbackground=self.widget_foreground),
                     Label(self.frame_widgets, textvariable=temp_1, width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Label(self.frame_widgets, textvariable=temp_2, width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Label(self.frame_widgets, textvariable=temp_3, width=10, bg=self.frame_background,
                           fg=self.widget_foreground),
                     Label(self.frame_widgets, textvariable=temp_4, width=10, bg=self.frame_background,
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
        self.frame_widgets.update_idletasks()

        # resize the canvas frame (width fits depending on input, height is static)
        first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns)) + 4
        first5rows_height = 190

        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                 height=first5rows_height)

        # set canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # remove slider stuff
        self.slider['state'] = DISABLED
        self.slider_label_title.config(text='')
        self.slider_label.config(text='')
        self.original_divisor_label.config(text='')
        self.message_variable.set('')

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
            self.frame_widgets.update_idletasks()

            # resize the canvas frame (width fits depending on input, height is static)
            first5columns_width = sum(self.grid[0][j].winfo_width() for j in range(0, self.columns)) + 4
            first5rows_height = 190

            self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                     height=first5rows_height)

            # set canvas scrolling region
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            # remove slider stuff
            self.slider['state'] = DISABLED
            self.slider_label_title.config(text='')
            self.slider_label.config(text='')
            self.original_divisor_label.config(text='')
            self.message_variable.set('')

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

            # remove slider stuff
            self.slider['state'] = DISABLED
            self.slider_label_title.config(text='')
            self.slider_label.config(text='')
            self.original_divisor_label.config(text='')
            self.message_variable.set('')

            # clear recent data
            data = open('../data/recent_table_data.csv', 'r+')
            data.truncate(0)
            data.close()

    def calculate(self):
        """
        calculate - calculates the results for the selected method
        """

        self.slider['state'] = DISABLED
        self.slider_label_title.config(text='')
        self.slider_label.config(text='')
        self.original_divisor_label.config(text='')
        self.message_variable.set('')

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
                    "Invalid input type for amount of seats.\n"
                    "Make sure there are not any letters in\n"
                    "the field for the amount of seats.")
            else:
                num_seats = 0
                try:
                    num_seats = float(self.num_seats.get())
                except ValueError:
                    valid_input = False

                if not valid_input:
                    self.message_variable.set(
                        'Invalid character type detected in seats field.\n'
                        'Make sure the seats field doesn\'t contain letters.')
                else:
                    populations = []
                    for i, x in enumerate(self.populations):
                        if x.get() == '':
                            valid_input = False
                            break
                        try:
                            populations.append(float(x.get()))
                        except ValueError:
                            valid_input = False
                            break

                    if not valid_input:
                        self.message_variable.set(
                            "At least one population textfield is empty or\n"
                            "contains invalid characters. Remove the state or\n"
                            "enter a valid population value.")
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
                            final_fair_shares, total_initial_fair_shares, lower_boundary, upper_boundary, \
                            self.divisor_estimations_history = method.calculate()

                            if original_divisor is None:
                                self.message_variable.set(
                                    f'Warning: results could not be calculated.\n'
                                    f'This can sometimes happen using {selected}\'s\n'
                                    f'method with very specific number combinations\n'
                                    f'and is rare. Make sure the correct values are\n'
                                    f'entered.')

                                # remove calculation values
                                for i in range(len(self.populations)):
                                    self.initial_quotas[i].set('-')
                                    self.final_quotas[i].set('-')
                                    self.initial_fair_shares[i].set('-')
                                    self.final_fair_shares[i].set('-')
                            else:
                                self.original_divisor = original_divisor
                                self.modified_divisor = modified_divisor
                                self.lower_boundary = lower_boundary
                                self.upper_boundary = upper_boundary
                                self.original_quota_values = initial_quotas
                                self.original_fair_share_values = initial_fair_shares

                                self.final_quota_values = final_quotas
                                self.final_fair_share_values = final_fair_shares

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
                                list_temp = [Label(self.frame_widgets, text='total', width=10, bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_widgets, text=sum(populations), width=10,
                                                   bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_widgets, text=f'~{round(sum(initial_quotas), 4)}',
                                                   width=10, bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_widgets, text=f'~{round(sum(final_quotas), 4)}', width=10,
                                                   bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_widgets, text=sum(initial_fair_shares), width=10,
                                                   bg=self.frame_background,
                                                   fg=self.widget_foreground),
                                             Label(self.frame_widgets, text=sum(final_fair_shares), width=10,
                                                   bg=self.frame_background,
                                                   fg=self.widget_foreground)]

                                self.grid.append(list_temp)

                                if selected == 'Hamilton':
                                    self.message_variable.set('')
                                else:
                                    self.message_variable.set('')

                                self.grid[self.rows - 1][0].grid(row=self.rows - 1, column=0, sticky='news', padx=10)
                                self.grid[self.rows - 1][1].grid(row=self.rows - 1, column=1, sticky='news', padx=10)
                                self.grid[self.rows - 1][2].grid(row=self.rows - 1, column=2, sticky='news', padx=10)
                                self.grid[self.rows - 1][3].grid(row=self.rows - 1, column=3, sticky='news', padx=10)
                                self.grid[self.rows - 1][4].grid(row=self.rows - 1, column=4, sticky='news', padx=10)
                                self.grid[self.rows - 1][5].grid(row=self.rows - 1, column=5, sticky='news', padx=10)

                                # update widget frames idle tasks to calculate widget sizes
                                self.frame_widgets.update_idletasks()

                                # resize the canvas frame (width fits depending on input, height is static)
                                first5columns_width = sum(
                                    self.grid[0][j].winfo_width() for j in range(0, self.columns)) + 4
                                first5rows_height = 190

                                self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                                                         height=first5rows_height)

                                # set canvas scrolling region
                                self.canvas.config(scrollregion=self.canvas.bbox("all"))

                                if selected != 'Hamilton':
                                    self.slider_label_title.config(text='Modified Divisor')
                                    self.slider.config(state='normal', from_=self.lower_boundary,
                                                       to=self.upper_boundary, value=self.modified_divisor)
                                    self.slider_label.config(text=round(self.modified_divisor, 4))

                                    if round(lower_boundary, 4) >= round(upper_boundary, 4) or (
                                            lower_boundary is None or upper_boundary is None):
                                        self.original_divisor_label.config(
                                            text=f'original divisor: {round(self.original_divisor, 4)}  |  could not '
                                                 f'estimate lowest or highest possible divisor ')
                                        self.slider['state'] = DISABLED
                                        self.slider_label_title.config(text='Modified Divisor')
                                        self.slider_label.config(text='N/A')
                                    else:
                                        self.original_divisor_label.config(
                                            text=f'original divisor: {round(self.original_divisor, 4)}  |  {round(lower_boundary, 4)} > safe divisor range < {round(upper_boundary, 4)}')
                                else:
                                    self.slider['state'] = DISABLED
                                    self.slider_label_title.config(text='Modified Divisor')
                                    self.slider_label.config(text='N/A')
                                    self.original_divisor_label.config(
                                        text=f'divisor: {round(self.original_divisor, 4)}')
                                    self.message_variable.set('')

                                # set calculate pressed to true
                                self.calculate_pressed = True
                                self.last_calculation.set(selected)

                                # shows charts and graphs in checkboxes are check
                                if self.show_chart.get() == 1 and self.show_graph.get() != 1:
                                    plot = Plot(self.original_divisor, self.modified_divisor, initial_quotas,
                                                final_quotas, initial_fair_shares, final_fair_shares,
                                                total_initial_fair_shares, lower_boundary, upper_boundary,
                                                self.divisor_estimations_history)
                                    plot.create_fair_share_plot()
                                elif self.show_graph.get() == 1 and self.show_chart.get() != 1 and selected != 'Hamilton':
                                    plot = Plot(self.original_divisor, self.modified_divisor, initial_quotas,
                                                final_quotas, initial_fair_shares, final_fair_shares,
                                                total_initial_fair_shares, lower_boundary, upper_boundary,
                                                self.divisor_estimations_history)
                                    plot.create_divisor_graph()
                                elif self.show_graph.get() == 1 and self.show_chart.get() == 1:
                                    if selected != 'Hamilton':
                                        plot = Plot(self.original_divisor, self.modified_divisor, initial_quotas,
                                                    final_quotas, initial_fair_shares, final_fair_shares,
                                                    total_initial_fair_shares, lower_boundary, upper_boundary,
                                                    self.divisor_estimations_history)
                                        plot.create_combined_graph()
                                    else:
                                        plot = Plot(self.original_divisor, self.modified_divisor, initial_quotas,
                                                    final_quotas, initial_fair_shares, final_fair_shares,
                                                    total_initial_fair_shares, lower_boundary, upper_boundary,
                                                    self.divisor_estimations_history)
                                        plot.create_fair_share_plot()

                                # save recent calculation
                                self.save_recent_data()

    def show_about(self):
        """
        show_about - displays a popup gui with information about the app
        """

        # create new tkinter window
        about_window = Toplevel(self.root)
        about_window.title('about')
        about_window.geometry("640x430")
        about_window.resizable(False, False)
        about_window.configure(bg=self.frame_background)

        # create heading label
        Label(about_window, text='About', bg=self.frame_background, fg=self.widget_foreground,
              width=50, font=self.font).place(relx=.5, y=20,
                                              anchor=CENTER)

        # about line 1
        Label(about_window, text='What this is:', bg=self.frame_background, fg=self.widget_foreground,
              width=50, font=self.tiny_font).place(relx=.5, y=60, anchor=CENTER)
        Label(about_window, text='This software allows users to apportion seats to states using four historic\n'
                                 'methods used in the United States hundreds of years ago. Those methods are\n'
                                 'Hamilton\'s, Adam\'s, Jefferson\'s, and Webster\'s methods of apportionment.',
              bg=self.frame_background, fg=self.widget_foreground,
              width=70, font=self.tiny_font).place(relx=.5, y=100, anchor=CENTER)

        # about line 2
        Label(about_window, text='Google Play free version with ads',
              bg=self.frame_background, fg=self.widget_foreground,
              width=70, font=self.tiny_font).place(relx=.5, y=165, anchor=CENTER)
        Button(about_window, text='view', width=9, height=1, bg=self.frame_background,
               fg=self.widget_foreground, relief='groove',
               borderwidth=2, font=self.font, command=lambda: webbrowser.open(
                'https://play.google.com/store/apps/details?id=com.brandon.apportionmentcalculator&hl=en_US&gl=US')).place(
            relx=.5, y=200, anchor=CENTER)

        # about line 3
        Label(about_window, text='Google Play 0.99c version without ads',
              bg=self.frame_background, fg=self.widget_foreground,
              width=70, font=self.tiny_font).place(relx=.5, y=250, anchor=CENTER)
        Button(about_window, text='view', width=9, height=1, bg=self.frame_background,
               fg=self.widget_foreground, relief='groove',
               borderwidth=2, font=self.font, command=lambda: webbrowser.open(
                'https://play.google.com/store/apps/details?id=com.brandon.apportionmentcalculatorpro&hl=en_US&gl=US')).place(
            relx=.5, y=288, anchor=CENTER)

        # about line 4
        Label(about_window, text='Check out our other apps',
              bg=self.frame_background, fg=self.widget_foreground,
              width=70, font=self.tiny_font).place(relx=.5, y=340, anchor=CENTER)
        Button(about_window, text='website', width=9, height=1, bg=self.frame_background,
               fg=self.widget_foreground, relief='groove',
               borderwidth=2, font=self.font, command=lambda: webbrowser.open(
                'https://ticerapps.com/')).place(
            relx=.5, y=378, anchor=CENTER)

    def show_guide(self):
        """
        show_guide - shows popup gui containing documentation on how to use the app
        """

        # create new tkinter window
        guide_window = Toplevel(self.root)
        guide_window.title('Software guide')
        guide_window.geometry("680x530")
        guide_window.resizable(False, False)
        guide_window.configure(bg=self.frame_background)

        # create heading label
        Label(guide_window, text='Instructions', bg=self.frame_background, fg=self.widget_foreground,
              width=50, font=self.font).place(relx=.5, y=20,
                                              anchor=CENTER)

        # instruction line 1
        Label(guide_window, text='Adding seats:', bg=self.frame_background, fg=self.widget_foreground,
              width=50, font=self.tiny_font).place(relx=.5, y=60, anchor=CENTER)
        Label(guide_window, text='Enter the number of seats you want to add in the field at the top left.',
              bg=self.frame_background, fg=self.widget_foreground,
              width=70, font=self.tiny_font).place(relx=.5, y=80, anchor=CENTER)

        # instruction line 2
        Label(guide_window, text='Selecting a method:', bg=self.frame_background, fg=self.widget_foreground,
              width=50, font=self.tiny_font).place(relx=.5, y=120, anchor=CENTER)
        Label(guide_window, text='Select one of the four methods at the top right to apply it.',
              bg=self.frame_background, fg=self.widget_foreground,
              width=70, font=self.tiny_font).place(relx=.5, y=140, anchor=CENTER)

        # instruction line 3
        Label(guide_window, text='Add/remove/clear states & calculate results:', bg=self.frame_background,
              fg=self.widget_foreground,
              width=50, font=self.tiny_font).place(relx=.5, y=180, anchor=CENTER)
        Label(guide_window,
              text='Use the calculator buttons at the top middle to add and remove. Press = to get results.',
              bg=self.frame_background, fg=self.widget_foreground,
              width=90, font=self.tiny_font).place(relx=.5, y=200, anchor=CENTER)

        # instruction line 4
        Label(guide_window, text='Show initial fair share chart:', bg=self.frame_background,
              fg=self.widget_foreground,
              width=50, font=self.tiny_font).place(relx=.5, y=240, anchor=CENTER)
        Label(guide_window,
              text='Navigate to view/charts and select "show fair share chart."',
              bg=self.frame_background, fg=self.widget_foreground,
              width=90, font=self.tiny_font).place(relx=.5, y=260, anchor=CENTER)

        # instruction line 5
        Label(guide_window, text='Show divisor boundaries graph:', bg=self.frame_background,
              fg=self.widget_foreground,
              width=50, font=self.tiny_font).place(relx=.5, y=300, anchor=CENTER)
        Label(guide_window,
              text='Navigate to view/charts and select "show estimated divisor graph."',
              bg=self.frame_background, fg=self.widget_foreground,
              width=90, font=self.tiny_font).place(relx=.5, y=320, anchor=CENTER)

        # instruction line 6
        Label(guide_window, text='Save data to csv/xlsx file:', bg=self.frame_background,
              fg=self.widget_foreground,
              width=50, font=self.tiny_font).place(relx=.5, y=360, anchor=CENTER)
        Label(guide_window,
              text='Navigate to file/export and select ".csv file" or ".xlsx file" to save current data to a file.',
              bg=self.frame_background, fg=self.widget_foreground,
              width=90, font=self.tiny_font).place(relx=.5, y=380, anchor=CENTER)

        # instruction line 7
        Label(guide_window, text='Dynamically change modified divisor:', bg=self.frame_background,
              fg=self.widget_foreground,
              width=50, font=self.tiny_font).place(relx=.5, y=420, anchor=CENTER)
        Label(guide_window,
              text='After calculating results for any method (except Hamilton) the slider at the bottom left\n'
                   'is enabled and you can use it to change the divisor to any value between the lowest and\n'
                   'highest possible divisor.',
              bg=self.frame_background, fg=self.widget_foreground,
              width=90, font=self.tiny_font).place(relx=.5, y=460, anchor=CENTER)

    def slider_changed(self, event):
        """
        slider_changed - listener to update table values and widgets when slider is changed

        :param event: event
        """

        # if not hamilton update the label displaying the slider value
        if self.calculate_pressed and self.clicked != 'Hamilton':
            self.slider_label.config(text=round(self.slider.get(), 4))

            # get the populations
            populations = []
            for i, x in enumerate(self.populations):
                if x.get() == '':
                    break
                try:
                    populations.append(float(x.get()))
                except ValueError:
                    break

            # get new values based on new information
            method = None
            if self.last_calculation.get() == 'Jefferson':
                method = Jefferson(float(self.num_seats.get()), self.rows - 1, populations)
            elif self.last_calculation.get() == 'Adam':
                method = Adam(float(self.num_seats.get()), self.rows - 1, populations)
            elif self.last_calculation.get() == 'Webster':
                method = Webster(float(self.num_seats.get()), self.rows - 1, populations)

            # gather filtered results
            final_quotas, final_fair_shares = method.calculate_with_divisor(round(self.slider.get(), 4))

            # update modified divisor depending on slider result
            self.modified_divisor = round(self.slider.get(), 4)

            # update widgets in the grid
            for i, initial_quota in enumerate(self.original_quota_values):
                self.initial_quotas[i].set(round(initial_quota, 4))
            for i, final_quota in enumerate(final_quotas):
                self.final_quotas[i].set(round(final_quota, 4))
            for i, initial_fair_share in enumerate(self.original_fair_share_values):
                self.initial_fair_shares[i].set(round(initial_fair_share, 4))
            for i, final_fair_share in enumerate(final_fair_shares):
                self.final_fair_shares[i].set(round(final_fair_share, 4))

            # if the boundary calculations are inconclusive, do not display results
            if round(self.lower_boundary, 4) >= round(self.upper_boundary, 4):
                self.original_divisor_label.config(
                    text=f'original divisor: {round(self.original_divisor, 4)}  |  could not estimate lowest or '
                         f'highest possible divisor ')
                self.slider['state'] = DISABLED
                self.slider_label_title.config(text='Modified Divisor')
                self.slider_label.config(text='N/A')
            else:
                self.original_divisor_label.config(
                    text=f'original divisor: {round(self.original_divisor, 4)}  |  {round(self.lower_boundary, 4)} > '
                         f'safe divisor range < {round(self.upper_boundary, 4)}')
            self.message_variable.set('')
            self.grid[self.rows - 1][0].config(text='total')
            self.grid[self.rows - 1][1].config(text=sum(populations))
            self.grid[self.rows - 1][2].config(text=f'~{round(sum(self.original_quota_values), 4)}')
            self.grid[self.rows - 1][3].config(text=f'~{round(sum(final_quotas), 4)}')
            self.grid[self.rows - 1][4].config(text=sum(self.original_fair_share_values))
            self.grid[self.rows - 1][5].config(text=round(sum(final_fair_shares), 4))

            # set calculate pressed to true
            self.calculate_pressed = True

    def change_theme_dark(self):
        """
        change_theme_dark - changes gui to dark mode
        """

        self.selected_theme = 0

        # clear data
        data = open('../data/settings.csv', 'r+')
        data.truncate(0)
        data.close()

        # write new data
        with open('../data/settings.csv', 'w', newline='') as file:
            headers = ['theme', 'fg', 'bg']
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            writer.writerow({headers[0]: self.selected_theme,
                             headers[1]: "ghost white",
                             headers[2]: "gray23"})

        # restart app
        self.root.destroy()
        App()

    def change_theme_light(self):
        """
        change_theme_light - changes gui to light mode
        """

        self.selected_theme = 1

        # clear data
        data = open('../data/settings.csv', 'r+')
        data.truncate(0)
        data.close()

        # write new data
        with open('../data/settings.csv', 'w', newline='') as file:
            headers = ['theme', 'fg', 'bg']
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            writer.writerow({headers[0]: self.selected_theme,
                             headers[1]: "gray23",
                             headers[2]: "ghost white"})

        # restart app
        self.root.destroy()
        App()

    def change_theme_clt_green(self):
        """
        change_theme_clt_green - changes gui to unc-charlotte school colors
        """

        self.selected_theme = 2

        # clear data
        data = open('../data/settings.csv', 'r+')
        data.truncate(0)
        data.close()

        # write new data
        with open('../data/settings.csv', 'w', newline='') as file:
            headers = ['theme', 'fg', 'bg']
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            writer.writerow({headers[0]: self.selected_theme,
                             headers[1]: "#B3A369",
                             headers[2]: "#2C5234"})

        # restart app
        self.root.destroy()
        App()

    def change_theme_tarheel_blue(self):
        """
        change_theme_tarheel_blue - changes gui to unc-chapel hill school colors
        """

        self.selected_theme = 3

        # clear data
        data = open('../data/settings.csv', 'r+')
        data.truncate(0)
        data.close()

        # write new data
        with open('../data/settings.csv', 'w', newline='') as file:
            headers = ['theme', 'fg', 'bg']
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            writer.writerow({headers[0]: self.selected_theme,
                             headers[1]: "ghost white",
                             headers[2]: "#4B9CD3"})

        # restart app
        self.root.destroy()
        App()

    def change_theme_wolfpack_red(self):
        """
        change_theme_tarheel_blue - changes gui to nc state school colors
        """

        self.selected_theme = 4

        # clear data
        data = open('../data/settings.csv', 'r+')
        data.truncate(0)
        data.close()

        # write new data
        with open('../data/settings.csv', 'w', newline='') as file:
            headers = ['theme', 'fg', 'bg']
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            writer.writerow({headers[0]: self.selected_theme,
                             headers[1]: "ghost white",
                             headers[2]: "#CC0000"})

        # restart app
        self.root.destroy()
        App()


if __name__ == '__main__':
    App()
