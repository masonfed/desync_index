from utilities.math.entropy import get_entropy, get_digital_entropy, get_bin_num, get_sturges_bin_num
from multiprocessing import Pool
from multiprocessing import cpu_count
import numpy as np
import scipy
import pathlib
import shutil
import timeit


def compute_channel_connections(phase_folder: str,
                                connection_technique: str,
                                connection_bin_rule: str,
                                signal_per_node: list, 
                                network_nodes: list,
                                missing_node_indexes: list,
                                network_edges: list,
                                missing_edge_indexes: list,
                                window_number: int,
                                sample_window_shift: float,
                                sample_window_duration: int,
                                sample_lags: list,
                                weights_per_edge: list,
                                lags_per_edge: list):
    
    cpu_num = cpu_count() - 1
    pool = Pool(processes=cpu_num)  
    
    if connection_technique == 'dpte' or\
        connection_technique == 'pte' or\
            connection_technique == 'pli':
        
        print('Computing phase distribution per node...')
        
        job_num = len(missing_node_indexes)
        job_a_index, job_b_index = 0, np.min((cpu_num*5, job_num))
    
        pathlib.Path(phase_folder).mkdir(parents=True, exist_ok=True)
        
        while job_a_index < job_num:
            
            pool_args = []
        
            for node_index in missing_node_indexes[job_a_index:job_b_index]:
                
                pool_args.append((phase_folder,
                                  node_index,
                                  signal_per_node[node_index],
                                  window_number,
                                  sample_window_shift,
                                  sample_window_duration,
                                  sample_lags,
                                  connection_bin_rule))
                
            if connection_technique == 'dpte':
            
                pool.starmap(compute_channel_digital_phases, pool_args)
                
            else:
                
                pool.starmap(compute_channel_phases, pool_args)
            
            job_a_index = job_b_index
            job_b_index = np.min((job_b_index + cpu_num*5, job_num))
            
    job_num = len(missing_edge_indexes)
    job_a_index, job_b_index = 0, np.min((cpu_num*5, job_num))
    
    print('Compunting connectivity for', job_num, 'edges...')
    
    job_start = timeit.default_timer()
    
    while job_a_index < job_num:
        
        pool_args = []

        for edge_index in missing_edge_indexes[job_a_index:job_b_index]:
        
            edge = network_edges[edge_index]
        
            if connection_technique == 'dpte' or\
                connection_technique == 'pte' or\
                    connection_technique == 'pli':

                source_channel, target_channel = edge[0], edge[1]
                source_channel_index, target_channel_index = network_nodes.index(source_channel), network_nodes.index(target_channel)
                
                source_phases = np.load(phase_folder + 'phases_per_lag_' + str(source_channel_index) + '.npz')['data'][0]
                target_phases_per_lag = np.load(phase_folder + 'phases_per_lag_' + str(target_channel_index) + '.npz')['data']
                source_bin_nums = np.load(phase_folder + 'bin_nums_per_lag_' + str(source_channel_index) + '.npz')['data'][0]
                target_bin_nums_per_lag = np.load(phase_folder + 'bin_nums_per_lag_' + str(target_channel_index) + '.npz')['data']
                
                if connection_technique == 'dpte' or\
                    connection_technique == 'pte':
                    
                    pool_args.append((source_phases,
                                      source_bin_nums,
                                      target_phases_per_lag,
                                      target_bin_nums_per_lag,
                                      sample_lags))
                
                else:
                    
                    pool_args.append((source_phases,
                                      target_phases_per_lag,
                                      sample_lags))
            
            elif connection_technique == 'pearson':
                
                source_channel, target_channel = edge[0], edge[1]
                source_channel_index, target_channel_index = network_nodes.index(source_channel), network_nodes.index(target_channel)                
                source_signal, target_signal = signal_per_node[source_channel_index], signal_per_node[target_channel_index]

                pool_args.append((source_signal,
                                  target_signal,
                                  window_number,
                                  sample_window_shift,
                                  sample_window_duration,
                                  sample_lags))
            
            else:
                
                raise ValueError
                    
        if connection_technique == 'dpte':
            
            pool_results = pool.starmap(compute_edge_dpte, pool_args)
            
        elif connection_technique == 'pte':
            
            pool_results = pool.starmap(compute_edge_pte, pool_args)
            
        elif connection_technique == 'pli':
            
            pool_results = pool.starmap(compute_edge_pli, pool_args)
            
        else:
            
            pool_results = pool.starmap(compute_edge_pearson, pool_args)
            
        for edge_index, results in zip(missing_edge_indexes[job_a_index:job_b_index], pool_results):
            
            weights_per_edge[edge_index].extend(results[0]) 
            lags_per_edge[edge_index].extend(results[1])
            
        job_a_index = job_b_index
        job_b_index = np.min((job_b_index + cpu_num * 5, job_num))
        
        job_end = timeit.default_timer()
        
        time_per_job = (job_end - job_start) / (60 * job_b_index) 
        
        print('Approximate residual time:', round(time_per_job * (job_num - job_b_index), 4), 'min', end='\r')
        
    print('\n')
    
    if connection_technique in ['pte', 'dpte', 'pli']:

        shutil.rmtree(phase_folder)


