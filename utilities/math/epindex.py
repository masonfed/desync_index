import numpy as np


def get_epindex(statistics_per_channel: np.ndarray,
                cumulative_sums_per_channel: np.ndarray,
                time_windows: np.ndarray,
                window_shift: float,
                epindex_threshold: float,
                epindex_decay: float,
                epindex_tonicity: float,
                seizure_onset: float,
                detection_size: int = 15):
    
    if epindex_threshold == 'adaptive':
        epindex_threshold = 0.5
        adaptive = True
    else:
        adaptive = False
    
    channel_number = len(cumulative_sums_per_channel)
    channel_indexes = np.arange(channel_number)
    
    if epindex_tonicity == 0:
        
        window_epindex_tonicity = None
        
    else:
        
        window_epindex_tonicity = int(epindex_tonicity / window_shift)
    
    detection_times_per_channel = [[None] for _ in channel_indexes]
    alarm_times_per_channel = [[None] for _ in channel_indexes]    
    epindex_alarms_per_channel = [[None] for _ in channel_indexes]
    epindex_tonicities_per_channel = [[None] for _ in channel_indexes]
    epindex_delays_per_channel = [[None] for _ in channel_indexes]
    epindex_values_per_channel = [[0] for _ in channel_indexes]
    
    positive_epindex_threshold = epindex_threshold * np.max(cumulative_sums_per_channel)
    
    for channel_index in channel_indexes:
                
        cumulative_sums = cumulative_sums_per_channel[channel_index]
        
        window_detection_time = 0
        detection_time = time_windows[0]
        
        for window_alarm_time, alarm_time in enumerate(time_windows):
            
            if cumulative_sums[window_alarm_time] > positive_epindex_threshold:
                    
                if window_epindex_tonicity is None:

                    tonicity = np.sum(statistics_per_channel[channel_index, window_detection_time:window_alarm_time]) / (window_alarm_time - window_detection_time)
                
                else:
                    
                    tonicity = np.sum(statistics_per_channel[channel_index, window_alarm_time - window_epindex_tonicity:window_alarm_time])

                delay = alarm_time + epindex_decay - seizure_onset
                
                epindex_value = tonicity / delay

                if epindex_value > epindex_values_per_channel[channel_index][-1]:
                
                    alarm_times_per_channel[channel_index][-1] = alarm_time
                    detection_times_per_channel[channel_index][-1] = detection_time
                    epindex_alarms_per_channel[channel_index][-1] = cumulative_sums[window_alarm_time]
                    epindex_tonicities_per_channel[channel_index][-1] = tonicity
                    epindex_delays_per_channel[channel_index][-1] = delay
                    epindex_values_per_channel[channel_index][-1] = epindex_value
                
            elif cumulative_sums[window_alarm_time] == 0:
                
                window_detection_time = window_alarm_time
                detection_time = alarm_time
                
                if alarm_times_per_channel[channel_index][-1] is not None:
                
                    alarm_times_per_channel[channel_index].append(None)
                    detection_times_per_channel[channel_index].append(None)
                    epindex_alarms_per_channel[channel_index].append(None)
                    epindex_tonicities_per_channel[channel_index].append(None)
                    epindex_delays_per_channel[channel_index].append(None)
                    epindex_values_per_channel[channel_index].append(0)
                
    for channel_index in channel_indexes:
        
        if alarm_times_per_channel[channel_index][-1] is None:
            
            del alarm_times_per_channel[channel_index][-1]
            del detection_times_per_channel[channel_index][-1]
            del epindex_alarms_per_channel[channel_index][-1]
            del epindex_tonicities_per_channel[channel_index][-1]
            del epindex_delays_per_channel[channel_index][-1]
            del epindex_values_per_channel[channel_index][-1]
            
    epindex_num = len([x for x in epindex_values_per_channel if len(x) > 0 and [y > 0 for y in x]])
    
    epindex_threshold_max = 1.0
    epindex_threshold_min = 0.0
    
    while adaptive and epindex_num != detection_size and epindex_threshold_max > epindex_threshold_min + 0.00001:
            
        if epindex_num > detection_size:
                
            epindex_threshold_min = epindex_threshold
            epindex_threshold = (epindex_threshold_max + epindex_threshold_min) / 2
            
        else:
            
            epindex_threshold_max = epindex_threshold
            epindex_threshold = (epindex_threshold_max + epindex_threshold_min) / 2
            
        detection_times_per_channel, alarm_times_per_channel,\
        epindex_alarms_per_channel, epindex_tonicities_per_channel,\
            epindex_delays_per_channel, epindex_values_per_channel,\
                positive_epindex_threshold, epindex_num =\
                    get_epindex(statistics_per_channel,
                                cumulative_sums_per_channel,
                                time_windows,
                                window_shift,
                                epindex_threshold,
                                epindex_decay,
                                epindex_tonicity,
                                seizure_onset)
        
    return detection_times_per_channel, alarm_times_per_channel,\
        epindex_alarms_per_channel, epindex_tonicities_per_channel,\
            epindex_delays_per_channel, epindex_values_per_channel,\
                positive_epindex_threshold, epindex_num