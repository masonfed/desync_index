from manage_signal_data.load_signal_data import load_work_signal
from analyze_seeg_features.compute_functions.compute_seeg_energy import compute_seeg_energy
from analyze_seeg_features.compute_functions.compute_seeg_connection import compute_seeg_connection
from analyze_seeg_features.compute_functions.compute_seeg_connection_alarm import compute_seeg_connection_alarm
from analyze_seeg_features.compute_functions.compute_seeg_desync_epindex import compute_seeg_desync_epindex
from analyze_seeg_features.compute_functions.compute_seeg_graph import compute_seeg_graph
from analyze_seeg_features.compute_functions.compute_seeg_bartolomei_epindex import compute_seeg_bartolomei_epindex
from analyze_seeg_features.folder_management import *
import numpy as np


def multi_compute_seeg_features(multi_legend: list,
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
                                compute_connection: bool,
                                compute_connection_alarm: bool,
                                compute_desync_epindex: bool,
                                compute_graph: bool,
                                compute_energy: bool,
                                compute_bartolomei_epindex: bool):
    
    print()
            
    for legend, group, patient, epoch, highpass_frequency, lowpass_frequency, notch_frequency, work_montage, window_duration, window_shift,\
        connection_technique, connection_bin_rule, connection_lag, connection_lag_num, alarm_smooth, alarm_baseline, alarm_low_percent, alarm_high_percent, graph_start, graph_base, graph_min, graph_max,\
            energy_low_freqs, energy_high_freqs, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity in\
                zip(multi_legend, multi_group, multi_patient, multi_epoch, multi_highpass_frequency, multi_lowpass_frequency, multi_notch_frequency, multi_work_montage, multi_window_duration, multi_window_shift,\
                    multi_connection_technique, multi_connection_bin_rule, multi_connection_lag, multi_connection_lag_num, multi_alarm_smooth, multi_alarm_baseline, multi_alarm_low_percent, multi_alarm_high_percent, multi_graph_start, multi_graph_base, multi_graph_min, multi_graph_max,\
                        multi_energy_low_freqs, multi_energy_high_freqs, multi_epindex_base, multi_epindex_start, multi_epindex_end, multi_epindex_bias, multi_epindex_threshold, multi_epindex_decay, multi_epindex_tonicity):
        
        print('Working on: ', legend, group, patient, epoch)        
        print()
        
        try:
        
            patient_folder = get_seeg_patient_folder(patient)
                
            signal_folder = get_signal_folder(patient_folder,
                                            epoch,
                                            highpass_frequency,
                                            lowpass_frequency,
                                            notch_frequency)
        
            work_signal, work_channels, sampling_frequency =\
                load_work_signal('seeg',
                                patient,
                                epoch,
                                work_montage,
                                highpass_frequency=highpass_frequency,
                                lowpass_frequency=lowpass_frequency,
                                notch_frequency=notch_frequency)
            
            window_folder = get_window_folder(signal_folder,
                                            work_montage,
                                            window_duration,
                                            window_shift)

            compute_features(signal_folder,
                             window_folder,
                             work_signal,
                             work_channels,
                             sampling_frequency,
                             window_duration,
                             window_shift,
                             connection_technique,
                             connection_bin_rule,
                             connection_lag,
                             connection_lag_num,
                             alarm_smooth,
                             alarm_baseline,
                             alarm_low_percent,
                             alarm_high_percent,
                             graph_start,
                             graph_base,
                             graph_min,
                             graph_max,
                             energy_low_freqs,
                             energy_high_freqs,
                             epindex_base,
                             epindex_start,
                             epindex_end,                            
                             epindex_bias,                            
                             epindex_threshold,
                             epindex_decay,
                             epindex_tonicity,
                             compute_connection,
                             compute_connection_alarm,
                             compute_desync_epindex,
                             compute_graph,
                             compute_energy,
                             compute_bartolomei_epindex)
        
        except:
            
            print('#################################################################')            
            print('#################### Computation failed #########################')
            print('#################################################################')

        print()


