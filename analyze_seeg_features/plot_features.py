from manage_signal_data.load_signal_data import load_work_signal, load_work_channels, load_frequency, load_signal_length
from analyze_seeg_features.plot_functions.plot_seeg_energy import plot_seeg_energy
from analyze_seeg_features.plot_functions.plot_seeg_connection import plot_seeg_connection
from analyze_seeg_features.plot_functions.plot_seeg_connection_alarm import plot_seeg_connection_alarm
from analyze_seeg_features.plot_functions.plot_seeg_channel import plot_seeg_channel
from analyze_seeg_features.plot_functions.plot_seeg_desync_epindex import plot_seeg_desync_epindex
from analyze_seeg_features.plot_functions.plot_seeg_graph import plot_seeg_graph
from analyze_seeg_features.plot_functions.plot_seeg_bartolomei_epindex import plot_seeg_bartolomei_epindex
from analyze_seeg_features.multi_plot_functions.multi_plot_seeg_bartolomei_epindex import multi_plot_seeg_bartolomei_epindex
from analyze_seeg_features.multi_plot_functions.multi_plot_seeg_connection_alarm import multi_plot_seeg_connection_alarm
from analyze_seeg_features.multi_plot_functions.multi_plot_seeg_energy import multi_plot_seeg_energy
from analyze_seeg_features.multi_plot_functions.multi_plot_seeg_connection import multi_plot_seeg_connection
from analyze_seeg_features.multi_plot_functions.multi_plot_seeg_graph import multi_plot_seeg_graph
from analyze_seeg_features.statistic_functions.compare_seeg_connection import compare_seeg_connection
from analyze_seeg_features.statistic_functions.compare_seeg_energy import compare_seeg_energy
from analyze_seeg_features.folder_management import *
import numpy as np
import matplotlib
matplotlib.use('TKAgg')


