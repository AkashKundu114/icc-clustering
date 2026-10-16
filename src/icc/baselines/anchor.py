"""
Anchor-based scalable clustering baselines for the ICC benchmark suite.

Methods:
- FCAG: Fast Clustering with Anchor Guidance (Nie, Xue, Yu, Li; IEEE TPAMI 2024, doi:10.1109/TPAMI.2023.3318603). NOTE: this is a k-means++-anchor spectral re-implementation, not the paper's PGD/IRW/CD solvers.
- FastMVC: [STUB] random-subspace anchor-graph SURROGATE. It is NOT a faithful implementation of FastMICE (Huang, Wang, Lai; IEEE TKDE 2023, doi:10.1109/TKDE.2023.3236698), the closest published method. Do not report it as that method.

References:
    Nie, Xue, Yu, Li. "Fast Clustering With Anchor Guidance."
    IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2024.
"""

import time 
from typing import Tuple 

import numpy as np 
import scipy .linalg as sla 
from scipy .spatial .distance import cdist 

from .classical import ModelMetadata 

_SKLEARN_AVAILABLE =False 
try :
    from sklearn .cluster import KMeans as _SkKMeans 
    from sklearn .cluster import kmeans_plusplus as _sk_kmeans_plusplus 
    _test =_SkKMeans (n_clusters =2 ,n_init =1 ).fit_predict (np .zeros ((4 ,2 )))
    _SKLEARN_AVAILABLE =True 
except (ImportError ,Exception ):
    _SKLEARN_AVAILABLE =False 


def _kmeans_plusplus_fallback (X :np .ndarray ,n_clusters :int ,random_state :int =42 )->Tuple [np .ndarray ,np .ndarray ]:
    rng =np .random .default_rng (random_state )
    n =X .shape [0 ]
    first_idx =int (rng .integers (0 ,n ))
    indices =[first_idx ]
    centers =[X [first_idx ]]
    for _ in range (1 ,n_clusters ):
        dists =np .min (cdist (X ,np .array (centers ),metric ="sqeuclidean"),axis =1 )
        dists_sum =float (dists .sum ())
        if dists_sum <1e-12 :
            probs =np .ones (n )/n 
        else :
            probs =dists /dists_sum 
        next_idx =int (rng .choice (n ,p =probs ))
        indices .append (next_idx )
        centers .append (X [next_idx ])
    return np .array (centers ),np .array (indices ,dtype =int )


def _kmeans_cluster (X :np .ndarray ,k :int ,random_state :int =42 ,n_init :int =10 )->np .ndarray :
    if _SKLEARN_AVAILABLE :
        try :
            return _SkKMeans (n_clusters =k ,n_init =n_init ,random_state =random_state ).fit_predict (X ).astype (np .int64 )
        except Exception :
            pass 
    from src .icc .core import run_clusterer 
    return run_clusterer ("kmeans",X ,k ,seed =random_state ).astype (np .int64 )


def construct_anchor_bipartite_graph (
X :np .ndarray ,
anchors :np .ndarray ,
s :int =5 ,
)->np .ndarray :
    """
    Construct sample-to-anchor bipartite similarity matrix Z.

    Uses adaptive neighbor weighting from Nie et al. (IEEE TPAMI 2024):
    For each sample x_i and its s nearest anchors, weights are assigned such that:
        z_{ij} = (d_{i, (s+1)} - d_{ij}) / (s * d_{i, (s+1)} - sum_{l=1}^s d_{il})
    subject to z_i >= 0 and sum_j z_{ij} = 1.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    anchors : np.ndarray of shape (m, D)
        Anchor point coordinates.
    s : int, default=5
        Number of nearest anchors to connect per sample.

    Returns
    -------
    Z : np.ndarray of shape (N, m)
        Row-stochastic bipartite affinity matrix with Z 1_m = 1_N.
    """
    N ,D =X .shape 
    m =anchors .shape [0 ]


    dist =cdist (X ,anchors ,metric ="sqeuclidean")

    s_actual =max (1 ,min (s ,m -1 ))if m >1 else 1 
    Z =np .zeros ((N ,m ),dtype =np .float64 )

    if m >s_actual +1 :

        idx =np .argpartition (dist ,s_actual ,axis =1 )[:,:s_actual +1 ]
        sub_dist =np .take_along_axis (dist ,idx ,axis =1 )
        sub_order =np .argsort (sub_dist ,axis =1 )
        sorted_idx =np .take_along_axis (idx ,sub_order ,axis =1 )
        sorted_dist =np .take_along_axis (sub_dist ,sub_order ,axis =1 )

        d_s1 =sorted_dist [:,s_actual :s_actual +1 ]
        d_top =sorted_dist [:,:s_actual ]
        denom =s_actual *d_s1 -np .sum (d_top ,axis =1 ,keepdims =True )

        w =np .where (
        denom >1e-12 ,
        (d_s1 -d_top )/np .maximum (denom ,1e-12 ),
        1.0 /s_actual ,
        )
        np .put_along_axis (Z ,sorted_idx [:,:s_actual ],w ,axis =1 )
    else :

        inv_d =1.0 /(dist +1e-6 )
        Z =inv_d /inv_d .sum (axis =1 ,keepdims =True )


    row_sums =Z .sum (axis =1 ,keepdims =True )
    row_sums [row_sums <1e-12 ]=1.0 
    Z /=row_sums 
    return Z 


