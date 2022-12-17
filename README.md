# DriverDemand

This script is itended to look for certain combinations of 
      **driver demands (accelerator pedal and brake pedal) in time-based signals recorded from the vehicle**.


i.e., return a list of events where the brake pedal was 'Zero' and the driver 'Lifted off' the accelerator pedal.
 
1. Migrate this Matlab (findDriverDemand) script to a Python script with equivalent functionality and producing the same results
   Migrated to python 
   1. Equivalent functionality
   2. Followed the Python standard way of coding
      1. Class structure with static methods - Did not go with instance approach to make the functions to use as utility methods
      2. Doc strings and appropriate comments
      3. Followed type hints and variable annotation and used **Typing** module to denote more advanced datatypes
      4. Used **mypy** package to check the static typing in the code
   3. Producing same results - Not done
2. Recreate the module structure so the name spacing in the provided Python scripts matches - Done

I prepared some input data for testing, please ignore if that is not a correct input

•	
o	analysis.py -> event_recognition.config.analysis
o	find_where_time_data_correspond.py -> event_recognition.algs.helpers.find_where_time_data_correspond
o	create you Python script for the migrated Matlab function in -> event_recognition.algs.helpers

•	The I/O for the Matlab function has been provided in JSON format (get_driver_demand.json)

•	Using this I/O data, implement a unit test using the Python unittest package to ensure the output of the Python function is the same as the Matlab script (JSON data)

•	Use a virtual environment in Python

•	Use Pandas.Series to represent time-based signals (e.g. accelerator pedal, brake pedal)

If something is unclear, add a comment about any assumptions you've made or email us directly – 
jfoste18@jaguarlandrover.com 
dlloyd2@jaguarlandrover.com
 
Please submit your files to Liam Dower by Monday 19th December


Challenges and Confusions or Mis understands

1. '.\event_recognition\algs\helpers\find_where_time_data_correspond.py' 
    I understood what this function does, but the this which i did not undertsnad is how this is relavent to the matlab script 'finddriverdemand.m'
    I added the lines for the function call by inputting json data 




Lead  13/12/2022
1. findstatustime parameters, time is time_pedal, data is data_pedal
2. Followed the case sensivity - standerdized strings to PascalCase in input
  thoufgh of inclding the comparison logic in the code itself
3. Though of implementing class structure, but if you want to use this as wrapper kind went with procedure oriented
4. Though of comparing the matlab code execution with python, i dont have matlab