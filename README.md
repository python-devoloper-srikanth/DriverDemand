# DriverDemand

This script is intended to look for certain combinations of 
      **driver demands (accelerator pedal and brake pedal) in time-based signals recorded from the vehicle**.

i.e., return a list of events where the brake pedal was 'Zero' and the driver 'Lifted off' the accelerator pedal.

# **Requirements and their status**
1. Migrate this Matlab (findDriverDemand) script to a Python script with equivalent functionality and producing the same results **- DONE**
2. Recreate the module structure so the name spacing in the provided Python scripts matches **- DONE**
3. Using this I/O data, implement a unit test using the Python unittest package to ensure the output of the 
   Python function is the same as the Matlab script (JSON data) **- DONE**
4. Use a virtual environment in Python **- DONE**
5. Use Pandas.Series to represent time-based signals (e.g. accelerator pedal, brake pedal)  **- DONE**

# **Execution steps for the given solution**
1. clone the code to local machine (Folder structure -> DriverDemand/event_recogniton)
2. create a virtual environment using below command (in DriverDemand fold)

       $ virtualenv -p python3 venv
3. activate the virtual enironment with below command
        
       $ source venv/bin/activate
4. Install packages using requirements.txt file

       $ pip3 install -r requirements.txt
5. Run the **main.py** 

# **Challenges in understanding given problem**

1. I understood what the function does, but what I did not understand is how this is relevant to the matlab script 'finddriverdemand.m'
   Still I added the lines for the function call by inputting json data
   '.\event_recognition\algs\helpers\find_where_time_data_correspond.py' 

2. Input json standardized - in few field all lower cases are there but max of jason, Pascal Case is used. so I manually changed below field in input output data
   Maintained Pascal Case for the below variables
   "end_type":"First",
   "time_type":"Start",

# **Challenges in understanding matlab script**

1. Confused with 'helpers.sqt.timeEqual()' method (line number 130 in matlab script and line number 139 in python script (find_driver_demand.py))

2. The below statements are not clear to me
   
       accel_T0 = seatRailAccelFilter(helpers.sqt.timeEqual(tSeatRailAccelFilter,T0));
   T0 definition is not there, so I hard coded those to zeros
   
3. I tried hard to understand this but i did not succeed. My way of understanding may be wrong, so I need some guidance on this


# **Coding standards which I followed**

1. Class structure with static methods - Did not go with instance method approach to make the functions to use as utility methods
2. Followed type hints and variable annotation and used **Typing** module to denote more advanced datatypes
3. Doc strings and appropriate comments added
4. Used **mypy** package to check the static typing in the code
5. Unit tests added for various sample data along with original json (I recommend pytest instead of unittest because we can have good fixture control which reduces the redundancy in code)
6. I prepared some input data for unit testing, please ignore if that is not a correct input
7. Pandas vs Numppy - need to explain
