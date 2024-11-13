from utilities.math.entropy import get_entropy, get_sturges_bin_num
import numpy as np
import scipy
import pathlib


def compute_seeg_energy(energy_folder: str,
                        work_signal: np.ndarray,
                        sampling_frequency: int,
                        window_duration: float,
                        window_shift: float,
                        low_frequencies: list,
                        high_frequencies: list):
    
    pathlib.Path(energy_folder).mkdir(parents=True, exist_ok=True)
    
    channel_num = work_signal.shape[0]
    channel_indexes = np.arange(channel_num)
    
    sample_signal_duration = work_signal.shape[1]
    sample_window_duration = int(sampling_frequency * window_duration)
    sample_window_shift = int(sampling_frequency * window_shift)  
    
    instant_phase_bin_num = get_sturges_bin_num(sample_window_duration)
    initial_phase_bin_num = get_sturges_bin_num(int(sample_window_duration / 2))
        
    instant_phase_bins = np.linspace(-np.pi, +np.pi, num=instant_phase_bin_num+1) 
    initial_phase_bins = np.linspace(-np.pi, +np.pi, num=initial_phase_bin_num+1) 
    
    window_number = int(sample_signal_duration / sample_window_shift) - int(sample_window_duration / sample_window_shift) + 1
        
    sample_windows = np.asarray([i * sample_window_shift for i in range(window_number)])
    
    energies_per_channel = []
    
    low_energies_per_channel = []
    high_energies_per_channel = []
    energy_ratios_per_channel = []
    
    initial_phase_distributions_per_channel = []
    instant_phase_distributions_per_channel = []
    
    initial_phase_entropies_per_channel = []
    instant_phase_entropies_per_channel = []
    
    signal_frequencies = np.fft.fftfreq(sample_window_duration, 1 / sampling_frequency)
    
    low_freq_index_0, low_freq_index_1 =\
        int(np.argmin(np.abs(signal_frequencies-low_frequencies[0]))), int(np.argmin(np.abs(signal_frequencies-low_frequencies[1])))
        
    high_freq_index_0, high_freq_index_1 =\
        int(np.argmin(np.abs(signal_frequencies-high_frequencies[0]))), int(np.argmin(np.abs(signal_frequencies-high_frequencies[1])))
    
    max_freq_index = int(np.argmin(np.abs(signal_frequencies- 250)))
    
    for channel_index in channel_indexes:
        
        signal = work_signal[channel_index]
        
        print('Computing fourier energy for channel', channel_index, end='\r')
        
        energies = []
        
        low_energies = []
        high_energies = []
        energy_ratios = []
        
        instant_phase_distributions = []
        initial_phase_distributions = []
        
        instant_phase_entropies = []
        initial_phase_entropies = []
        
        for window_index in np.arange(window_number):
            
            window = signal[window_index*sample_window_shift:window_index*sample_window_shift+sample_window_duration]
            
            energy = np.sum(np.power(window, 2))
        
            fft_window = np.fft.fft(window)
                        
            low_fft_window = fft_window[low_freq_index_0:low_freq_index_1]
            high_fft_window = fft_window[high_freq_index_0:high_freq_index_1]
            
            low_energy = np.sum(np.power(np.absolute(low_fft_window), 2))
            high_energy = np.sum(np.power(np.absolute(high_fft_window), 2))
            
            energies.append(energy)
            
            low_energies.append(low_energy)
            high_energies.append(high_energy)
            
            if low_energy > 0 and high_energy < np.infty:   
                energy_ratio = high_energy / low_energy
                energy_ratios.append(energy_ratio)
            else:
                energy_ratios.append(0)
                
            window -= np.median(window)
                
            fft_window = np.fft.fft(window)
                
            fft_window[np.argwhere(np.abs(fft_window) < 0.00001)] = 0
                
            initial_window_phases = np.angle(fft_window)[:max_freq_index] # take only real frequency

            hilb_window = scipy.signal.hilbert(window)     
            instant_window_phases = np.angle(hilb_window)
            
            instant_phase_distributions.append(np.copy(instant_window_phases))
            initial_phase_distributions.append(np.copy(initial_window_phases))
            
            instant_phase_entropy =\
                get_entropy(instant_window_phases,
                            bins=[instant_phase_bins])
                
            instant_phase_entropies.append(instant_phase_entropy)
            
            initial_phase_entropy =\
                get_entropy(initial_window_phases,
                            bins=[initial_phase_bins])
                
            initial_phase_entropies.append(initial_phase_entropy)
                
        energies_per_channel.append(energies)
        
        low_energies_per_channel.append(low_energies)
        high_energies_per_channel.append(high_energies)         
        energy_ratios_per_channel.append(energy_ratios)
        
        initial_phase_distributions_per_channel.append(initial_phase_distributions)
        instant_phase_distributions_per_channel.append(instant_phase_distributions)
        
        initial_phase_entropies_per_channel.append(initial_phase_entropies)
        instant_phase_entropies_per_channel.append(instant_phase_entropies)
        
    print('\n')
        
    np.savez_compressed(energy_folder + 'time_windows.npz', data=sample_windows / sampling_frequency)
    np.savez_compressed(energy_folder + 'low_energies_per_channel.npz', data=low_energies_per_channel)
    np.savez_compressed(energy_folder + 'high_energies_per_channel.npz', data=high_energies_per_channel)
    
    np.savez_compressed(energy_folder + 'energy_ratios_per_channel.npz', data=energy_ratios_per_channel)
    np.savez_compressed(energy_folder + 'energies_per_channel.npz', data=energies_per_channel)
    
    np.savez_compressed(energy_folder + 'initial_phase_distributions_per_channel.npz', data=initial_phase_distributions_per_channel)
    np.savez_compressed(energy_folder + 'instant_phase_distributions_per_channel.npz', data=instant_phase_distributions_per_channel)    
    
    np.savez_compressed(energy_folder + 'initial_phase_entropies_per_channel.npz', data=initial_phase_entropies_per_channel)
    np.savez_compressed(energy_folder + 'instant_phase_entropies_per_channel.npz', data=instant_phase_entropies_per_channel)    
             