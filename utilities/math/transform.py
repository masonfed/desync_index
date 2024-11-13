import numpy as np
import scipy


def continuos_wavelet_transform(signal: np.ndarray,
                                sampling_frequency: int,
                                frequency_number: int,
                                frequency_min: float,
                                frequency_max: float,
                                sigma: float = 5):
    
    frequencies = np.linspace(frequency_max, frequency_min, frequency_number)
    times = np.linspace(0, len(signal) / sampling_frequency, len(signal))
    
    scales = sigma * sampling_frequency / (2 * np.pi * frequencies)
    
    return times, frequencies, scipy.signal.cwt(signal, scipy.signal.morlet2, scales, w = sigma)


def short_time_fourier_transform(signal: np.ndarray,
                                 sampling_frequency: int,
                                 window_duration: float,
                                 window_shift: float):
    
    sample_window_shift, sample_window_duration =\
        int(sampling_frequency * window_shift), int(sampling_frequency * window_duration)

    sample_number = len(signal)    
    window_number = int(sample_number / sample_window_shift) - int(sample_window_duration / sample_window_shift) + 1
        
    signal_amplitudes = []
    signal_initial_phases = []
        
    for i in np.arange(window_number):
        
        window = signal[i*sample_window_shift:i*sample_window_shift+sample_window_duration]
        
        freq_signal = scipy.fft.fft(window)
        
        freq_signal[np.argwhere(np.abs(freq_signal) < 0.00001)] = 0
        
        signal_amplitudes.append(np.abs(freq_signal))
        
        initial_phases = np.angle(freq_signal)
    
        signal_initial_phases.append(initial_phases)
        
    return np.asarray(signal_amplitudes), np.asarray(signal_initial_phases)


def hilbert_transform(signal: np.ndarray, 
                      sampling_frequency: int,
                      window_duration: float,
                      window_shift: float):
    
    sample_window_shift, sample_window_duration = int(sampling_frequency * window_shift), int(sampling_frequency * window_duration)
    
    sample_number = len(signal)    
    window_number = int(sample_number/ sample_window_shift) - int(sample_window_duration / sample_window_shift) + 1
    
    signal_amplitudes = []
    instant_signal_phases = []
    
    for window_index in range(window_number):
        
        window = signal[window_index*sample_window_shift:window_index*sample_window_shift+sample_window_duration]
        
        signal_amplitudes.append(np.abs(window))
        
        window -= np.median(window)

        hilb_window = scipy.signal.hilbert(window)
        
        phases = np.angle(hilb_window)        
        
        instant_signal_phases.append(phases)
        
    instant_signal_phases = np.asarray(instant_signal_phases)
    
    return np.asarray(signal_amplitudes), np.asarray(instant_signal_phases)