def multi_plot_seeg_features(multi_legend: list,
                             multi_group: list,
                             multi_patient: list,
                             multi_epoch: list,
                             multi_highpass_frequency: list,
                             multi_lowpass_frequency: list,
                             multi_notch_frequency: list,                             
                             multi_work_montage: list,                                
                             multi_window_duration: list,
                             multi_window_shift: list,
                             multi_connection_technique: list,
                             multi_connection_bin_rule: list,
                             multi_connection_lag: list,
                             multi_connection_lag_num: list,
                             multi_alarm_smooth: list,
                             multi_alarm_baseline: list,
                             multi_alarm_low_percent: list,
                             multi_alarm_high_percent: list,
                             multi_graph_start: list,
                             multi_graph_base: list,
                             multi_graph_min: list,
                             multi_graph_max: list,
                             multi_energy_low_freqs: list,
                             multi_energy_high_freqs: list,
                             multi_epindex_base: list,
                             multi_epindex_start: list,
                             multi_epindex_end: list,
                             multi_epindex_bias: list,
                             multi_epindex_threshold: list,
                             multi_epindex_decay: list,
                             multi_epindex_tonicity: list,
                             multi_source_channel: list,
                             multi_target_channel: list,
                             multi_time_start: list,
                             multi_time_duration: list,
                             plot_connection: bool,
                             plot_channel: bool,
                             plot_connection_alarm: bool,                         
                             plot_desync_epindex: bool,
                             plot_graph: bool,
                             plot_energy: bool,
                             plot_bartolomei_epindex: bool,
                             compare_statistic: bool, 
                             max_plot_num: int,
                             plot_montage: str):
    
    configuration_num = len(multi_legend)
    
    unique_signal = len(np.unique(multi_patient)) == 1 and\
        len(np.unique(multi_epoch)) == 1 and len(np.unique(multi_work_montage)) == 1 and\
            len(np.unique([x for x in multi_lowpass_frequency if x is not None])) <= 1 and\
                len(np.unique([x for x in multi_highpass_frequency if x is not None])) <= 1 and\
                    len(np.unique([x for x in multi_notch_frequency if x is not None])) <= 1
            
    if unique_signal:
        
        patient_folder = get_seeg_patient_folder(multi_patient[0])
        
        signal_folder = get_signal_folder(patient_folder,
                                          multi_epoch[0],
                                          multi_highpass_frequency[0],
                                          multi_lowpass_frequency[0],
                                          multi_notch_frequency[0])
        
        work_signal, work_channels, sampling_frequency =\
            load_work_signal('seeg',
                             multi_patient[0],
                             multi_epoch[0],
                             multi_work_montage[0],
                             highpass_frequency=multi_highpass_frequency[0],
                             lowpass_frequency=multi_lowpass_frequency[0],                                                                     
                             notch_frequency=multi_notch_frequency[0])
            
        multi_signal_length = [len(work_signal[0]) for _ in range(configuration_num)]        
        multi_patient_folder = [patient_folder for _ in range(configuration_num)]
        multi_signal_folder = [signal_folder for _ in range(configuration_num)]
        multi_work_signal = [work_signal for _ in range(configuration_num)]
        multi_work_channels= [work_channels for _ in range(configuration_num)]
        multi_sampling_frequency = [sampling_frequency for _ in range(configuration_num)]
        
    else:
        
        multi_signal_length = []
        multi_patient_folder = []
        multi_signal_folder = []
        multi_work_signal = []
        multi_work_channels = []
        multi_sampling_frequency = []
        
        for patient, epoch, work_montage, highpass, lowpass, notch in\
            zip(multi_patient, multi_epoch, multi_work_montage, multi_highpass_frequency, multi_lowpass_frequency, multi_notch_frequency):
            
            patient_folder = get_seeg_patient_folder(patient)
            signal_folder = get_signal_folder(patient_folder, epoch, highpass, lowpass, notch)
            
            signal_length = load_signal_length('seeg',
                                                patient,
                                                epoch)
            
            work_channels = load_work_channels('seeg',
                                               patient,
                                               epoch,
                                               work_montage)
            
            sampling_frequency = load_frequency('seeg',
                                                patient,
                                                epoch)
            
            multi_signal_length.append(signal_length)
            multi_patient_folder.append(patient_folder)
            multi_signal_folder.append(signal_folder)
            multi_work_signal.append(None)
            multi_work_channels.append( work_channels)
            multi_sampling_frequency.append(sampling_frequency)
    
    multi_window_folder = [get_window_folder(signal_folder, work_montage, window_duration, window_shift)\
        for signal_folder, work_montage, window_duration, window_shift in zip(multi_signal_folder, multi_work_montage, multi_window_duration, multi_window_shift)]
    multi_connection_folder = [get_connection_folder(window_folder, connection_technique, connection_bin_rule, connection_lag, connection_lag_num)\
        for window_folder, connection_technique, connection_bin_rule, connection_lag, connection_lag_num in zip(multi_window_folder, multi_connection_technique, multi_connection_bin_rule, multi_connection_lag, multi_connection_lag_num)]          
    multi_connection_alarm_folder = [get_connection_alarm_folder(connection_folder, alarm_smooth, alarm_baseline, alarm_low_percent, alarm_high_percent)\
        for connection_folder, alarm_smooth, alarm_baseline, alarm_low_percent, alarm_high_percent in zip(multi_connection_folder, multi_alarm_smooth, multi_alarm_baseline, multi_alarm_low_percent, multi_alarm_high_percent)]
    multi_desync_epindex_folder = [get_epindex_folder(connection_alarm_folder, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity) + 'desync/'\
        for connection_alarm_folder, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity in zip(multi_connection_alarm_folder, multi_epindex_base, multi_epindex_start, multi_epindex_end, multi_epindex_bias, multi_epindex_threshold, multi_epindex_decay, multi_epindex_tonicity)]   
    multi_graph_folder = [get_graph_folder(connection_folder, graph_start, graph_base, graph_min, graph_max)\
        for connection_folder, graph_start, graph_base, graph_min, graph_max in zip(multi_connection_folder, multi_graph_start, multi_graph_base, multi_graph_min, multi_graph_max)]
    multi_energy_folder = [get_energy_folder(window_folder, energy_low_freqs, energy_high_freqs)\
        for window_folder, energy_low_freqs, energy_high_freqs in zip(multi_window_folder, multi_energy_low_freqs, multi_energy_high_freqs)]
    multi_bartolomei_epindex_folder = [get_epindex_folder(energy_folder, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity)\
        for energy_folder, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity in zip(multi_energy_folder, multi_epindex_base, multi_epindex_start, multi_epindex_end, multi_epindex_bias, multi_epindex_threshold, multi_epindex_decay, multi_epindex_tonicity)]

    if compare_statistic:
            
        print('Comparing statistic values!')
    
    if plot_bartolomei_epindex:
        
        multi_plot_seeg_bartolomei_epindex(multi_legend,
                                           multi_group,
                                           multi_energy_folder,
                                           multi_bartolomei_epindex_folder,
                                           multi_patient,
                                           multi_work_signal,
                                           multi_work_channels,
                                           multi_sampling_frequency,
                                           multi_window_duration,
                                           multi_window_shift,
                                           multi_epindex_start,
                                           multi_time_start,
                                           multi_time_duration,
                                           unique_signal,
                                           max_plot_num,
                                           plot_montage)
        
    elif plot_energy:
        
        if compare_statistic:
            
            compare_seeg_energy(multi_legend,
                        multi_group,
                        multi_work_signal,
                        multi_sampling_frequency,
                        multi_energy_folder,
                        multi_time_start,
                        multi_time_duration)
        else:
        
            multi_plot_seeg_energy(multi_legend,
                                multi_group,
                                multi_patient,
                                multi_work_signal,
                                multi_work_channels,
                                multi_sampling_frequency,
                                multi_energy_folder,
                                multi_time_start,
                                multi_time_duration,
                                unique_signal,
                                max_plot_num,
                                plot_montage)
            
    elif plot_connection:
        
        if compare_statistic:
        
            compare_seeg_connection(multi_legend,
                                    multi_group,
                                    multi_work_signal,
                                    multi_signal_length,
                                    multi_sampling_frequency,
                                    multi_connection_folder,
                                    multi_time_start,
                                    multi_time_duration)
            
        else:
        
            multi_plot_seeg_connection(multi_legend,
                                       multi_group,
                                       multi_patient,
                                       multi_work_signal,
                                       multi_work_channels,
                                       multi_sampling_frequency,
                                       multi_signal_length,
                                       multi_connection_folder,
                                       multi_time_start,
                                       multi_time_duration,
                                       unique_signal,
                                       max_plot_num,
                                       plot_montage)
        
    elif plot_graph:
        
        multi_plot_seeg_graph(multi_legend,
                              multi_group,
                              multi_patient,
                              multi_work_signal,
                              multi_work_channels,
                              multi_sampling_frequency,
                              multi_connection_folder,
                              multi_graph_folder,
                              multi_time_start,
                              multi_time_duration,
                              unique_signal,
                              max_plot_num,
                              plot_montage)
        
    elif plot_connection_alarm:
        
        multi_plot_seeg_connection_alarm(multi_legend,
                                         multi_group,
                                         multi_connection_folder,
                                         multi_connection_alarm_folder,
                                         multi_patient,
                                         multi_work_signal,
                                         multi_work_channels,
                                         multi_sampling_frequency,
                                         multi_window_duration,
                                         multi_window_shift,
                                         multi_time_start,
                                         multi_time_duration,
                                         unique_signal,
                                         max_plot_num,
                                         plot_montage)
    
    else:
        
        raise ValueError


