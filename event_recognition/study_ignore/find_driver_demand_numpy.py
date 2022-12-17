from typing import List

import numpy as np
import pandas as pd


def find_driver_demand_np(end_type: int, time_type: str,
                            time_brake: List[float], data_brake: List[int], brake_status: str,
                            time_acc: List[float], data_acc: List[float], acc_status: str,
                            time_start: float, t_seat_rail_acc_filter: List[float], seat_rail_acc_filter: List[float]):
    """

    Args:
        end_type:
        time_type:
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

    """
    # Initialise
    t = None
    type_ = None
    status = None

    time_brake_pd_sr = pd.Series(time_brake)
    data_brake_pd_sr = pd.Series(data_brake)
    time_acc_pd_sr = pd.Series(time_acc)
    data_acc_pd_sr = pd.Series(data_acc)
    t_seat_rail_acc_filter_pd_sr = pd.Series(t_seat_rail_acc_filter)
    seat_rail_acc_filter_pd_sr = pd.Series(seat_rail_acc_filter)

    # Brake conditions
    Tbrake = find_status_time_np('Brake', time_type, time_brake, data_brake, brake_status, time_start,
                                   t_seat_rail_acc_filter, seat_rail_acc_filter)
    Tbrake_1 = find_status_time_pd('Brake', time_type, time_brake_pd_sr, data_brake_pd_sr, brake_status, time_start,
                                 t_seat_rail_acc_filter_pd_sr, seat_rail_acc_filter_pd_sr)
    # Pedal conditions
    Tpedal = find_status_time_np('Pedal', time_type, time_acc, data_acc, acc_status, time_start,
                                   t_seat_rail_acc_filter, seat_rail_acc_filter)

    Tpedal_1 = find_status_time_pd('Pedal', time_type, time_acc_pd_sr, data_acc_pd_sr, acc_status, time_start,
                                 t_seat_rail_acc_filter_pd_sr, seat_rail_acc_filter_pd_sr)

    # No conditions
    if Tbrake is None and Tpedal is None:
        return t, type_, status

    # Both conditions
    if Tbrake is not None and Tpedal is not None:
        if end_type == 'Last':
            # Use the last action
            if Tbrake > Tpedal:
                type_ = 'Brake'
            else:
                type_ = 'Pedal'
        elif end_type == 'First':
            # Use the first action
            if Tbrake < Tpedal:
                type_ = 'Brake'
            else:
                type_ = 'Pedal'

    # Brake only
    if Tbrake is not None and Tpedal is None:
        type_ = 'Brake'

    # Pedal only
    if Tbrake is None and Tpedal is not None:
        type_ = 'Pedal'

    if type_ == 'Brake':
        t = Tbrake
        status = brake_status
    elif type_ == 'Pedal':
        t = Tpedal
        status = acc_status

    return t, type_, status

