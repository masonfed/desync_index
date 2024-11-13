from analyze_seeg_features.folder_management import *
from utilities.signal.time import get_times
from utilities.statistic.t_test import get_two_sample_t_test
from utilities.folder_management import get_output_folder
from utilities.plot.general import *
import pandas as pd
import numpy as np
import pathlib


def compare_seeg_energy(multi_legend: list,
                        multi_group: list,
                        multi_work_signal: list,
                        multi_sampling_frequency: list,
                        multi_energy_folder: list,
                        multi_time_start: list,
                        multi_time_duration: list):
    
    output_folder = get_output_folder('seeg')
        
    multi_mean_energy_ratios_per_channel = []
    multi_mean_energies_per_channel = []    
    multi_mean_initial_phase_entropies_per_channel = []
    multi_mean_instant_phase_entropies_per_channel = []
    
    multi_median_energy_ratios_per_channel = []
    multi_median_energies_per_channel = []    
    multi_median_initial_phase_entropies_per_channel = []
    multi_median_instant_phase_entropies_per_channel = []
    
    multi_std_energy_ratios_per_channel = []
    multi_std_energies_per_channel = []    
    multi_std_initial_phase_entropies_per_channel = []
    multi_std_instant_phase_entropies_per_channel = []
    
    multi_iqr_energy_ratios_per_channel = []
    multi_iqr_energies_per_channel = []    
    multi_iqr_initial_phase_entropies_per_channel = []
    multi_iqr_instant_phase_entropies_per_channel = []
    
    print('Loading...')
    
    for legend, group, energy_folder, time_start, time_duration, work_signal, sampling_frequency in\
        zip(multi_legend, multi_group, multi_energy_folder, multi_time_start, multi_time_duration,
            multi_work_signal, multi_sampling_frequency):
            
        print('Loading emergy data from', legend, group)

        time_windows = np.load(energy_folder + 'time_windows.npz')['data']
        
        _, _, window_time_start, window_time_end, _ =\
            get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
        
        energy_ratios_per_channel =\
            np.load(energy_folder + 'energy_ratios_per_channel.npz')['data'][:, window_time_start:window_time_end]
        energies_per_channel =\
            np.load(energy_folder + 'energies_per_channel.npz')['data'][:, window_time_start:window_time_end]
        instant_phase_entropies_per_channel =\
            np.load(energy_folder + 'instant_phase_entropies_per_channel.npz')['data'][:, window_time_start:window_time_end]
        initial_phase_entropies_per_channel =\
            np.load(energy_folder + 'initial_phase_entropies_per_channel.npz')['data'][:, window_time_start:window_time_end]

        multi_mean_energy_ratios_per_channel.append(np.mean(energy_ratios_per_channel))
        multi_mean_energies_per_channel.append(np.mean(energies_per_channel))
        multi_mean_instant_phase_entropies_per_channel.append(np.mean(instant_phase_entropies_per_channel))
        multi_mean_initial_phase_entropies_per_channel.append(np.mean(initial_phase_entropies_per_channel))
        
        multi_median_energy_ratios_per_channel.append(np.median(energy_ratios_per_channel))
        multi_median_energies_per_channel.append(np.median(energies_per_channel))
        multi_median_instant_phase_entropies_per_channel.append(np.median(instant_phase_entropies_per_channel))
        multi_median_initial_phase_entropies_per_channel.append(np.median(initial_phase_entropies_per_channel))
        
        multi_std_energy_ratios_per_channel.append(np.std(energy_ratios_per_channel))
        multi_std_energies_per_channel.append(np.std(energies_per_channel))
        multi_std_instant_phase_entropies_per_channel.append(np.std(instant_phase_entropies_per_channel))
        multi_std_initial_phase_entropies_per_channel.append(np.std(initial_phase_entropies_per_channel))
        
        multi_iqr_energy_ratios_per_channel.append(np.subtract(*np.percentile(energy_ratios_per_channel, [75, 25])))
        multi_iqr_energies_per_channel.append(np.subtract(*np.percentile(energies_per_channel, [75, 25])))
        multi_iqr_instant_phase_entropies_per_channel.append(np.subtract(*np.percentile(instant_phase_entropies_per_channel, [75, 25])))
        multi_iqr_initial_phase_entropies_per_channel.append(np.subtract(*np.percentile(initial_phase_entropies_per_channel, [75, 25])))
        
    multi_multi_data = [multi_mean_energy_ratios_per_channel,
                        multi_mean_energies_per_channel,
                        multi_mean_initial_phase_entropies_per_channel,
                        multi_mean_instant_phase_entropies_per_channel,
                        multi_median_energy_ratios_per_channel,
                        multi_median_energies_per_channel,
                        multi_median_initial_phase_entropies_per_channel,
                        multi_median_instant_phase_entropies_per_channel,
                        multi_std_energy_ratios_per_channel,
                        multi_std_energies_per_channel,
                        multi_std_initial_phase_entropies_per_channel,
                        multi_std_instant_phase_entropies_per_channel,
                        multi_iqr_energy_ratios_per_channel,
                        multi_iqr_energies_per_channel,
                        multi_iqr_initial_phase_entropies_per_channel,
                        multi_iqr_instant_phase_entropies_per_channel]
    
    multi_data_ylabel = ['mean_energy_ratio',
                         'mean_energy', 
                         'mean_initial_phase_entropy',
                         'mean_instant_phase_entropy',
                         'median_energy_ratio',
                         'median_energy', 
                         'median_initial_phase_entropy',
                         'median_instant_phase_entropy',
                         'std_energy_ratio',
                         'std_energy', 
                         'std_initial_phase_entropy',
                         'std_instant_phase_entropy',
                         'iqr_energy_ratio',
                         'iqr_energy', 
                         'iqr_initial_phase_entropy',
                         'iqr_instant_phase_entropy']
    
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
        
        pathlib.Path(output_folder + 'energy/').mkdir(parents=True, exist_ok=True)
        
        dataframe.to_excel(output_folder + 'energy/' + ylabel + '_t_test.xlsx', index=False)
