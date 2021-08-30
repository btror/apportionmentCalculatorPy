import tkinter as tk


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x400')
        self.root.title('Ticer\'s Apportionment Calculator 0.1.0')

        self.root.mainloop()


if __name__ == '__main__':
    App()
