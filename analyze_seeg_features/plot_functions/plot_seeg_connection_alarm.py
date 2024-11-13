from analyze_seeg_features.folder_management import *
from utilities.plot.matrix import plot_matrix
from utilities.plot.series import plot_series
from utilities.signal.time import get_times
from utilities.plot.signal import plot_signal_channels
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.general import get_plot_labels
import matplotlib.pyplot as plt
import numpy as np


def plot_seeg_connection_alarm(connection_folder: str,
                               connection_alarm_folder: str,
                               patient: str,
                               work_signal: list,
                               work_channels: list,
                               sampling_frequency: int,
                               time_start: float,
                               time_duration: float,
                               max_plot_num: int,
                               plot_montage: str = None):
    
    time_windows = np.load(connection_folder + 'time_windows.npz')['data']
    
    times, time_windows, window_time_start, window_time_end, work_signal =\
        get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
        
    input_connections_per_node = np.load(connection_alarm_folder + 'smoothed_input_connections_per_node.npz')['data']
    output_connections_per_node = np.load(connection_alarm_folder + 'smoothed_output_connections_per_node.npz')['data']
    smoothed_median_connections = np.load(connection_alarm_folder + 'smoothed_median_connections.npz')['data']
    
    input_connection_alarms_per_node = np.load(connection_alarm_folder + 'input_connection_alarms_per_node.npz')['data']
    output_connection_alarms_per_node = np.load(connection_alarm_folder + 'output_connection_alarms_per_node.npz')['data']
    
    node_num = len(input_connections_per_node)
    
    if plot_montage is None:
        
        channel_values = []
        
        for channel_index in range(node_num):
            
            channel_values.append(np.max(np.abs(input_connection_alarms_per_node[channel_index, window_time_start:window_time_end])))
            
        plot_channels, plot_channel_indexes =\
            get_plot_labels(work_channels, channel_values, max_plot_num)
        
    else:
        
        plot_channels = get_channels(patient, plot_montage)        
        plot_channels = [channel for channel in plot_channels if channel in work_channels]
        plot_channel_indexes = [work_channels.index(channel) for channel in plot_channels]
        
    bipolar_signal, bipolar_channels =\
        get_seeg_bipolar_channels(work_signal, work_channels)

    plot_signal_channels(times,
                         bipolar_channels[plot_channel_indexes],
                         bipolar_signal[plot_channel_indexes])
    
    plot_matrix(np.asarray(input_connections_per_node)[plot_channel_indexes, window_time_start:window_time_end],
                time_windows,
                plot_channels,
                'Input connection',
                'Time [s]',
                'Channel')
    
    plot_matrix(np.asarray(output_connections_per_node)[plot_channel_indexes, window_time_start:window_time_end],
                time_windows,
                plot_channels,
                'Output connection',
                'Time [s]',
                'Channel')
    
    plot_series(time_windows,
                smoothed_median_connections[window_time_start:window_time_end],
                'Median connection value',
                sample_size=1)
        
    plot_matrix(np.asarray(input_connection_alarms_per_node)[plot_channel_indexes, window_time_start:window_time_end],
                time_windows,
                plot_channels,
                'Desynchronization level',
                'Time [s]',
                'Channel')
    
    plot_matrix(np.asarray(output_connection_alarms_per_node)[plot_channel_indexes, window_time_start:window_time_end],
                time_windows,
                plot_channels,
                'Synchronization level',
                'Time [s]',
                'Channel')
    
    plt.show()   
