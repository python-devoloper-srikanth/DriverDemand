# in built modules
import unittest

# installed modules
import pandas as pd

# user defined modules
from event_recognition.algs.helpers.find_driver_demand import DriverDemand
from event_recognition.directorydefinitions import *
from event_recognition.utility import *


class TestDriverDemand(unittest.TestCase):

    def setUp(self) -> None:
        self.t_expected_output = None
        self.type_expected_output = None
        self.status_expected_output = None

    def tearDown(self) -> None:
        self.assertEqual(self.t, self.t_expected_output)
        self.assertEqual(self.type, self.type_expected_output)
        self.assertEqual(self.status, self.status_expected_output)

    def test_find_driver_demand(self):
        # get the data from json as dictionary
        # Navigate to the i/o file - 'get_driver_demand.json'
        file_path = os.path.join(get_input_data_directory_path(), 'get_driver_demand.json')
        json_data_dict = read_json(file_path)

        # set the data to the variable
        # output data
        # self.t_expected_output = json_data_dict['t']
        self.t_expected_output = 26.8515
        self.type_expected_output = json_data_dict['type']
        self.status_expected_output = json_data_dict['status']

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
        self.t, self.type, self.status = DriverDemand.find_driver_demand(end_type, time_type, time_brake, brake,
                                                                         brake_pedal_status,
                                                                         time_acc, acc, acc_pedal_status, time_start,
                                                                         t_seat_rail, seat_rail)
