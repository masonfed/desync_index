from utilities.folder_management import get_patient_folder, get_raw_patient_folder
import numpy as np
import mne
import pathlib
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')


def plot_raw_data(dataset: str,
                  patient: str,
                  raw: str,
                  time_start: float = 0,
                  time_duration: float = None):
    
    print()
    
    raw_data = mne.io.read_raw_edf(get_raw_patient_folder(patient) + raw + '.edf', encoding='latin1')
    
    mne.viz.set_browser_backend('matplotlib')
    
    print()
    
    print('Time start: ' + str(time_start) +\
                '\nTime duration: ' + str(time_duration) +\
                    '\nDate: ' + str(dict(raw_data.info)['meas_date']))
    
    print()
            
    print('Signal annotation:')
    
    for annot in raw_data.annotations:
        
        print(annot['description'], annot['onset'])
        
    times = raw_data.times
    
    if time_start is not None:    
        assert time_start >= times[0]
    else:        
        raise ValueError('Time start not defined!')    
        
    if time_duration is not None:   
        assert time_start + time_duration <= times[-1]
    else:
        time_duration = times[-1] - time_start
        
    time_slot = times[1] - times[0]
        
    time_end = time_start + time_duration - time_slot
    
    raw_channel_names = list(raw_data.ch_names)
    
    if dataset == 'seeg':
        channel_names, selected_channel_names = get_seeg_channels(raw_channel_names, patient)
    elif dataset == 'hrv':
        channel_names, selected_channel_names = get_hrv_channels(raw_channel_names, patient)
    elif dataset == 'cart' or dataset == 'melas':
        channel_names = raw_channel_names
        selected_channel_names = [x for x in raw_channel_names if x != 'ECG']
    else:
        raise ValueError
    
    print()
            
    mne.rename_channels(raw_data.info, {x: y for (x, y) in zip(raw_channel_names, channel_names)}, verbose=True)

    raw_data = raw_data.reorder_channels(selected_channel_names)
    
    raw_data = raw_data.crop(tmin=time_start, tmax=time_end)
    
    raw_data.plot(bgcolor='lightyellow', event_color='k', remove_dc=True)
    
    plt.show()


def extract_epoch(dataset: str,
                  patient: str,
                  raw: str,
                  epoch: str,
                  time_start: float,
                  time_duration: float):
    
    print()

    raw_data = mne.io.read_raw_edf(get_raw_patient_folder(patient) + raw + '.edf', encoding='latin1')
    
    patient_folder = get_patient_folder(dataset, patient)    
    
    pathlib.Path(patient_folder + 'epoch/').mkdir(parents=True, exist_ok=True)
    
    times = raw_data.times
    
    if time_start is not None:    
        assert time_start >= times[0]
    else:        
        raise ValueError('Time start not defined!')    
        
    if time_duration is not None:   
        assert time_start + time_duration <= times[-1]
    else:
        time_duration = times[-1] - time_start
        
    sampling_frequency = raw_data.info['sfreq']
    time_slot = times[1] - times[0]
    
    if sampling_frequency != int(np.ceil(sampling_frequency)):
        
        raw_data.info.sfreq = int(np.ceil(sampling_frequency))
        sampling_frequency = int(np.ceil(sampling_frequency))
    
    time_end = time_start + time_duration - time_slot
    
    raw_channel_names = list(raw_data.ch_names)
    
    if dataset == 'seeg':
        channel_names, selected_channel_names = get_seeg_channels(raw_channel_names, patient)
    elif dataset == 'hrv':
        channel_names, selected_channel_names = get_hrv_channels(raw_channel_names, patient)
    elif dataset == 'cart' or dataset == 'melas':
        channel_names = raw_channel_names
        selected_channel_names = [x for x in raw_channel_names if x != 'ECG']
    else:
        raise ValueError
    
    print()
    
    print('Signal annotation:')
    
    for annot in raw_data.annotations:
        
        print(annot['description'], annot['onset'])
        
    print()
            
    mne.rename_channels(raw_data.info, {x: y for (x, y) in zip(raw_channel_names, channel_names)}, verbose=True)

    epoch_data = raw_data.reorder_channels(selected_channel_names)
    
    epoch_data = epoch_data.crop(tmin=time_start, tmax=time_end)
    
    new_onsets = []
    new_durations = []
    new_descriptions = []
    
    for annot in epoch_data.annotations:
        
        if annot['onset'] > time_start:
            
            new_onsets.append(annot['onset'] - time_start)
            new_durations.append(annot['duration'])
            new_descriptions.append(annot['description'])
            
    new_annotations = mne.Annotations(onset=new_onsets,
                                      duration=new_durations,
                                      description=new_descriptions,
                                      orig_time = epoch_data.info['meas_date'] + datetime.timedelta(seconds=time_start))
    
    epoch_data._annotations = new_annotations
        
    mne.export.export_raw(patient_folder + 'epoch/' + epoch + '.edf', epoch_data, overwrite=True, verbose=2)

    with open(patient_folder + 'epoch/' + epoch + '.txt', 'w') as f:
        f.write('Input: ' + str(raw) +\
            '\nTime start: ' + str(time_start) +\
                '\nTime duration: ' + str(time_duration) +\
                    '\nDate: ' + str(dict(epoch_data.info)['meas_date']))

    
def get_seeg_channels(raw_channel_names: list,
                      patient: str):
    
    discarded_pattern = ['SSR', 'ECG', 'RESP',
                         'DC01', 'Fz', 'FZ', 'Cz',
                         'CZ', 'Pz', 'PZ', 'ABP',
                         'TIB', 'DELT', 'EOG', 'MILO',
                         'DEL', 'FA', 'VM', 'BP']
    
    try:
        
        seeg_channels = []
        channel_names = []
    
        x = 0
                
        for name in raw_channel_names:
            
            if any(y in name for y in discarded_pattern):
                    
                channel_names.append('DISCARDED ' + str(x))
                x += 1
                pass
            
            else:
            
                name_list = name.split()      
                
                if len(name_list) > 1:
                    
                    seeg_name = name.replace('-', ' ')
                    
                    seeg_name_list = seeg_name.split()  
                    
                    assert seeg_name_list[0] == 'POL' or seeg_name_list[0] == 'EEG'
                    
                    if len(seeg_name_list[1]) > 1 and (patient != 'ilas_adrian' or '\'' in seeg_name_list[1]):
                        seeg_channels.append(seeg_name_list[1])
                        channel_names.append(seeg_name_list[1])
                        
                    else:
                        channel_names.append('DISCARDED ' + str(x))
                        x += 1
                    
                else:
                    
                    channel_names.append('DISCARDED ' + str(x))
                    x += 1
        
        assert len(seeg_channels) > 0
    
    except:
        
        seeg_channels = []
        channel_names = []
        
        x = 0
                
        for name in raw_channel_names:
            
            if any(y in name for y in discarded_pattern):
                    
                channel_names.append('DISCARDED ' + str(x))
                x += 1
                pass
            
            else:
                    
                seeg_name = name.replace('-', ' ')
                
                seeg_name_list = seeg_name.split()  
                
                if len(seeg_name_list[0]) > 1 and seeg_name_list[0] not in seeg_channels:
                    seeg_channels.append(seeg_name_list[0])
                    channel_names.append(seeg_name_list[0])
                    
                else:
                    channel_names.append('DISCARDED ' + str(x))
                    x += 1
            
    seeg_channels = [x.replace('\'', '') for x in seeg_channels]            
    channel_names = [x.replace('\'', '') for x in channel_names]
            
    return channel_names, seeg_channels



