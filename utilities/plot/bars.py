import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def plot_bars(multi_value: list,
              multi_label: list,
              multi_color: list,
              ylabel: str,
              multi_yerr: list = None,
              ylim=None,
              title=None):

    _, axs = plt.subplots(1, 1)
    
    xticks = np.arange(1, len(multi_value) + 1)
    
    axs.bar(xticks, multi_value, color=multi_color, yerr=multi_yerr)

    axs.set_xticks(xticks)

    axs.set_xticklabels(multi_label)

    axs.set_ylabel(ylabel)

    axs.grid(which='both')
    
    if title is not None:
        
        axs.set_title(title)
        
    if ylim is not None:
        
        axs.set_ylim(ylim)
        

def plot_grouped_bars(multi_value: list,
                      multi_label: list,
                      multi_group: list,
                      unique_labels: list,
                      unique_groups: list,                      
                      color_per_label: list,
                      ylabel: str,
                      multi_yerr: list = None,
                      ylim: list = None,
                      title=None,
                      rotation=0):

    _, axs = plt.subplots(1, 1)
        
    legend_labels = []
        
    for color, label in zip(color_per_label, unique_labels):
        
        new_legend = (mpatches.Patch(color=color), label)
        
        legend_labels.append(new_legend)
            
    multi_color = []
            
    for label in multi_label:
        
        multi_color.append(color_per_label[unique_labels.index(label)])
    
    element_xticks = []
    
    group_sizes = [0 for _ in unique_groups]
    
    group_xticks = [0.5 for _ in unique_groups]
    
    for i, group in enumerate(multi_group):
        
        group_index = unique_groups.index(group)
        element_xticks.append(1 + i + group_index)
        group_sizes[group_index] += 1
        
    group_xticks[0] += group_sizes[0] / 2
        
    for i in range(1, len(group_xticks)):
        group_xticks[i] += group_xticks[i-1] - .5 + group_sizes[i-1] / 2  + 1 + group_sizes[i] / 2
        
    axs.bar(element_xticks, multi_value, color=multi_color, yerr=multi_yerr)
    
    axs.set_xticks(group_xticks)
    axs.set_xticklabels(unique_groups, rotation=rotation)

    axs.set_ylabel(ylabel)
    
    axs.legend(*zip(*legend_labels), loc='upper left', ncol=2)
    axs.grid(which='both')
    
    if title is not None:
        
        axs.set_title(title)
        
    if ylim is not None:
        
        axs.set_ylim(ylim)
        
    plt.tight_layout()         
        