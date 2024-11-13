import argparse
from analyze_seeg_features.compute_features import compute_seeg_features, multi_compute_seeg_features
from analyze_seeg_features.aggregate_features import aggregate_seeg_features
from analyze_seeg_features.plot_features import plot_seeg_features, multi_plot_seeg_features
from analyze_seeg_features.generate_label import generate_seeg_labels, get_seeg_default_parameters
parser = argparse.ArgumentParser()

parser.add_argument('-patient', '--patient', type=str, default=None)
parser.add_argument('-epoch', '--epoch', type=str, default=None)
parser.add_argument('-work_montage', '--work_montage', type=str, default='grey_0')
parser.add_argument('-plot_montage', '--plot_montage', type=str, default=None)
parser.add_argument('-time_start', '--time_start', type=float, default=0.0)
parser.add_argument('-time_duration', '--time_duration', type=float, default=None)

parser.add_argument('-highpass_frequency', '--highpass_frequency', type=float, default=None)
parser.add_argument('-lowpass_frequency', '--lowpass_frequency', type=float, default=None)
parser.add_argument('-notch_frequency', '--notch_frequency', type=float, default=None)
parser.add_argument('-window_duration', '--window_duration', type=float, default=1.0)
parser.add_argument('-window_shift', '--window_shift', type=float, default=0.25)

parser.add_argument('-energy_low_freq_0', '--energy_low_freq_0', type=float, default=4)
parser.add_argument('-energy_low_freq_1', '--energy_low_freq_1', type=float, default=12)
parser.add_argument('-energy_high_freq_0', '--energy_high_freq_0', type=float, default=30)
parser.add_argument('-energy_high_freq_1', '--energy_high_freq_1', type=float, default=250)

parser.add_argument('-target_channel', '--target_channel', type=str, default=None)
parser.add_argument('-source_channel', '--source_channel', type=str, default=None)

parser.add_argument('-connection_technique', '--connection_technique', type=str, default='dpte')
parser.add_argument('-connection_bin_rule', '--connection_bin_rule', type=str, default='sturges')
parser.add_argument('-connection_lag', '--connection_lag', type=float, default=0.010)
parser.add_argument('-connection_lag_num', '--connection_lag_num', type=int, default=10)

parser.add_argument('-alarm_smooth', '--alarm_smooth', type=float, default=0.1)
parser.add_argument('-alarm_baseline', '--alarm_baseline', type=float, default=1.0)
parser.add_argument('-alarm_low_percent', '--alarm_low_percent', type=float, default=25)
parser.add_argument('-alarm_high_percent', '--alarm_high_percent', type=float, default=75)

parser.add_argument('-graph_start', '--graph_start', type=float, default=0.0)
parser.add_argument('-graph_base', '--graph_base', type=float, default=None)
parser.add_argument('-graph_min', '--graph_min', type=str, default=str(0.1))
parser.add_argument('-graph_max', '--graph_max', type=str, default='default')

parser.add_argument('-epindex_start', '--epindex_start', type=float, default=0.0)
parser.add_argument('-epindex_base', '--epindex_base', type=float, default=None)
parser.add_argument('-epindex_end', '--epindex_end', type=float, default=None)
parser.add_argument('-epindex_bias', '--epindex_bias', type=float, default=0.0)
parser.add_argument('-epindex_threshold', '--epindex_threshold', type=str, default='adaptive')
parser.add_argument('-epindex_decay', '--epindex_decay', type=float, default=0.1)
parser.add_argument('-epindex_tonicity', '--epindex_tonicity', type=float, default=5.0)

parser.add_argument('-compute_connection', '--compute_connection', dest='compute_connection', action='store_true')
parser.add_argument('-compute_graph', '--compute_graph', dest='compute_graph', action='store_true')
parser.add_argument('-compute_energy', '--compute_energy', dest='compute_energy', action='store_true')
parser.add_argument('-compute_connection_alarm', '--compute_connection_alarm', dest='compute_connection_alarm', action='store_true')
parser.add_argument('-compute_desync_epindex', '--compute_desync_epindex', dest='compute_desync_epindex', action='store_true')
parser.add_argument('-compute_bartolomei_epindex', '--compute_bartolomei_epindex', dest='compute_bartolomei_epindex', action='store_true')

