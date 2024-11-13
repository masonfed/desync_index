import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import matplotlib

font = {'family' : 'STIXGeneral',
        'size'   : 16}

matplotlib.rc('font', **font)
    
    
def multi_plot_signal_channels(multi_legend: list,
                               multi_group: list,
                               multi_work_signal: list,
                               multi_work_channels: list,
                               multi_times: list,
                               multi_plot_channels: list,
                               unique_signal: bool):
    
    plot_channels = []
    for y in multi_plot_channels:
        plot_channels.extend([x for x in y if x not in plot_channels])
        
    plot_channels.sort()
    
    if unique_signal:  
        
        work_signal = multi_work_signal[0]
        work_channels = list(multi_work_channels[0])
        times = multi_times[0]
        
        plot_signal = [work_signal[work_channels.index(channel)] for channel in plot_channels]
            
        plot_signal_channels(times,
                             plot_channels,
                             plot_signal)
        
        
    else:
        
        if multi_group is not None:            
            multi_label = [legend +', ' + group for legend, group in zip(multi_legend, multi_group)]
            
        else:
            multi_label = multi_legend
        
        for label, work_signal, work_channels, times, plot_channels in\
            zip(multi_label, multi_work_signal, multi_work_channels, multi_times, multi_plot_channels):
                
            work_channels = list(work_channels)
            
            plot_signal = [work_signal[work_channels.index(channel)] for channel in plot_channels]
            
            plot_signal_channels(times,
                                 plot_channels,
                                 plot_signal,
                                 title=label)


def plot_signal_channels(times: np.ndarray,
                         channels: list,
                         signal_per_channel: list,
                         alarms_per_channel: list = None,
                         detections_per_channel: list = None,
                         signal_feature_label: str = None,
                         signal_feature_times: np.ndarray = None,
                         signal_features: np.ndarray = None,
                         vlines: float = None,
                         vline_labels: str = None,
                         vline_colors: list = None,
                         title: str = None,
                         amplitude: float = .25):
    
    if signal_features is not None:
        
        _, axes  = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [7, 1]})
        
        ax = axes[0]
        ax.set_facecolor('lightyellow')
        sub_ax = axes[1]
        sub_ax.set_facecolor('lightyellow')
        
    else:
        
        _, axes  = plt.subplots()
        
        ax = axes
        ax.set_facecolor('lightyellow')
        sub_ax = None  
        
    channel_num = len(channels)
    
    signal_per_channel = [signal * amplitude / np.mean(np.abs(signal_per_channel)) for signal in signal_per_channel]
    
    shift = 2
    
    for index, signal in zip(range(1, channel_num + 1), signal_per_channel):
        
        ax.plot(times, signal - index * shift, color='k', linewidth=0.3)
        
    if detections_per_channel is not None and alarms_per_channel is not None:        
        for index, detection_times, alarms_times in zip(range(1, channel_num + 1), detections_per_channel, alarms_per_channel):
            for detection_time, alarm_time in zip(detection_times, alarms_times): 
                              
                if alarm_time > times[0]:
                   
                   ax.scatter(x = alarm_time, y = - index * shift, color='lime', marker='d', edgecolor='black', linewidth=0.2, s=80, zorder=10)
                    
    ax.set_yticks([- i * shift for i in range(1, channel_num + 1)], channels)        
    
    ax.grid('on', which='both')       
    ax.set_ylabel('Channel')
    ax.set_xlim([times[0], times[-1]]) 
    
    vline_handles = []
     
    if vlines is not None:
        
        for vline, vline_label, vline_color in zip(vlines, vline_labels, vline_colors):
            
            ax.axvline(vline, linestyle=':', color=vline_color, linewidth=1.5)
            
            vline_handles.append(mlines.Line2D([], [], linestyle=':', color=vline_color, linewidth=2, label=vline_label))
            
    if detections_per_channel is not None and alarms_per_channel is not None:      
        
        ax.legend(handles=[mlines.Line2D([], [],
                                         color='lime',
                                         marker='d',
                                         linestyle='None',
                                         markersize=8,
                                         label='t$_\mathrm{x}$')] + vline_handles,
                  loc='upper left',
                  ncols=1)
            
    ax.set_ylim([-(channel_num + 1) * shift, shift])
        
    if title is not None:        
        plt.title(title)
    
    if sub_ax is not None:
        
        sub_ax.plot(signal_feature_times, signal_features, linestyle='-', color='orangered', linewidth=1.0)
        sub_ax.grid('on', which='both')    
        sub_ax.set_xlabel('Time [s]')
        
        if signal_feature_label is not None:
            sub_ax.set_ylabel(signal_feature_label)
            
        sub_ax.set_xlim([signal_feature_times[0], signal_feature_times[-1]])
        
    else:

        ax.set_xlabel('Time [s]') 
        
        
