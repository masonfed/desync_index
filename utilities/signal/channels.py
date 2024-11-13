from utilities.math.filter import highpass_filter, lowpass_filter
import numpy as np

def get_channels(patient: str,
                 montage: str,
                 max_electrode_index: int = 18):
    
    patient_name = None
    montage_name = None
    patient_montage_channels = []
    
    if patient == patient_name and montage == montage_name:
        
        return patient_montage_channels
        
    else:
        
        channels = []
            
        for channel_index in range(len(montage)):
            
            if montage[channel_index].isnumeric():
                
                pass
            
            else:
                
                character = montage[channel_index]
                
                if channel_index + 1 < len(montage) and montage[channel_index + 1].isnumeric():
                    
                    channels.extend([character + str(number) for number in range(1, int(montage[channel_index + 1]))])
                    
                else:
            
                    channels.extend([character + str(number) for number in range(1, max_electrode_index)])
        
    return channels


def generate_bipolar_channels(unipolar_channels):
    
    bipolar_channels = []
    
    for channel in unipolar_channels:
        
        try:            
            name = channel[:1]        
            index = int(channel[1:])
        
        except: 
            
            try:           
                name = channel[:2]    
                index = int(channel[2:])
                
            except:
                
                name = channel
                index = -1
        
        ref_channel = name + str(index + 1)
        
        if ref_channel in unipolar_channels:
            
            bipolar_channels.append((channel, ref_channel))
    
    return bipolar_channels


def get_seeg_bipolar_channels(work_signal: np.ndarray,
                              work_channels: list):
    
    
    bipolar_channels = []
    
    if work_signal is None:
        
        bipolar_signal = None
        
        for channel_index, channel in enumerate(work_channels):
            
            k = 1
            
            while not channel[k:].isnumeric(): 
                
                k += 1
            
            ref = channel[:k] + str(int(channel[k:]) + 1)
        
            if ref in work_channels:
                
                ref_index = work_channels.index(ref)                   
                bipolar_channels.append(channel + ' - ' + ref)
                
            else:         
                    
                bipolar_channels.append(channel)
            
    else:
        
        bipolar_signal = []
    
        for channel_index, channel in enumerate(work_channels):
            
            k = 1
            
            while not channel[k:].isnumeric(): 
                
                k += 1
            
            ref = channel[:k] + str(int(channel[k:]) + 1)
            
            if ref in work_channels:
            
                ref_index = work_channels.index(ref)                   
                bipolar_signal.append(work_signal[ref_index] - work_signal[channel_index])
                bipolar_channels.append(channel + ' - ' + ref)
                
            else:         
                    
                bipolar_signal.append(work_signal[channel_index])
                bipolar_channels.append(channel)
                    
        bipolar_signal = np.asarray(bipolar_signal)
    
    bipolar_channels = np.asarray(bipolar_channels)

    return bipolar_signal, bipolar_channels

