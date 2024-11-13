
def get_band_frequencies(band: str):
    
    if band == 'delta':
        
        return [2.0, 4.0]
    
    elif band == 'theta':
        
        return [4.0, 8.0]
    
    elif band == 'alpha':
        
        return [8.0, 14.0]
    
    elif band == 'beta':
        
        return [14.0, 30.0]
    
    elif band == 'gamma':
        
        return [30.0, 100.0]
    
    elif band == 'full':
        
        return [0.0, 10000]
    
    elif band == 'eeg':
        
        return [2.0, 30.0]

    elif band == 'delta+theta':
        
        return [2.0, 8.0]

    elif band == 'alpha+beta':
        
        return [8.0, 30.0]
    
    else: 
        
        raise ValueError