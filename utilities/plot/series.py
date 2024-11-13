import numpy as np
import matplotlib.pyplot as plt


def plot_series(times: np.ndarray,
                data: np.ndarray,
                ylabel: str,
                events: dict = None,
                thresholds: dict = None,
                plot_quartile=False,
                sample_size = None,
                title = None,
                xlim = None,
                ylim = None,
                logscale=False):

    fig = plt.figure()
    
    if data.ndim > 1:
        
        sample_size = len(data)
        sample_num = len(data[0])
        
        data_means = np.mean(data, axis=0)
        data_95percent = np.percentile(data, 95, axis=0)
        data_5percent = np.percentile(data, 5, axis=0) 
        
    else:
        
        if sample_size is None:
            
            sample_size = np.max((1, int(len(data) / 100)))
    
        sample_num = int(len(data) / sample_size)
         
        data = np.reshape(data[:sample_num * sample_size], (sample_num, sample_size))
        times = np.reshape(times[:sample_num * sample_size], (sample_num, sample_size))
        
        data_means = np.mean(data, axis=1)
        
        times = np.mean(times, axis=1)        
        data_95percent = np.percentile(data, 95, axis=1)
        data_5percent = np.percentile(data, 5, axis=1)   
        
    if xlim is None:
        xlim = (times[0], times[-1])
        
    if ylim is None:
        ylim = (np.min(data_means), np.max(data_means)) 
        
    if sample_size > 1 and plot_quartile:
        
        plt.plot(times, data_95percent, linestyle='-', color='orangered', label='5-95 percentile range')
        plt.plot(times, data_5percent, linestyle='-', color='orangered')
        plt.fill_between(times, y1=data_5percent, y2=data_95percent, color='lightsalmon')        
        plt.plot(times, data_means, linestyle='-', marker='d', color='orangered', label='Mean')
        
    else:
        
        plt.plot(times, data_means, linestyle='-', color='orangered')
            
    if events is not None:
        
        for description in events.keys():
        
            start_times = events[description][:, 0]
            
            plt.vlines(start_times, ylim[0], ylim[1], color='limegreen', label=description)
            
    if thresholds is not None:
        
        for description in thresholds.keys():
        
            yvalue = thresholds[description]
            
            plt.hlines(yvalue, xlim[0], xlim[1], color='limegreen', label=description, linestyles='--')
    

    plt.grid('on')        
    plt.xlabel('Time [s]')
    plt.ylabel(ylabel)
    
    if title is not None:
        plt.title(title)
    
    plt.xlim(xlim)
    
    if logscale:
        
        plt.yticks([10 ** -0.3, 10 ** -0.2, 10 ** 0, 10 ** 0.2, 10 ** 0.3], ['$10^{-0.3}$', '$10^{-0.2}$', '$10^{0}$', '$10^{0.2}$', '$10^{0.3}$'])
        
        
        plt.yscale('log')
    
    # fig.tight_layout()
        
        
def plot_multi_series(times_per_element: list,
                      data_per_element: list,
                      label_per_element: list,
                      color_per_element: list,
                      ylabel: str,
                      marker_per_element: list = None,
                      events: dict = None,
                      plot_quartile=False,
                      sample_size=None,
                      title=None,
                      xlim=None,
                      ylim=None):

    plt.figure()
    
    if marker_per_element is None:
        marker_per_element = [None for _ in color_per_element]
    
    first_time_per_element = []
    last_time_per_element = []
    data_means_per_element = []

    for times, data, label, color, marker in zip(times_per_element, data_per_element,
                                                 label_per_element, color_per_element,
                                                 marker_per_element):
        
        if data.ndim > 1:
        
            sample_size = len(data)
            sample_num = len(data[0])
            
            data_means = np.mean(data, axis=0)
            data_95percent = np.percentile(data, 95, axis=0)
            data_5percent = np.percentile(data, 5, axis=0)
            
        else:
            
            if sample_size is None:
            
                sample_size = np.max((1, int(len(data) / 100)))        
        
            sample_num = int(len(data) / sample_size)        
            data = np.reshape(data[:sample_num * sample_size], (sample_num, sample_size))
            times = np.reshape(times[:sample_num * sample_size], (sample_num, sample_size))          
            times = np.mean(times, axis=1)
            data_means = np.mean(data, axis=1)
            data_95percent = np.percentile(data, 95, axis=1)
            data_5percent = np.percentile(data, 5, axis=1)
            
        first_time_per_element.append(times[0])
        last_time_per_element.append(times[-1])
        
        if sample_size > 1 and plot_quartile:
            
            plt.plot(times, data_95percent, linestyle='-', color=color, alpha=0.7)
            plt.plot(times, data_5percent, linestyle='-', color=color, alpha=0.7)
            plt.plot(times, data_means, label=label, linestyle='-', color=color)
            
        else:
        
            plt.plot(times, data_means, label=label, linestyle='-', color=color, marker=marker)
            
        data_means_per_element.append(data_means)
            
    if xlim is None:
        
        xlim = (np.min(first_time_per_element), np.max(last_time_per_element))
        
    if ylim is None:
        ylim = (np.min([np.min(data_means) for data_means in data_means_per_element]), np.max([np.max(data_means) for data_means in data_means_per_element]))
            
    if events is not None:
    
        for description in events.keys():
        
            start_times = events[description][:, 0]
            
            plt.vlines(start_times, ylim[0], ylim[1], color='limegreen', label=description)       

    plt.grid('on')        
    plt.xlabel('Time [s]')
    plt.ylabel(ylabel)
    
    plt.legend()
    
    if title is not None:
        plt.title(title)
        
    plt.xlim(xlim)
    plt.ylim(ylim)