def compute_channel_phases(phase_folder: str,
                           channel_index: int,
                           signal: np.ndarray,
                           window_number: int,
                           sample_window_shift: int,
                           sample_window_duration: int,
                           sample_lags: list,
                           bin_rule: str):
                
    phases_per_lag = []
    bin_nums_per_lag = []
    
    if bin_rule == 'sturges':
        
        bin_num = get_sturges_bin_num(sample_window_duration)
        
    else:
        
        bin_rule = None
    
    for sample_lag in sample_lags:
        
        phases = []
        bin_nums = []
    
        for i in np.arange(window_number):
            
            window = signal[i*sample_window_shift+sample_lag:i*sample_window_shift+sample_window_duration+sample_lag]
        
            hilb_window_phases = np.angle(scipy.signal.hilbert(window))
            
            phases.append(hilb_window_phases)
            
            if bin_rule != 'sturges':
                
                bin_num = get_bin_num(hilb_window_phases,
                                      len(hilb_window_phases),
                                      2 * np.pi,
                                      bin_rule)
                
            bin_nums.append(bin_num)
            
        phases_per_lag.append(phases)
        bin_nums_per_lag.append(bin_nums)
        
    np.savez_compressed(phase_folder + 'phases_per_lag_' + str(channel_index), data=phases_per_lag)
    np.savez_compressed(phase_folder + 'bin_nums_per_lag_' + str(channel_index), data=bin_nums_per_lag)


def compute_channel_digital_phases(phase_folder: str,
                                   channel_index: int,
                                   signal: np.ndarray,
                                   window_number: int,
                                   sample_window_shift: int,
                                   sample_window_duration: int,
                                   sample_lags: list,
                                   bin_rule: str):        
    
    phases_per_lag = []
    bin_nums_per_lag = []
    
    if bin_rule == 'sturges':
        
        bin_num = get_sturges_bin_num(sample_window_duration)
        
        bins = np.linspace(-np.pi, np.pi, num = bin_num + 1)
        
    else:
        
        bins = None
    
    for sample_lag in sample_lags:
        
        digital_phases = []
        bin_nums = []
    
        for window_index in np.arange(window_number):
            
            window = signal[window_index*sample_window_shift+sample_lag:\
                window_index*sample_window_shift+sample_window_duration+sample_lag]
            
            window -= np.median(window)
            
            fft_window = np.fft.fft(window)
            hilb_window = scipy.signal.hilbert(window)
            
            initial_window_phases = np.angle(fft_window)
            instant_window_phases = np.angle(hilb_window)
            
            if bin_rule != 'sturges':
                
                bin_num = get_bin_num(instant_window_phases,
                                    len(instant_window_phases),
                                    2 * np.pi,
                                    bin_rule)
            
                bins = np.linspace(-np.pi, np.pi, num = bin_num + 1)
                
            digital_phases.append(np.digitize(instant_window_phases, bins) - 1)
                
            bin_nums.append(bin_num)
            
        phases_per_lag.append(digital_phases)
        bin_nums_per_lag.append(bin_nums)
        
    np.savez_compressed(phase_folder + 'phases_per_lag_' + str(channel_index), data=phases_per_lag)
    np.savez_compressed(phase_folder + 'bin_nums_per_lag_' + str(channel_index), data=bin_nums_per_lag)
    
    
