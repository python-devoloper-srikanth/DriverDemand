# in built modules
import os

"""
Any module which calls get_project_root can be moved without changing program behavior. 
Only when the module 'directorydefinitions.py' is moved we have to update get_project_root and the imports.
"""

def get_project_root() -> str:
    return os.path.dirname(os.path.abspath(__file__)) # This is event_recognition folder

def get_input_data_directory_path() -> str:
    return os.path.join(get_project_root(), 'input_data')

# print(get_project_root())
# print(get_input_data_directory_path())