parser.add_argument('-plot_energy', '--plot_energy', dest='plot_energy', action='store_true')
parser.add_argument('-plot_connection', '--plot_connection', dest='plot_connection', action='store_true')
parser.add_argument('-plot_channel', '--plot_channel', dest='plot_channel', action='store_true')
parser.add_argument('-plot_graph', '--plot_graph', dest='plot_graph', action='store_true')
parser.add_argument('-plot_connection_alarm', '--plot_connection_alarm', dest='plot_connection_alarm', action='store_true')
parser.add_argument('-plot_desync_epindex', '--plot_desync_epindex', dest='plot_desync_epindex', action='store_true')
parser.add_argument('-plot_bartolomei_epindex', '--plot_bartolomei_epindex', dest='plot_bartolomei_epindex', action='store_true')

parser.add_argument('-aggregate_signal', '--aggregate_signal', dest='aggregate_signal', action='store_true')
parser.add_argument('-aggregate_connection', '--aggregate_connection', dest='aggregate_connection', action='store_true')
parser.add_argument('-aggregate_graph', '--aggregate_graph', dest='aggregate_graph', action='store_true')
parser.add_argument('-aggregate_energy', '--aggregate_energy', dest='aggregate_energy', action='store_true')


parser.add_argument('-compare_statistic', '--compare_statistic', dest='compare_statistic', action='store_true')

parser.add_argument('-default', '--default', dest='default', action='store_true')

parser.add_argument('-export', '--export', type=str, default=None)
parser.add_argument('-multi_variable', '--multi_variable', type=str, default=None)
parser.add_argument('-max_plot', '--max_plot', type=int, default=15)

