from manage_signal_data.extract_epoch_data import extract_epoch, plot_raw_data
from manage_signal_data.extract_continuos_signal_data import extract_continuos_signal
from manage_signal_data.filter_signal_data import filter_signal
from utilities.folder_management import get_raw_patient_folder
from os import listdir
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-patient', '--patient', type=str, default=None)
parser.add_argument('-dataset', '--dataset', type=str, default=None)
parser.add_argument('-raw', '--raw', type=str, default=None)
parser.add_argument('-epoch', '--epoch', type=str, default=None)
parser.add_argument('-time_start', '--time_start', type=float, default=None)
parser.add_argument('-time_duration', '--time_duration', type=float, default=None)
parser.add_argument('-polarization', '--polarization', type=str, default='unipolar')
parser.add_argument('-high_freq', '--high_freq', type=float, default=None)
parser.add_argument('-low_freq', '--low_freq', type=float, default=None)
parser.add_argument('-notch_freq', '--notch_freq', type=float, default=None)
parser.add_argument('-powerline_freq', '--powerline_freq', type=float, default=50)
parser.add_argument('-pre_event_duration', '--pre_event_duration', type=float, default=None)
parser.add_argument('-post_event_duration', '--post_event_duration', type=float, default=None)
parser.add_argument('-event_raw_name', '--event_raw_name', type=str, default=None)
parser.add_argument('-event_new_name', '--event_new_name', type=str, default=None)
parser.add_argument('-max_duration', '--max_duration', type=float, default=None)
parser.add_argument('-multi_data', '--multi_data', dest='multi_data', action='store_true')
parser.add_argument('-plot', '--plot', dest='plot_raw', action='store_true')


if __name__ == '__main__':
    
    args = vars(parser.parse_args())

    max_duration = args['max_duration']
    event_map = (args['event_raw_name'], args['event_new_name'])
    pre_event_duration = args['pre_event_duration']
    post_event_duration = args['post_event_duration']    
    powerline_frequency = args['powerline_freq']
    highpass_frequency = args['high_freq']
    lowpass_frequency = args['low_freq']
    notch_frequency = args['notch_freq']
    plot_raw = args['plot_raw']
    
    if args['multi_data']:
        
        dataset = 'seeg'
        
        multi_patient = []
        multi_raw = []
        multi_epoch = []
        multi_time_start = []
        multi_time_duration = []
        
    else:
    
        dataset = args['dataset']
        patient = args['patient']
        raw = args['raw']
        epoch = args['epoch']
        time_start = args['time_start']
        time_duration = args['time_duration']
        
        multi_patient = [patient]
        multi_raw = [raw]
        multi_epoch = [epoch]
        multi_time_start = [time_start]
        multi_time_duration = [time_duration]
        
    if raw == 'all':
            
        print('Extracting all the epoch of ', patient, '!')
        
        raw_folder = get_raw_patient_folder(patient)
        
        multi_raw = listdir(raw_folder)
        
        multi_raw = [x.split('.')[0] for x in multi_raw]
        
        multi_epoch = multi_raw
    
    for patient, raw, epoch, time_start, time_duration in\
        zip(multi_patient, multi_raw, multi_epoch, multi_time_start, multi_time_duration):
            
        if plot_raw:
            
            plot_raw_data(dataset,
                          patient,
                          raw)
            
        else:

            extract_epoch(dataset,
                          patient,
                          raw,
                          epoch, 
                          time_start,
                          time_duration) 
        
            if dataset in ['seeg']:
                    
                extract_continuos_signal(dataset,
                                        patient,
                                        epoch,
                                        powerline_frequency)
                
            else:
                
                raise ValueError('Unknown dataset!')
                
            if highpass_frequency is not None or lowpass_frequency is not None or notch_frequency is not None:
                    
                filter_signal(dataset,
                            patient,
                            epoch,
                            highpass_frequency=highpass_frequency,
                            lowpass_frequency=lowpass_frequency,
                            notch_frequency=notch_frequency)