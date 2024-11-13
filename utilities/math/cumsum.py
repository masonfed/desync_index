import numpy as np

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
