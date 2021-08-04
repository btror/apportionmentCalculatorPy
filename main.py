from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout


class MyApp(App):
    def __init__(self, **kwargs):
        """
        init - define class variables

        :param kwargs: kivy stuff
        """

        super().__init__(**kwargs)

        # create app layout
        self.layout_1 = GridLayout(cols=2)
        self.screen = Screen()

        # create a list for the state widgets [state label, population input]
        self.states = []

        # create seats label and input field
        self.seats_label = Label(text="Enter an amount of seats:")  # default state label
        self.seats_input_field = TextInput(font_size=12)  # default population input field

        # create add/remove buttons
        self.add_button = Button(text="add")
        self.remove_button = Button(text="remove")

    def build(self):
        """
        build - creates a build of the app and creates a kivy gui

        :return: screen object
        """

        # assign an event to the add/remove buttons
        self.add_button.bind(on_press=self.add_state)
        self.remove_button.bind(on_press=self.remove_state)

        # create a default state (state label and population input field)
        state_label = Label(text="state " + str(len(self.states) + 1))
        population_input = TextInput(font_size=12)

        # add new state to states list
        state = [state_label, population_input]
        self.states.append(state)

        # add widgets to the layout
        self.layout_1.add_widget(self.seats_label)
        self.layout_1.add_widget(self.seats_input_field)
        self.layout_1.add_widget(self.add_button)
        self.layout_1.add_widget(self.remove_button)
        self.layout_1.add_widget(state_label)
        self.layout_1.add_widget(population_input)

        # add the layout to the screen and return it
        self.screen.add_widget(self.layout_1)

        return self.screen

    def add_state(self, event):
        """
        add_state - creates a new state like this: [state label, population input field]

        :param event: kivy event
        """

        # create a new state label and input field
        state_label = Label(text="state " + str(len(self.states) + 1))
        population_input = TextInput(font_size=12)

        # create a new state object
        state = [state_label, population_input]

        # add new state to the states list to track it
        self.states.append(state)

        # add the state object to the app layout
        self.layout_1.add_widget(state_label)
        self.layout_1.add_widget(population_input)

    def remove_state(self, event):
        """
        remove_state - removes an existing state

        :param event: kivy event
        """

        # remove a state unless there aren't any to remove
        if len(self.states) > 1:
            self.layout_1.remove_widget(self.states[len(self.states) - 1][0])  # state label (self.states[0])
            self.layout_1.remove_widget(self.states[len(self.states) - 1][1])  # population input field (self.states[1])

            # remove newest state object from states list
            self.states.pop()


MyApp().run()
