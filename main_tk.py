import tkinter as tk
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.geometry('500x400')
        self.root.title('Ticer\'s Apportionment Calculator 0.1.0')

        # frame
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=1)

        # canvas
        canvas = Canvas(main_frame, bg="red")
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # new frame
        secondary_frame = Frame(canvas)
        canvas.create_window((0, 0), window=secondary_frame, anchor="nw")

        for thing in range(100):
            Button(secondary_frame, text=f'Button {thing}').grid(row=thing, column=0)

        # title
        self.label_title = Label(self.root, text='Ticer\'s Apportionment Calculator 0.1.0').place(relx=.5, y=20,
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
        self.dropdown = OptionMenu(self.root, clicked, *options).place(relx=.5, y=50, anchor=CENTER)

        # add seats
        self.label_seats = Label(self.root, text='seats: ').place(relx=.45, y=85, anchor=CENTER)
        self.input_seats = Entry(self.root, width=7).place(relx=.54, y=85, anchor=CENTER)

        # add, remove, clear, and calculate buttons
        self.button_add = Button(self.root, text='+', width=5).place(relx=.35, y=120, anchor=CENTER)
        self.button_remove = Button(self.root, text='-', width=5).place(relx=.45, y=120, anchor=CENTER)
        self.button_clear = Button(self.root, text='CLEAR', width=5).place(relx=.55, y=120, anchor=CENTER)
        self.button_calculate = Button(self.root, text='=', width=5).place(relx=.65, y=120, anchor=CENTER)

        self.root.mainloop()


if __name__ == '__main__':
    App()
