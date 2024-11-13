import numpy as np


def get_window_times(time_start: float,
                     time_duration: float,
                     time_windows: np.ndarray):
    
    window_time_start = np.argmin(np.abs(time_start - time_windows))
    if time_duration is None:
        window_time_end = len(time_windows)
    else:
        window_time_end = np.argmin(np.abs(time_start + time_duration - time_windows)) + 1
    time_windows = time_windows[window_time_start:window_time_end]
    
    return window_time_start, window_time_end, time_windows


def get_times(time_start: float,
              time_duration: float,
              sampling_frequency: int,
              time_windows: np.ndarray,
              work_signal: np.ndarray = None,
              signal_length : int = None):
    
    window_time_shift = time_windows[1] - time_windows[0]
    
    sample_time_start = int(time_start * sampling_frequency)
    
    if time_duration is None:
        if work_signal is None:
            sample_time_end = signal_length
        else:
            sample_time_end = len(work_signal[0])
    else:
        sample_time_end = int((time_start + time_duration + window_time_shift) * sampling_frequency)
        
    times = np.arange(sample_time_start, sample_time_end) / sampling_frequency
    
    window_time_start, window_time_end, time_windows =\
        get_window_times(time_start, time_duration, time_windows)
        
    if work_signal is not None:
        work_signal = work_signal[:, sample_time_start:sample_time_end]
    
    return times, time_windows, window_time_start, window_time_end, work_signal