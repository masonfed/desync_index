from utilities.math.fit_distributions import fit_gaussian
from utilities.math.graph import compute_dynamic_graph_features
import numpy as np
import pathlib


def compute_seeg_graph(connection_folder: str,
                       graph_folder: str,
                       window_shift: float,
                       connection_technique: str,
                       graph_start: float,
                       graph_base: float,
                       graph_min: str,
                       graph_max: str):
    
    pathlib.Path(graph_folder).mkdir(parents=True, exist_ok=True)
    
    network_nodes = np.load(connection_folder + 'nodes.npz')['data'] 
    network_edges = np.load(connection_folder + 'edges.npz')['data']            
    connections_per_edge = np.load(connection_folder + 'connections_per_edge.npz')['data']
    lags_per_edge = np.load(connection_folder + 'lags_per_edge.npz')['data']
    
    window_graph_start = int(graph_start / window_shift)
    
    if graph_base is None:
        window_graph_base = len(connections_per_edge[0])

    else:        
        window_graph_base = int(graph_base / window_shift)
        
    if graph_min == 'mean':
        
        graph_min = np.mean(connections_per_edge[:, window_graph_start:window_graph_base])
        
    elif graph_min == 'median':
        
        graph_min = np.mean(connections_per_edge[:, window_graph_start:window_graph_base])
        
    elif len(graph_min) > 7 and graph_min[:7] == 'percent':
        
        graph_min = np.percentile(connections_per_edge[:, window_graph_start:window_graph_base]), int(graph_min[7:])
        
    elif graph_min == 'gauss':
        
        try:
            
            noise_threshold = np.load(graph_folder + 'gaussian_noise_threshold.npz')['data']
            
        except:
            
            print('Compute gaussian noise...')
        
            noise_threshold = fit_gaussian(connections_per_edge[:, window_graph_start:window_graph_base].flatten())[0][0]
            
            np.savez_compressed(graph_folder + 'gaussian_noise_threshold.npz', data=noise_threshold)
            
        graph_min = float(noise_threshold)
    
    else:
        
        graph_min = float(graph_min)
        
    if graph_max == 'default' and connection_technique == 'dpte':
        graph_max = 2.0
    else:        
        graph_max = float(graph_max)
            
    print('Compute graph features with ', graph_min, ' and ', graph_max, ' as minimum and maximum weight value!')
    print()
    
    compute_dynamic_graph_features(graph_folder,
                                   network_nodes,
                                   network_edges,
                                   connections_per_edge,
                                   lags_per_edge,
                                   graph_min,
                                   graph_max)
    

    
