import numpy as np
from event_recognition.config.analysis import DATA_LOG_COMPARISON_RASTER
from event_recognition.utility import *


def find_where_time_data_correspond(var1: list[float], var2: list[float]) -> (list[bool]):
    """Finds the indexes of where two time inputs closely correspond (i.e. difference less than a minimum threshold)
    Inputs are lists of floats of size n x 1 where n can be 1 or greater
    Previously called: timeEqual

    Args:
        var1 (list[float]): Input variable one. Previously time1
        var2 (list[float]): Input variable two. Previously time2

    Returns:
        equal_idx (list[bool]: Output boolean variable. Previously val

    """

    # Prepare inputs
    var1 = np.array(var1)
    var2 = np.array(var2)

    equal_idx = (np.abs(var1 - var2) <= DATA_LOG_COMPARISON_RASTER).tolist()

    return equal_idx


if __name__ == "__main__":
    # Navigate to the i/o file - 'get_driver_demand.json'
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    driver_demand_file_path = os.path.join(root_folder, 'input_data', 'get_driver_demand.json')

    # get the data from json as ictionery
    json_data_dict = read_json(driver_demand_file_path)

    time_acc = json_data_dict['t_acc_ped']
    data_acc = json_data_dict['acc_ped']
    time_brake = json_data_dict['time_brake']
    data_brake = json_data_dict['brake']

    equal_idx = find_where_time_data_correspond(data_acc, data_brake)
    print(equal_idx)

