from utilities.folder_management import get_patient_folder


def get_seeg_patient_folder(patient: str):

    patient_folder = get_patient_folder('seeg', patient)
        
    return patient_folder


def get_signal_folder(patient_folder: str,
                      epoch: str,
                      highpass_frequency: int,
                      lowpass_frequency: int,
                      notch_frequency: int):
        
    signal_folder = patient_folder + 'features/' + epoch + '/'
    
    filter_folder = ''
    
    if lowpass_frequency is not None:
        
        filter_folder += '_low=' + str(lowpass_frequency)
        
    if highpass_frequency is not None:
        
        filter_folder += '_high=' + str(highpass_frequency)
        
    if notch_frequency is not None:
        filter_folder += '_notch=' + str(notch_frequency)
        
    signal_folder += filter_folder[1:] + '/'
    
    if signal_folder[-2] == '/':
        signal_folder = signal_folder[:-1]
        
    return signal_folder


def get_window_folder(signal_folder: str,
                      work_montage: str,
                      window_duration: float,
                      window_shift: float):
        
    window_folder = signal_folder + 'montage=' + work_montage + '/duration=' +\
        str(window_duration) + '/shift=' + str(window_shift) + '/' 
        
    return window_folder


def get_connection_folder(window_folder: str,
                          connection_dataset: str,
                          connection_bin_rule: str,
                          connection_lag: float,
                          connection_lag_num: int):
    
    connection_folder = window_folder + 'connection=' + str(connection_dataset) +\
        '/rule=' + str(connection_bin_rule) + '/lag=' + str(connection_lag) +\
            '/lag_num=' + str(connection_lag_num) + '/'
        
    return connection_folder


def get_connection_alarm_folder(connection_folder: str,
                                smooth: float,
                                baseline: float,
                                low_percent: float,
                                high_percent: float):
    
    connection_alarm_folder = connection_folder + 'smooth=' + str(smooth) +\
        '/base=' + str(baseline) + '/low=' + str(low_percent) + '/high=' + str(high_percent) + '/'
        
    return connection_alarm_folder


def get_graph_folder(connection_folder: str,
                     graph_start: float,
                     graph_base: float,
                     graph_min: float,
                     graph_max: float):
    
    graph_folder = connection_folder + 'start=' + str(graph_start) + '/base=' + str(graph_base) +\
        '/min=' + str(graph_min) + '/max=' + str(graph_max) + '/'
        
    return graph_folder


def get_energy_folder(window_folder: str,
                      energy_low_freqs: list,
                      energy_high_freqs: list):
    
    energy_folder = window_folder + 'low=' + str(energy_low_freqs) + '/high=' + str(energy_high_freqs) + '/'
        
    return energy_folder


def get_epindex_folder(mother_folder: str,
                       epindex_base: float,
                       epindex_start: float,
                       epindex_end: float,
                       epindex_bias: float,
                       epindex_threshold: float,
                       epindex_decay: float,
                       epindex_tonicity: float):
    
    epindex_folder = mother_folder + 'epindex/base=' + str(epindex_base) +\
        '/start=' + str(epindex_start) + '/end=' + str(epindex_end) +\
            '/bias=' + str(epindex_bias) + '/thr=' + str(epindex_threshold) +\
                '/decay=' + str(epindex_decay) + '/ton=' + str(epindex_tonicity) + '/'
                
    return epindex_folder