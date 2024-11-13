from multiprocessing import Pool
from multiprocessing import cpu_count
import networkx as nx
import numpy as np


def compute_dynamic_graph_features(graph_folder: str,
                                   network_nodes: list,
                                   network_edges: list,
                                   weights_per_edge: list,
                                   lags_per_edge: list,
                                   min_weight: float,
                                   max_weight: float):
    
    node_num, edge_num = len(network_nodes), len(network_edges)
    
    original_graph = nx.DiGraph()
    
    for node in network_nodes:
        
        original_graph.add_node(str(node))
        
    window_num = len(weights_per_edge[0])
    
    cpu_num = cpu_count() - 1
    
    pool = Pool(processes=cpu_num)
    
    job_a_index, job_b_index = 0, np.min((cpu_num*5, window_num))
    
    in_degrees_per_window = []
    out_degrees_per_window = []
    betweeness_centralities_per_window = []
    eigenvector_centralities_per_window = []
    shortest_paths_per_window = []
    eccentricities_per_window = []
    diameters = []
    
    while job_a_index < window_num:
        
        pool_args = []
        
        for window_index in range(job_a_index, job_b_index):
            
            new_graph = original_graph.copy()
        
            for edge_index in range(edge_num):
                
                weight = weights_per_edge[edge_index][window_index]
                
                if weight > min_weight:
                    
                    new_graph.add_edge(str(network_edges[edge_index][0]),
                                       str(network_edges[edge_index][1]),
                                       connection=np.min((weight, max_weight)),
                                       inv_connection=max_weight - np.min((weight, max_weight)),
                                       lag=lags_per_edge[edge_index][window_index])
                
            pool_args.append((new_graph, 'connection', 'inv_connection'))
            
        pool_results = pool.starmap(compute_graph_features, pool_args)
        
        for results in pool_results:
            
            in_degrees, out_degrees, betweeness_centralities, eigenvector_centralities, shortest_paths, eccentricities, diameter = results
            
            in_degrees_per_window.append(in_degrees)
            out_degrees_per_window.append(out_degrees)
            betweeness_centralities_per_window.append(betweeness_centralities)
            eigenvector_centralities_per_window.append(eigenvector_centralities)
            shortest_paths_per_window.append(shortest_paths)
            eccentricities_per_window.append(eccentricities)
            diameters.append(diameter)
            
        print('Approximate job completion:', int(job_b_index * 100 / window_num), '%', end='\r')
    
        job_a_index = job_b_index
        
        job_b_index = np.min((job_b_index + cpu_num*5, window_num))
        
    print()
            
    connection_in_degrees_per_node = [[in_degrees[str(node)] for in_degrees in in_degrees_per_window] for node in network_nodes]
    
    np.savez_compressed(graph_folder + 'connection_in_degrees_per_node.npz', data=connection_in_degrees_per_node)
    
    del connection_in_degrees_per_node
    del in_degrees_per_window
    
    connection_out_degrees_per_node = [[out_degrees[str(node)] for out_degrees in out_degrees_per_window] for node in network_nodes]
    
    np.savez_compressed(graph_folder + 'connection_out_degrees_per_node.npz', data=connection_out_degrees_per_node)
    
    del connection_out_degrees_per_node
    del out_degrees_per_window
    
    connection_betweeness_centralities_per_node = [[betweeness_centralities[str(node)] for betweeness_centralities in betweeness_centralities_per_window] for node in network_nodes]

    np.savez_compressed(graph_folder + 'connection_betweeness_centralities_per_node.npz', data=connection_betweeness_centralities_per_node)

    del connection_betweeness_centralities_per_node
    del betweeness_centralities_per_window
    
    connection_eigenvector_centralities_per_node = [[eigenvector_centralities[str(node)] for eigenvector_centralities in eigenvector_centralities_per_window] for node in network_nodes]
    
    np.savez_compressed(graph_folder + 'connection_eigenvector_centralities_per_node.npz', data=connection_eigenvector_centralities_per_node)
    
    del connection_eigenvector_centralities_per_node
    del eigenvector_centralities_per_window
    
    connection_shortest_paths_per_edge = [[] for _ in network_edges]
    
    for edge_index, edge in enumerate(network_edges):
        
        for shortest_paths in shortest_paths_per_window:    
                
            if str([edge[0], edge[1]]) in shortest_paths.keys():                
                connection_shortest_paths_per_edge[edge_index].append(shortest_paths[str([edge[0], edge[1]])])
            
            else:
                connection_shortest_paths_per_edge[edge_index].append(np.infty)
    
    np.savez_compressed(graph_folder + 'connection_shortest_paths_per_edge.npz', data=connection_shortest_paths_per_edge)
    
    del shortest_paths_per_window
    
    connection_efficiencies_per_edge = [[1 / np.max((min_weight, path)) for path in shortest_paths] for shortest_paths in connection_shortest_paths_per_edge]
    
    np.savez_compressed(graph_folder + 'connection_efficiencies_per_edge.npz', data=connection_efficiencies_per_edge)
    
    del connection_shortest_paths_per_edge
    del connection_efficiencies_per_edge
    
    connection_eccentricities_per_node = [[eccentricities[str(node)] for eccentricities in eccentricities_per_window] for node in network_nodes]
    
    np.savez_compressed(graph_folder + 'connection_eccentricities_per_node.npz', data=connection_eccentricities_per_node)
    
    del connection_eccentricities_per_node
    del eccentricities_per_window
    
    np.savez_compressed(graph_folder + 'connection_diameters.npz', data=diameters)
    
    del diameters

def compute_graph_features(graph, weight, inv_weight):
    
    in_degrees = graph.in_degree(weight=weight)
    
    out_degrees =  graph.out_degree(weight=weight)
    
    betweeness_centralities = nx.betweenness_centrality(graph, weight=inv_weight)
    
    eigenvector_centralities = nx.eigenvector_centrality_numpy(graph.reverse(), weight=weight)
    
    eccentricities = {}
    
    shortest_paths = {}
    
    for source in graph.nodes:
    
        source_shortest_paths = nx.shortest_path_length(graph, source=source, weight=inv_weight)
        
        eccentricities[source] = np.max(list(source_shortest_paths.values()))
    
        for target in source_shortest_paths.keys():
            
            if source != target:
                
                shortest_paths[str([source, target])] = source_shortest_paths[target]
                
    diameter = np.max(list(eccentricities.values()))
    
    return in_degrees, out_degrees, betweeness_centralities, eigenvector_centralities, shortest_paths, eccentricities, diameter
    
