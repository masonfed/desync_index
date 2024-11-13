import numpy as np
import scipy

def autocorrelate(signal: np.ndarray, lag: int = None):
    
    correlations = scipy.signal.correlate(signal, signal, mode="full")
    lags = scipy.signal.correlation_lags(signal.size, signal.size, mode="full")
    
    if lag is None:        
        return lags, correlations
        
    else:        
        correlation_index = np.argwhere(lags==lag)[0]        
        return lag, correlations[correlation_index]

def crosscorrelate(signal_a: np.ndarray, signal_b: np.ndarray, lag: int = None):
        
    correlations = scipy.signal.correlate(signal_a, signal_b, mode="full")
    lags = scipy.signal.correlation_lags(signal_a.size, signal_b.size, mode="full")
    
    if lag is None:        
        return lags, correlations
        
    else:        
        correlation_index = np.argwhere(lags==lag)[0]        
        return lag, correlations[correlation_index]

def spectral_density(signal: np.ndarray, sampling_frequency: int):

    return scipy.signal.welch(signal, fs=sampling_frequency, nperseg=1024, noverlap=64)

def crossspectral_density(signal_a: np.ndarray, signal_b: np.ndarray, sampling_frequency: int):
    
    return scipy.signal.csd(signal_a, signal_b, fs=sampling_frequency, nfft=1024)

def crossspectral_density_arg(signal_a: np.ndarray, signal_b: np.ndarray, sampling_frequency: int):
    
    frequencies, density = crossspectral_density(signal_a, signal_b, sampling_frequency)
    
    phases = np.angle(density, deg=False)
    
    return frequencies, phases

def spectral_coherence(signal_a: np.ndarray, signal_b: np.ndarray, sampling_frequency: int):
    
    return scipy.signal.coherence(signal_a, signal_b, fs=sampling_frequency, nperseg=1024, noverlap=64, nfft=1024)
    