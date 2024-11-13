import numpy as np
from utilities.signal.channels import get_channels
from utilities.folder_management import get_patient_folder


def load_work_channels(dataset: str,
                  patient: str,
                  epoch: str,
                  work_montage: str = 'full'):
    
    patient_folder = get_patient_folder(dataset, patient)
    
    channels = list(np.load(patient_folder + 'signal/' + epoch + '_channels.npz')['data'])
    
    if work_montage == 'full':
        
        return channels
        
    else:
    
        work_channels = get_channels(patient, work_montage)
    
        channel_indexes = []
        
        for channel in work_channels:
            
            try:            
                channel_indexes.append(channels.index(channel))                
            except:
                pass
            
        channel_indexes = np.asarray(channel_indexes).astype(int)
        
        channels = [channels[x] for x in channel_indexes]
        
        return channels
    
    
def load_events(dataset: str,
                patient: str,
                epoch: str):
    
    patient_folder = get_patient_folder(dataset, patient)
    
    events = {}
    
    try:
    
        event_times = list(np.load(patient_folder + 'signal/' + epoch + '_event_times.npz')['data'])
        event_durations = list(np.load(patient_folder + 'signal/' + epoch + '_event_durations.npz')['data'])
        event_descriptions = list(np.load(patient_folder + 'signal/' + epoch + '_event_descriptions.npz')['data'])
        
        for time, duration, description in zip(event_times, event_durations, event_descriptions):
            
            if description not in events.keys():            
                events[description] = [[time, time + duration]]
            
            else:
                events[description].append([time, time + duration])
                
        for description in events.keys():
            
            events[description] = np.asarray(events[description])
    
    except:
        
        pass
    
    return events


def load_signal_length(dataset: str,
                       patient: str,
                       epoch: str):
    
    patient_folder = get_patient_folder(dataset, patient)
    
    signal_file = patient_folder + 'signal/' + epoch
    
    try:
        
        length = np.load(signal_file + '_length.npz', allow_pickle=True)['data']

    except:
        signal = np.load(signal_file + '_signal.npz', allow_pickle=True)['data']
        
        length = int(len(signal[0]))
        
        np.savez_compressed(signal_file + '_length.npz', data=length, allow_pickle=True)
    
    return length


def load_signal(dataset: str,
                patient: str,
                epoch: str,
                highpass_frequency: int = None,
                lowpass_frequency: int = None,
                notch_frequency: int = None):
    
    patient_folder = get_patient_folder(dataset, patient)
    
    signal_file = patient_folder + 'signal/' + epoch
        
    if highpass_frequency is not None:
        
        signal_file += '_high=' + str(highpass_frequency)
        
    if lowpass_frequency is not None:
        
        signal_file += '_low=' + str(lowpass_frequency)
        
    if notch_frequency is not None:
        
        signal_file += '_notch=' + str(notch_frequency)
    
    signal = np.load(signal_file + '_signal.npz', allow_pickle=True)['data']
    
    return signal


def load_frequency(dataset: str,
                   patient: str,
                   epoch: str):
    
    patient_folder = get_patient_folder(dataset, patient)
    
    sampling_frequency = np.load(patient_folder + 'signal/' + epoch + '_freq.npz')['data']
    
    return sampling_frequency
        

def load_work_signal(dataset: str,
                     patient: str,
                     epoch: str,
                     work_montage: str = 'full',
                     highpass_frequency: int = None,
                     lowpass_frequency: int = None,
                     notch_frequency: int = None):
    
    patient_folder = get_patient_folder(dataset,
                                        patient)
    
    signal = load_signal(dataset,
                         patient,
                         epoch,
                         highpass_frequency,
                         lowpass_frequency,
                         notch_frequency)
    
    sampling_frequency = load_frequency(dataset,
                                        patient,
                                        epoch)
        
    full_channels = list(np.load(patient_folder + 'signal/' + epoch + '_channels.npz')['data'])
    
    if work_montage == 'full':
        
        return signal, full_channels, sampling_frequency
        
    else:
    
        work_channels = get_channels(patient, work_montage)
    
        work_channel_indexes = []
        
        for channel in work_channels:
            
            try:            
                work_channel_indexes.append(full_channels.index(channel))                
            except:
                pass
            
        work_channel_indexes = np.asarray(work_channel_indexes).astype(int)
        
        work_signal = signal[work_channel_indexes, :]
            
        work_channels = [full_channels[x] for x in work_channel_indexes]
        
        return work_signal, work_channels, sampling_frequency
