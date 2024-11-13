from analyze_seeg_features.folder_management import *
from utilities.signal.time import get_times
from utilities.signal.channels import get_channels
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.signal import plot_signal_channels
from utilities.plot.violins import plot_violins, plot_grouped_violins
from utilities.plot.channels import plot_grouped_violins_per_channel
from utilities.plot.general import *
import matplotlib.pyplot as plt
import numpy as np



def multi_plot_seeg_graph(multi_legend: list,
                          multi_group: list,
                          multi_patient: list,
                          multi_work_signal: list,
                          multi_work_channels: list,
                          multi_sampling_frequency: list,
                          multi_connection_folder: list,
                          multi_graph_folder: list,
                          multi_time_start: list,
                          multi_time_duration: list,
                          unique_signal: bool,
                          max_plot_num: int,
                          plot_montage: str):
        
    multi_plot_channels = []
    multi_color_per_channel = []
    multi_time_windows = []
    multi_in_degrees_per_channel = []
    multi_out_degrees_per_channel = []
    multi_betweeness_centralities_per_channel = []      
    multi_eigenvector_centralities_per_channel = []
    multi_eccentricities_per_channel = []
    multi_eccentricity_in_degree_ratios_per_channel = []
    multi_diameters = []
    
    multi_times = []
    
    for legend, patient, work_channels, connection_folder, graph_folder, time_start, time_duration, sampling_frequency, work_signal in\
        zip(multi_legend, multi_patient, multi_work_channels, multi_connection_folder, multi_graph_folder, multi_time_start,\
            multi_time_duration, multi_sampling_frequency, multi_work_signal):

        time_windows = np.load(connection_folder + 'time_windows.npz')['data']
        
        times, time_windows, window_time_start, window_time_end, work_signal =\
            get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
                    
        multi_time_windows.append(time_windows)        
        multi_times.append(times)        
        
        in_degrees_per_channel = np.load(graph_folder + 'connection_in_degrees_per_node.npz')['data'][:, window_time_start:window_time_end]
        out_degrees_per_channel = np.load(graph_folder + 'connection_out_degrees_per_node.npz')['data'][:, window_time_start:window_time_end]
        betweeness_centralities_per_channel = np.load(graph_folder + 'connection_betweeness_centralities_per_node.npz')['data'][:, window_time_start:window_time_end]
        eigenvector_centralities_per_channel = np.load(graph_folder + 'connection_eigenvector_centralities_per_node.npz')['data'][:, window_time_start:window_time_end]
        eccentricities_per_channel = np.load(graph_folder + 'connection_eccentricities_per_node.npz')['data'][:, window_time_start:window_time_end]
        in_degrees_per_channel[in_degrees_per_channel < 0.1] = 0.1
        eccentricity_in_degree_ratios_per_channel = eccentricities_per_channel / in_degrees_per_channel
        diameters = np.load(graph_folder + 'connection_diameters.npz')['data'][window_time_start:window_time_end]
    
        multi_in_degrees_per_channel.append(in_degrees_per_channel)
        multi_out_degrees_per_channel.append(out_degrees_per_channel)
        multi_betweeness_centralities_per_channel.append(betweeness_centralities_per_channel)
        multi_eigenvector_centralities_per_channel.append(eigenvector_centralities_per_channel)
        multi_eccentricities_per_channel.append(eccentricities_per_channel)
        multi_eccentricity_in_degree_ratios_per_channel.append(eccentricity_in_degree_ratios_per_channel)    
        multi_diameters.append(diameters)
        
        if plot_montage is None:
            value_per_channel = [np.abs(np.mean(out_degrees_per_channel[i])- np.mean(out_degrees_per_channel)) for i in range(len(out_degrees_per_channel))]
            plot_channels, _ = get_plot_labels(work_channels, value_per_channel, max_plot_num)                
        else:
            plot_channels = get_channels(patient, plot_montage)
        
        plot_channel_num = len(plot_channels)
        multi_plot_channels.append(plot_channels)
        multi_color_per_channel.append(get_plot_colors(plot_channel_num))
    
    if unique_signal:
        
        bipolar_signal, _ = get_seeg_bipolar_channels(work_signal, work_channels)
        
        plot_signal = [bipolar_signal[work_channels.index(channel)] for channel in plot_channels]
            
        plot_signal_channels(multi_times[0],
                             list(multi_plot_channels[0]),
                             plot_signal)
    
    multi_color = get_plot_colors(len(multi_legend))
    color_per_label = get_plot_colors(len(np.unique(multi_legend)))
    
    unique_legends = []
    
    unique_groups = []
    
    for legend in multi_legend:
        
        if legend not in unique_legends:
        
            unique_legends.append(legend)
            
    for group in multi_group:
        
        if group not in unique_groups:
        
            unique_groups.append(group)
    
    for multi_data_per_channel, ylabel, ylim\
        in zip([multi_out_degrees_per_channel, multi_in_degrees_per_channel, multi_eccentricities_per_channel, multi_eccentricity_in_degree_ratios_per_channel, multi_diameters],
               ['Out-Degree', 'In-Degree', 'Eccentricity', 'Eccentricity-Degree Ratio', 'Diameter'],
               [None, None, None, None, None]):
            
        multi_data = [x.flatten() for x in multi_data_per_channel]

        if multi_group is None:
        
            plot_violins(multi_data,
                         multi_legend,
                         multi_color,
                         ylabel,
                         ylim=ylim)
            
        else:
            
            plot_grouped_violins(multi_data,
                                 multi_legend,
                                 multi_group,
                                 unique_legends,                             
                                 unique_groups,
                                 color_per_label,
                                 ylabel,
                                 ylim=ylim)
            
    multi_multi_data_per_channel = [multi_out_degrees_per_channel, multi_in_degrees_per_channel, multi_eccentricities_per_channel, multi_eccentricity_in_degree_ratios_per_channel]    
    multi_data_ylabel = ['Out-Degree', 'In-Degree', 'Eccentricity', 'Eccentricity-Degree Ratio']
    multi_data_range = [None, None, None, None]
    
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
