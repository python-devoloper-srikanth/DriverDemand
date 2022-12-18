# DriverDemand

This script is intended to look for certain combinations of 
      **driver demands (accelerator pedal and brake pedal) in time-based signals recorded from the vehicle**.

i.e., return a list of events where the brake pedal was 'Zero' and the driver 'Lifted off' the accelerator pedal.

### **Requirements and their status**

1. Migrate this Matlab (findDriverDemand) script to a Python script with equivalent functionality and producing the same results **- DONE**
2. Recreate the module structure so the name spacing in the provided Python scripts matches **- DONE**
3. Using this I/O data, implement a unit test using the Python unittest package to ensure the output of the 
   Python function is the same as the Matlab script (JSON data) **- DONE**
4. Use a virtual environment in Python **- DONE**
5. Use Pandas.Series to represent time-based signals (e.g. accelerator pedal, brake pedal)  **- DONE**

### **Execution steps for the given solution**

Please follow the below steps to clone and execute,
1. Clone the bundle to local (in working directory) -  **git clone DriverDemand.bundle DriverDemand** 
     
    **OR**

    Download and extract the folder (in working directory) - DriverDemand.7z
    
4. Set up environment (Pycharm or VS code)
    1. Load the project folder (DriverDemand) 
    2. Create a virtual environment
    3. Install packages which are there in requirements.txt - **pip install -r requirements.txt**
  
5. Run the **main.py** (DriverDemand/event_recognition/main.py)

6. Run the unitest with the below command
   1. python -m unittest event_recognition\unit_tests\test_find_driver_demand.py
            
      **OR**
   2. Run the **test_find_driver_demand.py** (DriverDemand/event_recognition\unit_tests\test_find_driver_demand.py

### **Coding standards and approach which I followed to resolve the challenge**

1. Class structure with static methods - Did not go with instance method approach to make the functions to use as utility methods
2. Followed type hints and variable annotation and used **Typing** module to denote more advanced datatypes
3. Doc strings and appropriate comments added
4. Used **mypy** package to check the static typing in the code (in terminal: mypy name(filepath or folder path)
5. Unit tests added for various sample data along with original json (I recommend pytest instead of unittest because we can have good fixture control which reduces the redundancy in code)
6. I prepared some input data for unit testing, please ignore if that is not a correct input
7. **ignore_study** folder is created to study the problem using various approaches - handled the problem (analysed the matlab script) using below ways
   1. traditional lists and loops, 
   2. using numpy, and 
   3. using pandas

### **Challenges in understanding given problem**

1. I understood what the below function does, but what I did not understand is how this is relevant to the matlab script 'finddriverdemand.m'
   
   But I tried adding the lines for the function call by inputting json data
   '**.\event_recognition\algs\helpers\find_where_time_data_correspond.py**' 

   This file also can be run directly which reads the json and finds the indexes of where two time inputs closely correspond

2. Input json standardized - lower cases used in few fields,but remaining jason, Pascal Case is used. 

   so I manually changed below fields to Pascal Case in input output data
   
   Maintained Pascal Case for the below variables
   1. "end_type":"First",
   2. "time_type":"Start",

### **Challenges in understanding matlab script**

1. Confused with 'helpers.sqt.timeEqual()' method (line number 130 in matlab script and line number 139 in python script (find_driver_demand.py))

2. The below statements are not clear to me
   
       accel_T0 = seatRailAccelFilter(helpers.sqt.timeEqual(tSeatRailAccelFilter,T0));
   T0 definition is not there, so I hard coded those to zeros
   
3. I tried hard to understand this but i did not succeed. My way of understanding may be wrong, so I need some guidance on this