def compute_edge_pearson(current_signal: np.ndarray,
                         target_signal: np.ndarray,
                         window_number: int,
                         sample_window_shift: int,
                         sample_window_duration: int,
                         sample_lags: list):
    
    connection_weights, connection_lags = [], []
    
    for window_index in np.arange(window_number):
        
        current_window = current_signal[window_index*sample_window_shift:window_index*sample_window_shift+sample_window_duration]
        normalized_current_window = current_window - np.mean(current_window)
        current_window_std = np.std(current_window)
        
        connection_per_lag = [0]
        
        for sample_lag in sample_lags[1:]:            
            
            target_window = target_signal[window_index*sample_window_shift+sample_lag:window_index*sample_window_shift+sample_window_duration+sample_lag]
            normalized_target_window = target_window - np.mean(target_window)
            target_window_std = np.std(target_window)
            
            connection = np.mean(normalized_current_window * normalized_target_window) / (target_window_std * current_window_std)

            connection_per_lag.append(connection)
            
        best_index = np.argmax(np.abs(connection_per_lag))
        connection_weights.append(connection_per_lag[best_index])
        connection_lags.append(sample_lags[best_index])     
    
    return connection_weights, connection_lags

    
def compute_edge_pli(current_phases: list,
                     phases_per_lag: list,
                     sample_lags: list):
    
    connection_weights, connection_lags = [], []
        
    for window_index, current_phase in enumerate(current_phases):
        
        connection_per_lag = [-1]
        
        for lagged_phase in phases_per_lag[1:]:

            connection_per_lag.append(get_phase_lag_index(current_phase, lagged_phase[window_index]))
            
        best_index = np.argmax(connection_per_lag)
        
        connection_weights.append(connection_per_lag[best_index])
        connection_lags.append(sample_lags[best_index])     
    
    return connection_weights, connection_lags

    
def compute_edge_pte(current_phases: list,
                     current_bin_nums: list,
                     phases_per_lag: list,
                     bin_nums_per_lag: list,
                     sample_lags: list):
    
    connection_weights, connection_lags = [], []
    
    window_index = -1
        
    for current_phase, current_bin_num in zip(current_phases, current_bin_nums):
        
        window_index += 1
        
        connection_per_lag = [-1]
        
        target_phases = phases_per_lag[0]
        target_bin_nums = bin_nums_per_lag[0]
        
        for lagged_phases, lagged_bin_nums in zip(phases_per_lag[1:], bin_nums_per_lag[1:]):

            connection_per_lag.append(get_phase_transfer_entropy(current_phase,
                                                                 target_phases[window_index], 
                                                                 lagged_phases[window_index],
                                                                 current_bin_num,
                                                                 target_bin_nums[window_index],
                                                                 lagged_bin_nums[window_index]))
            
        best_index = np.argmax(connection_per_lag)                
        connection_weights.append(connection_per_lag[best_index])
        connection_lags.append(sample_lags[best_index])    
        
        assert best_index > 0 
    
    return connection_weights, connection_lags


def compute_edge_dpte(current_phases: list,
                      current_bin_nums: list,
                      target_phases_per_lag: list,
                      target_bin_nums_per_lag: list,
                      sample_lags: list):
    
    connection_weights, connection_lags = [], []
    
    window_index = -1
        
    for current_phase, current_bin_num in zip(current_phases, current_bin_nums):
        
        window_index += 1
        
        connection_per_lag = [-1]
        
        target_phases = target_phases_per_lag[0]
        target_bin_nums = target_bin_nums_per_lag[0]
        
        for lagged_phase, lagged_bin_nums in zip(target_phases_per_lag[1:], target_bin_nums_per_lag[1:]):

            connection_per_lag.append(get_digital_phase_transfer_entropy(current_phase,
                                                                         target_phases[window_index],
                                                                         lagged_phase[window_index],
                                                                         current_bin_num,
                                                                         target_bin_nums[window_index],
                                                                         lagged_bin_nums[window_index]))
            
        best_index = np.argmax(connection_per_lag)
        connection_weights.append(connection_per_lag[best_index])
        connection_lags.append(sample_lags[best_index])    
        
        assert best_index > 0
    
    return connection_weights, connection_lags


