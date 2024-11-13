import pathlib
import numpy as np
import pandas as pd
from utilities.math.epindex import get_epindex 
from utilities.math.cumsum import get_cumulative_sums
    
    
def compute_seeg_bartolomei_epindex(energy_folder: str,
                                    bartolomei_epindex_folder: str,
                                    window_shift: float,
                                    epindex_base: float,
                                    epindex_start: float,
                                    epindex_end: float,
                                    epindex_bias: float,
                                    epindex_threshold: float,
                                    epindex_decay: float,
                                    epindex_tonicity: float,
                                    work_channels: list):
    
    pathlib.Path(bartolomei_epindex_folder).mkdir(parents=True, exist_ok=True)
    
    energy_ratios_per_channel = np.load(energy_folder + 'energy_ratios_per_channel.npz')['data']
    time_windows = np.load(energy_folder + 'time_windows.npz')['data']
    
    window_epindex_base = int(epindex_base / window_shift)
    window_epindex_start = int(epindex_start / window_shift)
    
    if epindex_end is None:
        window_epindex_end = len(time_windows)
    else:
        window_epindex_end = np.argmin(np.abs(time_windows - epindex_end)) + 1
        
    print('Computing cumulatives sums...')
    
    cumsum_time_windows, cumulative_sums_per_channel =\
        get_cumulative_sums(energy_ratios_per_channel,
                            time_windows,
                            window_epindex_base,
                            window_epindex_start,
                            window_epindex_end,
                            epindex_bias)
    
    np.savez_compressed(bartolomei_epindex_folder + 'time_windows.npz', data=cumsum_time_windows)   
    np.savez_compressed(bartolomei_epindex_folder + 'cumulative_sums_per_channel.npz', data=cumulative_sums_per_channel)

    print('Computing epileptogenic indexes...')
        
    detection_times_per_channel, alarm_times_per_channel,\
        epindex_alarms_per_channel, epindex_tonicities_per_channel,\
            epindex_delays_per_channel, epindex_values_per_channel,\
                positive_epindex_threshold, _ =\
                    get_epindex(energy_ratios_per_channel[:, window_epindex_start:window_epindex_end],
                                cumulative_sums_per_channel,
                                cumsum_time_windows,
                                window_shift,
                                epindex_threshold,
                                epindex_decay,
                                epindex_tonicity,
                                epindex_base)
            
    np.savez_compressed(bartolomei_epindex_folder + 'epindex_threshold.npz', data=positive_epindex_threshold)                  
    np.savez_compressed(bartolomei_epindex_folder + 'detection_times_per_channel.npz', data=detection_times_per_channel, dtype='object')
    np.savez_compressed(bartolomei_epindex_folder + 'alarm_times_per_channel.npz', data=alarm_times_per_channel, dtype='object')
    np.savez_compressed(bartolomei_epindex_folder + 'epindex_alarms_per_channel.npz', data=epindex_alarms_per_channel, dtype='object')
    np.savez_compressed(bartolomei_epindex_folder + 'epindex_tonicities_per_channel.npz', data=epindex_tonicities_per_channel, dtype='object')
    np.savez_compressed(bartolomei_epindex_folder + 'epindex_delays_per_channel.npz', data=epindex_delays_per_channel, dtype='object')
    np.savez_compressed(bartolomei_epindex_folder + 'epindex_values_per_channel.npz', data=epindex_values_per_channel, dtype='object')
    
    epindex_values = []
    epindex_tonicities = []
    epindex_delays = []
    significative_channels = []
    
    for channel_index in range(len(work_channels)):
        
        if len(epindex_values_per_channel[channel_index]) > 0:
        
            index = np.argmax(epindex_values_per_channel[channel_index])
            
            epindex_values.append(epindex_values_per_channel[channel_index][index])
            epindex_tonicities.append(epindex_tonicities_per_channel[channel_index][index])
            epindex_delays.append(epindex_delays_per_channel[channel_index][index]) 
            significative_channels.append(work_channels[channel_index]) 
            
    max_ei, min_ei = 1, 0
    max_er, min_er = np.max(epindex_tonicities), 0 
    max_delay, min_delay = np.max(epindex_delays), np.min(epindex_delays)
    
    max_radius, min_radius = 12, 5
        
    epindex_values = [x / np.max(epindex_values) for x in epindex_values]
    
    dataframe = pd.DataFrame({'channel': significative_channels,
                              'Bartolomei Index': epindex_values,
                              'Bartolomei Index radius': [ round(min_radius * (x > 0) + x * (max_radius - min_radius) / (max_ei - min_ei), 2) for x in epindex_values],
                              'Energy Ratio': epindex_tonicities,
                              'Energy Ratio radius': [ round(min_radius * (x > 0) + x * (max_radius - min_radius) / (max_er - min_er), 2) for x in epindex_tonicities],
                              'Delay': epindex_delays,
                              'Delay radius': [ round(min_radius * (x < (len(time_windows) * window_shift)) +  (max_delay - x) * (max_radius - min_radius) / (max_delay - min_delay), 2) for x in epindex_delays]})
    
    
    print(bartolomei_epindex_folder)
    
    dataframe.to_excel(bartolomei_epindex_folder + 'bartolomei_epindex_data.xlsx', index=False)
    
    
    