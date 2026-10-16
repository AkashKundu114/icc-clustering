"""
Classical single-model clustering baselines.

Refactored from experiments/exp3_real_world_benchmarks/src/benchmark_models.py.
Provides wrappers for K-Means, Ward, Spectral Clustering, and Fuzzy C-Means (FCM).
"""

import time 
from typing import Any ,Dict ,Tuple 

import numpy as np 

from src .icc .core import run_clusterer 


class ModelMetadata (int ):
    """
    Hybrid return container that behaves as an integer (for legacy scripts expecting `lc = N`)
    while also supporting full dictionary indexing (for scripts accessing `metadata["method"]`).
    """
    _data :Dict [str ,Any ]

    def __new__ (cls ,val :int ,**kwargs ):
        obj =super ().__new__ (cls ,int (val ))
        obj ._data =kwargs 
        obj ._data ["n_core"]=int (val )
        return obj 

    def __getitem__ (self ,item :str )->Any :
        return self ._data [item ]

    def get (self ,key :str ,default :Any =None )->Any :
        return self ._data .get (key ,default )

    def items (self ):
        return self ._data .items ()

    def keys (self ):
        return self ._data .keys ()

    def values (self ):
        return self ._data .values ()

    def __contains__ (self ,key :str )->bool :
        return key in self ._data 

    def __repr__ (self )->str :
        return f"{int (self )} ({self ._data })"


def run_kmeans (X :np .ndarray ,k :int ,seed :int =42 )->Tuple [np .ndarray ,float ,ModelMetadata ]:
    """
    Execute standard K-Means++ clustering baseline with 10 restarts.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k : int
        Number of clusters.
    seed : int, default=42
        Random seed for reproducibility.

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Cluster assignments.
    runtime_seconds : float
        Elapsed execution time.
    metadata : ModelMetadata
        Diagnostic properties with integer evaluation (n_core = N).
    """
    t0 =time .perf_counter ()
    from sklearn .cluster import KMeans 
    try :
        km =KMeans (n_clusters =k ,init ="k-means++",n_init =10 ,random_state =seed )
        labels =km .fit_predict (X )
    except Exception :
        labels =run_clusterer ("kmeans",X ,k ,seed =seed )
    runtime =time .perf_counter ()-t0 
    metadata =ModelMetadata (
    X .shape [0 ],
    method ="kmeans",
    n_samples =X .shape [0 ],
    n_features =X .shape [1 ],
    n_clusters =k ,
    )
    return labels ,runtime ,metadata 


def run_ward (X :np .ndarray ,k :int ,seed :int =42 )->Tuple [np .ndarray ,float ,ModelMetadata ]:
    """
    Execute Ward hierarchical agglomerative clustering.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    runtime_seconds : float
    metadata : ModelMetadata
    """
    t0 =time .perf_counter ()
    labels =run_clusterer ("ward",X ,k ,seed =seed )
    runtime =time .perf_counter ()-t0 
    metadata =ModelMetadata (
    X .shape [0 ],
    method ="ward",
    n_samples =X .shape [0 ],
    n_features =X .shape [1 ],
    n_clusters =k ,
    )
    return labels ,runtime ,metadata 


def run_spectral (X :np .ndarray ,k :int ,seed :int =42 )->Tuple [np .ndarray ,float ,ModelMetadata ]:
    """
    Execute Spectral Clustering with RBF affinity graph.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    runtime_seconds : float
    metadata : ModelMetadata
    """
    t0 =time .perf_counter ()
    labels =run_clusterer ("spectral",X ,k ,seed =seed )
    runtime =time .perf_counter ()-t0 
    metadata =ModelMetadata (
    X .shape [0 ],
    method ="spectral",
    n_samples =X .shape [0 ],
    n_features =X .shape [1 ],
    n_clusters =k ,
    )
    return labels ,runtime ,metadata 


def run_fcm (X :np .ndarray ,k :int ,seed :int =42 )->Tuple [np .ndarray ,float ,ModelMetadata ]:
    """
    Execute Fuzzy C-Means (FCM) clustering.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    runtime_seconds : float
    metadata : ModelMetadata
    """
    t0 =time .perf_counter ()
    labels =run_clusterer ("fcm",X ,k ,seed =seed )
    runtime =time .perf_counter ()-t0 
    metadata =ModelMetadata (
    X .shape [0 ],
    method ="fcm",
    n_samples =X .shape [0 ],
    n_features =X .shape [1 ],
    n_clusters =k ,
    )
    return labels ,runtime ,metadata 



run_single_kmeans =run_kmeans 
run_single_ward =run_ward 
run_single_spectral =run_spectral 
run_single_fcm =run_fcm 
