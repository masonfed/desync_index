import scipy.signal
import numpy as np


def highpass_filter(signal: np.ndarray, cutoff_frequency: float, sampling_frequency: float, order=5):
    nyq = 0.5 * sampling_frequency
    normal_cutoff_frequency = cutoff_frequency / nyq
    b, a = scipy.signal.butter(order, normal_cutoff_frequency, btype='high', analog=False)
    y = scipy.signal.filtfilt(b, a, signal)
    return y


def lowpass_filter(signal: np.ndarray, cutoff_frequency: float, sampling_frequency: float, order=5):    
    nyq = 0.5 * sampling_frequency
    normal_cutoff_frequency = cutoff_frequency / nyq
    if normal_cutoff_frequency < 1:
        b, a = scipy.signal.butter(order, normal_cutoff_frequency, btype='low', analog=False)
        y = scipy.signal.filtfilt(b, a, signal)
        return y
    else:
        return signal


def notch_filter(signal: np.ndarray, notch_frequency: float, sampling_frequency: float, quality_factor=30.0): 
    b, a = scipy.signal.iirnotch(notch_frequency, quality_factor, sampling_frequency)
    y = scipy.signal.filtfilt(b, a, signal)
    return y


def powerline_filter(signal: np.ndarray, powerline_frequency: float, sampling_frequency: float, quality_factor=30.0): 
    b, a = scipy.signal.iircomb(powerline_frequency, quality_factor, ftype='notch', fs=sampling_frequency)
    y = scipy.signal.filtfilt(b, a, signal)
    return y


def derivative_filter(signal: np.ndarray, sampling_frequency: float):
    
    derivative_signal = signal.copy()
    
    sample_signal_duration = len(signal)
    
    for index in range(sample_signal_duration):
        derivative_signal[index] = 0

        if (index >= 1):
            derivative_signal[index] -= 2 * signal[index-1]

        if (index >= 2):
            derivative_signal[index] -= signal[index-2]

        if (index >= 2 and index <= sample_signal_duration-2):
            derivative_signal[index] += 2 * signal[index+1]

        if (index >= 2 and index <= sample_signal_duration-3):
            derivative_signal[index] += signal[index+2]
        
        derivative_signal[index] = (derivative_signal[index]*sampling_frequency) / 8
        
    return derivative_signal


def moving_window_filter(signal: np.ndarray, sample_window: int):
    
    moving_windows = signal.copy()
    
    total_sum = 0

    for j in range(sample_window):
        total_sum += signal[j] / sample_window
        moving_windows[j] = total_sum
    
    for index in range(sample_window, len(signal)):  
        total_sum += signal[index] / sample_window - signal[index-sample_window] / sample_window
        moving_windows[index] = total_sum
      
    return moving_windows