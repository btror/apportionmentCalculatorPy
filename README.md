
# Apportionment Calculator
### Calculate quotas, fair-shares, and divisors for Jefferson's, Adam's, Webster's, and Hamilton's methods.

Dessktop icon (1.0.1)

<img src="res/icon.png" width="300" height="300" >

# Mobile App Implementation:
Android (free with ads): <a href="https://play.google.com/store/apps/details?id=com.brandon.apportionmentcalculator&hl=en_US&gl=US">View</a> on Play Store

Android (99c without ads): <a href="https://play.google.com/store/apps/details?id=com.brandon.apportionmentcalculatorpro&hl=en_US&gl=US">View</a> on Play Store

# Website
For more information visit the apps page of my website https://ticerapps.com/apps

# Desktop version

<details>
  <summary>Expand documentation</summary>
  
  ## apportionment_calculator.py
  ### class App
  - function init - initialize class variables (did not include widgets)
    - selected_theme: int - selected background theme number (combinations of different frame_background and widget_foreground values)
    - frame_background: str - background color of the software
    - widget_foreground: str - foreground color of the software (fonts & outlines)
    - font: font - Font for the widgets with the largest text
    - tiny_font: Font - font for the widgets with the smallest text
    - seats_font: Font - font for the seats label
    - show_chart: IntVar - value for tracking if fair share popup chart is enabled (1 is on 0 is off)
    - show_graph: IntVar - value for tracking if divisor algorithm visualization popup graph is enabled (1 is on 0 is off)
    - original_quota_values: list[float] - list of original quota calculations
    - original_fair_share_values: list[float] - list of original fair share calculations
    - final_quota_values: list[float] - list of final quota calculations
    - final_fair_share_values: list[float] - list of final fair share calculations
    - calculate_pressed: boolean - track if calculate button is pressed
    - original_divisor: float - track original divisor
    - modified_divisor: float - track modified divisor
    - lower_boundary: float - track lowest divisor possible
    - upper_boundary: float - track highest divisor possible
    - clicked: StringVar - track selected apportionment method
    - last_calculation: StringVar - track previously used apportionment method
    - num_seats: StringVar - tracks inputted amount of seats (used StringVar instead of IntVar because we don't want a default value of 0)
    - message_variable: StringVar - message to display depending on the calculation results
    - slider_value: StringVar - tracks divisor slider value
    - rows: int - number of rows in the grid (dynamic)
    - cols: int - number of cols in each row of the grid (always 6)
    - grid: list[any] - list holding widgets in the grid (labels and entries)
  
  - function save_recent_data - saves previous calculation, when app is closed previous data loads in the table
    - data: csv data - csv data from recent_table_data.csv file
    - file: csv data - csv data from recent_table_data.csv file
    - headers: list[str] - list of headers to write in recent_table_data.csv
    - method: str - selected method
    - seats: float - number of seats to apportion
    - original_divisor: float - original calculated divisor
    - modified_divisor: float - updated calculated divisor
    - list_state_numbers: list[int] - list of each state number
    - list_populations: list[float] - list of each state population
    - list_initial_quotas: list[float] - list of initial quotas
    - list_final_quotas: list[float] - list of final quotas
    - list_initial_fair_shares: list[float] - list of initial fair shares
    - list_final_fair_shares: list[float] - list of final fair shares
  
  - function load_saved_table_data - loads saved (or recent) data into the table
    - reader: csv data - reads csv data from recent_table_data.csv
    - line_count: int - number of lines (rows) to iterate through in the recent_table_data.csv
  
  - function save_csv - saves/exports a csv file containing data in the table
    - new_file: file - a new csv file
    - headers: list[str] - list of headers to write
    - method: str - selected method
    - seats: float - number of seats to apportion
    - original_divisor: float - original calculated divisor
    - modified_divisor: float - updated calculated divisor
    - list_state_numbers: list[int] - list of each state number
    - list_populations: list[float] - list of each state population
    - list_initial_quotas: list[float] - list of initial quotas
    - list_final_quotas: list[float] - list of final quotas
    - list_initial_fair_shares: list[float] - list of initial fair shares
    - list_final_fair_shares: list[float] - list of final fair shares
    
</details>

Release design (1.0.0)

<img src="res/demo_1.JPG" width="685" height="430">

Enter a number of seats to apportion, add some states and enter their populations, and select a method to use to apportion the seats.

<img src="res/demo_2.JPG" width="685" height="430">

Press = to calculate results.

<img src="res/demo_3.JPG" width="685" height="430">

You can use the slider at the bottom to change the divisor to any value that will result in the proper distributions

<img src="res/demo_4.gif" width="685" height="430">

You can also display a graph that shows all the estimated divisors guessed until a proper divisor is found and a bar graph showing the fair shares.

<img src="res/demo_5.gif" width="685" height="460">

# Downloads

| 1.1.2 (latest) | 1.1.1 | 1.1.0 | 
|-------|-------|-------|
| <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.1.2/apportionmentCalculatorPy.exe">Download exe</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.1.1/Apportionment.Calculator.exe">Download exe</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.1.0/apportionmentCalculatorPy.exe">Download exe</a> |
| <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.1.2.zip">Download zip</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.1.1.zip">Download zip</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.1.0.zip">Download zip</a>

| 1.0.1 | 1.0.0 |
|-------|-------|
| <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.0.1/apportionmentCalculatorPy.exe">Download exe</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.0.0/apportionmentCalculatorPy.exe">Download exe</a> |
| <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.0.1.zip">Download zip</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.0.0.zip">Download zip</a> |

