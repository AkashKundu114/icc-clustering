"""
Text/NLP dataset loaders for the ICC Benchmark Suite.

Datasets:
- 20 Newsgroups (TF-IDF vectorization, K=20)
- RCV1 Reuters Corpus Volume I (TF-IDF vectorization) [STUB]
"""

import os 
from pathlib import Path 
from typing import Any ,Dict ,Optional ,Tuple 

import numpy as np 
from sklearn .datasets import fetch_20newsgroups 
from sklearn .feature_extraction .text import TfidfVectorizer 

_PROJECT_ROOT =Path (__file__ ).resolve ().parents [3 ]
_DEFAULT_CACHE =_PROJECT_ROOT /"data"/"cache"


def load_20newsgroups (
n_features :int =10000 ,
cache_dir :Optional [str ]="data/cache",
force_download :bool =False ,
)->Tuple [np .ndarray ,np .ndarray ,Dict [str ,Any ]]:
    """
    Load 20 Newsgroups benchmark dataset vectorized with TF-IDF.

    Parameters
    ----------
    n_features : int, default=10000
        Maximum vocabulary size for TF-IDF feature extraction.
    cache_dir : str, optional, default='data/cache'
        Target directory for caching preprocessed arrays.
    force_download : bool, default=False
        Recompute and overwrite existing cache file if True.

    Returns
    -------
    X : np.ndarray of shape (N, n_features)
        Dense TF-IDF feature matrix (float32).
    y : np.ndarray of shape (N,)
        Integer class targets (0 to 19).
    metadata : dict
        Dataset descriptor properties (name, N, D, K, d_over_n, description).

    References
    ----------
    Lang, K. "Newsweeder: Learning to filter netnews." ICML, 1995.
    """
    if cache_dir is None :
        c_dir =str (_DEFAULT_CACHE )
    elif not os .path .isabs (cache_dir ):
        c_dir =os .path .abspath (os .path .join (_PROJECT_ROOT ,cache_dir ))
    else :
        c_dir =os .path .abspath (cache_dir )
    os .makedirs (c_dir ,exist_ok =True )
    cache_path =os .path .join (c_dir ,"newsgroups20.npz")


    if os .path .exists (cache_path )and not force_download :
        with np .load (cache_path )as data :
            X =data ["X"]
            y =data ["y"]
            if X .shape [1 ]==n_features :
                metadata ={
                "name":"newsgroups20",
                "N":int (X .shape [0 ]),
                "D":int (X .shape [1 ]),
                "K":int (len (np .unique (y ))),
                "d_over_n":round (float (X .shape [1 ]/X .shape [0 ]),2 ),
                "description":"20 Newsgroups document collection with TF-IDF vectorization (K=20)",
                }
                return X ,y ,metadata 


    print ("[*] Fetching 20 Newsgroups (subset='all', remove headers/footers/quotes)...")
    raw =fetch_20newsgroups (
    subset ="all",
    remove =("headers","footers","quotes"),
    )
    raw_texts =raw .data 
    raw_y =np .asarray (raw .target ,dtype =np .int64 )


    print (f"[*] Vectorizing {len (raw_texts )} documents (max_features={n_features }, sublinear_tf=True, min_df=5)...")
    vectorizer =TfidfVectorizer (
    max_features =n_features ,
    sublinear_tf =True ,
    min_df =5 ,
    )
    X_sparse =vectorizer .fit_transform (raw_texts )


    X =X_sparse .toarray ().astype (np .float32 )
    y =raw_y 


    np .savez_compressed (cache_path ,X =X ,y =y )
    print (f"[+] Cached 'newsgroups20' to {cache_path }: shape={X .shape }, K={len (np .unique (y ))}")

    metadata ={
    "name":"newsgroups20",
    "N":int (X .shape [0 ]),
    "D":int (X .shape [1 ]),
    "K":int (len (np .unique (y ))),
    "d_over_n":round (float (X .shape [1 ]/X .shape [0 ]),2 ),
    "description":"20 Newsgroups document collection with TF-IDF vectorization (K=20)",
    }
    return X ,y ,metadata 


def load_rcv1 (
cache_dir :Optional [str ]=None ,
force_download :bool =False ,
)->Tuple [np .ndarray ,np .ndarray ,Dict [str ,Any ]]:
    """
    Load RCV1 Reuters Corpus Volume I subset with TF-IDF representation.

    Parameters
    ----------
    cache_dir : str, optional
        Target directory for caching preprocessed arrays.
    force_download : bool, default=False
        Recompute and overwrite existing cache file if True.

    Returns
    -------
    X : np.ndarray of shape (N, D)
    y : np.ndarray of shape (N,)
    metadata : dict

    References
    ----------
    Lewis et al. "RCV1: A new benchmark collection for text categorization research." JMLR, 2004.
    """
    raise NotImplementedError ("Dataset loader not yet implemented. Enable in Phase 4.")
