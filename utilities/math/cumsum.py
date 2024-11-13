import numpy as np

def get_fusion_cumulative_sums(multi_statistics_per_channel: list,
                               time_windows: np.ndarray,
                               window_shift: float,
                               epindex_base: float,
                               epindex_start: int,
                               epindex_end: float,
                               epindex_bias: float,
                               use_std = True):
    
    window_epindex_base = int(epindex_base / window_shift)
    window_epindex_start = int(epindex_start / window_shift)
    
    if epindex_end is None:
        window_epindex_end = len(time_windows)
    else:
        window_epindex_end = np.argmin(np.abs(time_windows - epindex_end)) + 1
    
    channel_number = len(multi_statistics_per_channel[0])
    
    channel_indexes = np.arange(channel_number)
    
    variable_num = len(multi_statistics_per_channel)
    
    cumulative_sums_per_channel = [[[] for _ in range(variable_num)] for _ in channel_indexes]
        
    for channel_index in channel_indexes:
        
        cumsum = np.zeros(variable_num)
            
        for window_index in range(window_epindex_start, window_epindex_end):
            
            if window_index > window_epindex_base:
                
                for variable_index in range(variable_num):
            
                    statistic_mean = np.mean(multi_statistics_per_channel[variable_index][channel_index, window_epindex_start:window_epindex_base+1])
                
                    if use_std:
                        
                        statistic_std = np.std(multi_statistics_per_channel[variable_index][channel_index, window_epindex_start:window_epindex_base+1])        

                    else:
                        
                        statistic_std = 1
                        
                    deviation = multi_statistics_per_channel[variable_index][channel_index, window_index] / statistic_std - statistic_mean - epindex_bias

                    if deviation >= 0:
                    
                        cumsum[variable_index] += deviation
                        
                    else:
                        
                        cumsum[variable_index] = 0
                    
                    cumulative_sums_per_channel[channel_index][variable_index].append(cumsum[variable_index])
        
            else:
                
                for variable_index in range(variable_num):
                    
                    cumulative_sums_per_channel[channel_index][variable_index].append(0)
        
    cumulative_sums_per_channel = np.asarray([np.asarray(cumulative_sums_per_channel[channel_index]).max(axis=0) for channel_index in range(channel_number)])
            
    return time_windows[window_epindex_start:window_epindex_end], cumulative_sums_per_channel


def get_cumulative_sums(statistics_per_channel: np.ndarray,
                        time_windows: np.ndarray,
                        window_epindex_base: float,
                        window_epindex_start: float,
                        window_epindex_end: float,
                        epindex_bias: float,
                        use_mean: bool = True,
                        use_std: bool = True):
            
    channel_number = len(statistics_per_channel)
    channel_indexes = np.arange(channel_number)
    
    cumulative_sums_per_channel = [[] for _ in channel_indexes]
    
    mean_statistic_per_channel = []
        
    for channel_index in channel_indexes:
        
        cumsum = 0
        
        if use_std:
            statistic_std = np.max((0.001, np.std(statistics_per_channel[channel_index, window_epindex_start:window_epindex_base+1])))
        else:
            statistic_std = 1
            
        if use_mean:
            statistic_mean = np.mean(statistics_per_channel[channel_index, window_epindex_start:window_epindex_base+1])
        else:
            statistic_mean = 0
            
        mean_statistic_per_channel.append(statistic_mean)
            
        for window_index in range(window_epindex_start, window_epindex_end):
            
            if window_index > window_epindex_base:

                deviation = (statistics_per_channel[channel_index, window_index] - statistic_mean) / statistic_std - epindex_bias
                
                if deviation > 0:
                    cumsum = np.max((0, cumsum + deviation))
                else:
                    cumsum = 0
                    
                cumulative_sums_per_channel[channel_index].append(cumsum)
                
            else:
                cumulative_sums_per_channel[channel_index].append(0)
            
    return time_windows[window_epindex_start:window_epindex_end], np.asarray(cumulative_sums_per_channel)


def get_fusion_epindex(cumulative_sums_per_channel: np.ndarray,
                       time_windows: np.ndarray,
                       window_shift: float,
                       epindex_threshold: float,
                       epindex_decay: float,
                       epindex_tonicity: float):
    
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning) 
    
    seizure_onset = time_windows[-1]
    
    channel_number = len(cumulative_sums_per_channel)
    channel_indexes = np.arange(channel_number)
    
    if epindex_tonicity is None:
        
        window_epindex_tonicity = None
    
    else:
    
        window_epindex_tonicity = int(epindex_tonicity / window_shift)
    
    detection_times_per_channel = [[] for _ in channel_indexes]
    alarm_times_per_channel = [[] for _ in channel_indexes]
    
    epindex_alarms_per_channel = [[] for _ in channel_indexes]
    epindex_tonicities_per_channel = [[] for _ in channel_indexes]
    epindex_delays_per_channel = [[] for _ in channel_indexes]
    epindex_values_per_channel = [[] for _ in channel_indexes]
    
    epindex_threshold = epindex_threshold * np.max(cumulative_sums_per_channel)
        
    for channel_index in channel_indexes:
                
        cumulative_sums = cumulative_sums_per_channel[channel_index]
        
        window_detection_time = 0
        detection_time = time_windows[0]
        detect = True
        
        for window_alarm_time, alarm_time in enumerate(time_windows):
            
            if cumulative_sums[window_alarm_time] > epindex_threshold:  
                
                if detect:    
                    
                    if seizure_onset > alarm_time:
                        seizure_onset = alarm_time
                    
                    alarm_times_per_channel[channel_index].append(alarm_time)
                    detection_times_per_channel[channel_index].append(detection_time)
                    detect = False
                    
                    epindex_alarms_per_channel[channel_index].append(np.min(cumulative_sums[window_alarm_time]))
                    
                    if window_epindex_tonicity is None:
                    
                        tonicity = np.sum(cumulative_sums[window_detection_time:window_alarm_time])
                    else:
                        
                        tonicity = np.sum(cumulative_sums[window_alarm_time:window_alarm_time + window_epindex_tonicity])                        
                    
                    epindex_delays_per_channel[channel_index].append(detection_time + epindex_decay)
                    epindex_tonicities_per_channel[channel_index].append(tonicity)
                
                else:
                    
                    try:
                
                        epindex_alarms_per_channel[channel_index][-1] = np.min(cumulative_sums[window_alarm_time])
                        
                    except:
                        
                        pass
                
            elif cumulative_sums[window_alarm_time] * cumulative_sums[window_alarm_time - 1] <= 0:
                
                window_detection_time = window_alarm_time
                detection_time = alarm_time
                detect = True   
                
    for channel_index in channel_indexes:
        
        for index in range(len(epindex_alarms_per_channel[channel_index])):
            
            epindex_delays_per_channel[channel_index][index] -= seizure_onset
            
            tonicity = epindex_tonicities_per_channel[channel_index][index]
      
            epindex_value = tonicity / (epindex_delays_per_channel[channel_index][index] )
            
            epindex_values_per_channel[channel_index].append(epindex_value)
            
        
                
    return detection_times_per_channel, alarm_times_per_channel, epindex_alarms_per_channel, epindex_tonicities_per_channel, epindex_delays_per_channel, epindex_values_per_channel
            
        