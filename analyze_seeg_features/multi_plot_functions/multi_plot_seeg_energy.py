from analyze_seeg_features.folder_management import *
from utilities.signal.time import get_times
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.channels import plot_grouped_violins_per_channel
from utilities.plot.violins import plot_grouped_violins, plot_violins
from utilities.plot.signal import plot_signal_channels
from utilities.plot.general import *
import matplotlib.pyplot as plt
import numpy as np


def multi_plot_seeg_energy(multi_legend: list,
                           multi_group: list,
                           multi_patient: list,
                           multi_work_signal: list,
                           multi_work_channels: list,
                           multi_sampling_frequency: list,
                           multi_energy_folder: list,
                           multi_time_start: list,
                           multi_time_duration: list,
                           unique_signal: bool,
                           max_plot_num: int,
                           plot_montage: str):
        
    multi_plot_channels = []
    multi_color_per_channel = []
    multi_time_windows = []
    multi_energy_ratios_per_channel = []
    multi_energies_per_channel = []
    multi_initial_phase_entropies_per_channel = []
    multi_instant_phase_entropies_per_channel = []
    
    multi_window_time_start = []
    multi_window_time_end = []
    multi_times = []
    
    for patient, work_channels, energy_folder, time_start, time_duration, work_signal, sampling_frequency in\
        zip(multi_patient, multi_work_channels, multi_energy_folder, multi_time_start, multi_time_duration,
            multi_work_signal, multi_sampling_frequency):

        time_windows = np.load(energy_folder + 'time_windows.npz')['data']
        
        times, time_windows, window_time_start, window_time_end, work_signal =\
            get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
        
        multi_window_time_start.append(window_time_start)
        multi_window_time_end.append(window_time_end)
            
        multi_time_windows.append(time_windows)        
        multi_times.append(times)
        
        energy_ratios_per_channel =\
            np.load(energy_folder + 'energy_ratios_per_channel.npz')['data'][:, window_time_start:window_time_end]
        energies_per_channel =\
            np.load(energy_folder + 'energies_per_channel.npz')['data'][:, window_time_start:window_time_end]
        instant_phase_entropies_per_channel =\
            np.load(energy_folder + 'instant_phase_entropies_per_channel.npz')['data'][:, window_time_start:window_time_end]
        initial_phase_entropies_per_channel =\
            np.load(energy_folder + 'initial_phase_entropies_per_channel.npz')['data'][:, window_time_start:window_time_end]

        multi_energy_ratios_per_channel.append(energy_ratios_per_channel)
        multi_energies_per_channel.append(energies_per_channel)
        multi_instant_phase_entropies_per_channel.append(instant_phase_entropies_per_channel)
        multi_initial_phase_entropies_per_channel.append(initial_phase_entropies_per_channel)
        
        if plot_montage is None:            
            plot_value_per_channel = [np.mean(energy_ratios_per_channel[i]) for i in range(len(energy_ratios_per_channel))]                     
            plot_channels, _ = get_plot_labels(work_channels, plot_value_per_channel, max_plot_num)           
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
       
    print('Plotting...')
    
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
        
    for multi_data, ylabel, ylim in\
        zip([multi_energy_ratios_per_channel, multi_energies_per_channel,
             multi_initial_phase_entropies_per_channel, multi_instant_phase_entropies_per_channel],
            ['Energy ratio',
             'E [$V^2 \\times s$]',
             'Initial phase entropy',
             'Instant phase entropy'],
            [[0, 1], [0, 0.0001],
             [1, np.log2(5)], [2.2, np.log2(5)]]):

        if multi_group is None:
        
            plot_violins([np.mean(x, axis=0) for x in multi_data],
                         multi_legend,
                         multi_color,
                         ylabel,
                         ylim)
            
        else:         
            
            plot_grouped_violins([np.mean(x, axis=0) for x in multi_data],
                                 multi_legend,
                                 multi_group,
                                 unique_legends,
                                 unique_groups,
                                 color_per_label,
                                 ylabel,
                                 ylim)
    
    multi_multi_data_per_channel = [multi_energy_ratios_per_channel,
                                    multi_energies_per_channel,
                                    multi_initial_phase_entropies_per_channel,
                                    multi_instant_phase_entropies_per_channel]    
    multi_data_ylabel = ['Energy ratio', 'E [$V^2 \\times s$]', 'Initial phase entropy', 'Instant phase entropy']
    multi_data_range = [[0, 1], [0, 0.0001], [1, np.log2(5)], [2.2, np.log2(5)]]
    
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
    