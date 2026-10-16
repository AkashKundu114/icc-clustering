"""
Audio and speech benchmark dataset loaders for the ICC Benchmark Suite.

Datasets:
- Isolet (UCI spoken letter recognition, K=26)
"""

import os 
from pathlib import Path 
from typing import Any ,Dict ,Optional ,Tuple 

import numpy as np 
from sklearn .datasets import fetch_openml 
from sklearn .preprocessing import LabelEncoder ,StandardScaler 

_PROJECT_ROOT =Path (__file__ ).resolve ().parents [3 ]
_DEFAULT_CACHE =_PROJECT_ROOT /"data"/"cache"


def load_isolet (
cache_dir :Optional [str ]="data/cache",
force_download :bool =False ,
)->Tuple [np .ndarray ,np .ndarray ,Dict [str ,Any ]]:
    """
    Load Isolet spoken letter recognition dataset from UCI / OpenML.

    Contains 617 acoustic features from 150 speakers uttering letters A-Z (K=26).

    Parameters
    ----------
    cache_dir : str, optional, default='data/cache'
        Target directory for caching preprocessed arrays.
    force_download : bool, default=False
        Re-download and overwrite existing cache file if True.

    Returns
    -------
    X : np.ndarray of shape (7797, 617)
        Standardized acoustic spectral features (float32).
    y : np.ndarray of shape (7797,)
        Spoken letter class labels (0 to 25).
    metadata : dict
        Dataset descriptor properties.

    References
    ----------
    Fanty & Cole. "Spoken letter recognition." NIPS, 1990.
    """
    if cache_dir is None :
        c_dir =str (_DEFAULT_CACHE )
    elif not os .path .isabs (cache_dir ):
        c_dir =os .path .abspath (os .path .join (_PROJECT_ROOT ,cache_dir ))
    else :
        c_dir =os .path .abspath (cache_dir )
    os .makedirs (c_dir ,exist_ok =True )
    cache_path =os .path .join (c_dir ,"isolet.npz")


    if os .path .exists (cache_path )and not force_download :
        with np .load (cache_path )as data :
            X =data ["X"]
            y =data ["y"]
            metadata ={
            "name":"isolet",
            "N":int (X .shape [0 ]),
            "D":int (X .shape [1 ]),
            "K":int (len (np .unique (y ))),
            "d_over_n":round (float (X .shape [1 ]/X .shape [0 ]),2 ),
            "description":"Isolet spoken letter recognition dataset from UCI/OpenML (N=7797, D=617, K=26)",
            }
            return X ,y ,metadata 


    print ("[*] Fetching Isolet from OpenML (name='isolet', version=1)...")
    raw =fetch_openml ("isolet",version =1 ,parser ="auto")


    raw_X =np .asarray (raw .data ,dtype =np .float64 )
    raw_y =np .asarray (raw .target )


    if np .isnan (raw_X ).any ():
        col_means =np .nanmean (raw_X ,axis =0 )
        col_means =np .nan_to_num (col_means ,nan =0.0 )
        inds =np .where (np .isnan (raw_X ))
        raw_X [inds ]=np .take (col_means ,inds [1 ])


    print ("[*] Preprocessing: StandardScaler and LabelEncoder...")
    X =StandardScaler ().fit_transform (raw_X ).astype (np .float32 )
    y =LabelEncoder ().fit_transform (raw_y ).astype (np .int64 )


    np .savez_compressed (cache_path ,X =X ,y =y )
    print (f"[+] Cached 'isolet' to {cache_path }: shape={X .shape }, K={len (np .unique (y ))}")

    metadata ={
    "name":"isolet",
    "N":int (X .shape [0 ]),
    "D":int (X .shape [1 ]),
    "K":int (len (np .unique (y ))),
    "d_over_n":round (float (X .shape [1 ]/X .shape [0 ]),2 ),
    "description":"Isolet spoken letter recognition dataset from UCI/OpenML (N=7797, D=617, K=26)",
    }
    return X ,y ,metadata 
