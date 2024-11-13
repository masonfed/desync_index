from utilities.folder_management import get_multi_input_epoch
from manage_signal_data.aggregate_signal_data import aggregate_signal_data
from analyze_seeg_features.folder_management import *
import numpy as np
import pathlib


def aggregate_seeg_features(patient: str,
                            output_epoch: str,
                            highpass_frequency: int,
                            lowpass_frequency: int,
                            notch_frequency: int,
                            work_montage: str,
                            window_duration: float,
                            window_shift: float,
                            connection_technique: str,
                            connection_bin_rule: str,
                            connection_lag: float,
                            connection_lag_num: int,
                            graph_start: float,
                            graph_base: float,
                            graph_min: float,
                            graph_max: float,
                            energy_low_freqs: list,
                            energy_high_freqs: list,
                            aggregate_signal: bool,
                            aggregate_connection: bool,
                            aggregate_graph: bool,
                            aggregate_energy: bool):
    
    multi_input_epoch = get_multi_input_epoch(output_epoch)
    
    print('Aggregating the data of', multi_input_epoch)
    
    if aggregate_signal:
        
        print('Aggregating signal data...')
        
        aggregate_signal_data('seeg',
                              patient,
                              multi_input_epoch,
                              output_epoch,
                              highpass_frequency=highpass_frequency,
                              lowpass_frequency=lowpass_frequency,
                              notch_frequency=notch_frequency)
    
    patient_folder = get_seeg_patient_folder(patient)
    
    if aggregate_connection:
        
        print('Aggregating connection data...')
    
        multi_connection_time_windows = []
        multi_network_edges = []
        multi_network_nodes = []
        multi_connections_per_edge = []
        multi_lags_per_edge = []
        connection_time_shift = 0
        
        for epoch_index, epoch in enumerate(multi_input_epoch + [output_epoch]):
            
            signal_folder = get_signal_folder(patient_folder,
                                              epoch,
                                              highpass_frequency=highpass_frequency,
                                              lowpass_frequency=lowpass_frequency,
                                              notch_frequency=notch_frequency)

            window_folder = get_window_folder(signal_folder,
                                              work_montage,
                                              window_duration,
                                              window_shift)
            
            connection_folder = get_connection_folder(window_folder,
                                                      connection_technique,
                                                      connection_bin_rule,
                                                      connection_lag,
                                                      connection_lag_num)
            
            if epoch_index == len(multi_input_epoch):
                
                pathlib.Path(connection_folder).mkdir(parents=True, exist_ok=True)
                
                connection_time_windows = np.concatenate(multi_connection_time_windows, axis=-1)
                network_edges = multi_network_edges[0]
                network_nodes = multi_network_nodes[0]
                connections_per_edge = np.concatenate(multi_connections_per_edge, axis=-1)
                lags_per_edge = np.concatenate(multi_lags_per_edge, axis=-1)
                
                np.savez_compressed(connection_folder + 'time_windows.npz', data=connection_time_windows)
                np.savez_compressed(connection_folder + 'edges.npz', data=network_edges)
                np.savez_compressed(connection_folder + 'nodes.npz', data=network_nodes)    
                np.savez_compressed(connection_folder + 'connections_per_edge.npz', data=connections_per_edge)
                np.savez_compressed(connection_folder + 'lags_per_edge.npz', data=lags_per_edge)
                
            else:
                
                multi_connection_time_windows.append(connection_time_shift + np.load(connection_folder + 'time_windows.npz')['data'])
                multi_network_edges.append(np.load(connection_folder + 'edges.npz')['data'])
                multi_network_nodes.append(np.load(connection_folder + 'nodes.npz')['data'])
                multi_connections_per_edge.append(np.load(connection_folder + 'connections_per_edge.npz')['data'])
                multi_lags_per_edge.append(np.load(connection_folder + 'lags_per_edge.npz')['data'])
                
                connection_time_shift = multi_connection_time_windows[-1][-1] + window_shift
                
    if aggregate_graph:
        
        print('Aggregating graph data...')
    
        multi_connection_in_degrees_per_node = []
        multi_connection_out_degrees_per_node = []
        multi_connection_betweeness_centralities_per_node = []
        multi_connection_eigenvector_centralities_per_node = []
        multi_connection_shortest_paths_per_edge = []
        multi_connection_efficiencies_per_edge = []
        multi_connection_eccentricities_per_node = []
        multi_connection_diameters = []
        
        for epoch_index, epoch in enumerate(multi_input_epoch + [output_epoch]):
            
            signal_folder = get_signal_folder(patient_folder,
                                              epoch,
                                              highpass_frequency,
                                              lowpass_frequency,
                                              notch_frequency)

            window_folder = get_window_folder(signal_folder,
                                              work_montage,
                                              window_duration,
                                              window_shift)
            
            connection_folder = get_connection_folder(window_folder, connection_technique, connection_bin_rule, connection_lag, connection_lag_num)
            
            graph_folder = get_graph_folder(connection_folder, graph_start, graph_base, graph_min, graph_max)
            
            if epoch_index == len(multi_input_epoch):
                
                pathlib.Path(graph_folder).mkdir(parents=True, exist_ok=True)
                
                connection_in_degrees_per_node = np.concatenate(multi_connection_in_degrees_per_node, axis=-1)
                connection_out_degrees_per_node = np.concatenate(multi_connection_out_degrees_per_node, axis=-1)
                connection_betweeness_centralities_per_node = np.concatenate(multi_connection_betweeness_centralities_per_node, axis=-1)                
                connection_eigenvector_centralities_per_node = np.concatenate(multi_connection_eigenvector_centralities_per_node, axis=-1)                
                connection_shortest_paths_per_edge = np.concatenate(multi_connection_shortest_paths_per_edge, axis=-1)                
                connection_efficiencies_per_edge = np.concatenate(multi_connection_efficiencies_per_edge, axis=-1)                
                connection_eccentricities_per_node = np.concatenate(multi_connection_eccentricities_per_node, axis=-1)                
                connection_diameters = np.concatenate(multi_connection_diameters, axis=-1)
                
                np.savez_compressed(graph_folder + 'connection_in_degrees_per_node.npz', data=connection_in_degrees_per_node)
                np.savez_compressed(graph_folder + 'connection_out_degrees_per_node.npz', data=connection_out_degrees_per_node)
                np.savez_compressed(graph_folder + 'connection_betweeness_centralities_per_node.npz', data=connection_betweeness_centralities_per_node)
                np.savez_compressed(graph_folder + 'connection_eigenvector_centralities_per_node.npz', data=connection_eigenvector_centralities_per_node)
                np.savez_compressed(graph_folder + 'connection_shortest_paths_per_edge.npz', data=connection_shortest_paths_per_edge)
                np.savez_compressed(graph_folder + 'connection_efficiencies_per_edge.npz', data=connection_efficiencies_per_edge)
                np.savez_compressed(graph_folder + 'connection_eccentricities_per_node.npz', data=connection_eccentricities_per_node)
                np.savez_compressed(graph_folder + 'connection_diameters.npz', data=connection_diameters)
                
            else:
                
                multi_connection_in_degrees_per_node.append(np.load(graph_folder + 'connection_in_degrees_per_node.npz')['data'])
                multi_connection_out_degrees_per_node.append(np.load(graph_folder + 'connection_out_degrees_per_node.npz')['data'])
                multi_connection_betweeness_centralities_per_node.append(np.load(graph_folder + 'connection_betweeness_centralities_per_node.npz')['data'])                
                multi_connection_eigenvector_centralities_per_node.append(np.load(graph_folder + 'connection_eigenvector_centralities_per_node.npz')['data'])                
                multi_connection_shortest_paths_per_edge.append(np.load(graph_folder + 'connection_shortest_paths_per_edge.npz')['data'])                
                multi_connection_efficiencies_per_edge.append(np.load(graph_folder + 'connection_efficiencies_per_edge.npz')['data'])                
                multi_connection_eccentricities_per_node.append(np.load(graph_folder + 'connection_eccentricities_per_node.npz')['data'])                
                multi_connection_diameters.append(np.load(graph_folder + 'connection_diameters.npz')['data'])
                
    if aggregate_energy:
        
        print('Aggregating energy data...')
            
        multi_energy_time_windows = []
        multi_scott_bin_nums_per_channel = []
        multi_freedman_bin_nums_per_channel = []
        multi_freedman_1_bin_nums_per_channel = []
        multi_low_energies_per_channel = []
        multi_high_energies_per_channel = []
        multi_energy_ratios_per_channel = []
        energy_time_shift = 0
                
        for epoch_index, epoch in enumerate(multi_input_epoch + [output_epoch]):
        
            signal_folder = get_signal_folder(patient_folder,
                                              epoch,
                                              highpass_frequency,
                                              lowpass_frequency,
                                              notch_frequency)

            window_folder = get_window_folder(signal_folder,
                                              work_montage,
                                              window_duration,
                                              window_shift)
            
            energy_folder = get_energy_folder(window_folder, energy_low_freqs, energy_high_freqs)
            
            if epoch_index == len(multi_input_epoch):
                
                pathlib.Path(energy_folder).mkdir(parents=True, exist_ok=True)
                
                energy_time_windows = np.concatenate(multi_energy_time_windows, axis=-1)
                scott_bin_nums_per_channel = np.concatenate(multi_scott_bin_nums_per_channel, axis=-1)
                freedman_bin_nums_per_channel = np.concatenate(multi_freedman_bin_nums_per_channel, axis=-1)
                freedman_1_bin_nums_per_channel = np.concatenate(multi_freedman_1_bin_nums_per_channel, axis=-1)
                low_energies_per_channel = np.concatenate(multi_low_energies_per_channel, axis=-1)
                high_energies_per_channel = np.concatenate(multi_high_energies_per_channel, axis=-1)
                energy_ratios_per_channel = np.concatenate(multi_energy_ratios_per_channel, axis=-1)
                
                np.savez_compressed(energy_folder + 'time_windows.npz', data=energy_time_windows)
                np.savez_compressed(energy_folder + 'scott_bin_nums_per_channel.npz', data=scott_bin_nums_per_channel)
                np.savez_compressed(energy_folder + 'freedman_bin_nums_per_channel.npz', data=freedman_bin_nums_per_channel)
                np.savez_compressed(energy_folder + 'freedman_1_bin_nums_per_channel.npz', data=freedman_1_bin_nums_per_channel)
                np.savez_compressed(energy_folder + 'low_energies_per_channel.npz', data=low_energies_per_channel)
                np.savez_compressed(energy_folder + 'high_energies_per_channel.npz', data=high_energies_per_channel)
                np.savez_compressed(energy_folder + 'energy_ratios_per_channel.npz', data=energy_ratios_per_channel)
                
            else:
                
                multi_energy_time_windows.append(energy_time_shift + np.load(energy_folder + 'time_windows.npz')['data'])
                multi_scott_bin_nums_per_channel.append(np.load(energy_folder + 'scott_bin_nums_per_channel.npz')['data'])
                multi_freedman_bin_nums_per_channel.append(np.load(energy_folder + 'freedman_bin_nums_per_channel.npz')['data'])
                multi_freedman_1_bin_nums_per_channel.append(np.load(energy_folder + 'freedman_1_bin_nums_per_channel.npz')['data'])
                multi_low_energies_per_channel.append(np.load(energy_folder + 'low_energies_per_channel.npz')['data'])
                multi_high_energies_per_channel.append(np.load(energy_folder + 'high_energies_per_channel.npz')['data'])
                multi_energy_ratios_per_channel.append(np.load(energy_folder + 'energy_ratios_per_channel.npz')['data'])
                
                energy_time_shift = multi_energy_time_windows[-1][-1] + window_shift