def run_fcag (
X :np .ndarray ,
k :int ,
n_anchors :int =100 ,
seed :int =42 ,
**kwargs ,
)->Tuple [np .ndarray ,float ,ModelMetadata ]:
    """
    Execute Fast Clustering with Anchor Guidance (FCAG, Nie et al., IEEE TPAMI 2024).

    Core steps:
    a) Select m anchor points via k-means++.
    b) Construct anchor-to-sample bipartite graph Z in O(N m).
    c) Solve generalized eigenvalue problem on m x m matrix M = D_c^{-1/2} Z^T Z D_c^{-1/2}.
       Project eigenvectors to samples via F = Z D_c^{-1/2} U_m Lambda^{-1/2} in O(N m k).
    d) Discretize row-normalized eigenvectors for final cluster assignment.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k : int
        Number of clusters (k >= 2).
    n_anchors : int, default=100
        Number of anchor points to select. Clamped to [k, N].
    seed : int, default=42
        Random seed for reproducibility.
    **kwargs : dict
        Optional hyperparameters:
        - s : int, number of nearest anchors per sample (default: 5)
        - n_init : int, number of k-means initializations for discretization (default: 10)

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Cluster assignments (int64, values in 0 to k-1).
    runtime_seconds : float
        Elapsed execution time.
    metadata : ModelMetadata
        Diagnostic container (subclasses int with n_core = m).

    References
    ----------
    Nie, Wang, Huang, Li. "Fast Clustering With Anchor Guidance."
    IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2024.
    """
    t0 =time .perf_counter ()
    X_arr =np .asarray (X ,dtype =np .float64 )
    if X_arr .ndim !=2 :
        raise ValueError (f"Input X must be a 2D matrix, got shape {X_arr .shape }")
    N ,D =X_arr .shape 

    if N <k :
        raise ValueError (f"Number of samples N={N } cannot be smaller than number of clusters k={k }")
    if k <2 :
        raise ValueError (f"Number of clusters k must be >= 2, got {k }")


    m =min (n_anchors ,N )
    if m <k :
        m =k 

    s =kwargs .get ("s",5 )
    n_init =kwargs .get ("n_init",10 )


    if m >=N :
        anchors =np .copy (X_arr )
    else :
        if _SKLEARN_AVAILABLE :
            try :
                anchors ,_ =_sk_kmeans_plusplus (X_arr ,n_clusters =m ,random_state =seed )
            except Exception :
                anchors ,_ =_kmeans_plusplus_fallback (X_arr ,n_clusters =m ,random_state =seed )
        else :
            anchors ,_ =_kmeans_plusplus_fallback (X_arr ,n_clusters =m ,random_state =seed )


    Z =construct_anchor_bipartite_graph (X_arr ,anchors ,s =s )



    d_c =np .sum (Z ,axis =0 )
    d_c_inv_sqrt =1.0 /np .sqrt (np .fmax (d_c ,1e-12 ))


    ZT_Z =Z .T @Z 
    M =(d_c_inv_sqrt [:,None ]*ZT_Z )*d_c_inv_sqrt [None ,:]
    M =0.5 *(M +M .T )

    evals ,evecs =sla .eigh (M )


    top_indices =np .argsort (evals )[::-1 ][:k ]
    evals_top =np .fmax (evals [top_indices ],1e-12 )
    U_m =evecs [:,top_indices ]


    F =(Z *d_c_inv_sqrt [None ,:])@(U_m /np .sqrt (evals_top )[None ,:])


    F_norm =F /(np .linalg .norm (F ,axis =1 ,keepdims =True )+1e-12 )
    labels =_kmeans_cluster (F_norm ,k =k ,random_state =seed ,n_init =n_init )

    runtime_seconds =time .perf_counter ()-t0 
    metadata =ModelMetadata (
    m ,
    method ="FCAG",
    n_samples =N ,
    n_features =D ,
    n_clusters =k ,
    n_anchors =m ,
    n_core =m ,
    )
    return labels ,runtime_seconds ,metadata 


