from utilities.signal.channels import get_channels
from utilities.plot.violins import plot_grouped_violins
from utilities.plot.general import *
import numpy as np


def plot_grouped_violins_per_channel(plot_montage: str,
                                     multi_work_channels: list,
                                     multi_plot_channels: list,
                                     multi_patient: list,                                
                                     multi_multi_data_per_channel: list,
                                     multi_data_ylabel: list,
                                     multi_data_range: list,
                                     multi_legend: list,
                                     multi_group: list,
                                     ):
    
    if plot_montage is None:        
        plot_channels = []        
        for y in multi_plot_channels:            
            plot_channels.extend([x for x in y if x not in plot_channels])
    else:
        
        plot_channels = []
        
        for patient in multi_patient:
            
            plot_channels.extend([x for x in get_channels(patient, plot_montage) if x not in plot_channels])
                        
    plot_channels.sort()
    
    for multi_data_per_channel, ylabel, ylim in zip(multi_multi_data_per_channel,
                                                    multi_data_ylabel,
                                                    multi_data_range):
        
        plot_data_per_channel = []
        plot_legend_per_channel = []
        plot_group_per_channel = []
        
        unique_legends = []
        unique_groups = []
        
        if multi_group is not None and len(np.unique(multi_group)) > 1:            
            multi_label = [legend +', ' + group for legend, group in zip(multi_legend, multi_group)]
            
        else:
            multi_label = multi_legend
        
        for channel in plot_channels:
            
            for data_per_channel, work_channels, label in zip(multi_data_per_channel, multi_work_channels, multi_label):
    
                if channel in work_channels:
                
                    plot_data_per_channel.append(data_per_channel[work_channels.index(channel)])
                    plot_legend_per_channel.append(label)
                    plot_group_per_channel.append(channel)
                    
                    if label not in unique_legends:
                        unique_legends.append(label)
                        
                    if channel not in unique_groups:
                        unique_groups.append(channel)
                        
        color_per_legend = get_plot_colors(len(unique_legends))
        
        plot_grouped_violins(plot_data_per_channel,
                             plot_legend_per_channel,
                             plot_group_per_channel,
                             unique_legends,
                             unique_groups,                            
                             color_per_legend,
                             ylabel,
                             ylim=ylim)