def plot_time_freq_signal(times: np.ndarray,
                          time_windows: np.ndarray,
                          frequencies: np.ndarray,
                          signal: np.ndarray,
                          signal_amplitudes: np.ndarray,                          
                          signal_phases: np.ndarray,
                          title: str = None,
                          phase_label: str = 'Phase',
                          xtick_num: int = 30,
                          ytick_num: int = 10,
                          ztick_num: int = 10):
    
    if xtick_num > len(time_windows):
        xtick_num = len(time_windows)
    
    xtick_size = int(np.floor((len(time_windows) / xtick_num)))
    xtick_num = int(np.floor(len(time_windows) / xtick_size)) 
    xticks = [int(np.floor(xtick_size / 2)) + i * xtick_size for\
        i in range(xtick_num)]    
    xtick_labels = [time_windows[int(np.floor(xtick_size / 2)) + i * xtick_size]\
        for i in range(xtick_num)]
    
    ytick_size = int(np.floor(len(frequencies) / ytick_num))    
    yticks = [int(np.floor(ytick_size / 2)) + i * ytick_size\
        for i in range(ytick_num)]
    ytick_labels = [frequencies[int(np.floor(ytick_size / 2)) + i * ytick_size]\
        for i in reversed(range(ytick_num))]
    
    fig, axes  = plt.subplots(3, 2, sharex='col',
                              gridspec_kw={'width_ratios':[149,1]})
    
    axes[0,0].set_facecolor('lightyellow')
    
    axes[0,0].plot(times - times[0], signal * 1000, color='k', linewidth=0.3)
    
    axes[0,0].grid(True)
    
    if title is not None:
    
        axes[0,0].set_title(title)
    
    axes[0,0].set_ylabel('Voltage [mV]')
    axes[0,0].set_ylim([-.25, .25])
    
    sns.heatmap(np.flip(signal_amplitudes.transpose(), axis=0),
                cmap='plasma',
                annot_kws={'fontsize': 10},
                fmt='s',
                vmin=0,
                vmax=np.percentile(signal_amplitudes, 95),
                cbar_kws={'label': 'Amplitude'},
                ax=axes[1,0],
                cbar_ax=axes[1,1])
    
    axes[1,0].set_ylabel('Frequency [Hz]')
    axes[1,0].yaxis.set_ticks(yticks)        
    axes[1,0].yaxis.set_ticklabels(ytick_labels)
            
    axes[1,0].xaxis.set_ticks(xticks)
    axes[1,0].xaxis.set_ticklabels(xtick_labels)
    
    phases = np.linspace(np.min(signal_phases),
                         np.max(signal_phases), 100)  
    ztick_size = int(np.floor(len(phases) / ztick_num))
    zticks = [int(np.floor(ztick_size / 2)) + i * ztick_size\
        for i in range(ztick_num)]    
    
    ztick_labels = [int(phases[int(np.floor(ztick_size / 2))\
        + i * ztick_size] * 180 / np.pi)\
            for i in range(ztick_num)]
    
    signal_phases -= np.min(signal_phases)
    signal_phases /= np.max(signal_phases) / 100
    
    signal_times = np.zeros(signal_phases.shape)
    
    if len(time_windows) > len(signal_times):
        
        time_windows = np.copy(time_windows)[:len(signal_times)]
    
    for i, window in enumerate(time_windows):
        signal_times[i] = (window - time_windows[0]) * len(time_windows) / ((len(time_windows)-1)* (time_windows[1] - time_windows[0]))
    
    h = axes[2,0].hist2d(signal_times.flatten(),
                         signal_phases.flatten(),                         
                         bins=[len(time_windows), 100],
                         density=True,
                         facecolor='b')
    
    fig.colorbar(h[3], cax=axes[2,1], label=phase_label + ' probability')
    
    axes[2,0].set_ylabel(phase_label + ' [grad]') 
    axes[2,0].yaxis.set_ticks(zticks)        
    axes[2,0].yaxis.set_ticklabels(ztick_labels)  
    
    axes[2,0].xaxis.set_ticks(xticks)
    axes[2,0].xaxis.set_ticklabels(xtick_labels)
    axes[2,0].set_xlabel('Time [s]')

    axes[0,1].remove()
        
        
def plot_signal_features(times: np.ndarray,
                         time_windows: np.ndarray,
                         signal: np.ndarray,
                         data_per_feature: list,
                         label_per_features: list,
                         title: str = None):
    
    feature_num = len(data_per_feature)
    
    fig, axes  = plt.subplots(feature_num + 1, 1)
    
    axes[0].set_facecolor('lightyellow')
    
    axes[0].plot(times, signal * 1000, color='k', linewidth=0.3)
    
    axes[0].grid(True)
    
    if title is not None:
    
        axes[0].set_title(title)
    
    axes[0].set_ylabel('Voltage [mV]')
    
    axes[0].set_xlim([time_windows[0], time_windows[-1]])
    
    for ax, data, label in zip(axes[1:], data_per_feature, label_per_features): 
        
        if data.ndim > 1:    
            
            data_means = np.mean(data, axis=0)
            data_75percent = np.percentile(data, 75, axis=0)
            data_25percent = np.percentile(data, 25, axis=0)
            
            ax.plot(time_windows, data_75percent, linestyle='-', color='orangered', label='Inter-quartile range')
            ax.plot(time_windows, data_25percent, linestyle='-', color='orangered')
            ax.fill_between(time_windows, y1=data_25percent, y2=data_75percent, color='lightsalmon')
            ax.plot(time_windows, data_means, linestyle='-.', color='orangered', label='Mean')  
            ax.legend()  
        else:
            
            ax.plot(time_windows, data, linestyle='-', color='orangered')
        
        ax.set_ylabel(label)
        ax.grid(True)
        
        ax.set_xlim([time_windows[0], time_windows[-1]])
        
    axes[-1].set_xlabel('Times [s]')     
    
    fig.tight_layout()