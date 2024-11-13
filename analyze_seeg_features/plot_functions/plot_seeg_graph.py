from analyze_seeg_features.folder_management import *
import matplotlib.pyplot as plt
from utilities.plot.signal import plot_signal_channels
from utilities.signal.time import get_times
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.general import get_plot_labels
from utilities.plot.matrix import plot_matrix_max
from utilities.plot.series import plot_series
import numpy as np


def plot_seeg_graph(connection_folder: str,
                    graph_folder: str,
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
    
    in_degrees_per_channel = np.load(graph_folder + 'connection_in_degrees_per_node.npz')['data'][:, window_time_start:window_time_end]
    out_degrees_per_channel = np.load(graph_folder + 'connection_out_degrees_per_node.npz')['data'][:, window_time_start:window_time_end]
    betweeness_centralities_per_channel = np.load(graph_folder + 'connection_betweeness_centralities_per_node.npz')['data'][:, window_time_start:window_time_end]
    eigenvector_centralities_per_channel = np.load(graph_folder + 'connection_eigenvector_centralities_per_node.npz')['data'][:, window_time_start:window_time_end]
    eccentricities_per_channel = np.load(graph_folder + 'connection_eccentricities_per_node.npz')['data'][:, window_time_start:window_time_end]
    diameters = np.load(graph_folder + 'connection_diameters.npz')['data'][window_time_start:window_time_end]
    
    if plot_montage is None:
        
        value_per_channel = [np.max(np.abs(out_degrees_per_channel[i])) for i in range(len(out_degrees_per_channel))]        
        plot_channels, plot_channel_indexes = get_plot_labels(work_channels, value_per_channel, max_plot_num)
        
        
    else:
        
        plot_channels = get_channels(patient, plot_montage)
        plot_channels = [channel for channel in plot_channels if channel in work_channels]
        plot_channel_indexes = [work_channels.index(channel) for channel in plot_channels]
    
    bipolar_signal, bipolar_channels =\
        get_seeg_bipolar_channels(work_signal, work_channels)
        
    in_degrees_per_channel[in_degrees_per_channel < 0.1] = 0.1
        
    decentrality_per_channel = np.mean(eccentricities_per_channel / in_degrees_per_channel, axis=0)
    
    plot_signal_channels(times,
                         bipolar_channels[plot_channel_indexes],
                         bipolar_signal[plot_channel_indexes],
                         signal_feature_label='Eccentricity $/$ In-degree',
                         signal_feature_times=time_windows,
                         signal_features=decentrality_per_channel)
    
    if plot_montage is None:
        plot_montage = 'Selected channel'

    for feature_per_channel, feature_label in zip(\
        [in_degrees_per_channel, out_degrees_per_channel, betweeness_centralities_per_channel, eigenvector_centralities_per_channel, eccentricities_per_channel],
        ['In degree',  'Out degree', 'Betweeness centrality', 'Eigenvector centrality', 'Eccentricity']):
        
        plot_matrix_max(feature_per_channel,
                        time_windows,
                        work_channels,
                        feature_label,
                        'Time [s]',
                        'Channel')
        
        plot_series(time_windows,
                    feature_per_channel,
                    feature_label,
                    sample_size=1)

    plot_series(time_windows,
                diameters,
                'Diameter',
                sample_size=1)
        
    plt.show()
