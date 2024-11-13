import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def plot_violins(multi_data: list,
                 multi_label: list,
                 multi_color: list,
                 ylabel: str,
                 ylim: list = None,
                 title=None,
                 rotation=60):
    
    data_num = len(multi_data)

    _, axs = plt.subplots(1, 1)

    quantiles = [[0.05, 0.25, 0.75, 0.95]] * data_num

    distributions = axs.violinplot(multi_data,
                                   showmeans=False, 
                                   showextrema=True,
                                   showmedians=False,
                                   points=500,
                                   quantiles=quantiles)

    medians = [np.median(x) for x in multi_data]
    
    means = [np.mean(x) for x in multi_data]

    axs.scatter(range(1, data_num+1), medians, label='Median', marker='o', color='white', edgecolors='royalblue', s=30, zorder=3)
    
    axs.scatter(range(1, data_num+1), means, label='Mean', marker='d', color='white', edgecolors='royalblue', s=30, zorder=3)

    axs.set_xticks(np.arange(1, data_num + 1))

    axs.set_xticklabels(multi_label, rotation=rotation)

    axs.set_ylabel(ylabel)
        
    for dist, color in zip(distributions['bodies'], multi_color):
        dist.set_facecolor(color)

    axs.grid(which='both')
    axs.legend(ncol=3)
    
    if title is not None:
        
        axs.set_title(title)
        
    if ylim is None:
        
        ylim = [np.min([np.min(x) for x in multi_data]), np.max([np.percentile(x, 95) for x in multi_data])]
        
    axs.set_ylim(ylim)
        

def plot_grouped_violins(multi_data: list,
                         multi_label: list,
                         multi_group: list,
                         unique_labels: list,
                         unique_groups: list,
                         color_per_label: list,
                         ylabel: str,
                         ylim: list = None,
                         title=None,
                         figsize=None,
                         rotation=60):
    
    data_num = len(multi_data)
    
    if figsize is None:

        _, axs = plt.subplots(1, 1)
        
    else:
        
        _, axs = plt.subplots(1, 1, figsize=figsize)

    quantiles = [[0.05, 0.25, 0.75, 0.95]] * data_num
        
    legend_labels = []
        
    for color, label in zip(color_per_label, unique_labels):
        
        new_legend = (mpatches.Patch(color=color), label)
        
        legend_labels.append(new_legend)
    
    medians = [np.median(x) for x in multi_data]
    
    means = [np.mean(x) for x in multi_data]
            
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
        
    distributions = axs.violinplot(multi_data, showmeans=False, showextrema=True, showmedians=False, points=500, quantiles=quantiles, positions=element_xticks)        
    for dist, color, label in zip(distributions['bodies'], multi_color, multi_label):
        dist.set_facecolor(color)
    
    axs.scatter(element_xticks, medians, label='Median', marker='o', color='white', edgecolors='royalblue', s=30, zorder=3)
    axs.scatter(element_xticks, means, label='Mean', marker='d', color='white', edgecolors='royalblue', s=30, zorder=3)
    
    axs.set_xticks(group_xticks)
    
    axs.set_xticklabels(unique_groups, rotation=rotation)

    axs.set_ylabel(ylabel) 
            
    legend = plt.legend(*zip(*legend_labels), loc=2)
    
    plt.gca().add_artist(legend)
    
    axs.grid(which='both')
    
    if title is not None:
        
        axs.set_title(title)
        
    if ylim is None:
        
        ylim = [np.min([np.min(x) for x in multi_data]), np.max([np.percentile(x, 95) for x in multi_data])]
        
    axs.set_ylim(ylim)