if __name__ == '__main__':

    args = vars(parser.parse_args())

    patient = args['patient']
    epoch = args['epoch']
    highpass_frequency = args['highpass_frequency']
    lowpass_frequency = args['lowpass_frequency']
    notch_frequency = args['notch_frequency']
    work_montage = args['work_montage']
    plot_montage = args['plot_montage']
    multi_variable = args['multi_variable']
    max_plot_num = args['max_plot']

    compute_connection = args['compute_connection']
    compute_graph = args['compute_graph']
    compute_energy = args['compute_energy']
    compute_connection_alarm = args['compute_connection_alarm']
    compute_desync_epindex = args['compute_desync_epindex'] or args['plot_desync_epindex']
    compute_bartolomei_epindex = args['compute_bartolomei_epindex'] or args['plot_bartolomei_epindex']
    
    plot_channel = args['plot_channel']
    plot_connection = args['plot_connection']
    plot_graph = args['plot_graph']
    plot_energy = args['plot_energy']  
    plot_connection_alarm = args['plot_connection_alarm']
    plot_desync_epindex = args['plot_desync_epindex']  
    plot_bartolomei_epindex = args['plot_bartolomei_epindex']
    
    aggregate_signal = args['aggregate_signal']
    aggregate_connection = args['aggregate_connection']
    aggregate_graph = args['aggregate_graph']
    aggregate_energy = args['aggregate_energy']
    
    compare_statistic = args['compare_statistic']
    
    window_duration = args['window_duration']
    window_shift = args['window_shift']
    
    connection_technique = args['connection_technique']
    connection_bin_rule = args['connection_bin_rule']
    connection_lag = args['connection_lag']
    connection_lag_num = args['connection_lag_num']
    
    alarm_smooth = args['alarm_smooth']
    alarm_baseline = args['alarm_baseline']    
    alarm_low_percent = args['alarm_low_percent']
    alarm_high_percent = args['alarm_high_percent']
    
    epindex_start = args['epindex_start']
    epindex_base = args['epindex_base']
    epindex_end = args['epindex_end']
    epindex_bias = args['epindex_bias']
    epindex_threshold = args['epindex_threshold']
    epindex_decay = args['epindex_decay']
    epindex_tonicity = args['epindex_tonicity']

    graph_start = args['graph_start']
    graph_base = args['graph_base']    
    graph_min = args['graph_min']
    graph_max = args['graph_max']
    
    energy_low_freqs = [args['energy_low_freq_0'], args['energy_low_freq_1']]
    energy_high_freqs = [args['energy_high_freq_0'], args['energy_high_freq_1']]
    
    target_channel = args['target_channel']    
    source_channel = args['source_channel']   
     
    time_start = args['time_start']    
    time_duration = args['time_duration']
    
    multi_group = None
    multi_patient = None
    multi_epoch = None
    multi_highpass_frequency = None
    multi_lowpass_frequency = None
    multi_notch_frequency = None
    multi_work_montage = None
    multi_window_shift = None
    multi_window_duration = None
    multi_connection_technique = None
    multi_connection_bin_rule = None
    multi_connection_lag = None
    multi_connection_lag_num = None
    multi_alarm_smooth = None
    multi_alarm_baseline = None
    multi_alarm_low_percent = None
    multi_alarm_high_percent = None
    multi_epindex_base = None
    multi_epindex_start = None
    multi_epindex_end = None
    multi_epindex_bias = None
    multi_epindex_threshold = None
    multi_epindex_decay = None
    multi_epindex_tonicity = None
    multi_graph_start = None
    multi_graph_base = None
    multi_graph_min = None
    multi_graph_max = None
    multi_energy_low_freqs = None
    multi_energy_high_freqs = None
    multi_target_channel = None
    multi_source_channel = None
    multi_time_start = None
    multi_time_duration = None  
    
    if args['default']:
        
        time_start, time_duration, epindex_start, epindex_base, epindex_end =\
            get_seeg_default_parameters(patient, epoch)

    if multi_variable is not None:
        
        multi_epoch, multi_patient, multi_legend, multi_group, multi_time_start, multi_time_duration =\
            generate_seeg_labels(multi_variable, patient)
            
        configuration_num = len(multi_legend)
        
        if multi_patient is None:
            multi_patient = [patient for _ in range(configuration_num)]

        if multi_epoch is None:
            multi_epoch = [epoch for _ in range(configuration_num)]
            
        if multi_highpass_frequency is None:
            multi_highpass_frequency = [highpass_frequency for _ in range(configuration_num)]
            
        if multi_lowpass_frequency is None:
            multi_lowpass_frequency = [lowpass_frequency for _ in range(configuration_num)]
            
        if multi_notch_frequency is None:
            multi_notch_frequency = [notch_frequency for _ in range(configuration_num)]
            
        if multi_work_montage is None:
            multi_work_montage = [work_montage for _ in range(configuration_num)]
            
        if multi_window_shift is None:
            multi_window_shift = [window_shift for _ in range(configuration_num)]
            
        if multi_window_duration is None:
            multi_window_duration = [window_duration for _ in range(configuration_num)]
            
        if multi_connection_technique is None:
            multi_connection_technique = [connection_technique for _ in range(configuration_num)]
            
        if multi_connection_bin_rule is None:
            multi_connection_bin_rule = [connection_bin_rule for _ in range(configuration_num)]
            
        if multi_connection_lag is None:
            multi_connection_lag = [connection_lag for _ in range(configuration_num)]
            
        if multi_connection_lag_num is None:
            multi_connection_lag_num = [connection_lag_num for _ in range(configuration_num)]
            
        if multi_alarm_smooth is None:
            multi_alarm_smooth = [alarm_smooth for _ in range(configuration_num)]
            
        if multi_alarm_baseline is None:
            multi_alarm_baseline = [alarm_baseline for _ in range(configuration_num)]
            
        if multi_alarm_low_percent is None:
            multi_alarm_low_percent = [alarm_low_percent for _ in range(configuration_num)]
            
        if multi_alarm_high_percent is None:
            multi_alarm_high_percent = [alarm_high_percent for _ in range(configuration_num)]
        
        if multi_epindex_base is None:
            multi_epindex_base = [epindex_base for _ in range(configuration_num)]
          
        if multi_epindex_start is None:
            multi_epindex_start = [epindex_start for _ in range(configuration_num)]
            
        if multi_epindex_end is None:
            multi_epindex_end = [epindex_end for _ in range(configuration_num)]
            
        if multi_epindex_bias is None:
            multi_epindex_bias = [epindex_bias for _ in range(configuration_num)]
            
        if multi_epindex_threshold is None:
            multi_epindex_threshold = [epindex_threshold for _ in range(configuration_num)]
        
        if multi_epindex_decay is None:
            multi_epindex_decay = [epindex_decay for _ in range(configuration_num)]
        
        if multi_epindex_tonicity is None:
            multi_epindex_tonicity = [epindex_tonicity for _ in range(configuration_num)]
            
        if multi_graph_start is None:
            multi_graph_start = [graph_start for _ in range(configuration_num)]
            
        if multi_graph_base is None:
            multi_graph_base = [graph_base for _ in range(configuration_num)]
            
        if multi_graph_min is None:
            multi_graph_min = [graph_min for _ in range(configuration_num)]
            
        if multi_graph_max is None:
            multi_graph_max = [graph_max for _ in range(configuration_num)]
            
        if multi_energy_low_freqs is None:
            multi_energy_low_freqs = [energy_low_freqs for _ in range(configuration_num)]
            
        if multi_energy_high_freqs is None:
            multi_energy_high_freqs = [energy_high_freqs for _ in range(configuration_num)]
            
        if multi_target_channel is None:
            multi_target_channel = [target_channel for _ in range(configuration_num)]
        
        if multi_source_channel is None:
            multi_source_channel = [source_channel for _ in range(configuration_num)]
            
        if multi_time_start is None:
            multi_time_start = [time_start for _ in range(configuration_num)]
            
        if multi_time_duration is None:
            multi_time_duration = [time_duration for _ in range(configuration_num)]
        
        if aggregate_signal or aggregate_connection or aggregate_graph or aggregate_energy:
            
            for epoch, patient in zip(multi_epoch, multi_patient):
                
                aggregate_seeg_features(patient,
                                        epoch,
                                        highpass_frequency,
                                        lowpass_frequency,
                                        notch_frequency,
                                        work_montage,
                                        window_duration,
                                        window_shift,
                                        connection_technique,
                                        connection_bin_rule,
                                        connection_lag,
                                        connection_lag_num,
                                        graph_start,
                                        graph_base,
                                        graph_min,
                                        graph_max,
                                        energy_low_freqs,
                                        energy_high_freqs,
                                        aggregate_signal,
                                        aggregate_connection,
                                        aggregate_graph,
                                        aggregate_energy)
        
        if compute_connection or compute_connection_alarm or compute_desync_epindex or compute_graph or compute_energy or compute_bartolomei_epindex:
                
            multi_compute_seeg_features(multi_legend,
                                        multi_group,
                                        multi_patient,
                                        multi_epoch,
                                        multi_highpass_frequency,
                                        multi_lowpass_frequency,
                                        multi_notch_frequency,
                                        multi_work_montage,
                                        multi_window_duration,
                                        multi_window_shift,
                                        multi_connection_technique,
                                        multi_connection_bin_rule,
                                        multi_connection_lag,
                                        multi_connection_lag_num,
                                        multi_alarm_smooth,
                                        multi_alarm_baseline,
                                        multi_alarm_low_percent,
                                        multi_alarm_high_percent,
                                        multi_graph_start,
                                        multi_graph_base,
                                        multi_graph_min,
                                        multi_graph_max,
                                        multi_energy_low_freqs,
                                        multi_energy_high_freqs,
                                        multi_epindex_base,
                                        multi_epindex_start,
                                        multi_epindex_end,
                                        multi_epindex_bias,
                                        multi_epindex_threshold,
                                        multi_epindex_decay,
                                        multi_epindex_tonicity,
                                        compute_connection,
                                        compute_connection_alarm,
                                        compute_desync_epindex,
                                        compute_graph,
                                        compute_energy,
                                        compute_bartolomei_epindex)
            
        if plot_connection or plot_channel or plot_connection_alarm or plot_desync_epindex or plot_graph or plot_energy or plot_bartolomei_epindex:
    
            multi_plot_seeg_features(multi_legend,
                                     multi_group,
                                     multi_patient,
                                     multi_epoch,
                                     multi_highpass_frequency,
                                     multi_lowpass_frequency,
                                     multi_notch_frequency,
                                     multi_work_montage,
                                     multi_window_duration,
                                     multi_window_shift,
                                     multi_connection_technique,
                                     multi_connection_bin_rule,
                                     multi_connection_lag,
                                     multi_connection_lag_num,
                                     multi_alarm_smooth,
                                     multi_alarm_baseline,
                                     multi_alarm_low_percent,
                                     multi_alarm_high_percent,
                                     multi_graph_start,
                                     multi_graph_base,
                                     multi_graph_min,
                                     multi_graph_max,
                                     multi_energy_low_freqs,
                                     multi_energy_high_freqs,
                                     multi_epindex_base,
                                     multi_epindex_start,
                                     multi_epindex_end,
                                     multi_epindex_bias,
                                     multi_epindex_threshold,
                                     multi_epindex_decay,
                                     multi_epindex_tonicity,
                                     multi_source_channel,
                                     multi_target_channel,
                                     multi_time_start,
                                     multi_time_duration,
                                     plot_connection,
                                     plot_channel,
                                     plot_connection_alarm,
                                     plot_desync_epindex,
                                     plot_graph,
                                     plot_energy,
                                     plot_bartolomei_epindex,
                                     compare_statistic,
                                     max_plot_num,
                                     plot_montage)
            
            
            
    else:
        
        if aggregate_signal or aggregate_connection or aggregate_graph or aggregate_energy:
            
            aggregate_seeg_features(patient,
                                    epoch,
                                    highpass_frequency,
                                    lowpass_frequency,
                                    notch_frequency,
                                    work_montage,
                                    window_duration,
                                    window_shift,
                                    connection_technique,
                                    connection_bin_rule,
                                    connection_lag,
                                    connection_lag_num,
                                    graph_start,
                                    graph_base,
                                    graph_min,
                                    graph_max,
                                    energy_low_freqs,
                                    energy_high_freqs,
                                    aggregate_signal,
                                    aggregate_connection,
                                    aggregate_graph,
                                    aggregate_energy)
        
        if compute_energy or compute_connection or compute_graph or compute_connection_alarm or compute_desync_epindex or compute_bartolomei_epindex:
        
            compute_seeg_features(patient,
                                  epoch,
                                  highpass_frequency,
                                  lowpass_frequency,
                                  notch_frequency,
                                  work_montage,
                                  window_duration,
                                  window_shift,
                                  connection_technique,
                                  connection_bin_rule,
                                  connection_lag,
                                  connection_lag_num,
                                  alarm_smooth,
                                  alarm_baseline,
                                  alarm_low_percent,
                                  alarm_high_percent,
                                  graph_start,
                                  graph_base,
                                  graph_min,
                                  graph_max,
                                  energy_low_freqs,
                                  energy_high_freqs,
                                  epindex_base,
                                  epindex_start,
                                  epindex_end,
                                  epindex_bias,
                                  epindex_threshold,
                                  epindex_decay,
                                  epindex_tonicity,
                                  compute_connection,
                                  compute_connection_alarm,
                                  compute_desync_epindex,
                                  compute_graph,
                                  compute_energy,
                                  compute_bartolomei_epindex)                 
          
        if plot_connection or plot_channel or plot_connection_alarm or plot_desync_epindex or plot_graph or plot_energy or plot_bartolomei_epindex:
            
            plot_seeg_features(patient,
                               epoch,
                               highpass_frequency,
                               lowpass_frequency,
                               notch_frequency,
                               work_montage,
                               window_duration,
                               window_shift,
                               connection_technique,
                               connection_bin_rule,
                               connection_lag,
                               connection_lag_num,
                               alarm_smooth,
                               alarm_baseline,
                               alarm_low_percent,
                               alarm_high_percent,
                               graph_start,
                               graph_base,
                               graph_min,
                               graph_max,
                               energy_low_freqs,
                               energy_high_freqs,
                               epindex_base,
                               epindex_start,
                               epindex_end,
                               epindex_bias,
                               epindex_threshold,
                               epindex_decay,
                               epindex_tonicity,
                               source_channel,
                               target_channel,
                               time_start,
                               time_duration,
                               plot_connection,
                               plot_channel,
                               plot_connection_alarm,
                               plot_desync_epindex,
                               plot_graph,
                               plot_energy,
                               plot_bartolomei_epindex,
                               max_plot_num,
                               plot_montage)