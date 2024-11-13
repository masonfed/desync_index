
from analyze_seeg_features.folder_management import *
from utilities.signal.time import get_times
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.violins import plot_grouped_violins, plot_violins
from utilities.plot.channels import plot_grouped_violins_per_channel
from utilities.plot.signal import plot_signal_channels
from utilities.plot.general import *
import matplotlib.pyplot as plt
import numpy as np


def multi_plot_seeg_connection_alarm(multi_legend: list,
                                     multi_group: list,
                                     multi_connection_folder: list,
                                     multi_connection_alarm_folder: list,
                                     multi_patient: list,
                                     multi_work_signal: list,
                                     multi_work_channels: list,
                                     multi_sampling_frequency: list,
                                     multi_window_duration: list,
                                     multi_window_shift: list,
                                     multi_time_start: list,
                                     multi_time_duration: list,
                                     unique_signal: bool,
                                     max_plot_num: int,
                                     plot_montage: str): 
        
    multi_plot_channels = []
    
    multi_time_windows = []
    
    multi_output_connections_per_channel = []
    multi_output_connection_alarms_per_channel = [] 
    multi_input_connections_per_channel = []
    multi_input_connection_alarms_per_channel = []
    
    multi_times = []
    
    for connection_folder, connection_alarm_folder, patient, work_channels, window_duration, window_shift, time_start, time_duration, sampling_frequency, work_signal in\
        zip(multi_connection_folder, multi_connection_alarm_folder, multi_patient, multi_work_channels, multi_window_duration, multi_window_shift, multi_time_start, multi_time_duration, multi_sampling_frequency, multi_work_signal):

        time_windows = np.load(connection_folder + 'time_windows.npz')['data']
    
        times, time_windows, window_time_start, window_time_end, work_signal =\
            get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
        
        multi_time_windows.append(time_windows)        
        multi_times.append(times)
        
        output_connections_per_node = np.load(connection_alarm_folder + 'smoothed_output_connections_per_node.npz')['data'][:, window_time_start:window_time_end]
        output_connection_alarms_per_node = np.load(connection_alarm_folder + 'output_connection_alarms_per_node.npz')['data'][:, window_time_start:window_time_end]

        input_connections_per_node = np.load(connection_alarm_folder + 'smoothed_input_connections_per_node.npz')['data'][:, window_time_start:window_time_end]
        input_connection_alarms_per_node = np.load(connection_alarm_folder + 'input_connection_alarms_per_node.npz')['data'][:, window_time_start:window_time_end]
            
        if plot_montage is None:    
            
            plot_value_per_channel = [np.abs(np.mean(-input_connection_alarms_per_node[i]) - np.mean(-input_connection_alarms_per_node)) for i in range(len(input_connections_per_node))]                  
            plot_channels, _ = get_plot_labels(work_channels, plot_value_per_channel, max_plot_num)
            
        else:
            
            plot_channels = get_channels(patient, plot_montage)
            
        multi_plot_channels.append(plot_channels)
            
        multi_output_connections_per_channel.append(output_connections_per_node)
        multi_output_connection_alarms_per_channel.append(output_connection_alarms_per_node)
        multi_input_connections_per_channel.append(input_connections_per_node)
        multi_input_connection_alarms_per_channel.append(input_connection_alarms_per_node) 
    
    if unique_signal:
        
        bipolar_signal, _ = get_seeg_bipolar_channels(work_signal, work_channels)
        
        plot_signal = [bipolar_signal[work_channels.index(channel)] for channel in plot_channels]
            
        plot_signal_channels(multi_times[0],
                             list(multi_plot_channels[0]),
                             plot_signal)
       
    print('Plotting...')
    
    if multi_group is not None and len(np.unique(multi_group)) > 1:
        
        multi_label = [legend + ', ' + group for legend, group in zip(multi_legend, multi_group)]
        
    else:
        
        multi_label = multi_legend
        
    multi_color = get_plot_colors(len(multi_label))
        
    unique_legends = []
    unique_groups = []
    
    for legend in multi_legend:
        if legend not in unique_legends:
            unique_legends.append(legend)
    for group in multi_group:
        if group not in unique_groups:
            unique_groups.append(group)
            
    color_per_group = get_plot_colors(len(unique_groups))
            
    for multi_data, ylabel\
        in zip([multi_input_connection_alarms_per_channel,
                multi_output_connection_alarms_per_channel],
               ['Desynchronization Level',
                'Synchronization Level']):
                
        if len(unique_groups) > 1:
        
            plot_grouped_violins(multi_data,
                                 multi_legend,
                                 multi_group,
                                 unique_legends,
                                 unique_groups,                            
                                 color_per_group,
                                 ylabel)
        
        else:
            
            plot_violins([x.flatten() for x in multi_data],
                         multi_label,
                         multi_color,
                         ylabel)
            
            plot_violins([np.max(x, axis=0) for x in multi_data],
                         multi_label,
                         multi_color,
                         'Max ' + ylabel)
            
    multi_multi_data_per_channel =[multi_input_connection_alarms_per_channel, multi_output_connection_alarms_per_channel]
    multi_data_ylabel = ['Desynchronization Level', 'Synchronization Level']
    multi_data_range = [[0, 1], [-1, 1]]
            
    plot_grouped_violins_per_channel(plot_montage,
                                     multi_work_channels,
                                     multi_plot_channels,
                                     multi_patient,
                                     multi_multi_data_per_channel,
                                     multi_data_ylabel,
                                     multi_data_range,
                                     multi_legend,
                                     multi_group) 

    plt.show()
    