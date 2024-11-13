from utilities.folder_management import get_patient_folder
from utilities.math.filter import powerline_filter     
import numpy as np
import mne
import pathlib


def extract_continuos_signal(dataset: str,
                             patient: str,
                             epoch: str,
                             powerline_frequency: float = None):
    
    patient_folder = get_patient_folder(dataset, patient)

    epoch_data = mne.io.read_raw_edf(patient_folder + 'epoch/' + epoch + '.edf')
    
    channels = epoch_data.ch_names
    
    sampling_frequency = float(epoch_data.info['sfreq'])
    
    signal_folder = patient_folder + 'signal/'
    
    pathlib.Path(signal_folder).mkdir(parents=True, exist_ok=True)
    
    signal = []
    
    for channel in channels:
                    
        channel_signal = epoch_data[epoch_data.ch_names.index(channel)][0][0]
        
        if powerline_frequency is not None:
        
            channel_signal = powerline_filter(channel_signal, powerline_frequency, sampling_frequency)
        
        signal.append(channel_signal)
        
    np.savez_compressed(signal_folder + epoch + '_signal.npz', data=np.asarray(signal))        
    np.savez_compressed(signal_folder + epoch + '_freq.npz', data=sampling_frequency)  
    np.savez_compressed(signal_folder + epoch + '_channels.npz', data=np.asarray(epoch_data.ch_names))