def get_phase_diffs(phase_a: np.ndarray, phase_b: np.ndarray):
    
    phase_diffs = phase_a - phase_b
    
    indexes = np.argwhere(phase_diffs >= np.pi)
    
    phase_diffs[indexes] = phase_diffs[indexes] - 2 * np.pi
    
    return phase_diffs


def get_phase_lag_index(phase_a: np.ndarray, phase_b: np.ndarray):
    
    phase_diffs = get_phase_diffs(phase_a, phase_b)
    
    return np.abs(np.mean(np.sign(phase_diffs)))


def get_phase_locking_value(phase_a: np.ndarray, phase_b: np.ndarray):
    
    phase_diffs = get_phase_diffs(phase_a, phase_b)
    
    return np.abs(np.mean(np.exp(1j * phase_diffs)))


def get_imaginary_phase_locking_value(phase_a: np.ndarray, phase_b: np.ndarray):
    
    phase_diffs = get_phase_diffs(phase_a, phase_b)
    
    return np.abs(np.mean(np.imag(np.exp( - 1j * phase_diffs))))


def get_digital_phase_transfer_entropy(current_phase: np.ndarray,
                                       target_phase: np.ndarray,
                                       lagged_phase: np.ndarray,
                                       current_bin_num: int,
                                       target_bin_num: int,
                                       lagged_bin_num: int):
    
    target_lagged_phase = target_phase * lagged_bin_num + lagged_phase
    current_target_phase = current_phase * target_bin_num + target_phase
    current_target_lagged_phase = current_phase * target_bin_num * lagged_bin_num +\
        target_phase * lagged_bin_num + lagged_phase

    phase_transfer_entropy =\
        get_digital_entropy(target_lagged_phase, target_bin_num * lagged_bin_num) +\
        get_digital_entropy(current_target_phase, current_bin_num * target_bin_num) -\
        get_digital_entropy(target_phase, target_bin_num) -\
        get_digital_entropy(current_target_lagged_phase, current_bin_num * target_bin_num * lagged_bin_num)
    
    return phase_transfer_entropy

def get_phase_transfer_entropy(current_phase: np.ndarray,
                               target_phase: np.ndarray,
                               lagged_phase: np.ndarray,
                               current_bin_num: int,
                               target_bin_num: int,
                               lagged_bin_num: int):
    
    target_lagged_phase = np.stack([target_phase, lagged_phase], axis=1)
    current_target_phase = np.stack([current_phase, target_phase], axis=1)
    current_target_lagged_phase = np.stack([current_phase, target_phase, lagged_phase], axis=1)
    
    current_bins = np.linspace(-np.pi, np.pi, num=current_bin_num + 1)
    target_bins = np.linspace(-np.pi, np.pi, num=target_bin_num + 1)
    lagged_bins = np.linspace(-np.pi, np.pi, num=lagged_bin_num + 1)

    phase_transfer_entropy =\
        get_entropy(target_lagged_phase, bins=[target_bins, lagged_bins]) +\
        get_entropy(current_target_phase, bins=[current_bins, target_bins]) -\
        get_entropy(target_phase, bins=[target_bins]) -\
        get_entropy(current_target_lagged_phase, bins=[current_bins, target_bins, lagged_bins])
    
    return phase_transfer_entropy


def get_magnitude_squared_coherence(signal_a: np.ndarray, signal_b: np.ndarray, sampling_frequency: int):
    
    _, coherences = scipy.signal.coherence(signal_a, signal_b, fs=sampling_frequency)
    
    return np.mean(coherences)


def get_imaginary_coherence(signal_a: np.ndarray, signal_b: np.ndarray, sampling_frequency: int):
    
    _, coherences = scipy.signal.csd(signal_a, signal_b, fs=sampling_frequency)
    
    return np.mean(np.imag(coherences))