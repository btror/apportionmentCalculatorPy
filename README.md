
# Apportionment calculator
### Calculate quotas, fair-shares, and divisors for Jefferson's, Adam's, Webster's, and Hamilton's methods.

Dessktop icon (1.0.1)

<img src="res/icon.png" width="300" height="300" >

# Mobile app implementation
Android (free with ads): <a href="https://play.google.com/store/apps/details?id=com.brandon.apportionmentcalculator&hl=en_US&gl=US">view</a> on Play Store

Android (99c without ads): <a href="https://play.google.com/store/apps/details?id=com.brandon.apportionmentcalculatorpro&hl=en_US&gl=US">view</a> on Play Store

# Other implementations
Web version: access webpage <a href="https://btror.github.io/apportionment.github.io/">here</a>

.NET version: <a href="https://github.com/btror/apportionmentCalculatorCS">view</a> repository

# Website
For more information visit the apps page of my website https://ticerapps.com/apps

# Desktop version

<details>
  <summary>Expand documentation</summary>
  <br>
  <details>
    <summary>GUI</summary>
    
      Scripts responsible for building the GUI
    
      apportionment_calculator.py
    
      class - App
        functions
          save_recent_data - saves previous calculation, when app is closed previous data loads in the table 
          load_saved_table_data - loads saved (or recent) data into the table
          save_csv - saves/exports a csv file containing data in the table
          save_xlsx - saves/exports an xlsx file containing data in the table
          change_method_hamilton - changes apportionment method to hamilton
          change_method_jefferson - changes apportionment method to jefferson
          change_method_adam - changes apportionment method to adam
          change_method_webster - changes apportionment method to webster
          add_state - adds a new row to the table with six columns
          remove_state - removes a row from the table
          clear_states - clears data from the table 
          calculate - calculates quotas, fair shares, and divisors and displays results in table
          show_about - shows a popup with information about this software
          show_guide - shows a popup with instructions on how to use the software
          slider_changed - updates divisor and table values when the slider widget is used
          change_theme_dark - changes app theme to dark mode
          change_theme_light - changes app theme to light mode
          change_theme_clt_green - changes app theme to unc charlotte school colors
          change_theme_tarheel_blue - changes app theme to unc chapel hill school colors
          change_theme_wolfpack_red - changes app theme to nc state school colors
  
    
      main_plots.py
    
      class - Plot
        functions
          create_combined_graph - creates a single popup containg divisor algorithm graph and fair share chart
          create_divisor_graph - creates a popup graph displaying how the algorithm calculates an acceptable divisor 
                                 as well as the lowest and highest possible estimated divisors
          create_fair_share_plot - creates a popup chart displaying the fair share allocations to each state
          calculate_plot_points - creates lists for estimations, lowest, and highest possible estimated divisors

  </details>
  
  <details>
    <summary>Methods</summary>
    
      Packages
    
      class - Hamilton
        parameters 
          num_seats: int - number of seats to apportion
          states: int - number of states to apportion seats to
          populations: [float] * states - list of populations per state (list must be same size as number of states)
    
        functions
          calculate_quotas([0] * states) - calculates the original quotas for each state and initializes a list for 
                                           final quotas
          calculate_fair_shares([0] * states, quotas) - calculates final fair shares and final quotas
          calculate - apportions seats to states, uses calculate_quotas and calculate_fair_shares
    
        Usage
          method = Hamilton(num_seats, states, populations)
          results = method.calculate() -> returns original divisor, modified divisor, original quotas, final quotas, 
                                          initial fair shares, final fair shares, sum of inititial fair shares, 0, 0, 0
          ```
          # define parameters
          num_seats = 15
          states = 3
          populations = [2400, 3300, 955]
            
          # create object
          method = Hamilton(num_seats, states, populations)
            
          # calculate results
          results = method.calculate()
          ```
    
    
    
      class - Jefferson
        parameters 
          num_seats: int - number of seats to apportion
          states: int - number of states to apportion seats to
          populations: [float] * states - list of populations per state (list must be same size as number of states)
    
        functions
          calculate_quotas([0] * states) - calculates the original quotas for each state and initializes a list for 
                                           final quotas
          calculate_fair_shares([0] * states, quotas) - calculates final fair shares and final quotas
          calculate - apportions seats to states, uses calculate_quotas and calculate_fair_shares
          calculate_with_divisor(float: divisor) - calculates results given a divisor as a parameter
          calculate_lower_boundary(float: divisor) - calculates lowest estimated possible divisor that can be used
          calculate_upper_boundary(float: divisor) - calculates highest estimated possible divisor that can be used
          calculate_plot_points(lower_divisor, upper_divisor) - creates lists of divisors and estimations
    
        Usage
          method = Jefferson(num_seats, states, populations)
          results = method.calculate() -> returns original divisor, modified divisor, original quotas, final quotas, 
                                          initial fair shares, final fair shares, sum of inititial fair shares, 
                                          lower boundary, upper boundary, estimation history
          ```
          # define parameters
          num_seats = 15
          states = 3
          populations = [2400, 3300, 955]
            
          # create object
          method = Jefferson(num_seats, states, populations)
            
          # calculate results
          results = method.calculate()
          ```
    
    
    
      class - Adam
        parameters 
          num_seats: int - number of seats to apportion
          states: int - number of states to apportion seats to
          populations: [float] * states - list of populations per state (list must be same size as number of states)
    
        functions
          calculate_quotas([0] * states) - calculates the original quotas for each state and initializes a list for 
                                           final quotas
          calculate_fair_shares([0] * states, quotas) - calculates final fair shares and final quotas
          calculate - apportions seats to states, uses calculate_quotas and calculate_fair_shares
          calculate_with_divisor(float: divisor) - calculates results given a divisor as a parameter
          calculate_lower_boundary(float: divisor) - calculates lowest estimated possible divisor that can be used
          calculate_upper_boundary(float: divisor) - calculates highest estimated possible divisor that can be used
          calculate_plot_points(lower_divisor, upper_divisor) - creates lists of divisors and estimations
    
        Usage
          method = Adam(num_seats, states, populations)
          results = method.calculate() -> returns original divisor, modified divisor, original quotas, final quotas, 
                                          initial fair shares, final fair shares, sum of inititial fair shares, 
                                          lower boundary, upper boundary, estimation history
          ```
          # define parameters
          num_seats = 15
          states = 3
          populations = [2400, 3300, 955]
            
          # create object
          method = Adam(num_seats, states, populations)
            
          # calculate results
          results = method.calculate()
          ```
    
    
    
      class - Webster
        parameters 
          num_seats: int - number of seats to apportion
          states: int - number of states to apportion seats to
          populations: [float] * states - list of populations per state (list must be same size as number of states)
    
        functions
          calculate_quotas([0] * states) - calculates the original quotas for each state and initializes a list for 
                                           final quotas
          calculate_fair_shares([0] * states, quotas) - calculates final fair shares and final quotas
          calculate - apportions seats to states, uses calculate_quotas and calculate_fair_shares
          calculate_with_divisor(float: divisor) - calculates results given a divisor as a parameter
          calculate_lower_boundary(float: divisor) - calculates lowest estimated possible divisor that can be used
          calculate_upper_boundary(float: divisor) - calculates highest estimated possible divisor that can be used
          calculate_plot_points(lower_divisor, upper_divisor) - creates lists of divisors and estimations
    
        Usage
          method = Webster(num_seats, states, populations)
          results = method.calculate() -> returns original divisor, modified divisor, original quotas, final quotas, 
                                          initial fair shares, final fair shares, sum of inititial fair shares, 
                                          lower boundary, upper boundary, estimation history
          ```
          # define parameters
          num_seats = 15
          states = 3
          populations = [2400, 3300, 955]
            
          # create object
          method = Webster(num_seats, states, populations)
            
          # calculate results
          results = method.calculate()
          ```
        
    
      
  </details>
  
