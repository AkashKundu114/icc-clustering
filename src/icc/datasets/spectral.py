"""
Hyperspectral imaging dataset loaders for the ICC Benchmark Suite.

Datasets:
- Indian Pines (K=16, 200 spectral bands)
- Pavia University (K=9, 103 spectral bands) [STUB]
"""

import os 
from pathlib import Path 
from typing import Any ,Dict ,Optional ,Tuple 

import numpy as np 
import scipy .io as sio 
from sklearn .preprocessing import LabelEncoder ,StandardScaler 

_PROJECT_ROOT =Path (__file__ ).resolve ().parents [3 ]
_DEFAULT_CACHE =_PROJECT_ROOT /"data"/"cache"
_DEFAULT_RAW =_PROJECT_ROOT /"data"/"raw"/"indian_pines"


def _download_file (url :str ,dest_path :str ):
    """Download a file with user-agent headers and SSL verification handling."""
    import ssl 
    import urllib .request 
    ctx =ssl ._create_unverified_context ()
    req =urllib .request .Request (
    url ,
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    with urllib .request .urlopen (req ,timeout =45 ,context =ctx )as response ,open (dest_path ,"wb")as out_file :
        while chunk :=response .read (65536 ):
            out_file .write (chunk )


def download_indian_pines (
raw_dir :Optional [str ]=None ,
force :bool =False ,
)->Tuple [str ,str ]:
    """
    Download Indian Pines hyperspectral scene and ground-truth .mat files.

    Parameters
    ----------
    raw_dir : str, optional
        Target directory to store raw .mat files. Defaults to 'data/raw/indian_pines'.
    force : bool, default=False
        Re-download and overwrite existing files if True.

    Returns
    -------
    Tuple[str, str]
        Absolute paths to (Indian_pines_corrected.mat, Indian_pines_gt.mat).
    """
    if raw_dir is None :
        target_dir =str (_DEFAULT_RAW )
    elif not os .path .isabs (raw_dir ):
        target_dir =os .path .abspath (os .path .join (_PROJECT_ROOT ,raw_dir ))
    else :
        target_dir =os .path .abspath (raw_dir )
    os .makedirs (target_dir ,exist_ok =True )

    img_path =os .path .join (target_dir ,"Indian_pines_corrected.mat")
    gt_path =os .path .join (target_dir ,"Indian_pines_gt.mat")

    if os .path .exists (img_path )and os .path .exists (gt_path )and not force :
        return img_path ,gt_path 


    mirrors =[
    (
    "https://huggingface.co/datasets/danaroth/indian_pines/resolve/main/Indian_pines_corrected.mat",
    "https://huggingface.co/datasets/danaroth/indian_pines/resolve/main/Indian_pines_gt.mat",
    ),
    (
    "https://www.ehu.eus/ccwintco/uploads/6/67/Indian_pines_corrected.mat",
    "https://www.ehu.eus/ccwintco/uploads/c/c4/Indian_pines_gt.mat",
    ),
    ]

    for img_url ,gt_url in mirrors :
        try :
            print (f"[*] Downloading Indian Pines from {img_url }...")
            _download_file (img_url ,img_path )
            print (f"[*] Downloading Indian Pines ground truth from {gt_url }...")
            _download_file (gt_url ,gt_path )
            return img_path ,gt_path 
        except Exception as e :
            print (f"[!] Mirror failed ({img_url }): {e }. Attempting fallback...")

    raise RuntimeError (
    "Failed to download Indian Pines dataset from all available mirrors. "
    "Please manually place 'Indian_pines_corrected.mat' and 'Indian_pines_gt.mat' in data/raw/indian_pines/."
    )


def load_indian_pines (
cache_dir :Optional [str ]="data/cache",
raw_dir :Optional [str ]=None ,
force_download :bool =False ,
)->Tuple [np .ndarray ,np .ndarray ,Dict [str ,Any ]]:
    """
    Load Indian Pines hyperspectral dataset (AVIRIS sensor flight line).

    Contains 145x145 pixels with 200 spectral bands and 16 ground-truth classes.
    Background pixels (ground-truth label = 0) are excluded.

    Parameters
    ----------
    cache_dir : str, optional, default='data/cache'
        Target directory for caching preprocessed arrays.
    raw_dir : str, optional
        Directory where raw .mat files are stored or downloaded.
    force_download : bool, default=False
        Re-download and overwrite existing cache file if True.

    Returns
    -------
    X : np.ndarray of shape (10249, 200)
        Standardized reflectance spectra of labeled pixels (float32).
    y : np.ndarray of shape (10249,)
        Land-cover category labels (0 to 15, int64).
    metadata : dict
        Dataset descriptor properties.

    References
    ----------
    Baumgardner et al. "220 Band AVIRIS Hyperspectral Image Data Set:
    June 12, 1992 Indian Pine Test Site 3." IEEE TGRS, 2015.
    """
    if cache_dir is None :
        c_dir =str (_DEFAULT_CACHE )
    elif not os .path .isabs (cache_dir ):
        c_dir =os .path .abspath (os .path .join (_PROJECT_ROOT ,cache_dir ))
    else :
        c_dir =os .path .abspath (cache_dir )
    os .makedirs (c_dir ,exist_ok =True )
    cache_path =os .path .join (c_dir ,"indian_pines.npz")


    if os .path .exists (cache_path )and not force_download :
        with np .load (cache_path )as data :
            X =data ["X"]
            y =data ["y"]
            metadata ={
            "name":"indian_pines",
            "N":int (X .shape [0 ]),
            "D":int (X .shape [1 ]),
            "K":int (len (np .unique (y ))),
            "d_over_n":round (float (X .shape [1 ]/X .shape [0 ]),2 ),
            "description":"Indian Pines hyperspectral AVIRIS flight line (N=10249, D=200, K=16, background excluded)",
            }
            return X ,y ,metadata 


    img_path ,gt_path =download_indian_pines (raw_dir =raw_dir ,force =force_download )

    img_mat =sio .loadmat (img_path )
    gt_mat =sio .loadmat (gt_path )


    data_keys =[k for k in img_mat .keys ()if not k .startswith ("__")]
    gt_keys =[k for k in gt_mat .keys ()if not k .startswith ("__")]

    X_cube =img_mat ["indian_pines_corrected"]if "indian_pines_corrected"in img_mat else img_mat [data_keys [0 ]]
    gt_map =gt_mat ["indian_pines_gt"]if "indian_pines_gt"in gt_mat else gt_mat [gt_keys [0 ]]


    valid_mask =gt_map >0 
    X_raw =X_cube [valid_mask ].astype (np .float64 )
    y_raw =gt_map [valid_mask ]


    print (f"[*] Preprocessing {X_raw .shape [0 ]} pixels across {X_raw .shape [1 ]} spectral bands...")
    X =StandardScaler ().fit_transform (X_raw ).astype (np .float32 )
    y =LabelEncoder ().fit_transform (y_raw ).astype (np .int64 )


    np .savez_compressed (cache_path ,X =X ,y =y )
    print (f"[+] Cached 'indian_pines' to {cache_path }: shape={X .shape }, K={len (np .unique (y ))}")

    metadata ={
    "name":"indian_pines",
    "N":int (X .shape [0 ]),
    "D":int (X .shape [1 ]),
    "K":int (len (np .unique (y ))),
    "d_over_n":round (float (X .shape [1 ]/X .shape [0 ]),2 ),
    "description":"Indian Pines hyperspectral AVIRIS flight line (N=10249, D=200, K=16, background excluded)",
    }
    return X ,y ,metadata 


def load_pavia_university (
cache_dir :Optional [str ]=None ,
force_download :bool =False ,
)->Tuple [np .ndarray ,np .ndarray ,Dict [str ,Any ]]:
    """
    Load Pavia University hyperspectral dataset (ROSIS sensor over Pavia, Italy).

    Returns
    -------
    X : np.ndarray of shape (~42776, 103)
    y : np.ndarray of shape (~42776,)
    metadata : dict
    """
    raise NotImplementedError ("Dataset loader not yet implemented. Enable in Phase 4.")
