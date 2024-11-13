from analyze_seeg_features.folder_management import *
from utilities.math.fit_distributions import fit_gaussian
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.signal.time import get_times
from utilities.plot.general import get_plot_labels
from utilities.plot.series import plot_series
from utilities.plot.signal import plot_signal_channels
from utilities.plot.matrix import plot_matrix
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np


def plot_seeg_connection(connection_folder: str,
                         patient: str,
                         work_signal: list,
                         work_channels: list,
                         sampling_frequency: int,
                         connection_lag_num: int,
                         time_start: float,
                         time_duration: float,
                         max_plot_num: int,
                         plot_montage: str = None,
                         fit_connection: bool = False):
    
    time_windows = np.load(connection_folder + 'time_windows.npz')['data']
    
    times, time_windows, window_time_start, window_time_end, work_signal =\
        get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
    
    connections_per_edge = np.load(connection_folder + 'connections_per_edge.npz')['data']    
    lags_per_edge = np.load(connection_folder + 'lags_per_edge.npz')['data']
    
    connections_per_edge = connections_per_edge[:, window_time_start:window_time_end]
    lags_per_edge = lags_per_edge[:, window_time_start:window_time_end]
    
    edges = list(np.load(connection_folder + 'edges.npz')['data'])
    nodes = list(np.load(connection_folder + 'nodes.npz')['data'])
    
    node_num = len(nodes)
    
    input_connections_per_channel = [np.zeros(len(connections_per_edge[0])) for _ in nodes]
    output_connections_per_channel = [np.zeros(len(connections_per_edge[0])) for _ in nodes]
    input_lags_per_channel = [np.zeros(len(connections_per_edge[0])) for _ in nodes]
    output_lags_per_channel = [np.zeros(len(connections_per_edge[0])) for _ in nodes]
    
    for edge_index, edge in enumerate(edges):
        
        input_index = nodes.index(edge[1])
        output_index = nodes.index(edge[0])
        
        input_connections_per_channel[input_index] += connections_per_edge[edge_index]
        output_connections_per_channel[output_index] += connections_per_edge[edge_index]
        input_lags_per_channel[input_index] += lags_per_edge[edge_index]
        output_lags_per_channel[output_index] += lags_per_edge[edge_index]
    
    input_connections_per_channel = np.asarray(input_connections_per_channel) / node_num
    output_connections_per_channel = np.asarray(output_connections_per_channel) / node_num
    input_lags_per_channel = np.asarray(input_lags_per_channel) / node_num
    output_lags_per_channel = np.asarray(output_lags_per_channel) / node_num
    
    if plot_montage is None:
        
        plot_channels, plot_channel_indexes =\
            get_plot_labels(work_channels, [np.abs(np.mean(output_connections_per_channel) - np.mean(output_connections_per_channel[node_index]))\
                 for node_index in range(node_num)], max_plot_num)
        
    else:
        
        plot_channels = get_channels(patient, plot_montage)
        plot_channels = [channel for channel in plot_channels if channel in work_channels]
        plot_channel_indexes = [work_channels.index(channel) for channel in plot_channels]
    
    bipolar_signal, bipolar_channels =\
        get_seeg_bipolar_channels(work_signal, work_channels)
        
    plot_signal_channels(times,
                         bipolar_channels[plot_channel_indexes],
                         bipolar_signal[plot_channel_indexes])
    
    plot_series(time_windows,
                np.mean(connections_per_edge, axis=0),
                'Expected network connection')
    
    plt.figure()    
    hist = plt.hist2d(connections_per_edge.flatten(),
                      lags_per_edge.flatten(),
                      bins=[100, connection_lag_num],
                      density=True, facecolor='b')    
    plt.colorbar(hist[3])
    plt.xlabel('Weight')
    plt.ylabel('Lag [ms]')
    
    plt.figure()    
    plt.hist(lags_per_edge.flatten(), connection_lag_num,
             density=True, facecolor='b')    
    plt.xlabel('Lag [ms]')
    plt.ylabel('Probability')
    plt.grid(True)
    
    plt.axvline(np.mean(lags_per_edge), color='r', linestyle='--', linewidth=1, label='Mean: ' + str("%.3f" % np.mean(lags_per_edge)))
    plt.axvline(np.median(lags_per_edge), color='r', linestyle='-.', linewidth=1, label='Median: ' + str("%.3f" % np.median(lags_per_edge)))
    plt.axvline(np.percentile(lags_per_edge, 25), color='r', linestyle='-', linewidth=1, label='1st quartile: ' + str("%.3f" % np.percentile(lags_per_edge, 25)))
    plt.axvline(np.percentile(lags_per_edge, 75), color='r', linestyle='-', linewidth=1, label='3rd quartile: ' + str("%.3f" % np.percentile(lags_per_edge, 75)))
    plt.legend()
    
    plt.figure()    
    plt.hist(connections_per_edge.flatten().reshape(-1, 1), 1000, density=True, facecolor='b')    
    plt.xlabel('Weight')
    plt.ylabel('Probability')
    plt.grid(True)
        
    if fit_connection:
    
        x = np.linspace(np.min(connections_per_edge), np.max(connections_per_edge), 1000)
        
        mixture_means, mixture_covariances, mixture_intersections = fit_gaussian(connections_per_edge.flatten())
    
        mixture_models = [stats.norm.pdf(x, mean, np.sqrt(cov)) for mean, cov in zip(mixture_means, mixture_covariances)]
        
        for i, model in enumerate(mixture_models):
        
            plt.plot(x, model, label='Model ' + str(i))
            
        for y in mixture_intersections:
        
            plt.axvline(y, color='k', linestyle='--', linewidth=1, label='Intersection: ' + str("%.3f" % y[0]))
        
    else:
        
        plt.axvline(np.mean(connections_per_edge), color='r', linestyle='--', linewidth=1, label='Mean: ' + str("%.3f" % np.mean(connections_per_edge)))
        plt.axvline(np.median(connections_per_edge), color='r', linestyle='-.', linewidth=1, label='Median: ' + str("%.3f" % np.median(connections_per_edge)))
        plt.axvline(np.percentile(connections_per_edge, 25), color='r', linestyle='-', linewidth=1, label='1st quartile: ' + str("%.3f" % np.percentile(connections_per_edge, 25)))
        plt.axvline(np.percentile(connections_per_edge, 75), color='r', linestyle='-', linewidth=1, label='3rd quartile: ' + str("%.3f" % np.percentile(connections_per_edge, 75)))

    plt.legend()
    
    plot_matrix(input_connections_per_channel[plot_channel_indexes],
                time_windows,
                plot_channels,
                'Input connection',
                'Time [s]',
                'Channel')
    
    plot_matrix(output_connections_per_channel[plot_channel_indexes],
                time_windows,
                plot_channels,
                'Output connection',
                'Time [s]',
                'Channel')

    plt.show()