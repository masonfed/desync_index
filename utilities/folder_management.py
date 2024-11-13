from utilities.data_folder import input_data_folder, raw_data_folder, output_data_folder



def get_output_folder(dataset: str):

    dataset_folder = output_data_folder + dataset + '/' 

    return dataset_folder


def get_dataset_folder(dataset: str):

    dataset_folder = input_data_folder + dataset + '/' 

    return dataset_folder


def get_raw_patient_folder(patient: str):

    patient_folder = raw_data_folder  + patient + '/'

    return patient_folder


def get_patient_folder(dataset: str, patient: str):

    patient_folder = get_dataset_folder(dataset) + patient + '/'

    return patient_folder


def get_multi_input_epoch(output_epoch: str):
    
    splitted_output_epoch = output_epoch.split('_')
    
    multi_input_epoch = [splitted_output_epoch[0]]
    
    for epoch_code in splitted_output_epoch[1:]:
        
        if '+' in epoch_code:

            assert len(epoch_code) == 3
            
            first_index = int(epoch_code[0])
            last_index = int(epoch_code[2])
            
            new_multi_input_epoch = []
            
            for x in multi_input_epoch:
                
                new_multi_input_epoch.extend([x + '_' + str(index) for index in range(first_index, last_index + 1)])
            
            multi_input_epoch = new_multi_input_epoch
            
        else:
            
            multi_input_epoch = [x + '_' + epoch_code for x in multi_input_epoch]
            
    return multi_input_epoch