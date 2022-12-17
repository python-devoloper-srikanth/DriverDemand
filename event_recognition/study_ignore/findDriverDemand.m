function [t,type,status] = findDriverDemand(endType,timeType,tBrake,brake,brakeStatus,tAccPed,accPed,pedalStatus,tStart,tSeatRailAccelFilter,seatRailAccelFilter)

% A more generic version of #1
% Need to recode other areas if used to replace #1
% Only has increase/reduction to zero implemented

% endType = find either the first or last driver demand
% timeType = find either the start time or the end time of the change

% Initialise
t = [];
type = [];
status = [];

% Brake conditions
Tbrake = findStatusTime('Brake',timeType,brakeStatus,tBrake,brake,tStart,tSeatRailAccelFilter,seatRailAccelFilter);

% Pedal conditions
Tpedal = findStatusTime('Pedal',timeType,pedalStatus,tAccPed,accPed,tStart,tSeatRailAccelFilter,seatRailAccelFilter);

% No conditions
if isempty(Tbrake) && isempty(Tpedal)
    return
end

% Both conditions 
if ~isempty(Tbrake) && ~isempty(Tpedal)
    switch endType
        case 'Last'
            % Use the last action
            if Tbrake > Tpedal
                type = 'Brake';
            else
                type = 'Pedal';
            end
        case 'First'
            % Use the first action
            if Tbrake < Tpedal
                type = 'Brake';
            else
                type = 'Pedal';
            end
    end
end

% Brake only
if ~isempty(Tbrake) && isempty(Tpedal)
    type = 'Brake';
end

% Pedal only
if isempty(Tbrake) && ~isempty(Tpedal)
    type = 'Pedal';
end

switch type
    case 'Brake'
        t = Tbrake;
        status = brakeStatus;
    case 'Pedal'
        t = Tpedal;
        status = pedalStatus;
end


function t = findStatusTime(pedalType,timeType,pedalStatus,time,data,tStart,tSeatRailAccelFilter,seatRailAccelFilter)
% Find where the data starts to increase above tolerance value

switch pedalType
    
    case 'Brake'
        tol = 0.1;
    case 'Pedal'
        tol = 0.1;
end

% Initialise
t = [];

% Abort if no data
if isempty(pedalStatus) || isempty(time) || isempty(data) || isempty(tStart)
    return
end

% Find when tolerance is met
switch pedalStatus
    
    case {'Zero Step In','Applying'} 
        
        % Increase from zero
        switch timeType
            
            case 'End'
                
                p = find(time >= tStart & data >= tol,1,'first');
                
            case 'Start'
                
                p = findDeltaTime('Max',time,data,tStart,0.5);
                
        end
        
    case {'Step In','Increasing'}
        
        % Increase from above zero
        switch timeType
            
            case 'End'
                
                p = [];
                
            case 'Start'
                
                p = findDeltaTime('Max',time,data,tStart,0.5);
                
        end
        
    case {'Lift Off','Releasing'}
        
        % Reduction to zero
        switch timeType
            
            case 'End'
                
                switch pedalType
                    
                    case 'Brake'
                        
                        % Get seat rail accel at start of event
                        accel_T0 = seatRailAccelFilter(helpers.sqt.timeEqual(tSeatRailAccelFilter,T0));
                        
                        % findBrakeRelease
                        p = find((tBrake >= T0 & (seatRailAccelFilter - accel_T0) >= tol), 1 ,'first');
                        
                    case 'Pedal'
                        
                        p = find(time >= tStart & data <= tol,1,'first');
                        
                end
                
            case 'Start'
                
                p = findDeltaTime('Min',time,data,tStart,0.5);
                
        end
        
    case {'Part Back Out','Reducing'}
        
        % Reduction above zero
        switch timeType
            
            case 'End'
                
                p = [];
                
            case 'Start'
                
                p = findDeltaTime('Min',time,data,tStart,0.5);
                
        end
        
    otherwise
        
        p = [];
        
end

if isempty(p)
    return
end

% Time of threshold
t = time(p);


function p = findDeltaTime(type,time,data,tStart,tol)

% Initialise
p = [];

iEvt = time >= tStart;

if ~any(iEvt)
    return
end

dataEvt = data(iEvt);
timeEvt = time(iEvt);

% Find the signal difference
delta = [diff(dataEvt);0];

% Find the zero entries
iZero = delta == 0;

% Use non zero data only
deltaValid = delta(~iZero);
timeValid = timeEvt(~iZero);

% Find the min/max positions
switch type
    case 'Min'
        [peak,kPeak] = min(deltaValid);
    case 'Max'
        [peak,kPeak] = max(deltaValid);
end

if isempty(kPeak)
    return
end

% Time of the min/max
tPeak = timeValid(kPeak);

% Delta tolerance to search for
limit = peak*tol;

% Find the position
switch type
    case 'Min'
        k = find(timeValid < tPeak & deltaValid >= limit,1,'last');
    case 'Max'
        k = find(timeValid < tPeak & deltaValid <= limit,1,'last');
end

if isempty(k)
    return
end

% Get the time from the filtered data
t = timeValid(k);

% Find the postion in the original time series
p = find(time >= t,1,'first');


