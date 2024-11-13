from analyze_seeg_features.folder_management import *
from utilities.signal.time import get_times
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.series import plot_multi_series
from utilities.plot.violins import plot_grouped_violins, plot_violins
from utilities.plot.signal import plot_signal_channels
from utilities.plot.general import *
import matplotlib.pyplot as plt
import numpy as np


def multi_plot_seeg_connection(multi_legend: list,
                               multi_group: list,
                               multi_patient: list,
                               multi_work_signal: list,
                               multi_work_channels: list,
                               multi_signal_length: list,
                               multi_sampling_frequency: list,
                               multi_connection_folder: list,
                               multi_time_start: list,
                               multi_time_duration: list,
                               unique_signal: bool,
                               max_plot_num: int,
                               plot_montage: str):
        
    multi_plot_channels = []
    multi_color_per_channel = []
    multi_time_windows = []
    
    multi_connections_per_edge = [] 
    multi_lags_per_edge = []
    
    multi_input_connections_per_ez_channel = []
    multi_output_connections_per_ez_channel = []
    
    multi_window_time_start = []
    multi_window_time_end = []
    multi_times = []
    
    unique_legends = []
    unique_groups = []
    
    for legend in multi_legend:
        if legend not in unique_legends:
            unique_legends.append(legend)
    for group in multi_group:
        if group not in unique_groups:
            unique_groups.append(group)
    
    print()
    
    print('Loading...')
    
    for legend, group, patient, work_channels, connection_folder, signal_length, time_start, time_duration, work_signal, sampling_frequency in\
        zip(multi_legend, multi_group, multi_patient, multi_work_channels, multi_connection_folder, multi_signal_length, multi_time_start, multi_time_duration, multi_work_signal, multi_sampling_frequency):

        print('Loading connectivity data from', legend, group)
        
        time_windows = np.load(connection_folder + 'time_windows.npz')['data']
            
        times, time_windows, window_time_start, window_time_end, work_signal =\
            get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal, signal_length)
        
        multi_window_time_start.append(window_time_start)
        multi_window_time_end.append(window_time_end)
            
        multi_time_windows.append(time_windows)        
        multi_times.append(times)
        
        connections_per_edge = np.load(connection_folder +
                                       'connections_per_edge.npz')['data'][:, window_time_start:window_time_end]
        lags_per_edge = np.load(connection_folder +
                                'lags_per_edge.npz')['data'][:, window_time_start:window_time_end]
            
        multi_connections_per_edge.append(connections_per_edge)
        multi_lags_per_edge.append(lags_per_edge)
        
        if plot_montage is None:            
            plot_value_per_channel = [np.abs(np.mean(connections_per_edge[i]) - np.mean(connections_per_edge))
                                      for i in range(len(connections_per_edge))]                     
            plot_channels, _ = get_plot_labels(work_channels, plot_value_per_channel, max_plot_num)  
                     
        else:
            plot_channels = get_channels(patient, plot_montage)
        
        plot_channel_num = len(plot_channels)
        multi_plot_channels.append(plot_channels)
        multi_color_per_channel.append(get_plot_colors(plot_channel_num))
        
        if multi_group is None or len(unique_groups) == 1:
        
            ez_channels = get_channels(patient, 'ez')
            
            input_connections_per_ez_channel = []
            output_connections_per_ez_channel = []
            
            edges = list(np.load(connection_folder + 'edges.npz')['data'])
                
            for edge_index, edge in enumerate(edges):
                
                source_channel, target_channel = edge[0], edge[1]
            
                if source_channel in ez_channels and target_channel not in ez_channels:
                    
                    output_connections_per_ez_channel.append(connections_per_edge[edge_index])
                    
                if target_channel in ez_channels and source_channel not in ez_channels:
                    
                    input_connections_per_ez_channel.append(connections_per_edge[edge_index])
                    
            multi_input_connections_per_ez_channel.append(np.asarray(input_connections_per_ez_channel))
            multi_output_connections_per_ez_channel.append(np.asarray(output_connections_per_ez_channel))
                
    if unique_signal:
        
        bipolar_signal, _ = get_seeg_bipolar_channels(work_signal, work_channels)
        
        plot_signal = [bipolar_signal[work_channels.index(channel)] for channel in plot_channels]
            
        plot_signal_channels(multi_times[0],
                             list(multi_plot_channels[0]),
                             plot_signal)
        
    print('Plotting...')
    
    multi_multi_data_per_channel = [multi_connections_per_edge,
                                    multi_lags_per_edge]
    
    multi_data_ylabel = ['Connection magnitude', 'Connection lag [ms]']
    
    multi_data_range = [[0.8, 1.0], [50, 100]]    
            
    multi_color = get_plot_colors(len(multi_legend))
    color_per_legend = get_plot_colors(len(unique_legends))
    marker_per_legend = get_plot_markers(len(unique_legends))
        
    for multi_data_per_channel, ylabel, ylim in\
        zip(multi_multi_data_per_channel,
            multi_data_ylabel,
            multi_data_range):
            
        multi_data = [np.mean(x, axis=0) for x in\
            multi_data_per_channel]

        if multi_group is None or len(unique_groups) == 1:
        
            plot_violins(multi_data,
                         multi_legend,
                         multi_color,
                         ylabel,
                         ylim)
            
            plot_multi_series(multi_time_windows,
                              multi_data,
                              multi_legend,
                              multi_color,
                              ylabel
                              )
            
        else:

            plot_grouped_violins(multi_data,
                                 multi_legend,
                                 multi_group,
                                 unique_legends,
                                 unique_groups,
                                 color_per_legend,
                                 ylabel,
                                 ylim)
            
    if multi_group is None or len(np.unique(multi_group)) == 1:
        
        new_multi_data = []
        new_multi_legend = []
        new_multi_group = []
        
        for group_index, group in enumerate(multi_legend):
            
            new_multi_data.append(np.mean(multi_connections_per_edge[group_index], axis=0))
            new_multi_data.append(np.mean(multi_input_connections_per_ez_channel[group_index], axis=0))
            new_multi_data.append(np.mean(multi_output_connections_per_ez_channel[group_index], axis=0))
            
            new_multi_group.append(group)
            new_multi_group.append(group)
            new_multi_group.append(group)
            
            new_multi_legend += ['Network', 'EZ inward', 'EZ outward']
                
        new_unique_legends = ['Network', 'EZ inward', 'EZ outward']
        new_unique_groups = unique_legends
        
        color_per_legend = get_plot_colors(len(new_unique_legends))
        
        plot_grouped_violins(new_multi_data,
                             new_multi_legend,
                             new_multi_group,
                             new_unique_legends,
                             new_unique_groups,
                             color_per_legend,
                             'Connection magnitude',
                             [0.5, 1.0])    

    plt.show()
    