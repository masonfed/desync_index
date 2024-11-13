import numpy as np
import scipy

z_value_map = {90: 1.645, 95: 1.96, 98: 2.33, 99: 2.58}


def get_two_sample_z_test(multi_data, multi_legend, multi_group, confidence_level):
    
    z_value = z_value_map[confidence_level]
    
    dataframe = {}
    
    group_num = len(np.unique(multi_group))
    legend_num = len(np.unique(multi_legend))
    
    if group_num > 1 and legend_num > 1:
            
        dataframe['legend_1'] = []
        dataframe['legend_2'] = []    
        dataframe['group_1'] = []
        dataframe['group_2'] = []
            
    elif legend_num == 1:
         
        dataframe['group_1'] = []
        dataframe['group_2'] = []
        
    elif group_num == 1:
        
        dataframe['legend_1'] = []
        dataframe['legend_2'] = []    
        
    else:
        
        raise ValueError
    
    dataframe['mean_1'] = []    
    dataframe['ci_1'] = [] 
    dataframe['mean_2'] = []
    dataframe['ci_2'] = []     
    dataframe['z score'] = []        
    dataframe['p value (diff)'] = []
    
    i = -1
    
    for data_1, legend_1, group_1 in zip(multi_data, multi_legend, multi_group):
        
        i += 1
        
        for data_2, legend_2, group_2 in zip(multi_data[i+1:], multi_legend[i+1:], multi_group[i+1:]):
            
            if group_num > 1 and legend_num > 1:
            
                dataframe['legend_1'].append(legend_1)
                dataframe['legend_2'].append(legend_2)
                dataframe['group_1'].append(group_1)
                dataframe['group_2'].append(group_2)
                
            elif legend_num == 1:
                
                dataframe['group_1'].append(group_1)
                dataframe['group_2'].append(group_2)
                
            elif group_num == 1:
                
                dataframe['legend_1'].append(legend_1)
                dataframe['legend_2'].append(legend_2)
                
            else:
                
                raise ValueError
            
            size_1 = len(data_1)
            size_2 = len(data_2)
            
            if size_1 > 0 and size_2 > 0:
            
                mean_1 = np.mean(data_1)
                mean_2 = np.mean(data_2)
                
                std_1 = np.std(data_1)
                std_2 = np.std(data_2)
                
                var_1 = np.var(data_1)
                var_2 = np.var(data_2)
                
                ci_1 = std_1 * z_value / np.sqrt(len(data_1))
                ci_2 = std_2 * z_value / np.sqrt(len(data_2))
                
                z_score = (mean_1 - mean_2) / np.sqrt(var_1 / size_1 + var_2 / size_2)
                
                diff_p_value = 2 * scipy.stats.norm.sf(abs(z_score))
                
                dataframe['mean_1'].append(mean_1)
                dataframe['mean_2'].append(mean_2)
                dataframe['ci_1'].append(ci_1)
                dataframe['ci_2'].append(ci_2)
                dataframe['z score'].append(z_score)
                dataframe['p value (diff)'].append(diff_p_value) 
            else:
                
                dataframe['mean_1'].append('')
                dataframe['mean_2'].append('')
                dataframe['ci_1'].append('')
                dataframe['ci_2'].append('')
                dataframe['z score'].append('')
                dataframe['p value (diff)'].append('') 
                    
    return dataframe