
from utilities.math.entropy import get_bin_num
import numpy as np
import matplotlib.pyplot as plt


def plot_hist_1d(data: np.ndarray,
                 sample_num: int,
                 data_label: str):
    
    plt.figure()    
    plt.hist(data.flatten(), sample_num, density=True, facecolor='b')    
    plt.xlabel(data_label)
    plt.ylabel('Probability')
    plt.grid(True)
    
    plt.axvline(np.mean(data), color='r', linestyle='--', linewidth=1, label='Mean: ' + str("%.3f" % np.mean(data)))
    plt.axvline(np.median(data), color='r', linestyle='-.', linewidth=1, label='Median: ' + str("%.3f" % np.median(data)))
    plt.axvline(np.percentile(data, 25), color='r', linestyle='-', linewidth=1, label='1st quartile: ' + str("%.3f" % np.percentile(data, 25)))
    plt.axvline(np.percentile(data, 75), color='r', linestyle='-', linewidth=1, label='3rd quartile: ' + str("%.3f" % np.percentile(data, 75)))
    plt.legend()
    
    


def plot_hist_2d(data_1: np.ndarray,
                 data_2: np.ndarray,
                 ylabel_1: str,
                 ylabel_2: str,
                 bin_num_1: int = None,
                 bin_num_2: int = None,
                 title: str = None):
    
    if bin_num_1 is None:
        
        bin_num_1 = get_bin_num(data_1, len(data_1), np.max(data_1) - np.min(data_1), 'freedman')
        
    if bin_num_2 is None:
            
        bin_num_2 = get_bin_num(data_2, len(data_2), np.max(data_2) - np.min(data_2), 'freedman')
        
    plt.figure()
    hist = plt.hist2d(data_1, data_2, bins=[bin_num_1, bin_num_2], density=True, facecolor='b', cmap='plasma')
    plt.colorbar(hist[3], label='Probability')
    plt.xlabel(ylabel_1)
    plt.ylabel(ylabel_2)
    
    if title is not None:
        plt.title(title)