def find_status_time_pd(pedal_type: str, time_type: str, time_pedal: pd.Series,
                          data_pedal: pd.Series, pedal_status: str, time_start: float,
                          t_seat_rail_acc_filter: pd.Series, seat_rail_acc_filter: pd.Series):
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

    # Initialise
    t = None
    p = None

    # Abort if no data
    if pedal_status == "" or len(time_pedal) == 0 or len(data_pedal) == 0 or time_start is None:
        return t

    # Find when tolerance is met

    if pedal_status in ['Zero Step In', 'Applying']:
        if time_type == 'End':
            # p = find(time_pedal >= time_start and data_pedal >= tolerance, 1, 'first')
            bool_time_pedal = time_pedal >= time_start
            bool_data_pedal = data_pedal >= tolerance
            bool_time_data = np.logical_and(bool_time_pedal, bool_data_pedal)

            p = bool_time_data[bool_time_data == True].first_valid_index()
            if p is None:
                return p
        elif time_type == 'Start':
            p = find_delta_time_pd('Max', time_pedal, data_pedal, time_start, 0.5)

    elif pedal_status in ['Lift Off', 'Releasing']:
        if time_type == 'End':
            if pedal_type == 'Brake':
                # Get seat rail accel at start of event
                accel_T0 = 0
                # accel_T0 = seatRailAccelFilter(helpers.sqt.timeEqual(tSeatRailAccelFilter,T0));

                # findBrakeRelease
                T0 = 0
                bool_time_pedal = time_pedal >= time_start
                bool_data_pedal = (seat_rail_acc_filter - accel_T0) >= tolerance
                bool_time_data = np.logical_and(bool_time_pedal, bool_data_pedal)

                p = bool_time_data[bool_time_data == True].first_valid_index()
                if p is None:
                    return p

            elif pedal_type == 'Pedal':
                bool_time_pedal = time_pedal >= time_start
                bool_data_pedal = data_pedal >= tolerance
                bool_time_data = np.logical_and(bool_time_pedal, bool_data_pedal)

                p = bool_time_data[bool_time_data == True].first_valid_index()
                if p is None:
                    return p

        elif time_type == 'Start':
            p = find_delta_time_pd('Min', time_pedal, data_pedal, time_start, 0.5)

    elif pedal_status in ['Part Back Out', 'Reducing']:
        # Reduction above zero
        if time_type == 'End':
            p = None
        elif time_type == 'Start':
            p = find_delta_time_pd('Min', time_pedal, data_pedal, time_start, 0.5)

    else:
        p = None

    if p is None:
        return t

    # Time of threshold
    t = time_pedal.loc[p]
    return t

def find_status_time_np(pedal_type: str, time_type: str, time_pedal: List[float],
                          data_pedal: List[int], pedal_status: str, time_start: float,
                          t_seat_rail_acc_filter: List[float], seat_rail_acc_filter: List[float]):
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
    time_pedal = np.array(time_pedal)
    data_pedal = np.array(data_pedal)

    time_pedal_pd_sr = pd.Series(time_pedal)
    data_pedal_pd_sr = pd.Series(data_pedal)

    t_seat_rail_acc_filter = np.array(t_seat_rail_acc_filter)
    seat_rail_acc_filter = np.array(seat_rail_acc_filter)

    if pedal_type == 'Pedal':
        tolerance = 0.1
    elif pedal_type == 'Brake':
        tolerance = 0.1

    # Initialise
    t = None
    p = None

    # Abort if no data
    if pedal_status == "" or len(time_pedal) == 0 or len(data_pedal) == 0 or time_start is None:
        return t


    # Find when tolerance is met

    if pedal_status in ['Zero Step In', 'Applying']:
        if time_type == 'End':
            # p = find(time_pedal >= time_start and data_pedal >= tolerance, 1, 'first')
            bool_time_pedal = time_pedal >= time_start
            bool_data_pedal = data_pedal >= tolerance
            bool_time_data = np.logical_and(bool_time_pedal, bool_data_pedal)
            if True not in bool_time_data:
                return t
            # get the required index from first
            _, k = find_last_n_trues(bool_time_data, 1)
            p = len(bool_time_data) - k
        elif time_type == 'Start':
            p = find_delta_time_np('Max', time_pedal, data_pedal, time_start, 0.5)

    elif pedal_status in ['Lift Off', 'Releasing']:
        if time_type == 'End':
            if pedal_type == 'Brake':
                # Get seat rail accel at start of event
                accel_T0 = 0
                # accel_T0 = seatRailAccelFilter(helpers.sqt.timeEqual(tSeatRailAccelFilter,T0));

                # findBrakeRelease
                T0 = 0
                bool_time_pedal = time_pedal >= time_start
                bool_data_pedal = (seat_rail_acc_filter - accel_T0) >= tolerance
                bool_time_data = np.logical_and(bool_time_pedal, bool_data_pedal)
                if True not in bool_time_data:
                    return t
                # get the required index from first
                _, k = find_last_n_trues(bool_time_data, 1)
                p = len(bool_time_data) - k
            elif pedal_type == 'Pedal':
                bool_time_pedal = time_pedal >= time_start
                bool_data_pedal = data_pedal >= tolerance
                bool_time_data = np.logical_and(bool_time_pedal, bool_data_pedal)
                if True not in bool_time_data:
                    return t
                # get the required index from first
                _, k = find_last_n_trues(bool_time_data, 1)
                p = len(bool_time_data) - k
        elif time_type == 'Start':
            p = find_delta_time_np('Min', time_pedal, data_pedal, time_start, 0.5)
            #p = find_delta_time_pd('Min', time_pedal_pd_sr, data_pedal_pd_sr, time_start, 0.5)

    elif pedal_status in ['Part Back Out', 'Reducing']:
        # Reduction above zero
        if time_type == 'End':
            p = None
        elif time_type == 'Start':
            p = find_delta_time_np('Min', time_pedal, data_pedal, time_start, 0.5)

    else:
        p = None

    if p is None:
        return t

    # Time of threshold
    t = time_pedal[p]
    return t

