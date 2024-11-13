from analyze_seeg_features.folder_management import *
from utilities.math.connectivity import compute_channel_connections
import timeit
import pathlib
import numpy as np
import itertools
import os


def compute_seeg_connection(polarization_folder: str,
                            connection_folder: str,
                            work_signal: np.ndarray,
                            work_channels: list,
                            sampling_frequency: int,
                            window_duration: float,
                            window_shift: float,
                            connection_technique: str,
                            connection_bin_rule: str,
                            connection_lag: float,
                            connection_lag_num: int,
                            recovering_data=True):
    
    start = timeit.default_timer()
    
    pathlib.Path(connection_folder).mkdir(parents=True, exist_ok=True)
    
    sample_signal_duration = work_signal.shape[1]
    sample_window_duration = int(sampling_frequency * window_duration)
    sample_window_shift = int(sampling_frequency * window_shift)
    sample_lag = int(connection_lag * sampling_frequency)
    
    sample_lags = [i * sample_lag for i in range(connection_lag_num+1)]    
    max_sample_lag = sample_lags[-1]
    
    print('Considering', connection_technique, 'as connection technique and', connection_bin_rule, 'as connection bin rule and', sample_lags[-1], 'as maximimum sample lag!')
    
    window_number = int(sample_signal_duration / sample_window_shift) - int(sample_window_duration / sample_window_shift) + 1 - np.max((1, int(max_sample_lag / sample_window_shift)))        
    sample_windows = np.asarray([i * sample_window_shift for i in range(window_number)])
    
    print('Considering', window_number, 'time windows and', len(work_channels), 'nodes!')
    
    print()
    
    np.savez_compressed(connection_folder + 'time_windows.npz', data=sample_windows / sampling_frequency)
    
    network_edges = []
    connections_per_edge = []
    lags_per_edge = []
    
    for index_a, index_b in itertools.product(np.arange(len(work_signal)), np.arange(len(work_signal))):
        
        if index_a != index_b:
            
            network_edges.append([work_channels[index_a], work_channels[index_b]])
            connections_per_edge.append([])
            lags_per_edge.append([])
            
    missing_edge_indexes = [x for x in range(len(network_edges))]

    if recovering_data:
        
        extra_montage_list = [montage_folder for montage_folder in os.listdir(polarization_folder)]
        
        if 'montage=full' in extra_montage_list:
            extra_montage_list = ['montage=full']
        
        for extra_montage in extra_montage_list:
            
            extra_montage = extra_montage.split('=')[1]

            extra_folder = get_connection_folder(get_window_folder(polarization_folder, extra_montage, window_duration, window_shift), connection_technique, connection_bin_rule, connection_lag, connection_lag_num)
            
            if os.path.isfile(extra_folder + 'edges.npz'):
                
                extra_network_edges = np.load(extra_folder + 'edges.npz')['data'].tolist()
                extra_connections_per_edges = np.load(extra_folder + 'connections_per_edge.npz')['data']
                extra_lags_per_edges = np.load(extra_folder + 'lags_per_edge.npz')['data']
                
                print('Recovering connection data from ', extra_montage, '!')
                
                for extra_index, extra_edge in enumerate(extra_network_edges):     

                    if extra_edge in network_edges:
                        
                        index = network_edges.index(extra_edge)
                        
                        if index in missing_edge_indexes:   
                            
                            connections_per_edge[index] = extra_connections_per_edges[extra_index]
                            lags_per_edge[index] = extra_lags_per_edges[extra_index]
                            
                            missing_edge_indexes.remove(index)

    phase_folder = connection_folder + 'phase/'
    
    pathlib.Path(phase_folder).mkdir(parents=True, exist_ok=True)
    
    missing_channel_indexes = []
    
    for edge_index in missing_edge_indexes:
        
        edge = network_edges[edge_index]
        
        source_channel, target_channel = edge[0], edge[1]
        
        source_channel_index, target_channel_index = work_channels.index(source_channel), work_channels.index(target_channel)
        
        if source_channel_index not in missing_channel_indexes:
            missing_channel_indexes.append(source_channel_index)
            
        if target_channel_index not in missing_channel_indexes:
            missing_channel_indexes.append(target_channel_index)
            
    compute_channel_connections(phase_folder,
                                connection_technique,
                                connection_bin_rule,
                                work_signal, 
                                work_channels,
                                missing_channel_indexes,
                                network_edges,
                                missing_edge_indexes,
                                window_number,
                                sample_window_shift,
                                sample_window_duration,
                                sample_lags,
                                connections_per_edge,
                                lags_per_edge)
    
    stop = timeit.default_timer()

    print('Total computational time: ', round((stop - start) / 3600, 4), 'h' )
    
    np.savez_compressed(connection_folder + 'edges.npz', data=network_edges)
    np.savez_compressed(connection_folder + 'nodes.npz', data=work_channels)    
    np.savez_compressed(connection_folder + 'connections_per_edge.npz', data=connections_per_edge)
    np.savez_compressed(connection_folder + 'lags_per_edge.npz', data=lags_per_edge)   
