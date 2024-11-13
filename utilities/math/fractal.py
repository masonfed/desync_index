import numpy as np



def get_higuchi_dimension(series: np.ndarray, k_max: int = 2):
    
    x = []
    y = []
    
    for k in range(1, k_max):
        
        x.append(np.log(1 / k))
        
        y.append((1 / k) * np.sum([  get_higuchi_length(series, m, k)  for m in range(1, k+1)]))
    
    slope, _ = np.polyfit(x, y, 1)
    
    return slope
    
    
def get_higuchi_length(series: np.ndarray, m: int, k: int):
    
    n = len(series)
    
    b = int( (n - m) / k )
    
    return (n - 1) / ( b * (k ** 2)) * np.sum([np.abs(series[ m + i * k ] - series[m + (i - 1) * k]) for i in range(1, b)])
    
    
    
    