def find_delta_time_pd(type_: str, time_pedal: pd.Series,
                         data_pedal: pd.Series, time_start: float, tolerance: float):

    p = None
    bool_evt = time_pedal >= time_start

    if bool_evt.any() == False:
        return p

    data_evt = data_pedal.loc[bool_evt]
    time_evt = time_pedal.loc[bool_evt]

    # find the signal difference
    delta_data_evt = data_evt.diff()
    #delta_data_evt = delta_data_evt.append(pd.Series(0), ignore_index=True)

    # find the zero entries
    bool_zero = delta_data_evt == 0

    # Use non zero data only
    delta_data_valid = delta_data_evt.loc[~bool_zero]
    time_valid = time_evt.loc[~bool_zero]

    # Find the min/max positions
    if type_ == 'Min':
        peak = delta_data_valid.min()
    elif type_ == 'Max':
        peak = delta_data_valid.max()

    kPeak = delta_data_valid[delta_data_valid == peak].index[0]
    #kPeak = delta_data_valid.loc[kPeak]

    # Time of the min/max
    tPeak = time_valid[kPeak]

    # Delta tolerance to search for
    limit = peak * tolerance

    bool_time_valid = time_valid < tPeak
    if type_ == 'Min':
        bool_delta_data_valid = delta_data_valid >= limit
    elif type_ == 'Max':
        bool_delta_data_valid = delta_data_valid <= limit

    bool_time_delta = np.logical_and(bool_time_valid, bool_delta_data_valid)

    k = bool_time_delta[bool_time_delta==True].last_valid_index()
    if k is None:
        return p

    # Get the time from the filtered data
    t = time_valid.loc[k]

    # Find the postion in the original time series
    bool_time_pedal = time_pedal >= t
    p = bool_time_pedal[bool_time_pedal == True].last_valid_index()

    return p

def find_delta_time_np(type_: str, time_pedal: List[float],
                         data_pedal: List[int], time_start: float, tolerance: float):
    time_pedal = np.array(time_pedal)
    data_pedal = np.array(data_pedal)

    p = None
    bool_evt = time_pedal >= time_start

    if True not in bool_evt:
        return p

    data_evt = np.array(data_pedal)[bool_evt]
    time_evt = np.array(time_pedal)[bool_evt]

    # find the signal difference
    delta_data_evt = np.diff(data_evt)
    delta_data_evt = np.append(delta_data_evt, 0)

    # find the zero entries
    bool_zero = delta_data_evt == 0

    # Use non zero data only
    delta_data_valid = np.array(delta_data_evt)[~bool_zero]
    time_valid = np.array(time_evt)[~bool_zero]

    # Find the min/max positions
    if type_ == 'Min':
        kPeak = np.argmin(delta_data_valid)
    elif type_ == 'Max':
        kPeak = np.argmax(delta_data_valid)
    peak = delta_data_valid[kPeak]

    # Time of the min/max
    tPeak = time_valid[kPeak]

    # Delta tolerance to search for
    limit = peak * tolerance

    bool_time_valid = time_valid < tPeak
    if type_ == 'Min':
        bool_delta_data_valid = delta_data_valid >= limit
    elif type_ == 'Max':
        bool_delta_data_valid = delta_data_valid <= limit

    bool_time_delta = np.logical_and(bool_time_valid, bool_delta_data_valid)
    if True not in bool_time_delta:
        return p
    _, k = find_last_n_trues(bool_time_delta, 1)

    # Get the time from the filtered data
    t = time_valid[k]

    # Find the postion in the original time series
    bool_time_pedal = time_pedal >= t
    if True not in bool_time_delta:
        return p
    _, p = find_last_n_trues(bool_time_pedal, 1)

    return p


