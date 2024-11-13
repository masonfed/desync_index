from analyze_seeg_features.folder_management import *
from utilities.math.transform import short_time_fourier_transform, hilbert_transform
from utilities.signal.channels import get_channels, get_seeg_bipolar_channels
from utilities.plot.signal import plot_signal_channels
from utilities.plot.signal import plot_time_freq_signal
from utilities.plot.general import get_plot_labels
from utilities.plot.matrix import plot_matrix
from utilities.signal.time import get_times
import matplotlib.pyplot as plt
import numpy as np
import scipy

    
def plot_seeg_energy(energy_folder,
                     patient: str,
                     work_signal,
                     work_channels,
                     sampling_frequency,
                     window_duration: float,
                     window_shift: float,
                     time_start: float,
                     time_duration: float,
                     max_plot_num: int,
                     plot_montage: str,
                     source_channel: str = None):
    
    time_windows = np.load(energy_folder + 'time_windows.npz')['data']
    
    if source_channel is not None:
        source_channel_index = work_channels.index(source_channel)
    
        signal_amplitudes, initial_signal_phases =\
                short_time_fourier_transform(work_signal[source_channel_index],
                                            sampling_frequency,
                                            window_duration,
                                            window_shift)
                
        _, instant_signal_phases = hilbert_transform(work_signal[source_channel_index],
                                                    sampling_frequency,
                                                    window_duration,
                                                    window_shift)
    
    times, time_windows, window_time_start, window_time_end, work_signal =\
        get_times(time_start, time_duration, sampling_frequency, time_windows, work_signal)
        
    energy_ratios_per_channel = np.load(energy_folder + 'energy_ratios_per_channel.npz')['data'][:,window_time_start:window_time_end]
    energies_per_channel = np.load(energy_folder + 'energies_per_channel.npz')['data'][:,window_time_start:window_time_end]

    initial_phase_distributions_per_channel =\
        np.load(energy_folder + 'initial_phase_distributions_per_channel.npz')['data'][:,window_time_start:window_time_end]
    instant_phase_distributions_per_channel =\
        np.load(energy_folder + 'instant_phase_distributions_per_channel.npz')['data'][:,window_time_start:window_time_end]

    initial_phase_entropies_per_channel =\
        np.load(energy_folder + 'initial_phase_entropies_per_channel.npz')['data'][:,window_time_start:window_time_end]
    instant_phase_entropies_per_channel =\
        np.load(energy_folder + 'instant_phase_entropies_per_channel.npz')['data'][:,window_time_start:window_time_end]

    if plot_montage is None:
        
        value_per_channel = [-np.min(instant_phase_entropies_per_channel[i])
                             for i in range(len(work_channels))]    
        plot_channels, plot_channel_indexes =\
            get_plot_labels(work_channels, value_per_channel, max_plot_num)
        
    else:
        
        plot_channels = get_channels(patient, plot_montage)
        plot_channels = [channel for channel in plot_channels if channel in work_channels]                      
        plot_channel_indexes = [work_channels.index(channel) for channel in plot_channels]
    
    bipolar_signal, bipolar_channels =\
        get_seeg_bipolar_channels(work_signal, work_channels)
    
    plot_signal_channels(times - times[0],
                         np.asarray(work_channels)[plot_channel_indexes],
                         bipolar_signal[plot_channel_indexes])
    
    print('Channel number:', len(work_channels))
    
    
    time_windows_distributions_per_channel = np.ones(initial_phase_distributions_per_channel.shape)
    
    for window_index in range(len(time_windows)):
        
        time_windows_distributions_per_channel[:, window_index, :] = time_windows[window_index]
        
    time_windows_distributions_1_per_channel = np.ones(instant_phase_distributions_per_channel.shape)
    
    for window_index in range(len(time_windows)):
        
        time_windows_distributions_1_per_channel[:, window_index, :] = time_windows[window_index]
    
    if source_channel is not None:
        signal_amplitudes = signal_amplitudes[window_time_start:window_time_end]
        initial_signal_phases = initial_signal_phases[window_time_start:window_time_end]
        instant_signal_phases = instant_signal_phases[window_time_start:window_time_end]

        plt.figure()    
        hist = plt.hist2d(time_windows_distributions_per_channel[source_channel_index].flatten(),
                        initial_phase_distributions_per_channel[source_channel_index].flatten(),                      
                        bins=[len(time_windows), 100], density=True, facecolor='b')    
        plt.colorbar(hist[3])
        plt.ylabel('Initial phase [rad]')
        plt.xlabel('Time [s]')
        plt.title(work_channels[source_channel_index])
        
        plt.figure()    
        hist = plt.hist2d(time_windows_distributions_1_per_channel[source_channel_index].flatten(),
                        instant_phase_distributions_per_channel[source_channel_index].flatten(),                      
                        bins=[len(time_windows), 100], density=True, facecolor='b')    
        plt.colorbar(hist[3])
        plt.ylabel('Instantaneous phase [rad]')
        plt.xlabel('Time [s]')
        plt.title(work_channels[source_channel_index])
                
        frequencies = scipy.fft.fftfreq(int(sampling_frequency * window_duration), 1 / sampling_frequency)
                
        max_freq_index = np.argmin(np.abs(frequencies - 250))
        
        plot_time_freq_signal(times / window_shift,
                              time_windows,
                              frequencies[:max_freq_index],
                              bipolar_signal[source_channel_index],
                              signal_amplitudes[:, :max_freq_index],
                              instant_signal_phases,
                              title=work_channels[source_channel_index])

    plot_matrix(instant_phase_entropies_per_channel[plot_channel_indexes],
                time_windows,
                plot_channels,
                'Instant phase entropy',
                'Time [s]',
                'Channel')
    
    plot_matrix(initial_phase_entropies_per_channel[plot_channel_indexes],
                time_windows,
                plot_channels,
                'Initial phase entropy',
                'Time [s]',
                'Channel')
       
    plot_matrix(energy_ratios_per_channel[plot_channel_indexes],
                time_windows,
                plot_channels,
                'Energy ratio',
                'Time [s]',
                'Channel')
    
    plot_matrix(energies_per_channel[plot_channel_indexes],
                time_windows,
                plot_channels,
                'Energy [$V^2 \\times s$]',
                'Time [s]',
                'Channel')
    
    print('Plotting...')
        
    plt.show()