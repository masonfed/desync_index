import numpy as np
from utilities.folder_management import get_patient_folder
from manage_signal_data.load_signal_data import load_signal, load_frequency


def aggregate_signal_data(dataset: str,
                          patient: str,
                          multi_epoch: str,
                          output_epoch: str,
                          highpass_frequency: float = None,
                          lowpass_frequency: float = None,
                          notch_frequency: float = None):
    
    patient_folder = get_patient_folder(dataset, patient)
    
    multi_signal = []
    
    for epoch in multi_epoch:
        
        signal = load_signal(dataset,
                             patient,
                             epoch,
                             highpass_frequency, 
                             lowpass_frequency,
                             notch_frequency)
        
        multi_signal.append(signal)
        
    if len(signal.shape) == 3:
        signal = np.concatenate(multi_signal, axis=0)
    else:
        signal = np.concatenate(multi_signal, axis=1)
    
    sampling_frequency = load_frequency(dataset, patient, epoch)
        
    channels = np.load(patient_folder + 'signal/' + epoch + '_channels.npz')['data']
    
    signal_file = patient_folder + 'signal/' + output_epoch
        
    if highpass_frequency is not None:
        
        signal_file += '_high=' + str(highpass_frequency)
        
    if lowpass_frequency is not None:
        
        signal_file += '_low=' + str(lowpass_frequency)
        
    if notch_frequency is not None:
        
        signal_file += '_notch=' + str(notch_frequency)
        
    if dataset == 'hrv':
        
        multi_event_times = []
        multi_event_durations = []
        multi_event_descriptions = []
        
        time_shift = 0
        
        for i, epoch in enumerate(multi_epoch):            
        
            event_times = np.load(patient_folder + 'signal/' + epoch + '_event_times.npz')['data']
            event_durations = np.load(patient_folder + 'signal/' + epoch + '_event_durations.npz')['data']
            event_descriptions = np.load(patient_folder + 'signal/' + epoch + '_event_descriptions.npz')['data']
            
            multi_event_times.append(event_times + time_shift)
            multi_event_durations.append(event_durations)
            multi_event_descriptions.append(event_descriptions)
            
            time_shift += len(multi_signal[i][0]) / sampling_frequency
            
        event_times = np.concatenate(multi_event_times, axis=-1)
        event_durations = np.concatenate(multi_event_durations, axis=-1)
        event_descriptions = np.concatenate(multi_event_descriptions, axis=-1)
        
        np.savez_compressed(patient_folder + 'signal/' + output_epoch + '_event_times.npz', data=event_times)
        np.savez_compressed(patient_folder + 'signal/' + output_epoch + '_event_durations.npz', data=event_durations)
        np.savez_compressed(patient_folder + 'signal/' + output_epoch + '_event_descriptions.npz', data=event_descriptions)
        
    np.savez_compressed(signal_file + '_signal.npz', data=signal)
    np.savez_compressed(patient_folder + 'signal/' + output_epoch + '_channels.npz', data=channels)
    np.savez_compressed(patient_folder + 'signal/' + output_epoch + '_freq.npz', data=sampling_frequency)