def plot_seeg_features(patient: str,
                       epoch: str,
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
                       alarm_smooth: float,
                       alarm_baseline: float,
                       alarm_low_percent: float,
                       alarm_high_percent: float,
                       graph_start: float,
                       graph_base: float,
                       graph_min: float,
                       graph_max: float,
                       energy_low_freqs: list,
                       energy_high_freqs: list,
                       epindex_base: float,
                       epindex_start: float,
                       epindex_end: float,
                       epindex_bias: float,
                       epindex_threshold: float,
                       epindex_decay: float,
                       epindex_tonicity: float,
                       source_channel: str,
                       target_channel: str,
                       time_start: float,
                       time_duration: float,
                       plot_connection: bool,
                       plot_channel: bool,
                       plot_connection_alarm: bool,
                       plot_desync_epindex: bool,
                       plot_graph: bool,
                       plot_energy: bool,
                       plot_bartolomei_epindex: bool,
                       max_plot_num: int,
                       plot_montage: str):
    
    patient_folder = get_seeg_patient_folder(patient)
    
    signal_folder = get_signal_folder(patient_folder,
                                      epoch,
                                      highpass_frequency,
                                      lowpass_frequency,
                                      notch_frequency)

    window_folder = get_window_folder(signal_folder,
                                      work_montage,
                                      window_duration,
                                      window_shift)
    
    connection_folder = get_connection_folder(window_folder, connection_technique, connection_bin_rule,
                                              connection_lag, connection_lag_num)  
    
    connection_alarm_folder = get_connection_alarm_folder(connection_folder, alarm_smooth, alarm_baseline,
                                                          alarm_low_percent, alarm_high_percent)
    
    desync_epindex_folder = get_epindex_folder(connection_alarm_folder, epindex_base, epindex_start, epindex_end, epindex_bias,
                                               epindex_threshold, epindex_decay, epindex_tonicity) + 'desync/'
    
    graph_folder = get_graph_folder(connection_folder, graph_start, graph_base, graph_min, graph_max)
    
    energy_folder = get_energy_folder(window_folder, energy_low_freqs, energy_high_freqs)
    
    bartolomei_epindex_folder = get_epindex_folder(energy_folder, epindex_base, epindex_start, epindex_end, epindex_bias,
                                                   epindex_threshold, epindex_decay, epindex_tonicity)
    
    connection_energy_folder = get_energy_folder(connection_alarm_folder, energy_low_freqs, energy_high_freqs)

    work_signal, work_channels, sampling_frequency =\
        load_work_signal('seeg',
                         patient,
                         epoch,
                         work_montage,
                         highpass_frequency=highpass_frequency,
                         lowpass_frequency=lowpass_frequency,
                         notch_frequency=notch_frequency)
    
    
    if plot_connection:
        
        plot_seeg_connection(connection_folder,
                             patient,
                             work_signal,
                             work_channels,
                             sampling_frequency,
                             connection_lag_num,
                             time_start,
                             time_duration,
                             max_plot_num,
                             plot_montage)
        
    if plot_channel:
        
        plot_seeg_channel(energy_folder,
                          connection_folder,
                          connection_alarm_folder,
                          patient,
                          work_signal,
                          work_channels,
                          sampling_frequency,
                          window_duration,
                          window_shift,
                          source_channel,
                          target_channel,
                          time_start,
                          time_duration,
                          max_plot_num,
                          plot_montage)
        
    if plot_connection_alarm:
        
        plot_seeg_connection_alarm(connection_folder,
                                   connection_alarm_folder,
                                   patient,
                                   work_signal,
                                   work_channels,
                                   sampling_frequency,
                                   time_start,
                                   time_duration,
                                   max_plot_num,
                                   plot_montage)
        
    if plot_desync_epindex:
        
        plot_seeg_desync_epindex(connection_folder,
                                 connection_alarm_folder,
                                 desync_epindex_folder,
                                 patient,
                                 work_signal,
                                 work_channels,
                                 sampling_frequency,
                                 epindex_start,
                                 epindex_base,
                                 time_start,
                                 time_duration,
                                 max_plot_num,
                                 plot_montage)    
        
    if plot_graph:
        
        plot_seeg_graph(connection_folder, 
                        graph_folder,
                        patient,
                        work_signal,
                        work_channels,
                        sampling_frequency,
                        time_start,
                        time_duration,
                        max_plot_num,
                        plot_montage)
    
    if plot_energy:
        
        plot_seeg_energy(energy_folder,
                         patient,
                         work_signal,
                         work_channels,
                         sampling_frequency,
                         window_duration,
                         window_shift,
                         time_start,
                         time_duration,
                         max_plot_num,
                         plot_montage,
                         source_channel)
        
        
        
    if plot_bartolomei_epindex:
        
        plot_seeg_bartolomei_epindex(energy_folder,
                                     bartolomei_epindex_folder,
                                     patient,
                                     work_signal,
                                     work_channels,
                                     sampling_frequency,
                                     epindex_start,
                                     epindex_base,
                                     time_start,
                                     time_duration,      
                                     max_plot_num,
                                     plot_montage)