</details>

<br>

Release design (1.0.0)

<img src="res/demo_1.JPG" width="685" height="430">

Enter a number of seats to apportion, add some states and enter their populations, and select a method to use to apportion the seats.

<img src="res/demo_2.JPG" width="685" height="430">

Press = to calculate results.

<img src="res/demo_3.JPG" width="685" height="430">

Use the slider at the bottom to change the divisor to any value that will result in the proper distributions

<img src="res/demo_4.gif" width="685" height="430">

Display a graph that shows all the estimated divisors guessed until a proper divisor is found and a bar graph showing the fair shares.

<img src="res/demo_5.gif" width="685" height="460">

Save and export data to .csv or .xlsx file

<img src="res/demo_6.gif" width="685" height="380">

Change themes

<img src="res/demo_7.gif" width="685" height="380">

# Downloads

| 1.1.2 (latest) | 1.1.1 | 1.1.0 | 
|-------|-------|-------|
| <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.1.2/apportionmentCalculatorPy.exe">Download exe</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.1.1/Apportionment.Calculator.exe">Download exe</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.1.0/apportionmentCalculatorPy.exe">Download exe</a> |
| <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.1.2.zip">Download zip</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.1.1.zip">Download zip</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.1.0.zip">Download zip</a>

| 1.0.1 | 1.0.0 |
|-------|-------|
| <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.0.1/apportionmentCalculatorPy.exe">Download exe</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/releases/download/1.0.0/apportionmentCalculatorPy.exe">Download exe</a> |
| <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.0.1.zip">Download zip</a> | <a href="https://github.com/btror/apportionmentCalculatorPy/archive/refs/tags/1.0.0.zip">Download zip</a> |

