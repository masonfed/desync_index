import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_matrix_min(matrix_values: np.ndarray,
                    xtick_labels: np.ndarray,
                    ytick_labels: np.ndarray,
                    label: str,
                    xlabel: str,
                    ylabel: str,
                    xtick_num: int = 20,
                    ytick_num: int = 10,
                    title: str = None):
    
    plt.figure()
    
    xtick_size = int(len(xtick_labels) / xtick_num)     
    xtick_num = int(len(xtick_labels) / xtick_size)   
    xticks = [0.5 + i for i in range(xtick_num)]
    xtick_labels = [xtick_labels[int(xtick_size / 2) + i * xtick_size] for i in range(xtick_num)]
        
    matrix_max_values = np.zeros((ytick_num, xtick_num))
    matrix_max_labels = [[None for _ in range(xtick_num)] for _ in range(ytick_num)]
    
    for i in np.arange(0, xtick_num):
        
        values = np.mean(matrix_values[:, i*xtick_size:(i+1)*xtick_size], axis=1)
        
        for j in range(ytick_num):
            
            index = np.argmin(values)
            
            matrix_max_values[j, i] = values[index]
            matrix_max_labels[j][i] = ytick_labels[index]
            
            values[index] = np.infty
    
    sns.heatmap(matrix_max_values, cmap='plasma', annot=matrix_max_labels, annot_kws={'fontsize': 10}, fmt='s',\
        vmin=np.min(matrix_max_values), vmax=np.max(matrix_max_values), cbar_kws={'label': label}) 
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.xticks(xticks, xtick_labels)
    plt.yticks(0.5 + np.arange(ytick_num), ['' for _ in range(ytick_num)])
    
    if title is not None:
        
        plt.title(title)


def plot_matrix_max(matrix_values: np.ndarray,
                    xtick_labels: np.ndarray,
                    ytick_labels: np.ndarray,
                    label: str,
                    xlabel: str,
                    ylabel: str,
                    xtick_num: int = 20,
                    ytick_num: int = 10,
                    title: str = None):
    
    plt.figure()
    
    xtick_size = int(len(xtick_labels) / xtick_num)     
    xtick_num = int(len(xtick_labels) / xtick_size)   
    xticks = [0.5 + i for i in range(xtick_num)]
    xtick_labels = [xtick_labels[int(xtick_size / 2) + i * xtick_size] for i in range(xtick_num)]
        
    matrix_max_values = np.zeros((ytick_num, xtick_num))
    matrix_max_labels = [[None for _ in range(xtick_num)] for _ in range(ytick_num)]
    
    for i in range(xtick_num):
        
        values = np.mean(matrix_values[:, i*xtick_size:(i+1)*xtick_size], axis=1)
        
        for j in range(ytick_num):
            
            index = np.argmax(values)
            
            matrix_max_values[j, i] = values[index]
            matrix_max_labels[j][i] = ytick_labels[index]
            
            values[index] = -np.infty
    
    sns.heatmap(matrix_max_values, cmap='plasma', annot=matrix_max_labels, annot_kws={'fontsize': 10}, fmt='s',\
        vmin=np.min(matrix_max_values), vmax=np.max(matrix_max_values), cbar_kws={'label': label}) 
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.xticks(xticks, xtick_labels)
    plt.yticks(0.5 + np.arange(ytick_num), ['' for _ in range(ytick_num)])
    
    if title is not None:
        
        plt.title(title)


def plot_matrix(matrix_values: np.ndarray,
                xtick_labels: np.ndarray,
                ytick_labels: np.ndarray,
                label: str,
                xlabel: str,
                ylabel: str,
                xtick_num: int = 30,
                ytick_num: int = None,
                title: str = None,
                lim=None):
    
    plt.figure()
    
    if xtick_num > len(xtick_labels):
        xtick_num = len(xtick_labels)
    
    xtick_size = int(np.floor(len(xtick_labels) / xtick_num))
    xtick_num = int(np.floor(len(xtick_labels) / xtick_size))
    xticks = [int(np.floor(xtick_size / 2)) + i * xtick_size for i in range(xtick_num)]
    
    xtick_labels = [xtick_labels[int(np.floor(xtick_size / 2)) +  i * xtick_size]\
        for i in range(xtick_num)]
    
    if ytick_num is None:
        yticks = 0.5 + np.arange(len(ytick_labels))
    else:        
        ytick_size = int(len(ytick_labels) / ytick_num)     
        yticks = [int(np.floor(ytick_size / 2)) + i * ytick_size for i in range(ytick_num)]
        ytick_labels = [ytick_labels[int(np.floor(ytick_size / 2)) + i * ytick_size] for i in range(ytick_num)]
        
    if lim is None:
        vmin=np.min(matrix_values)
        vmax=np.max(matrix_values)
    else:
        vmin=lim[0]
        vmax=lim[1]
    
    sns.heatmap(matrix_values,
                cmap='plasma',
                annot_kws={'fontsize': 10},
                fmt='s',
                vmin=vmin,
                vmax=vmax,
                cbar_kws={'label': label})
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.xticks(xticks, xtick_labels)
    plt.yticks(yticks, ytick_labels)
    
    plt.yticks(rotation=0)
    
    if title is not None:
        
        plt.title(title)