import numpy as np
import scipy

z_value_map = {90: 1.645, 95: 1.96, 98: 2.33, 99: 2.58}


def get_two_sample_t_test(multi_data: list,
                          multi_legend: list,
                          multi_group: list,
                          confidence_level: float,
                          alternative: str,
                          multi_norm = None):
    
    if multi_norm is not None:
        multi_norm_data = [x / y for x, y in zip(multi_data, multi_norm)]
    else:
        multi_norm_data = multi_data
    
    z_value = z_value_map[confidence_level]
    
    dataframe = {}
    
    group_num = len(np.unique(multi_group))
    legend_num = len(np.unique(multi_legend))
            
    dataframe['legend_1'] = []
    dataframe['legend_2'] = []    
    dataframe['group_1'] = []
    dataframe['group_2'] = []
    
    dataframe['mean_1'] = []
    dataframe['ci_1'] = []
    dataframe['mean_2'] = []
    dataframe['ci_2'] = []        
    dataframe['t score'] = []
    dataframe['degree of freedom'] = []        
    dataframe['p value (diff)'] = []     
    
    unique_legends = []
    
    for legend in multi_legend:
        
        if legend not in unique_legends:
            
            unique_legends.append(legend)
            
    unique_groups = []
    
    for group in multi_group:
        
        if group not in unique_groups:
            
            unique_groups.append(group)
            
    for legend_1 in unique_legends:
        
        for legend_2 in unique_legends:
            
            data_1 = []
            norm_data_1 = []
            data_2 = []
            norm_data_2 = []
                
            group_1, group_2 = None, None
            
            if legend_1 != legend_2:
            
                for data, norm_data, legend in zip(multi_data, multi_norm_data, multi_legend):
                    
                    if legend == legend_1:
                        
                        if np.ndim(data) > 0:
                                    
                            data_1.append(data)
                            norm_data_1.append(norm_data)
                        
                        else: 
                            
                            data_1.append([data])
                            norm_data_1.append([norm_data])
                    
                    elif legend == legend_2:
                        
                        if np.ndim(data) > 0:
                                    
                            data_2.append(data)
                            norm_data_2.append(norm_data)
                        
                        else: 
                            
                            data_2.append([data])
                            norm_data_2.append([norm_data])
                            
                size_1 = len(data_1)
                size_2 = len(data_2)
                
                if size_1 > 1 and size_2 > 1:
                            
                    data_1 = np.concatenate(data_1)
                    norm_data_1 = np.concatenate(norm_data_1)
                    data_2 = np.concatenate(data_2)
                    norm_data_2 = np.concatenate(norm_data_2)

                    if group_num > 1 and legend_num > 1\
                        and legend_1 is not None and group_1 is not None:
                    
                        dataframe['legend_1'].append(legend_1)
                        dataframe['legend_2'].append(legend_2)
                        dataframe['group_1'].append(group_1)
                        dataframe['group_2'].append(group_2)
                        
                    elif legend_num == 1 or legend_1 is None:
                        
                        dataframe['group_1'].append(group_1)
                        dataframe['group_2'].append(group_2)
                        
                        dataframe['legend_1'].append('')
                        dataframe['legend_2'].append('')
                        
                    elif group_num == 1 or group_1 is None:
                        
                        dataframe['group_1'].append('')
                        dataframe['group_2'].append('')
                        
                        dataframe['legend_1'].append(legend_1)
                        dataframe['legend_2'].append(legend_2)
                        
                    else:
                        
                        raise ValueError
            
                    result = scipy.stats.ttest_ind(norm_data_1,
                                                   norm_data_2,
                                                   equal_var=False,
                                                   alternative=alternative)
                    
                    mean_1 = np.mean(data_1)
                    mean_2 = np.mean(data_2)
                    
                    std_1 = np.std(data_1)
                    std_2 = np.std(data_2)
                    
                    df = result.df
                    
                    t_score = result.statistic
                    
                    p_value = result.pvalue
                    
                    ci_1 = std_1 * z_value / np.sqrt(len(data_1))
                    ci_2 = std_2 * z_value / np.sqrt(len(data_2))
                    
                    dataframe['mean_1'].append(mean_1)
                    dataframe['ci_1'].append(ci_1)
                    dataframe['mean_2'].append(mean_2)
                    dataframe['ci_2'].append(ci_2)
                    dataframe['t score'].append(t_score)
                    dataframe['degree of freedom'].append(df)
                    dataframe['p value (diff)'].append(p_value)
        
    for group_1 in unique_groups:
        
        for group_2 in unique_groups:
            
            data_1 = []
            data_2 = []
            
            legend_1, legend_2 = None, None
            
            if group_1 != group_2:
            
                for data, group in zip(multi_data, multi_group):
                    
                    if group == group_1:
                        
                        if np.ndim(data) > 0:
                                    
                            data_1.append(data)
                                
                        else: 
                                    
                            data_1.append([data])
                    
                    elif group == group_2:
                        
                        if np.ndim(data) > 0:
                                    
                            data_2.append(data)
                                
                        else: 
                                    
                            data_2.append([data])
                            
                size_1 = len(data_1)
                size_2 = len(data_2)
                
                if size_1 > 1 and size_2 > 1:
                            
                    data_1 = np.concatenate(data_1)
                    data_2 = np.concatenate(data_2)

                    if group_num > 1 and legend_num > 1\
                        and legend_1 is not None and group_1 is not None:
                    
                        dataframe['legend_1'].append(legend_1)
                        dataframe['legend_2'].append(legend_2)
                        dataframe['group_1'].append(group_1)
                        dataframe['group_2'].append(group_2)
                        
                    elif legend_num == 1 or legend_1 is None:
                        
                        dataframe['group_1'].append(group_1)
                        dataframe['group_2'].append(group_2)
                        
                        dataframe['legend_1'].append('')
                        dataframe['legend_2'].append('')
                        
                    elif group_num == 1 or group_1 is None:
                        
                        dataframe['group_1'].append('')
                        dataframe['group_2'].append('')
                        
                        dataframe['legend_1'].append(legend_1)
                        dataframe['legend_2'].append(legend_2)
                        
                    else:
                        
                        raise ValueError
            
                    result = scipy.stats.ttest_ind(data_1, data_2, equal_var=False, alternative=alternative)
                    
                    mean_1 = np.mean(data_1)
                    mean_2 = np.mean(data_2)
                    
                    std_1 = np.std(data_1)
                    std_2 = np.std(data_2)
                    
                    df = result.df
                    
                    t_score = result.statistic
                    
                    p_value = result.pvalue
                    
                    ci_1 = std_1 * z_value / np.sqrt(len(data_1))
                    ci_2 = std_2 * z_value / np.sqrt(len(data_2))
                    
                    dataframe['mean_1'].append(mean_1)
                    dataframe['ci_1'].append(ci_1)
                    dataframe['mean_2'].append(mean_2)
                    dataframe['ci_2'].append(ci_2)
                    dataframe['t score'].append(t_score)
                    dataframe['degree of freedom'].append(df)
                    dataframe['p value (diff)'].append(p_value)
                    
    return dataframe
