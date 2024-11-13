def generate_seeg_labels(multi_variable, patient):
    
    multi_epoch = []
        
    multi_patient = []
    
    multi_legend = []
    
    multi_group = []
    
    multi_time_start = []
    
    multi_time_duration = []
    
    if multi_variable == 'patient':
        
        rep = 5
        duration = 40
        
        multi_patient += [patient for _ in range(1 + 5 * rep)]
        
        multi_epoch += ['seizure_0' for _ in range(1)] +\
            ['awake_0' for _ in range(rep)] +\
                ['asleep_0' for _ in range(rep)] +\
                    ['awake_1' for _ in range(rep)] +\
                        ['asleep_1' for _ in range(rep)] +\
                            ['hyperpnea_0' for _ in range(rep)]

        multi_time_start += [160 for _ in range(1)] +\
            [i*duration for i in range(rep)] +\
                [i*duration for i in range(rep)] +\
                    [i*duration for i in range(rep)] +\
                        [i*duration for i in range(rep)] +\
                            [i*duration for i in range(rep)] 
                    
        multi_time_duration += [40 for _ in range(1)] +\
            [duration for _ in range(rep)] +\
                [duration for _ in range(rep)] +\
                    [duration for _ in range(rep)] +\
                        [duration for _ in range(rep)] +\
                            [duration for _ in range(rep)] 

        multi_legend += ['ICTAL'] +\
            ['AWAKE' for _ in range(rep)]+\
                ['ASLEEP' for _ in range(rep)]+\
                    ['AWAKE 1' for _ in range(rep)]+\
                        ['ASLEEP 1' for _ in range(rep)]+\
                            ['HYPERPNEA' for _ in range(rep)] 
                
        group = ''
        
        for y in [x.upper()[0] for x in list(patient.split('_'))]:
            
            group += y + '.'
        
        multi_group += [group for _ in range(1 + 5* rep)]
            
    else:
        raise ValueError
    
    return multi_epoch, multi_patient, multi_legend, multi_group, multi_time_start, multi_time_duration


def get_seeg_default_parameters(patient: str, epoch: str):
    
    patient_name = None
    epoch_name = None
    
    if patient == patient_name:
        
        if epoch == epoch_name:
        
            time_start = 0.0
            time_duration = 0.0
                            
            epindex_start = 0.0
            epindex_base = 0.0 
            epindex_end = 0.0 
            
        else:
            
            raise ValueError
        
    return time_start, time_duration, epindex_start, epindex_base, epindex_end
