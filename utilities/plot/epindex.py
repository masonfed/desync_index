from utilities.plot.general import get_plot_colors
from analyze_seeg_features.folder_management import *
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import seaborn as sns
import matplotlib

font = {'family' : 'STIXGeneral',
        'size'   : 16}

matplotlib.rc('font', **font)


def plot_cumulative_sums(plot_channels: list,
                         time_windows: np.ndarray,
                         cumsum_time_windows: np.ndarray,
                         statistics_per_channel: np.ndarray,
                         cumulative_sums_per_channel: np.ndarray,
                         alarm_times_per_channel: list,
                         detection_times_per_channel: list,
                         color_per_channel: list,
                         statistic_label: str,
                         alarm_threshold = None,
                         xtick_num: int = 10,
                         title: str = None,
                         xlim: list = None,
                         ylim: list = None,
                         epindex_target_colors: list = None,
                         epindex_target_labels: list = None,
                         epindex_targets: list = None):
        
    plot_channel_num = len(plot_channels)
    
    if plot_channel_num > 0:    
        
        min_cumulative_sum = np.min([np.min(x) for x in cumulative_sums_per_channel])
        max_cumulative_sum = np.max([np.max(x) for x in cumulative_sums_per_channel])
    
    else:        
        min_cumulative_sum = 0
        max_cumulative_sum = 0
        
    if plot_channel_num > 0:
        shift = (max_cumulative_sum - min_cumulative_sum) / plot_channel_num
    else:
        shift = 0
    
    plt.figure()
    
    for color, channel, cumulative_sums in zip(color_per_channel,
                                               plot_channels,
                                               cumulative_sums_per_channel):
      
        plt.plot(cumsum_time_windows, cumulative_sums, color=color, label=channel, zorder=1)
        
    for alarm_times, detection_times, color in zip(alarm_times_per_channel,
                                                   detection_times_per_channel,
                                                   color_per_channel):
        
        for alarm_time, detection_time in zip(alarm_times, detection_times):
            
            plt.scatter(x=detection_time, y=0, color=color, marker='X', s=60, zorder=2, edgecolor='black', linewidth=0.1) 
            plt.scatter(x=alarm_time, y=0, color=color, marker='D', s=60,  zorder=2, edgecolor='black', linewidth=0.1)
                
    if alarm_threshold is not None:
        plt.axhline(y=alarm_threshold, color='k', linestyle='dashdot', label='Alarm threshold')  
        plt.legend()
    
    plt.legend(loc='upper left', ncol=1)    
    plt.grid('on')    
    plt.xlabel('Time [s]')
    plt.ylabel('Cumulative sum')
    
    if title is not None:        
        plt.title(title)
        
    if xlim is not None:        
        plt.xlim(xlim)
        
    plt.ylim([min_cumulative_sum - shift, max_cumulative_sum + shift])
    
    fig = plt.figure()
    
    if ylim is None:
        vmin = np.min(statistics_per_channel)
        vmax=np.max(statistics_per_channel)
    else:
        vmin, vmax = ylim[0], ylim[1]
        
    sns.heatmap(statistics_per_channel,
                cmap='plasma',
                fmt='s',
                vmin=vmin,
                vmax=vmax,
                cbar_kws={'label': statistic_label})
     
    plt.xlabel('Time [s]')
    plt.ylabel('Channel')
    
    window_num = len(time_windows)
    xtick_size =  int(window_num / xtick_num)
    
    if xtick_size * xtick_num + int(xtick_size / 2) >= window_num:        
        xtick_num -= 1
    else:
        while xtick_size * (xtick_num +1) + int(xtick_size / 2) < window_num:
            xtick_num += 1
    
    xticks = [int(xtick_size / 2) + xtick_size * i for i in range(xtick_num + 1)]
    xtick_labels = [int(time_windows[int(xtick_size / 2) + xtick_size * i]) for i in range(xtick_num + 1)]
    
    detection_xticks = []
    detection_yticks = []
    
    alarm_xticks = []
    alarm_yticks = []
    
    for plot_index, detection_times in enumerate(detection_times_per_channel):
        
        alarm_times = alarm_times_per_channel[plot_index]
        
        for alarm_time, detection_time in zip(alarm_times, detection_times):
        
            detection_xticks.append(np.argmin(np.abs(detection_time - time_windows)))
            detection_yticks.append(.5 + plot_index)
            
            alarm_xticks.append(np.argmin(np.abs(alarm_time - time_windows)))
            alarm_yticks.append(.5 + plot_index)
    
    #plt.scatter(detection_xticks, detection_yticks, color='greenyellow', marker='X', s=60, zorder=2, edgecolor='black', linewidth=0.1, label='Shift')

    plt.scatter(alarm_xticks, alarm_yticks,
                color='lime', marker='d', s=60, zorder=2,
                edgecolor='black', linewidth=0.1, label='t$_\mathrm{x}$')
    
    if epindex_targets is not None:
        
        for epindex_target, epindex_target_label, epindex_target_color in zip(epindex_targets, epindex_target_labels, epindex_target_colors):
        
            epindex_target_xtick = np.argmin(np.abs(time_windows - epindex_target))
            
            plt.axvline(epindex_target_xtick, label=epindex_target_label, linestyle=':', color=epindex_target_color, linewidth=1.5)
    
    plt.xticks(xticks, xtick_labels)
    
    plt.yticks(.5 + np.arange(plot_channel_num), plot_channels)
    
    plt.xticks(rotation=-360)
    plt.yticks(rotation=-360)
    
    plt.legend(loc='upper left', ncols=1)
    
    fig.tight_layout()
    
    if title is not None:
        
        plt.title(title)
        
        
