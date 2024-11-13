import numpy as np


def get_sturges_bin_num(data_num: int):
    
    return int(np.max((1, np.log2(data_num) + 1)))


def get_bin_num(data: np.ndarray,
                data_num: int,
                data_range: float,
                technique: str):
    
    if technique == 'scott':
        
        if np.std(data) == 0:
            return data_num
        
        else:
            return np.max((1, int(data_range * (data_num ** (1/3)) /\
                (3.49 * np.std(data)))))  
        
    elif technique == 'doane':
        
        if np.std(data) == 0:
            
            return data_num
            
        else:

            sg1 = np.sqrt(6.0 * (data_num - 2.0) / ((data_num + 1.0) * (data_num + 3.0)))
            skew = np.mean(((data - np.mean(data)) / np.std(data)) ** 3)
            Ke = np.log2(1.0 + np.absolute(skew) / sg1)
            bin_num = int(1.0 + np.log2(data_num) + Ke)
            
            return int(np.ceil(bin_num) // 2 * 2 + 1)            

    elif technique == 'freedman':
        
        if np.subtract(*np.percentile(data, [75, 25])) == 0:
            return data_num
        else:            
            return np.max((1, int(data_range * (data_num ** (1/3)) /\
                    (2 * np.subtract(*np.percentile(data, [75, 25]))))))
            
    elif technique == 'freedman_1':

        if np.subtract(*np.percentile(data, [95, 5])) == 0:
            return data_num
        else:            
            return np.max((1, int(data_range * (data_num ** (1/3))\
                / (2 * np.subtract(*np.percentile(data, [95, 5]))))))
        
    elif technique == 'sturges':

        return get_sturges_bin_num(data_num)
        
    else:
        
        return int(technique)
    

def get_bins(data: np.ndarray, bin_rule: str):
    
    bin_num = get_bin_num(data, len(data), np.max(data) - np.min(data), bin_rule)
    
    return np.linspace(np.min(data), np.max(data), num=bin_num+1)


def get_entropy(data: np.ndarray,
                data_domain: tuple = None,
                bins: np.ndarray = None,
                bin_rule: str = None):
    
    if bins is None:
        
        assert bin_rule is not None
            
        if data_domain is None:
            
            data_range = np.max(data) - np.min(data)
            
        else:
            
            data_range = data_domain[1] - data_domain[0]
    
        bin_num = get_bin_num(data, len(data), data_range, bin_rule)
        
        bins = np.linspace(data_domain[0], data_domain[1], num=bin_num+1)

        if data.ndim > 1:
        
            bins = [bins for _ in range(data.shape[1])]
            
        else:
            
            bins = [bins]

    counts, _ = np.histogramdd(data, bins=bins)

    counts /= np.sum(counts)
        
    probs = counts.flatten()
    
    prob_indexes = np.argwhere(probs > 0)
        
    entropy = -np.sum(probs[prob_indexes] * np.log(probs[prob_indexes]))
    
    return entropy
    
    
def get_digital_entropy(digital_data: np.ndarray, bin_num: int):
    
    counts = np.bincount(digital_data, minlength=bin_num-1)
    
    probs = counts / np.sum(counts)
    
    prob_indexes = np.argwhere(probs > 0)
        
    entropy = -np.sum(probs[prob_indexes] * np.log(probs[prob_indexes]))
    
    return entropy