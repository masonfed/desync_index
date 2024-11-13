import numpy as np


def get_smoothed_values(values: np.ndarray,
                        smoothed_coefficient: float):
    
    alpha = smoothed_coefficient
    beta = 1 - alpha
    
    smoothed_values = np.copy(values)
    
    if values.ndim == 1:
        
        time_num = len(values)
    
        for time_index in range(1, time_num):
                
            smoothed_values[time_index] = alpha * smoothed_values[time_index] + beta * smoothed_values[time_index - 1]
    
    else:
        
        time_num = len(values[0])
        
        for time_index in range(1, time_num):
            
            smoothed_values[:, time_index] = alpha * smoothed_values[:, time_index] + beta * smoothed_values[:, time_index - 1]
                
    return smoothed_values


def get_expected_values(values: np.ndarray, baseline: int):
    
    if values.ndim == 1:
        
        time_num = len(values)
        
        expected_values = np.zeros(time_num)
        
        for time_index in range(baseline, time_num):
            expected_values[time_index] = np.mean(values[time_index+1-baseline:time_index+1])
            
    else:
        
        time_num = len(values[0])
        
        expected_values = np.zeros(time_num)
        
        for time_index in range(baseline):
            expected_values[time_index] = np.mean(values[:, time_index])
        
        for time_index in range(baseline, time_num):
            expected_values[time_index] = np.mean(values[:, time_index+1-baseline:time_index+1])
        
    return expected_values


def get_std_values(values: np.ndarray, baseline: int):
    
    if values.ndim == 1:
        
        time_num = len(values)
        
        std_values = np.zeros(time_num)
        
        for time_index in range(baseline, time_num):
            std_values[time_index] = np.std(values[time_index-baseline:time_index])
            
    else:
        
        time_num = len(values[0])
        
        std_values = np.zeros(time_num)
        
        for time_index in range(baseline):
            std_values[time_index] = np.std(values[:, time_index])
        
        for time_index in range(baseline, time_num):
                
            std_values[time_index] = np.std(values[:, time_index-baseline:time_index])
        
    return std_values



def get_percent_values(values: np.ndarray, baseline: int, percent: int):
    
    if values.ndim == 1:
        
        time_num = len(values)
        
        percent_values = np.zeros(time_num)
        
        for time_index in range(baseline, time_num):
            percent_values[time_index] = np.percentile(values[time_index-baseline:time_index], percent)
            
    else:
        
        time_num = len(values[0])
        
        percent_values = np.zeros(time_num)
        
        for time_index in range(baseline):
            percent_values[time_index] = np.percentile(values[:, time_index], percent)
        
        for time_index in range(baseline, time_num):
                
            percent_values[time_index] = np.percentile(values[:, time_index-baseline:time_index], percent)
        
    return percent_values