def find_last_n_trues(bools, last_n_trues):
    result = bools[:]
    count = 0
    for i in range(len(bools) - 1, -1, -1):
        if count < last_n_trues:
            if result[i]:
                count += 1
        else:
            result[i] = False

    index = None
    if (len(result)):
        arr = np.where(result == True)
        if(len(arr[0])):
            index = arr[0][0]

    return result, index


def find_delta_time_ver2(type_: str, time_pedal: List[float],
                         data_pedal: List[int], time_start: float, tolerance: float):
    p = []
    # i_evt = time_pedal >= time_start
    bool_evt = [True if value >= time_start else False for value in time_pedal]
    # expectation i_evt holds values or booleans based on above condition

    if not True in bool_evt:
        return

    data_evt = [value for value, evt in zip(data_pedal, bool_evt) if evt == True]
    time_evt = [value for value, evt in zip(time_pedal, bool_evt) if evt == True]

    # find the signal difference
    # diff(data_evt)
    # need to check this delta = [diff(dataEvt);0];
    delta_data_evt = [value2 - value1 for value1, value2 in zip(data_evt[0::], data_evt[1::])]

    # find the zero entries
    # iZero = delta == 0;
    bool_zero = [True if value == 0 else False for value in delta_data_evt]

    # Use non zero data only
    # deltaValid = delta_data_evt(~iZero);
    # timeValid = time_evt(~iZero);
    delta_data_valid = [value for value, evt in zip(delta_data_evt, bool_zero) if evt == False]
    time_valid = [value for value, evt in zip(time_evt, bool_zero) if evt == False]

    # Find the min/max positions
    if type_ == 'Min':
        # [peak,kPeak] = min(deltaValid)
        # peak is the min value and kPeak is index f min value
        peak = min(delta_data_valid)  # value
        kPeak = delta_data_valid.index(peak)  # index
    elif type_ == 'Max':
        peak = max(delta_data_valid)  # value
        kPeak = delta_data_valid.index(peak)  # index

    # if kPeak == 0:
    # return

    # Time of the min/max
    tPeak = time_valid[kPeak]

    # Delta tolerance to search for
    limit = peak * tolerance

    if type_ == 'Min':
        # k = find(timeValid < tPeak & deltaValid >= limit,1,'last')
        # timeValid < tPeak
        bool_time_valid = [True if value < tPeak else False for value in time_valid]
        # deltaValid <= limit
        bool_delta_data_valid = [True if value >= limit else False for value in delta_data_valid]
        # timeValid < tPeak & deltaValid >= limit
        bool_time_delta = [value1 and value2 for value1, value2 in zip(bool_time_valid, bool_delta_data_valid)]
        # find index of non zero from last
        k = [value for value in bool_time_delta if value == True][-1]

    elif type_ == 'Max':
        # k = find(timeValid < tPeak & deltaValid <= limit,1,'last');
        # timeValid < tPeak
        bool_time_valid = [True if value < tPeak else False for value in time_valid]
        # deltaValid <= limit
        bool_delta_data_valid = [True if value <= limit else False for value in delta_data_valid]
        # timeValid < tPeak & deltaValid <= limit
        bool_time_delta = [value1 and value2 for value1, value2 in zip(bool_time_valid, bool_delta_data_valid)]
        # find index of non zero from last
        k = [value for value in bool_time_delta if value == True][-1]

    # Get the time from the filtered data
    t = time_valid[k]

    # Find the postion in the original time series
    # p = find(time >= t,1,'first');
    bool_time_pedal = [True if value >= t else False for value in time_pedal]

    # Find the postion in the original time series
    p = 0
    for value in bool_time_pedal:
        if value == True:
            break
        p = p + 1

    return p
