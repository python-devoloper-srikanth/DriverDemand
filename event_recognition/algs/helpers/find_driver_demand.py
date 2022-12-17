# in built modules
from typing import Tuple, Optional

# installed modules
import numpy as np
import pandas as pd


class DriverDemand:
    """
    The reason for creation statis methods instead of instance methods is,
    these methods can be used as utility methods wherever we require
    """

    @staticmethod
    def find_driver_demand(end_type: int, time_type: str,
                           time_brake: pd.Series, data_brake: pd.Series, brake_status: str,
                           time_acc: pd.Series, data_acc: pd.Series, acc_status: str,
                           time_start: float, t_seat_rail_acc_filter: pd.Series,
                           seat_rail_acc_filter: pd.Series) -> Tuple[Optional[float], Optional[str], Optional[str]]:
        """
        
        Args:
            end_type:  = find either the first or last driver demand
            time_type:  = find either the start time or the end time of the change
            time_brake: 
            data_brake: 
            brake_status: 
            time_acc: 
            data_acc: 
            acc_status: 
            time_start: 
            t_seat_rail_acc_filter: 
            seat_rail_acc_filter: 

        Returns:

        """""

        # Brake pedal conditions
        time_of_threshold_brake = DriverDemand.find_status_time('Brake', time_type, time_brake, data_brake,
                                                                brake_status, time_start,
                                                                t_seat_rail_acc_filter, seat_rail_acc_filter)
        # Accelerator pedal conditions
        time_of_threshold_acc = DriverDemand.find_status_time('Pedal', time_type, time_acc, data_acc, acc_status,
                                                              time_start,
                                                              t_seat_rail_acc_filter, seat_rail_acc_filter)

        # No conditions
        if time_of_threshold_brake is None and time_of_threshold_acc is None:
            return None, None, None

        # Both conditions
        if time_of_threshold_brake is not None and time_of_threshold_acc is not None:
            if end_type == 'Last':
                # Use the last action
                if time_of_threshold_brake > time_of_threshold_acc:
                    type_ = 'Brake'
                else:
                    type_ = 'Pedal'
            elif end_type == 'First':
                # Use the first action
                if time_of_threshold_brake < time_of_threshold_acc:
                    type_ = 'Brake'
                else:
                    type_ = 'Pedal'

        # Brake only
        if time_of_threshold_brake is not None and time_of_threshold_acc is None:
            type_ = 'Brake'

        # Pedal only
        if time_of_threshold_brake is None and time_of_threshold_acc is not None:
            type_ = 'Pedal'

        if type_ == 'Brake':
            t = time_of_threshold_brake
            status = brake_status
        elif type_ == 'Pedal':
            t = time_of_threshold_acc
            status = acc_status

        return t, type_, status

    @staticmethod
    def find_status_time(pedal_type: str, time_type: str, time_pedal: pd.Series,
                         data_pedal: pd.Series, pedal_status: str, time_start: float,
                         t_seat_rail_acc_filter: pd.Series, seat_rail_acc_filter: pd.Series) -> Optional[float]:
        """
        Find where the data starts to increase above tolerance value
        Args:
            pedal_type:
            time_type:
            time_pedal:
            data_pedal:
            pedal_status:
            time_start:
            t_seat_rail_acc_filter:
            seat_rail_acc_filter:

        Returns:

        """
        if pedal_type == 'Pedal':
            tolerance = 0.1
        elif pedal_type == 'Brake':
            tolerance = 0.1

        # Abort if no data
        if pedal_status == "" or len(time_pedal) == 0 or len(data_pedal) == 0 or time_start is None:
            return None

        # Find when tolerance is met
        if pedal_status in ['Zero Step In', 'Applying']:
            # Increase from zero
            if time_type == 'End':
                bool_time_data = np.logical_and(time_pedal >= time_start, data_pedal >= tolerance)
                p = bool_time_data[bool_time_data == True].first_valid_index()
            elif time_type == 'Start':
                p = DriverDemand.find_delta_time('Max', time_pedal, data_pedal, time_start, 0.5)

        elif pedal_status in ['Step In', 'Increasing']:
            # Increase from above zero
            if time_type == 'End':
                p = None
            elif time_type == 'Start':
                p = DriverDemand.find_delta_time('Max', time_pedal, data_pedal, time_start, 0.5)

        elif pedal_status in ['Lift Off', 'Releasing']:
            # Reduction to zero
            if time_type == 'End':
                if pedal_type == 'Brake':
                    # developer note: ToDo
                    # Confused with 'helpers.sqt.timeEqual()' method
                    # The below statements are ot clear, the returned parameter are hard coded to zero
                    # I need some support on this

                    # Get seat rail accel at start of event
                    # accel_T0 = seatRailAccelFilter(helpers.sqt.timeEqual(tSeatRailAccelFilter,T0));
                    accel_T0 = 0
                    T0 = 0
                    # findBrakeRelease
                    bool_time_data = np.logical_and(time_pedal >= T0, (seat_rail_acc_filter - accel_T0) >= tolerance)
                    p = bool_time_data[bool_time_data == True].first_valid_index()

                elif pedal_type == 'Pedal':
                    bool_time_pedal = time_pedal >= time_start
                    bool_data_pedal = data_pedal >= tolerance
                    bool_time_data = np.logical_and(bool_time_pedal, bool_data_pedal)

                    p = bool_time_data[bool_time_data == True].first_valid_index()

            elif time_type == 'Start':
                p = DriverDemand.find_delta_time('Min', time_pedal, data_pedal, time_start, 0.5)

        elif pedal_status in ['Part Back Out', 'Reducing']:
            # Reduction above zero
            if time_type == 'End':
                p = None
            elif time_type == 'Start':
                p = DriverDemand.find_delta_time('Min', time_pedal, data_pedal, time_start, 0.5)

        else:
            p = None

        if p is None:
            return None

        # Time of threshold
        t = time_pedal.loc[p]
        return t

    @staticmethod
    def find_delta_time(type_: str, time_pedal: pd.Series,
                        data_pedal: pd.Series, time_start: float, tolerance: float) -> Optional[int]:

        # 1. get the events greater than or equal to given time start
        bool_evt = time_pedal >= time_start

        if bool_evt.any() == False:
            return None

        # 1. take only the events and data greater than or equal to given time start
        data_evt = data_pedal.loc[bool_evt]
        time_evt = time_pedal.loc[bool_evt]

        # find the signal difference
        delta_data_evt = data_evt.diff()
        delta_data_evt = delta_data_evt.replace(np.nan, 0)

        # find the zero entries
        bool_zero = delta_data_evt == 0

        # Use non zero data only
        delta_data_valid = delta_data_evt.loc[~bool_zero]
        time_valid = time_evt.loc[~bool_zero]

        if len(delta_data_valid) == 0:
            return None

        # Find the min/max positions
        if type_ == 'Min':
            peak = delta_data_valid.min()
        elif type_ == 'Max':
            peak = delta_data_valid.max()

        kPeak = delta_data_valid[delta_data_valid == peak].index[0]

        # Time of the min/max
        tPeak = time_valid[kPeak]

        # Delta tolerance to search for
        limit = peak * tolerance

        # Find the position
        bool_time_valid = time_valid < tPeak
        if type_ == 'Min':
            bool_delta_data_valid = delta_data_valid >= limit
        elif type_ == 'Max':
            bool_delta_data_valid = delta_data_valid <= limit

        bool_time_delta = np.logical_and(bool_time_valid, bool_delta_data_valid)

        k = bool_time_delta[bool_time_delta == True].last_valid_index()
        if k is None:
            return None

        # Get the time from the filtered data
        t = time_valid.loc[k]

        # Find the position in the original time series
        bool_time_pedal = time_pedal >= t
        p = bool_time_pedal[bool_time_pedal == True].last_valid_index()

        return p