def compute_seeg_features(patient: str,
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
                          epindex_bias: float,
                          epindex_base: float,
                          epindex_start: float,
                          epindex_end: float,
                          epindex_threshold: float,
                          epindex_decay: float,
                          epindex_tonicity: float,
                          compute_connection: bool,
                          compute_connection_alarm: bool,
                          compute_desync_epindex: bool,
                          compute_graph: bool,
                          compute_energy: bool,
                          compute_bartolomei_epindex: bool):
    
    work_signal, work_channels, sampling_frequency =\
        load_work_signal('seeg',
                         patient,
                         epoch,
                         work_montage,
                         highpass_frequency,
                         lowpass_frequency,
                         notch_frequency)
    
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
    
    compute_features(signal_folder,
                     window_folder,
                     work_signal,
                     work_channels,
                     sampling_frequency,
                     window_duration,
                     window_shift,
                     connection_technique,
                     connection_bin_rule,
                     connection_lag,
                     connection_lag_num,
                     alarm_smooth,
                     alarm_baseline,
                     alarm_low_percent,
                     alarm_high_percent,
                     graph_start,
                     graph_base,
                     graph_min,
                     graph_max,
                     energy_low_freqs,
                     energy_high_freqs,
                     epindex_bias,
                     epindex_base,
                     epindex_start,
                     epindex_end,
                     epindex_threshold,
                     epindex_decay,
                     epindex_tonicity,
                     compute_connection,
                     compute_connection_alarm,
                     compute_desync_epindex,
                     compute_graph,
                     compute_energy,
                     compute_bartolomei_epindex)
    
    
def compute_features(signal_folder: str,
                     window_folder: str,
                     work_signal: np.ndarray,
                     work_channels: list,
                     sampling_frequency: int,
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
                     compute_connection: bool,
                     compute_connection_alarm: bool,
                     compute_desync_epindex: bool,
                     compute_graph: bool,
                     compute_energy: bool,
                     compute_bartolomei_epindex: bool):
    
    connection_folder = get_connection_folder(window_folder, connection_technique, connection_bin_rule, connection_lag, connection_lag_num)  
    connection_alarm_folder = get_connection_alarm_folder(connection_folder, alarm_smooth, alarm_baseline, alarm_low_percent, alarm_high_percent) 
    sync_epindex_folder = get_epindex_folder(connection_alarm_folder, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity) + 'sync/' 
    desync_epindex_folder = get_epindex_folder(connection_alarm_folder, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity) + 'desync/' 
    graph_folder = get_graph_folder(connection_folder, graph_start, graph_base, graph_min, graph_max)
    energy_folder = get_energy_folder(window_folder, energy_low_freqs, energy_high_freqs)
    bartolomei_epindex_folder = get_epindex_folder(energy_folder, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity)    
    connection_energy_folder = get_energy_folder(connection_alarm_folder, energy_low_freqs, energy_high_freqs)
    fusion_epindex_folder = get_epindex_folder(connection_energy_folder, epindex_base, epindex_start, epindex_end, epindex_bias, epindex_threshold, epindex_decay, epindex_tonicity)

    
    if compute_connection:
        
        compute_seeg_connection(signal_folder, 
                                connection_folder,
                                work_signal,
                                work_channels,
                                sampling_frequency,
                                window_duration,
                                window_shift,
                                connection_technique,
                                connection_bin_rule,
                                connection_lag,
                                connection_lag_num)
        
    if compute_connection_alarm:
        
        compute_seeg_connection_alarm(connection_folder,
                                      connection_alarm_folder,
                                      window_shift,
                                      alarm_smooth,
                                      alarm_baseline,
                                      alarm_low_percent,
                                      alarm_high_percent)
        
    if compute_desync_epindex:
        
        compute_seeg_desync_epindex(connection_folder,
                                    connection_alarm_folder,
                                    desync_epindex_folder,
                                    window_shift,
                                    alarm_baseline,
                                    epindex_base,
                                    epindex_start,
                                    epindex_end,
                                    epindex_bias,
                                    epindex_threshold,
                                    epindex_decay,
                                    epindex_tonicity,
                                    work_channels)
        
    if compute_graph:
        
        compute_seeg_graph(connection_folder,
                           graph_folder,
                           window_shift,
                           connection_technique,
                           graph_start,
                           graph_base,
                           graph_min,
                           graph_max)        
    
    if compute_energy:
        
        compute_seeg_energy(energy_folder,
                            work_signal,
                            sampling_frequency,
                            window_duration,
                            window_shift,
                            energy_low_freqs,
                            energy_high_freqs)
        
        
        
    if compute_bartolomei_epindex:
        
        compute_seeg_bartolomei_epindex(energy_folder,
                                        bartolomei_epindex_folder,
                                        window_shift,
                                        epindex_base,
                                        epindex_start,
                                        epindex_end,
                                        epindex_bias,
                                        epindex_threshold,
                                        epindex_decay,
                                        epindex_tonicity,
                                        work_channels)
