import sklearn.mixture as mixture
import matplotlib.pyplot as plt
import numpy as np


def fit_uniform(data: np.ndarray):
    
    probs, bins, _ = plt.hist(data, len(np.unique(data)), density=True, facecolor='b')
    
    i = len(bins)
    
    for prob in reversed(probs):
        
        i -= 1
        
        if prob < np.mean(probs):
            break
    
    return bins[i]


def fit_gaussian(data: np.ndarray):
        
    clf = mixture.GaussianMixture(n_components=2, covariance_type="full", tol=0.00001, verbose=0, max_iter=1000)
    mixtures = clf.fit(data.reshape(-1, 1))
    
    mixture_means, mixture_covariances = np.asarray(mixtures.means_).flatten() / 2, np.asarray(mixtures.covariances_).flatten() / 4
    mixture_intersections = []
    
    old_mean = None
    
    for mean, cov in zip(mixture_means, mixture_covariances):
        
        if old_mean is not None:
            
            a = - 1 / cov + 1 / old_cov
            b = - 2 * old_mean / old_cov + 2 * mean / cov
            c = - mean ** 2 / cov + old_mean ** 2 / old_cov + np.log(old_cov/cov)
            
            y = np.roots([a,b,c])
            
            mixture_intersections.append(y.flatten())
        
        old_mean, old_cov = mean, cov
        
    return mixture_means, mixture_covariances, mixture_intersections