from analyze_seeg_features.folder_management import *
from utilities.signal.time import get_times
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.general import get_plot_colors
from utilities.math.transform import short_time_fourier_transform, hilbert_transform
from utilities.plot.signal import plot_time_freq_signal, plot_signal_features
from utilities.plot.series import plot_series, plot_multi_series
import matplotlib.pyplot as plt
import scipy
import numpy as np


def plot_seeg_channel(energy_folder: str,
                      connection_folder: str,
                      connection_alarm_folder: str,
                      patient: str,
                      work_signal: list,
                      work_channels: list,
                      sampling_frequency: int,
                      window_duration: float,
                      window_shift: float,
                      source_channel: str,
                      target_channel: str,
                      time_start: float,
                      time_duration: float,
                      max_plot_num: int,
                      plot_montage: str):
    
    sample_signal_duration = work_signal.shape[1]
    sample_window_duration = int(sampling_frequency * window_duration)    
    sample_window_shift = int(sampling_frequency * window_shift)  
    
    window_number = int(sample_signal_duration / sample_window_shift) -\
        int(sample_window_duration / sample_window_shift) + 1
        
    sample_windows = np.asarray([i * sample_window_shift for i in range(window_number)])
    
    time_windows = sample_windows / sampling_frequency

    energy_ratios_per_channel = np.load(energy_folder + 'energy_ratios_per_channel.npz')['data']
    instant_phase_entropies_per_channel = np.load(energy_folder + 'instant_phase_entropies_per_channel.npz')['data']
    initial_phase_entropies_per_channel = np.load(energy_folder + 'initial_phase_entropies_per_channel.npz')['data']
        
    time_windows = np.load(connection_folder + 'time_windows.npz')['data']
    
    if window_number > len(time_windows):
        
        discarded_window_number = window_number  - len(time_windows)
        window_number = len(time_windows)
        energy_ratios_per_channel = energy_ratios_per_channel[:, :-discarded_window_number]
        initial_phase_entropies_per_channel = initial_phase_entropies_per_channel[:, :-discarded_window_number] 
        instant_phase_entropies_per_channel = instant_phase_entropies_per_channel[:, :-discarded_window_number] 

    connections_per_edge = np.load(connection_folder + 'connections_per_edge.npz')['data']
    
    edges = list(np.load(connection_folder + 'edges.npz')['data'])
    nodes = list(np.load(connection_folder + 'nodes.npz')['data'])
    
    input_connections_per_node = np.zeros((len(nodes), window_number))
    output_connections_per_node = np.zeros((len(nodes), window_number))

    source_input_connections_per_node = [np.asarray([0 for _ in range(window_number)]) for _ in nodes]
    target_input_connections_per_node = [np.asarray([0 for _ in range(window_number)]) for _ in nodes]
    
    source_output_connections_per_node = [np.asarray([0 for _ in range(window_number)]) for _ in nodes]
    target_output_connections_per_node = [np.asarray([0 for _ in range(window_number)]) for _ in nodes]
    
    for edge_index, edge in enumerate(edges):
        
        node_index = nodes.index(str(edge[1]))
        
        input_connections_per_node[node_index] += connections_per_edge[edge_index]
        
        node_index = nodes.index(str(edge[0]))
        
        output_connections_per_node[node_index] += connections_per_edge[edge_index]
        
        if edge[1] == source_channel:
            
            node_index = nodes.index(str(edge[0]))
            
            source_input_connections_per_node[node_index] = connections_per_edge[edge_index]
            
            if edge[0] == target_channel:
                
                target_source_connections = connections_per_edge[edge_index]
            
        elif edge[1] == target_channel:
            
            node_index = nodes.index(str(edge[0]))
            
            target_input_connections_per_node[node_index] = connections_per_edge[edge_index]
            
            if edge[0] == source_channel:
                
                source_target_connections = connections_per_edge[edge_index]
                
        if edge[0] == source_channel:
            
            node_index = nodes.index(str(edge[1]))
            
            source_output_connections_per_node[node_index] = connections_per_edge[edge_index]
                
        elif edge[0] == target_channel:
            
            node_index = nodes.index(str(edge[1]))
                
            target_output_connections_per_node[node_index] = connections_per_edge[edge_index]
                
        source_input_connections_per_node = np.asarray(source_input_connections_per_node)
        target_input_connections_per_node = np.asarray(target_input_connections_per_node)
        
        source_output_connections_per_node = np.asarray(source_output_connections_per_node)
        target_output_connections_per_node = np.asarray(target_output_connections_per_node)
        
    input_connection_alarms_per_node = np.load(connection_alarm_folder + 'input_connection_alarms_per_node.npz')['data']
    output_connection_alarms_per_node = np.load(connection_alarm_folder + 'output_connection_alarms_per_node.npz')['data']            

    times, time_windows, window_time_start, window_time_end, work_signal =\
        get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
        
    bipolar_signal, _ =\
        get_seeg_bipolar_channels(work_signal, work_channels)
        
    if plot_montage is None:
        
        plot_channel_indexes = np.random.randint(0, len(work_channels), max_plot_num)
        plot_channels = [work_channels[index] for index in plot_channel_indexes]
        
    else:
        
        plot_channels = get_channels(patient, plot_montage)
        plot_channels = [channel for channel in plot_channels if channel in work_channels]
        plot_channel_indexes = [work_channels.index(channel) for channel in plot_channels]
    
    if source_channel is not None:
    
        source_index = work_channels.index(source_channel)
        
        if target_channel is not None:
            target_index = work_channels.index(target_channel)
            indexes, channels = [source_index, target_index], [source_channel, target_channel]
        else:
            indexes, channels = [source_index], [source_channel]
        
        for channel_index, channel in\
            zip(indexes, channels):
            
            signal_amplitudes, signal_initial_phases =\
                short_time_fourier_transform(work_signal[channel_index],
                                             sampling_frequency,
                                             window_duration,
                                             window_shift)
                
            frequencies = scipy.fft.fftfreq(int(sampling_frequency * window_duration), 1 / sampling_frequency)
                
            max_freq_index = np.argmin(np.abs(frequencies - 250))
            
            signal_amplitudes = signal_amplitudes[:, :max_freq_index]
            
            signal_initial_phases = signal_initial_phases[:, :max_freq_index]
            
            plot_time_freq_signal((times - time_start) / window_shift,
                                  time_windows - time_windows[0],
                                  frequencies[:max_freq_index],
                                  bipolar_signal[channel_index],
                                  signal_amplitudes,
                                  signal_initial_phases,
                                  phase_label='Initial phase',
                                  title=channel)
            
            _, signal_instant_phases =\
                hilbert_transform(work_signal[channel_index],
                                  sampling_frequency,
                                  window_duration,
                                  window_shift)
            
            signal_instant_phases = signal_instant_phases[:, :max_freq_index]
            
            plot_time_freq_signal((times - time_start) / window_shift,
                                  time_windows - time_windows[0],
                                  frequencies[:max_freq_index],
                                  bipolar_signal[channel_index],
                                  signal_amplitudes,
                                  signal_instant_phases,
                                  phase_label='Instant phase',
                                  title=channel)
            
            plot_signal_features(times - time_start,
                                 time_windows - time_windows[0],                         
                                 bipolar_signal[channel_index],                         
                                 [energy_ratios_per_channel[channel_index, window_time_start:window_time_end],
                                 initial_phase_entropies_per_channel[channel_index, window_time_start:window_time_end],
                                 instant_phase_entropies_per_channel[channel_index, window_time_start:window_time_end]],
                                 ['Energy ratio', 'Entropy of initial phase', 'Entropy of instant phase'],
                                 title=channel)
            
            plot_signal_features(times - time_start,
                                 time_windows - time_windows[0],                         
                                 bipolar_signal[channel_index],                         
                                 [input_connections_per_node[channel_index, window_time_start:window_time_end],
                                 output_connections_per_node[channel_index, window_time_start:window_time_end]],
                                 ['Input connection', 'Output connection'],
                                 title=channel)
            
            plot_signal_features(times - time_start,
                                 time_windows - time_windows[0],
                                 bipolar_signal[channel_index],                         
                                 [input_connection_alarms_per_node[channel_index, window_time_start:window_time_end],
                                  output_connection_alarms_per_node[channel_index, window_time_start:window_time_end]],
                                 ['Desync abnormality', 'Hypersync abnormality'],
                                 title=channel)
                
        if target_channel is not None and connections_per_edge is not None:  
            
            connection_ratios = source_target_connections[window_time_start:window_time_end] / target_source_connections[window_time_start:window_time_end]
            
            plot_series(time_windows - time_windows[0],
                        connection_ratios,
                        source_channel + '-' + target_channel + ' connection ratio',
                        plot_quartile=True,
                        sample_size=10,
                        ylim=[0.5, 2],
                        thresholds={'Normal ratio': 1.0},
                        logscale=True)
            
            plot_multi_series([time_windows - time_windows[0], time_windows - time_windows[0]],
                              [source_target_connections[window_time_start:window_time_end], target_source_connections[window_time_start:window_time_end]],
                              [source_channel + ' -> ' + target_channel, target_channel + ' -> ' + source_channel],
                              get_plot_colors(2),
                              'Connection',
                              plot_quartile=False,
                              sample_size=10,
                              title=None,
                              xlim=None)
        
    plt.show()