from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout


class MyApp(App):
    def build(self):
        self.layout_1 = GridLayout(cols=2)
        self.screen = Screen()

        self.states = []

        self.label_1 = Label(text="Enter an amount of seats:")
        self.seats_input_field = TextInput(font_size=12)

        self.add_button = Button(text="add")
        self.remove_button = Button(text="remove")

        self.add_button.bind(on_press=self.add_state)
        self.remove_button.bind(on_press=self.remove_state)

        state_label = Label(text="state " + str(len(self.states) + 1))
        population_input = TextInput(font_size=12)

        state = [state_label, population_input]
        self.states.append(state)

        self.layout_1.add_widget(self.label_1)
        self.layout_1.add_widget(self.seats_input_field)
        self.layout_1.add_widget(self.add_button)
        self.layout_1.add_widget(self.remove_button)
        self.layout_1.add_widget(state_label)
        self.layout_1.add_widget(population_input)

        self.screen.add_widget(self.layout_1)
        return self.screen

    def add_state(self, event):
        state_label = Label(text="state " + str(len(self.states) + 1))
        population_input = TextInput(font_size=12)

        state = [state_label, population_input]
        self.states.append(state)

        self.layout_1.add_widget(state_label)
        self.layout_1.add_widget(population_input)

    def remove_state(self, event):
        if len(self.states) > 1:
            self.layout_1.remove_widget(self.states[len(self.states) - 1][0])
            self.layout_1.remove_widget(self.states[len(self.states) - 1][1])

            self.states.pop()
        print(len(self.states))


MyApp().run()