import numpy as np
from manage_signal_data.load_signal_data import load_signal, load_frequency
from utilities.folder_management import get_patient_folder
from utilities.math.filter import highpass_filter, lowpass_filter, notch_filter      
        
        
def filter_signal(dataset: str,
                  patient: str,
                  epoch: str,
                  highpass_frequency: int = None,
                  lowpass_frequency: int = None,
                  notch_frequency: int = None):
    
    patient_folder = get_patient_folder(dataset, patient)
    
    sampling_frequency = load_frequency(dataset, patient, epoch)
    
    signal = load_signal(dataset, patient, epoch)

    signal_file = patient_folder + 'signal/' + epoch
    
    if highpass_frequency is not None:
        
        signal_file += '_high=' + str(highpass_frequency)
        
    if lowpass_frequency is not None:
        
        signal_file += '_low=' + str(lowpass_frequency)
        
    if notch_frequency is not None:
        
        signal_file += '_notch=' + str(notch_frequency)
        
    if isinstance(signal[0][0], np.ndarray) and len(signal[0][0]) > 1:
        
        filtered_signal = []
        
        for segment in signal:
            
            filtered_signal.append(filter_channels(segment, highpass_frequency, lowpass_frequency, notch_frequency, sampling_frequency))   
            
    else:
        
        filtered_signal = filter_channels(signal, highpass_frequency, lowpass_frequency, notch_frequency, sampling_frequency)
        
    np.savez_compressed(signal_file + '_signal.npz', data=filtered_signal, allow_pickle=True)


def filter_channels(signal: np.ndarray,
                    highpass_frequency: int = None,
                    lowpass_frequency: int = None,
                    notch_frequency: int = None,
                    sampling_frequency: int = None):
    
    filtered_signal = []
    
    for channel_signal in signal:
    
        if highpass_frequency is not None:
    
            channel_signal = highpass_filter(channel_signal, highpass_frequency, sampling_frequency)
            
        if lowpass_frequency is not None:
        
            channel_signal = lowpass_filter(channel_signal, lowpass_frequency, sampling_frequency)

        if notch_frequency is not None:           
            
            channel_signal = notch_filter(channel_signal, notch_frequency, sampling_frequency)
            
        filtered_signal.append(channel_signal)
        
    return filtered_signal