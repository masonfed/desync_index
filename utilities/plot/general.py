import numpy as np
import matplotlib.cm as cm

def get_plot_labels(labels: list,
                    values_per_label: list,
                    max_label_num: int):
    
    sorted_label_indexes = [x for _, x in sorted(zip(values_per_label, list(range(len(labels)))), reverse=True)]
    
    plot_label_indexes = sorted_label_indexes[:np.min((max_label_num, len(sorted_label_indexes)))]
    
    plot_label_indexes = np.asarray(sorted(plot_label_indexes)).astype(int)
    
    plot_labels = [labels[i] for i in plot_label_indexes]
    
    return plot_labels, plot_label_indexes


def get_plot_colors(configuration_num: int, multi_label: list = None):
    
    color_map = cm.get_cmap('plasma')
    
    if multi_label is None:
    
        colors = [color_map(i) for i in np.arange(configuration_num) / configuration_num]
        
    else:
        
        unique_labels = list(np.unique(multi_label))
        
        label_num = len(unique_labels)
        
        colors = [color_map(i) for i in np.arange(label_num) / label_num]
        
        colors = [colors[unique_labels.index(label)] for label in multi_label]
    
    return colors


def get_plot_markers(configuration_num: int, multi_label: list = None):
    
    markers = ['o', 'v', '^', '<', '>', 's', 'd', 'P', 'X']
    
    if multi_label is None:
    
        markers = markers[:configuration_num]
        
    else:
        
        unique_labels = list(np.unique(multi_label))
        
        label_num = len(unique_labels)
        
        markers = [markers(i) for i in np.arange(label_num)]
        
        markers = [markers[unique_labels.index(label)] for label in multi_label]
    
    return markers




