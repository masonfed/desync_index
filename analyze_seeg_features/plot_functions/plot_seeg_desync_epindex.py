from analyze_seeg_features.folder_management import *
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.general import get_plot_labels, get_plot_colors
from utilities.plot.signal import plot_signal_channels
from utilities.signal.time import get_times, get_window_times
from utilities.plot.epindex import plot_cumulative_sums, plot_epindex_statistics
import matplotlib.pyplot as plt
import numpy as np


def plot_seeg_desync_epindex(connection_folder: str,
                             connection_alarm_folder: str,
                             epindex_folder: str,
                             patient: str,
                             work_signal: list,
                             work_channels: list,
                             sampling_frequency: int,
                             epindex_start: float,
                             epindex_base: float,
                             time_start: float,
                             time_duration: float,      
                             max_plot_num: int,
                             plot_montage: str,
                             anonymous_data = False):
    
    time_windows = np.load(connection_folder + 'time_windows.npz')['data']

    input_connection_alarms_per_channel = np.load(connection_alarm_folder + 'input_connection_alarms_per_node.npz')['data']  

    cumsum_time_windows = np.load(epindex_folder + 'time_windows.npz')['data']    
    cumulative_sums_per_channel = np.load(epindex_folder + 'cumulative_sums_per_channel.npz')['data']    
    alarm_threshold = np.load(epindex_folder + 'epindex_threshold.npz', allow_pickle=True)['data']   
    alarm_times_per_channel = np.load(epindex_folder + 'alarm_times_per_channel.npz', allow_pickle=True)['data']   
    detection_times_per_channel = np.load(epindex_folder + 'detection_times_per_channel.npz', allow_pickle=True)['data']    
    epindex_alarms_per_channel = np.load(epindex_folder + 'epindex_alarms_per_channel.npz', allow_pickle=True)['data'] 
    epindex_tonicities_per_channel = np.load(epindex_folder + 'epindex_tonicities_per_channel.npz', allow_pickle=True)['data']
    epindex_delays_per_channel = np.load(epindex_folder + 'epindex_delays_per_channel.npz', allow_pickle=True)['data']
    epindex_values_per_channel = np.load(epindex_folder + 'epindex_values_per_channel.npz', allow_pickle=True)['data']
    
    times, time_windows, window_time_start, window_time_end, work_signal =\
        get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
        
    bipolar_signal, _ =\
        get_seeg_bipolar_channels(work_signal, work_channels)
    
    cumsum_window_time_start, cumsum_window_time_end, cumsum_time_windows =\
        get_window_times(time_start, time_duration, cumsum_time_windows)
    
    channel_num = len(detection_times_per_channel)
    epileptogenic_channel_num = 0
    
    for channel_index in range(channel_num):
        
        alarm_times = []
        detection_times = []
        epindex_alarms = []
        epindex_tonicities = []
        epindex_delays = []
        epindex_values = []
        
        epileptogenic_channel = False
        
        for alarm_time, detection_time, epindex_alarm, epindex_tonicity, epindex_delay, epindex_value in\
            zip(alarm_times_per_channel[channel_index], detection_times_per_channel[channel_index], epindex_alarms_per_channel[channel_index], epindex_tonicities_per_channel[channel_index], epindex_delays_per_channel[channel_index], epindex_values_per_channel[channel_index]):
        
            if detection_time >= time_start and (time_duration is None or detection_time <= time_start + time_duration):
                
                epileptogenic_channel = True
                
                alarm_times.append(alarm_time - epindex_base)
                detection_times.append(detection_time - epindex_base)
                epindex_alarms.append(epindex_alarm)
                epindex_tonicities.append(epindex_tonicity)
                epindex_delays.append(epindex_delay)
                epindex_values.append(epindex_value)
                
        if epileptogenic_channel:
            
            epileptogenic_channel_num += 1
            
        else:
            
            alarm_times.append(0)
            detection_times.append(0)
            epindex_alarms.append(0)
            epindex_tonicities.append(0)
            epindex_delays.append(time_duration)
            epindex_values.append(0)
        
        alarm_times_per_channel[channel_index] = alarm_times     
        detection_times_per_channel[channel_index] = detection_times
        epindex_alarms_per_channel[channel_index] = epindex_alarms
        epindex_tonicities_per_channel[channel_index] = epindex_tonicities
        epindex_delays_per_channel[channel_index] = epindex_delays
        epindex_values_per_channel[channel_index] = epindex_values
    
    if anonymous_data:  
        work_channels = np.arange(len(work_channels))
    else:
        work_channels = np.asarray(work_channels)
        
    if max_plot_num > epileptogenic_channel_num:
        max_plot_num = epileptogenic_channel_num       

    if plot_montage is None:
        
        value_per_channel = [np.max(epindex_values) for epindex_values in epindex_values_per_channel]
        
        plot_channels, plot_channel_indexes =\
            get_plot_labels(work_channels, value_per_channel, max_plot_num)
        
    else:
        
        plot_channels = get_channels(patient, plot_montage)        
        plot_channels = [channel for channel in plot_channels if channel in work_channels]
        plot_channel_indexes = [list(work_channels).index(channel) for channel in plot_channels]
    
    plot_channel_num = len(plot_channels)    
    color_per_channel = get_plot_colors(plot_channel_num)

    plot_signal_channels(times - epindex_base,
                         work_channels[plot_channel_indexes],
                         bipolar_signal[plot_channel_indexes],
                         alarm_times_per_channel[plot_channel_indexes],
                         detection_times_per_channel[plot_channel_indexes],
                         vlines=[epindex_start - epindex_base, 0],
                         vline_labels=['t$_\mathrm{base}$','t$_\mathrm{start}$'],                         
                         vline_colors=['cyan', 'lime'])
    
    plot_cumulative_sums(plot_channels,
                         time_windows - epindex_base,
                         cumsum_time_windows - epindex_base,
                         input_connection_alarms_per_channel[plot_channel_indexes, window_time_start:window_time_end],
                         cumulative_sums_per_channel[plot_channel_indexes, cumsum_window_time_start:cumsum_window_time_end],
                         [alarm_times_per_channel[index] for index in plot_channel_indexes],
                         [detection_times_per_channel[index] for index in plot_channel_indexes],
                         color_per_channel,
                         'D$_\mathrm{x}$',
                         alarm_threshold=alarm_threshold,
                         epindex_targets=[epindex_start - epindex_base, 0],
                         epindex_target_colors=['cyan', 'lime'],
                         epindex_target_labels=['t$_\mathrm{base}$','t$_\mathrm{start}$'])
    
    plot_epindex_statistics(plot_channels,
                            epindex_alarms_per_channel[plot_channel_indexes],
                            epindex_tonicities_per_channel[plot_channel_indexes],
                            epindex_delays_per_channel[plot_channel_indexes],
                            epindex_values_per_channel[plot_channel_indexes],
                            color_per_channel,
                            'Desynchronization Index',
                            alarm_threshold,
                            patient=patient)
    
    print('Plotting...')
        
    plt.show()