def run_fastmvc (
X :np .ndarray ,
k :int ,
n_anchors :int =100 ,
seed :int =42 ,
**kwargs ,
)->Tuple [np .ndarray ,float ,ModelMetadata ]:
    """
    Execute Fast Multi-view Clustering (FastMVC, Huang et al., IEEE TKDE 2023).

    Pipeline:
    1. Select m anchor points via k-means++ across the global sample space.
    2. Treat diverse subspace partitions as 'views' (leveraging random subspace generation).
    3. Construct view-specific sample-to-anchor bipartite graphs Z^(v).
    4. Fuse bipartite graphs across views into unified bipartite matrix Z_fused.
    5. Solve generalized eigenvalue problem on m x m matrix
       M = D_c^{-1/2} Z_fused^T Z_fused D_c^{-1/2}.
       Project eigenvectors to samples via F = Z_fused D_c^{-1/2} U_m Lambda^{-1/2} in O(N).
    6. Discretize row-normalized eigenvectors for final cluster assignment.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k : int
        Number of clusters (k >= 2).
    n_anchors : int, default=100
        Number of anchor points to select. Clamped to [k, N].
    seed : int, default=42
        Random seed for reproducibility.
    **kwargs : dict
        Optional hyperparameters:
        - n_views : int, number of diverse subspace views (default: 15)
        - subspace_rate : float, fraction of features per subspace view (default: 0.5)
        - s : int, number of nearest anchors per sample (default: 5)
        - n_init : int, number of k-means initializations for discretization (default: 10)

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Cluster assignments (int64, values in 0 to k-1).
    runtime_seconds : float
        Elapsed execution time.
    metadata : ModelMetadata
        Diagnostic container (subclasses int with n_core = m).

    References
    ----------
    Huang, Wang, Lai. "Fast Multi-view Clustering via Ensembles: Towards
    Scalability, Superiority, and Simplicity." IEEE TKDE, 2023.
    """
    t0 =time .perf_counter ()
    X_arr =np .asarray (X ,dtype =np .float64 )
    if X_arr .ndim !=2 :
        raise ValueError (f"Input X must be a 2D matrix, got shape {X_arr .shape }")
    N ,D =X_arr .shape 

    if N <k :
        raise ValueError (f"Number of samples N={N } cannot be smaller than number of clusters k={k }")
    if k <2 :
        raise ValueError (f"Number of clusters k must be >= 2, got {k }")


    m =min (n_anchors ,N )
    if m <k :
        m =k 

    n_views =kwargs .get ("n_views",15 )
    subspace_rate =kwargs .get ("subspace_rate",0.5 )
    s =kwargs .get ("s",5 )
    n_init =kwargs .get ("n_init",10 )

    rng =np .random .default_rng (seed )


    if m >=N :
        anchor_indices =np .arange (N )
    else :
        if _SKLEARN_AVAILABLE :
            try :
                _ ,anchor_indices =_sk_kmeans_plusplus (X_arr ,n_clusters =m ,random_state =seed )
            except Exception :
                _ ,anchor_indices =_kmeans_plusplus_fallback (X_arr ,n_clusters =m ,random_state =seed )
        else :
            _ ,anchor_indices =_kmeans_plusplus_fallback (X_arr ,n_clusters =m ,random_state =seed )


    sub_d =max (2 ,int (D *subspace_rate ))
    sub_d =min (sub_d ,D )

    Z_fused =np .zeros ((N ,m ),dtype =np .float64 )

    for _ in range (n_views ):

        if sub_d <D :
            feat_idx =rng .choice (D ,size =sub_d ,replace =False )
            X_v =X_arr [:,feat_idx ]
        else :
            X_v =X_arr 

        anchors_v =X_v [anchor_indices ]
        Z_v =construct_anchor_bipartite_graph (X_v ,anchors_v ,s =s )
        Z_fused +=Z_v 


    Z_fused /=max (1 ,n_views )


    d_c =np .sum (Z_fused ,axis =0 )
    d_c_inv_sqrt =1.0 /np .sqrt (np .fmax (d_c ,1e-12 ))

    ZT_Z =Z_fused .T @Z_fused 
    M =(d_c_inv_sqrt [:,None ]*ZT_Z )*d_c_inv_sqrt [None ,:]
    M =0.5 *(M +M .T )

    evals ,evecs =sla .eigh (M )


    top_indices =np .argsort (evals )[::-1 ][:k ]
    evals_top =np .fmax (evals [top_indices ],1e-12 )
    U_m =evecs [:,top_indices ]


    F =(Z_fused *d_c_inv_sqrt [None ,:])@(U_m /np .sqrt (evals_top )[None ,:])


    F_norm =F /(np .linalg .norm (F ,axis =1 ,keepdims =True )+1e-12 )
    labels =_kmeans_cluster (F_norm ,k =k ,random_state =seed ,n_init =n_init )

    runtime_seconds =time .perf_counter ()-t0 
    metadata =ModelMetadata (
    m ,
    method ="FastMVC",
    n_samples =N ,
    n_features =D ,
    n_clusters =k ,
    n_anchors =m ,
    n_views =n_views ,
    n_core =m ,
    )
    return labels ,runtime_seconds ,metadata 

