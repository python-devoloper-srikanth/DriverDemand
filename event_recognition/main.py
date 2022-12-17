# in built modules
from typing import Tuple, Optional

# installed modules
import pandas as pd

# user defined modules
from event_recognition.algs.helpers.find_driver_demand import DriverDemand
from event_recognition.directorydefinitions import *
from event_recognition.utility import *


def driver_demand_for_acc_brake_pedals() -> Tuple[Optional[float], Optional[str], Optional[str]]:
    """
    Returns:
    """
    # Navigate to the i/o file - 'get_driver_demand.json'
    driver_demand_file_path = os.path.join(get_input_data_directory_path(), 'get_driver_demand.json')

    # get the data from json as dictionary
    json_data_dict = read_json(driver_demand_file_path)

    # set the data to the variable
    # output data
    t = json_data_dict['t']
    type = json_data_dict['type']
    status = json_data_dict['status']

    # input data for finding driver demand
    end_type = json_data_dict['end_type']
    time_type = json_data_dict['time_type']

    time_brake = pd.Series(json_data_dict['time_brake'])
    brake = pd.Series(json_data_dict['brake'])
    brake_pedal_status = json_data_dict['brake_status']

    time_acc = pd.Series(json_data_dict['t_acc_ped'])
    acc = pd.Series(json_data_dict['acc_ped'])
    acc_pedal_status = json_data_dict['pedal_status']

    time_start = json_data_dict['time_start']

    t_seat_rail = pd.Series(json_data_dict['t_seat_rail'])
    seat_rail = pd.Series(json_data_dict['seat_rail'])

    # find driver demand
    t, type, status = DriverDemand.find_driver_demand(end_type, time_type, time_brake, brake, brake_pedal_status,
                                                      time_acc, acc, acc_pedal_status, time_start,
                                                      t_seat_rail, seat_rail)

    print(t)
    print(type)
    print(status)


if __name__ == '__main__':
    driver_demand_for_acc_brake_pedals()
