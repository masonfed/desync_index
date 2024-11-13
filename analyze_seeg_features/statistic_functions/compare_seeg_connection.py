from analyze_seeg_features.folder_management import *
from utilities.signal.time import get_times
from utilities.statistic.t_test import get_two_sample_t_test
from utilities.folder_management import get_output_folder
from utilities.plot.general import *
import pathlib
import pandas as pd
import numpy as np



def compare_seeg_connection(multi_legend: list,
                            multi_group: list,
                            multi_work_signal: list,
                            multi_signal_length: list,
                            multi_sampling_frequency: list,
                            multi_connection_folder: list,
                            multi_time_start: list,
                            multi_time_duration: list):
    
    output_folder = get_output_folder('seeg')
    
    multi_mean_connections_per_edge = []
    multi_mean_lags_per_edge = []
    
    multi_median_connections_per_edge = []
    multi_median_lags_per_edge = []   
    
    multi_std_connections_per_edge = []
    multi_std_lags_per_edge = []  
    
    multi_iqr_connections_per_edge = []
    multi_iqr_lags_per_edge = []  
    
    print('Loading...')
    
    for legend, group, connection_folder, signal_length, time_start, time_duration, work_signal, sampling_frequency in\
        zip(multi_legend, multi_group, multi_connection_folder, multi_signal_length, multi_time_start, multi_time_duration, multi_work_signal, multi_sampling_frequency):

        print('Loading connectivity data from', legend, group)
        
        time_windows = np.load(connection_folder + 'time_windows.npz')['data']
            
        _, _, window_time_start, window_time_end, _ =\
            get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal, signal_length)
        
        connections_per_edge =\
            np.load(connection_folder + 'connections_per_edge.npz')['data'][:, window_time_start:window_time_end]
        lags_per_edge =\
            np.load(connection_folder + 'lags_per_edge.npz')['data'][:, window_time_start:window_time_end]
        
        multi_mean_connections_per_edge.append(np.mean(connections_per_edge))
        multi_mean_lags_per_edge.append(np.mean(lags_per_edge))
        
        multi_median_connections_per_edge.append(np.median(connections_per_edge))
        multi_median_lags_per_edge.append(np.median(lags_per_edge))
        
        multi_std_connections_per_edge.append(np.std(connections_per_edge))
        multi_std_lags_per_edge.append(np.std(lags_per_edge))
        
        multi_iqr_connections_per_edge.append(np.subtract(*np.percentile(connections_per_edge, [75, 25])))
        multi_iqr_lags_per_edge.append(np.subtract(*np.percentile(lags_per_edge, [75, 25])))
        
    multi_multi_data = [multi_mean_connections_per_edge,
                        multi_mean_lags_per_edge,
                        multi_median_connections_per_edge,
                        multi_median_lags_per_edge,
                        multi_std_connections_per_edge,
                        multi_std_lags_per_edge,
                        multi_iqr_connections_per_edge,
                        multi_iqr_lags_per_edge]
    
    multi_data_ylabel = ['mean_connection_magnitude',
                         'mean_connection_lag',
                         'median_connection_magnitude',
                         'median_connection_lag',
                         'std_connection_magnitude',
                         'std_connection_lag',
                         'iqr_connection_magnitude',
                         'iqr_connection_lag']
    
    unique_legends = []
    unique_groups = []
    
    for legend in multi_legend:
        if legend not in unique_legends:
            unique_legends.append(legend)
    for group in multi_group:
        if group not in unique_groups:
            unique_groups.append(group)
        
    for multi_data, ylabel in\
        zip(multi_multi_data,
            multi_data_ylabel):
        
        norm_value_per_group = []
        
        for group in unique_groups:
            
            norm_value_per_group.append(0)
            
            alpha = 0
            
            for data, legend, group_1 in zip(multi_data, multi_legend, multi_group):
                
                if legend == 'AWAKE' and group_1 == group:
                    
                    norm_value_per_group[-1] += data
                    
                    alpha += 1
                    
            norm_value_per_group[-1] /= alpha
            
        multi_norm = [norm_value_per_group[unique_groups.index(group)] for group in multi_group]            
            
        dataframe = pd.DataFrame.from_dict(\
            get_two_sample_t_test(multi_data,
                                  multi_legend,
                                  multi_group,
                                  confidence_level=95,
                                  alternative='greater',
                                  multi_norm=multi_norm))
        
        pathlib.Path(output_folder + 'connection/').mkdir(parents=True, exist_ok=True)
        
        dataframe.to_excel(output_folder + 'connection/' + ylabel + '_t_test.xlsx', index=False)
    