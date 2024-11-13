from utilities.math.smooth import get_smoothed_values, get_percent_values
from multiprocessing import Pool
from multiprocessing import cpu_count
from analyze_seeg_features.folder_management import *
import numpy as np   
import pathlib

def get_connection_alarms(network_edges: np.ndarray,
                          network_nodes: np.ndarray,
                          connections_per_edge: np.ndarray,
                          median_connections: np.ndarray,
                          low_percent_connections: np.ndarray,
                          high_percent_connections: np.ndarray,
                          target_node: str):
    
    node_num = len(network_nodes)    
    time_num = len(connections_per_edge[0])
    
    input_connections_per_node = np.zeros((node_num, time_num))
    median_input_connections_per_node = np.zeros((node_num, time_num))
    
    output_connections_per_node = np.zeros((node_num, time_num))
    median_output_connections_per_node = np.zeros((node_num, time_num))
        
    for edge_index, edge in enumerate(network_edges):
        
        if str(edge[1]) == target_node:
            
            node_index = network_nodes.index(str(edge[0]))            
            input_connections_per_node[node_index, :] += connections_per_edge[edge_index, :]
            median_input_connections_per_node[node_index, :] += median_connections
        
        if str(edge[0]) == target_node:
            
            node_index = network_nodes.index(str(edge[0]))            
            output_connections_per_node[node_index, :] += connections_per_edge[edge_index, :]
            median_output_connections_per_node[node_index, :] += median_connections

    target_output_node_teams = np.zeros(output_connections_per_node.shape)
    target_input_node_teams = np.zeros(output_connections_per_node.shape)
       
    target_input_node_teams[input_connections_per_node <= low_percent_connections] = 1
    target_input_connections = np.sum(input_connections_per_node * target_input_node_teams, axis=0)    
    target_median_input_connections = np.sum(median_input_connections_per_node * target_input_node_teams, axis=0)
    
    target_output_node_teams[output_connections_per_node >= high_percent_connections] = 1
    target_output_connections = np.sum(output_connections_per_node * target_output_node_teams, axis=0)    
    target_median_output_connections = np.sum(median_output_connections_per_node * target_output_node_teams, axis=0)  
    
    input_connections = np.mean(input_connections_per_node, axis=0)
    output_connections = np.mean(output_connections_per_node, axis=0)
    
    input_connection_alarms = np.sqrt(target_median_input_connections) - np.sqrt(target_input_connections)
    output_connection_alarms = np.sqrt(target_output_connections) - np.sqrt(target_median_output_connections)
    
    input_team_sizes = np.sum(target_input_node_teams, axis=0)
    output_team_sizes = np.sum(target_output_node_teams, axis=0)
    
    return output_connection_alarms, input_connection_alarms,\
        output_connections, input_connections,\
            output_team_sizes, input_team_sizes



def compute_seeg_connection_alarm(connection_folder,
                                  connection_alarm_folder: str,
                                  window_shift: float,
                                  alarm_smooth: float,
                                  alarm_baseline: float,
                                  alarm_low_percent: float,
                                  alarm_high_percent: float):
    
    pathlib.Path(connection_alarm_folder).mkdir(parents=True, exist_ok=True)
        
    print('Smooth connection values...')
    
    network_nodes = list(np.load(connection_folder + 'nodes.npz')['data'])
    network_edges = list(np.load(connection_folder + 'edges.npz')['data'])
    
    connections_per_edge = np.load(connection_folder + 'connections_per_edge.npz')['data']
    lags_per_edge = np.load(connection_folder + 'lags_per_edge.npz')['data']
    
    window_alarm_baseline = np.max((int(alarm_baseline / window_shift), 1))
    
    smoothed_connections_per_edge =\
        get_smoothed_values(connections_per_edge, alarm_smooth)
    
    median_connections =\
        get_percent_values(connections_per_edge, window_alarm_baseline, 50)
        
    low_percent_connections =\
        get_percent_values(connections_per_edge, window_alarm_baseline, alarm_low_percent)
        
    high_percent_connections =\
        get_percent_values(connections_per_edge, window_alarm_baseline, alarm_high_percent)
    
    smoothed_median_connections =\
        get_smoothed_values(median_connections, alarm_smooth) 
        
    smoothed_low_percent_connections =\
        get_smoothed_values(low_percent_connections, alarm_smooth)
        
    smoothed_high_percent_connections =\
        get_smoothed_values(high_percent_connections, alarm_smooth)

    print('Compute connection alarms...')
    
    network_nodes = np.load(connection_folder + 'nodes.npz')['data'] 
    network_edges = np.load(connection_folder + 'edges.npz')['data']
    
    network_nodes = [str(x) for x in network_nodes]
    
    pool = Pool(processes=cpu_count() - 1)
    
    node_num = len(network_nodes)
        
    output_connection_alarms_per_node = []
    input_connection_alarms_per_node = []
    smoothed_output_connections_per_node = []
    output_team_sizes_per_node = []
    smoothed_input_connections_per_node = []
    input_team_sizes_per_node = []
    
    a, b = 0, np.min((10, node_num))
    
    while a < node_num:
        
        pool_args = []
    
        for target_node in network_nodes[a:b]:
            
            pool_args.append((network_edges,
                              network_nodes,
                              smoothed_connections_per_edge,
                              smoothed_median_connections,
                              smoothed_low_percent_connections,
                              smoothed_high_percent_connections,
                              target_node))
            
        pool_results = pool.starmap(get_connection_alarms, pool_args)
            
        for output_connection_alarms, input_connection_alarms, smoothed_output_connections, smoothed_input_connections, output_team_sizes, input_team_sizes in pool_results:
        
            output_connection_alarms_per_node.append(output_connection_alarms)
            input_connection_alarms_per_node.append(input_connection_alarms)
            smoothed_output_connections_per_node.append(smoothed_output_connections)
            smoothed_input_connections_per_node.append(smoothed_input_connections)
            output_team_sizes_per_node.append(output_team_sizes)
            input_team_sizes_per_node.append(input_team_sizes)
            
        print('Approximate job completion:', int(b * 100 / node_num), '%', end='\r')
    
        a = b
        b = np.min((b + 10, node_num))
        
    print()
        
    np.savez_compressed(connection_alarm_folder + 'smoothed_median_connections.npz', data=smoothed_median_connections)
    np.savez_compressed(connection_alarm_folder + 'output_connection_alarms_per_node.npz', data=output_connection_alarms_per_node)
    np.savez_compressed(connection_alarm_folder + 'input_connection_alarms_per_node.npz', data=input_connection_alarms_per_node)
    np.savez_compressed(connection_alarm_folder + 'smoothed_input_connections_per_node.npz', data=smoothed_input_connections_per_node) 
    np.savez_compressed(connection_alarm_folder + 'smoothed_output_connections_per_node.npz', data=smoothed_output_connections_per_node) 
    np.savez_compressed(connection_alarm_folder + 'input_team_sizes_per_node.npz', data=input_team_sizes_per_node)
    np.savez_compressed(connection_alarm_folder + 'output_team_sizes_per_node.npz', data=output_team_sizes_per_node)
