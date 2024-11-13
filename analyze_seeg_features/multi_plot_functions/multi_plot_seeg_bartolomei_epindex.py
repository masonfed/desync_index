
from analyze_seeg_features.folder_management import *
from utilities.signal.time import get_times
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.general import *
from utilities.plot.bars import plot_grouped_bars
from utilities.plot.signal import plot_signal_channels
from utilities.plot.epindex import plot_cumulative_sums
import matplotlib.pyplot as plt
import numpy as np


def multi_plot_seeg_bartolomei_epindex(multi_legend: list,
                                       multi_group: list,
                                       multi_energy_folder: list,
                                       multi_epindex_folder: list,
                                       multi_patient: list,
                                       multi_work_signal: list,
                                       multi_work_channels: list,
                                       multi_sampling_frequency: list,
                                       multi_window_duration: float,
                                       multi_window_shift: float,
                                       multi_epindex_start: list,
                                       multi_time_start: list,
                                       multi_time_duration: list,
                                       unique_signal: bool,
                                       max_plot_num: int,
                                       plot_montage: str):
        
    multi_plot_channels = []
    multi_color_per_channel = []
    multi_tonicities_per_channel = []
    multi_delays_per_channel = []
    multi_epileptogenic_values_per_channel = []
    multi_epileptogenic_indexes_per_channel = []
    
    multi_time_start = [np.max((time_start, epindex_start)) for time_start, epindex_start in zip(multi_time_start, multi_epindex_start)]
    
    for patient, work_channels, epindex_folder, sampling_frequency, work_signal in\
        zip(multi_patient, multi_work_channels, multi_epindex_folder, multi_sampling_frequency, multi_work_signal):
        
        tonicity_per_channel = np.load(epindex_folder + 'epindex_tonicities_per_channel.npz', allow_pickle=True)['data']
        delay_per_channel = np.load(epindex_folder + 'epindex_delays_per_channel.npz', allow_pickle=True)['data']
        epileptogenic_value_per_channel = np.load(epindex_folder + 'epindex_values_per_channel.npz', allow_pickle=True)['data']
        
        max_epileptogenic_value = np.max([np.max(y) for y in epileptogenic_value_per_channel if len(y) > 0])        
        epileptogenic_index_per_channel =  [[np.max((0, x)) / max_epileptogenic_value for x in y] for y in epileptogenic_value_per_channel]
        
        if plot_montage is None:   
            
            plot_value_per_channel = []
        
            for x in epileptogenic_value_per_channel:
                
                if len(x) > 0:
                    
                    plot_value_per_channel.append(np.max(x))
                    
                else:
                    
                    plot_value_per_channel.append(0)
                   
            plot_channels, plot_channel_indexes = get_plot_labels(work_channels, plot_value_per_channel, max_plot_num)                
        else:
            plot_channels = get_channels(patient, plot_montage)
            plot_channel_indexes = [work_channels.index(channel) for channel in plot_channels]
        
        plot_channel_num = len(plot_channels)
        multi_plot_channels.append(plot_channels)
        multi_color_per_channel.append(get_plot_colors(plot_channel_num))    
               
        multi_tonicities_per_channel.append(tonicity_per_channel)
        multi_delays_per_channel.append(delay_per_channel)
        multi_epileptogenic_values_per_channel.append(epileptogenic_value_per_channel)
        multi_epileptogenic_indexes_per_channel.append(epileptogenic_index_per_channel)
        
    multi_times = []
    new_multi_work_signal = []
    
    for energy_folder, epindex_folder, patient, work_channels, epindex_start, time_start, time_duration   in\
        zip(multi_energy_folder, multi_epindex_folder, multi_patient, multi_work_channels, multi_epindex_start, multi_time_start, multi_time_duration):
            
        time_windows = np.load(energy_folder + 'time_windows.npz')['data']
        cumsum_time_windows = np.load(epindex_folder + 'time_windows.npz')['data']
       
        times, time_windows, _, window_time_end, work_signal =\
            get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
        
        multi_times.append(times)
        new_multi_work_signal.append(work_signal)
            
        window_epindex_start = np.argmin(np.asb(epindex_start - time_windows))
                
        energy_ratios_per_channel = np.load(energy_folder + 'energy_ratios_per_channel.npz')['data'][:, window_epindex_start:window_time_end]
        alarm_threshold = np.load(epindex_folder + 'epindex_threshold.npz')['data']
        cumulative_sums_per_channel = np.load(epindex_folder + 'cumulative_sums_per_channel.npz')['data'][:, :window_time_end-window_epindex_start]
        alarm_times_per_channel = np.load(epindex_folder + 'alarm_times_per_channel.npz', allow_pickle=True)['data']   
        detection_times_per_channel = np.load(epindex_folder + 'detection_times_per_channel.npz', allow_pickle=True)['data']
        
        color_per_channel = get_plot_colors(len(plot_channels))
        
        plot_cumulative_sums(plot_channels,
                             time_windows,
                             cumsum_time_windows,
                             energy_ratios_per_channel[plot_channel_indexes],
                             cumulative_sums_per_channel[plot_channel_indexes],
                             alarm_times_per_channel[plot_channel_indexes],
                             detection_times_per_channel[plot_channel_indexes],
                             color_per_channel,
                             'Energy Ratio',
                             alarm_threshold=alarm_threshold,
                             xlim=[time_start, time_start + time_duration])
        
    multi_work_signal = new_multi_work_signal
        
    if unique_signal:
        
        bipolar_signal, _ = get_seeg_bipolar_channels(work_signal, work_channels)
        
        plot_signal = [bipolar_signal[work_channels.index(channel)] for channel in plot_channels]
            
        plot_signal_channels(multi_times[0],
                             list(multi_plot_channels[0]),
                             plot_signal)
        
    if plot_montage is None:   
             
        plot_channels = []        
        
        for y in multi_plot_channels:            
            plot_channels.extend([x for x in y if x not in plot_channels])
            
    else:
        
        plot_channels = []
        
        for patient in multi_patient:
            
            plot_channels.extend([x for x in get_channels(patient, plot_montage) if x not in plot_channels])
                      
    plot_channels.sort()
    
    for multi_data_per_channel, ylabel in\
        zip([multi_epileptogenic_indexes_per_channel, multi_epileptogenic_values_per_channel, multi_tonicities_per_channel, multi_delays_per_channel],
            ['Normalized EI', 'EI', 'Tonicity', 'Delay']):
            
        plot_data_per_channel = []
        plot_legend_per_channel = []
        plot_group_per_channel = []
        
        for data_per_channel, work_channels, legend, group in zip(multi_data_per_channel,
                                                                 multi_work_channels,
                                                                 multi_legend,
                                                                 multi_group):
        
            for channel in plot_channels:  
                
                if channel in work_channels:
                    
                    for x in data_per_channel[work_channels.index(channel)]:
                        plot_data_per_channel.append(x)
                        plot_legend_per_channel.append(channel)
                        if group is None:
                            plot_group_per_channel.append(legend)
                        else:
                            plot_group_per_channel.append(legend + ', ' + group)
                            
        color_per_label = get_plot_colors(len(np.unique(plot_legend_per_channel)))
    
        plot_grouped_bars(plot_data_per_channel,
                          plot_legend_per_channel,
                          plot_group_per_channel,
                          list(np.unique(plot_legend_per_channel)),
                          list(np.unique(plot_group_per_channel)),
                          color_per_label,
                          ylabel)
    
    print('Plotting...')
    
    plt.show()