def plot_epindex_statistics(plot_channels: list,
                            epindex_alarms_per_channel: list,
                            epindex_tonicities_per_channel: list,
                            epindex_delays_per_channel: list,
                            epindex_values_per_channel: list,
                            color_per_channel: list,
                            epindex_name: str,
                            alarm_threshold: float = None,
                            title: str = None,
                            patient: str = None):
    
    max_epindex_values = []
    max_epindex_alarms = []
    max_epindex_delays = []
    max_epindex_tonicities = []
    max_epindex_labels = []
    max_epindex_colors = []
    
    for values, alarms, delays, tonicities, channel, color in\
        zip(epindex_values_per_channel,
            epindex_alarms_per_channel,
            epindex_delays_per_channel,
            epindex_tonicities_per_channel,
            plot_channels,
            color_per_channel):
            
        max_epindex_colors.append(color)
        max_epindex_labels.append(channel)
        max_index = np.argmax(values)
        
        if delays[max_index] is None:
            
            max_epindex_values.append(0)
            max_epindex_alarms.append(0)
            max_epindex_tonicities.append(0)
            max_epindex_delays.append(0)
            
        else:
        
            max_epindex_values.append(values[max_index])
            max_epindex_alarms.append(alarms[max_index])
            max_epindex_tonicities.append(tonicities[max_index])
            max_epindex_delays.append(delays[max_index])
        
    max_epindex_values = [x / np.max(max_epindex_values) for x in max_epindex_values]
        
    # color_map = get_plot_colors(4)
            
    # max_epindex_colors =\
    #     ['tab:grey' for _ in range(4)] +\
    #     [color_map[0] for _ in range(2)] +\
    #     [color_map[1] for _ in range(3)] +\
    #     [color_map[2] for _ in range(4)] +\
    #     [color_map[1] for _ in range(1)] +\
    #     [color_map[3] for _ in range(1)]
            
    epindex_coordinates = np.arange(len(max_epindex_labels)) + 1

    plt.figure(figsize=(8, 3))
    plt.bar(epindex_coordinates, max_epindex_values, color=max_epindex_colors, width=0.5)
    plt.grid('on')    
    plt.xticks(ticks=epindex_coordinates, labels=max_epindex_labels)
    plt.xlim([epindex_coordinates[0] - 1, epindex_coordinates[-1] + 1])
    plt.ylim([0, 1])
    
    # legend_elements = [Patch(facecolor=color_map[0], edgecolor='k',
    #                     label='Superior occupital gyrus'),
    #                    Patch(facecolor=color_map[1], edgecolor='k',
    #                     label='Collateral sulcus'),
    #                    Patch(facecolor=color_map[2], edgecolor='k',
    #                     label='Fusiform gyrus'),
    #                    Patch(facecolor=color_map[3], edgecolor='k',
    #                          label='Middle occipital gyrus')]
    
    # plt.legend(handles=legend_elements, ncol=1, loc='upper left', prop={'size': 12})
    
    plt.ylabel(epindex_name)
        
    if title is not None:
        plt.title(title)
        
    # plt.figure()   

    # plt.bar(epindex_coordinates, max_epindex_delays, color=max_epindex_colors, width=0.5)    
    # plt.grid('on')    
    # plt.ylabel('Delay [s]')
    # plt.xticks(ticks=epindex_coordinates, labels=max_epindex_labels)
    
    # if title is not None:
    #     plt.title(title)
        
    # plt.figure()  
     
    # plt.bar(epindex_coordinates, max_epindex_alarms, color=max_epindex_colors, width=0.5)  
    # if alarm_threshold is not None:
    #     plt.axhline(y=alarm_threshold, color='k', linestyle='dashdot', label='Alarm threshold')  
    #     plt.legend()
    # plt.grid('on')    
    # plt.ylabel('Alarm')
    # plt.xticks(ticks=epindex_coordinates, labels=max_epindex_labels)
    
    # if title is not None:
    #     plt.title(title)
        
    # plt.figure()  
     
    # plt.bar(epindex_coordinates, max_epindex_tonicities, color=max_epindex_colors, width=0.5)    
    # plt.grid('on')    
    # plt.ylabel('Tonicity')
    # plt.xticks(ticks=epindex_coordinates, labels=max_epindex_labels)
    
    # if title is not None:
    #     plt.title(title)
        
    # plt.savefig('output/ilas_connection_values.eps', format='eps', dpi=600)