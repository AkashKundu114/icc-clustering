"""
Unified dataset registry — YAML-driven loader for all ICC benchmark datasets.

Discovers dataset configurations from configs/datasets.yaml and provides
standardized loading, metadata querying, and unified preprocessing:
    NaN imputation -> log-transform (optional) -> StandardScaler -> LabelEncoder.
"""

import os 
from dataclasses import dataclass ,field 
from pathlib import Path 
from typing import Any ,Dict ,List ,Optional ,Tuple 

import numpy as np 
import yaml 
from sklearn .preprocessing import LabelEncoder ,StandardScaler 


_PROJECT_ROOT =Path (__file__ ).resolve ().parents [3 ]
_DEFAULT_CACHE =_PROJECT_ROOT /"data"/"cache"
_DEFAULT_CACHE .mkdir (parents =True ,exist_ok =True )
_CONFIG_PATH =_PROJECT_ROOT /"configs"/"datasets.yaml"


@dataclass 
class DatasetInfo :
    """Metadata container for a benchmark dataset."""
    name :str 
    domain :str 
    expected_N :int 
    expected_D :int 
    expected_K :int 
    d_over_n :float 
    description :str 
    enabled :bool =True 
    source :str ="openml"
    priority :str ="medium"
    openml_id :Optional [int ]=None 
    openml_name :Optional [str ]=None 
    openml_version :int =1 
    as_frame :bool =False 
    subsample_n :Optional [int ]=None 
    preprocessing :Dict [str ,Any ]=field (default_factory =dict )

    def __str__ (self )->str :
        return self .name 

    def __repr__ (self )->str :
        status ="enabled"if self .enabled else "disabled"
        return (
        f"DatasetInfo(name='{self .name }', domain='{self .domain }', "
        f"N={self .expected_N }, D={self .expected_D }, K={self .expected_K }, "
        f"D/N={self .d_over_n }, status={status })"
        )


def _load_registry_yaml ()->Dict [str ,Any ]:
    """Load configs/datasets.yaml from disk."""
    if not _CONFIG_PATH .exists ():
        return {}
    with open (_CONFIG_PATH ,"r",encoding ="utf-8")as f :
        data =yaml .safe_load (f )
    return data or {}


def get_dataset_info (name :str )->DatasetInfo :
    """
    Retrieve metadata for a dataset from configs/datasets.yaml without loading data arrays.

    Parameters
    ----------
    name : str
        Dataset identifier (e.g., 'leukemia', 'sonar', 'newsgroups20').

    Returns
    -------
    DatasetInfo dataclass with dataset parameters.

    Raises
    -------
    KeyError if the dataset is not registered in configs/datasets.yaml.
    """
    data =_load_registry_yaml ()
    datasets =data .get ("datasets",{})
    if name not in datasets :
        raise KeyError (f"Dataset '{name }' not found in registry. Available: {list (datasets .keys ())}")

    entry =datasets [name ]
    d_over_n =float (entry .get ("d_over_n_ratio",entry .get ("d_over_n",0.0 )))
    return DatasetInfo (
    name =entry .get ("name",name ),
    domain =entry .get ("domain","unknown"),
    expected_N =int (entry .get ("expected_N",0 )),
    expected_D =int (entry .get ("expected_D",0 )),
    expected_K =int (entry .get ("expected_K",0 )),
    d_over_n =d_over_n ,
    description =entry .get ("description",""),
    enabled =bool (entry .get ("enabled",True )),
    source =entry .get ("source","openml"),
    priority =entry .get ("priority","medium"),
    openml_id =entry .get ("openml_id"),
    openml_name =entry .get ("openml_name",name ),
    openml_version =int (entry .get ("openml_version",1 )),
    as_frame =bool (entry .get ("as_frame",False )),
    subsample_n =entry .get ("subsample_n"),
    preprocessing =entry .get ("preprocessing",{}),
    )


def list_datasets (enabled_only :bool =True )->List [DatasetInfo ]:
    """
    List registered benchmark datasets.

    Parameters
    ----------
    enabled_only : bool, default=True
        If True, returns only datasets currently marked enabled: true in configs/datasets.yaml.

    Returns
    -------
    List of DatasetInfo objects.
    """
    data =_load_registry_yaml ()
    datasets =data .get ("datasets",{})
    results :List [DatasetInfo ]=[]
    for name in datasets :
        info =get_dataset_info (name )
        if not enabled_only or info .enabled :
            results .append (info )
    return results 


def preprocess_dataset (
raw_X :np .ndarray ,
raw_y :np .ndarray ,
impute_nan :bool =True ,
log_transform :bool =False ,
standardize :bool =True ,
)->Tuple [np .ndarray ,np .ndarray ]:
    """
    Unified dataset preprocessing pipeline:
        1. NaN imputation: replaces missing values with column means
        2. Log-transform (optional): applies log1p to non-negative expressions
        3. Feature standardization: StandardScaler (zero mean, unit variance)
        4. Target encoding: LabelEncoder to contiguous 0-indexed integer classes
    """
    X =np .asarray (raw_X ,dtype =np .float64 ).copy ()
    if impute_nan and np .isnan (X ).any ():
        col_means =np .nanmean (X ,axis =0 )
        col_means =np .nan_to_num (col_means ,nan =0.0 )
        inds =np .where (np .isnan (X ))
        X [inds ]=np .take (col_means ,inds [1 ])

    if log_transform :
        X =np .log1p (np .maximum (X ,0.0 ))

    if standardize :
        X =StandardScaler ().fit_transform (X )

    y =LabelEncoder ().fit_transform (raw_y )
    return X ,y 


def load_dataset (
name :str ,
cache_dir :str ="data/cache",
force_download :bool =False ,
)->Tuple [np .ndarray ,np .ndarray ,Dict [str ,Any ]]:
    """
    Unified entry point to load any benchmark dataset in the ICC registry.

    Dispatches to appropriate domain loader with automatic cache resolution:
    - npz cache for small/dense datasets
    - h5ad cache for scRNA-seq datasets

    Parameters
    ----------
    name : str
        Dataset identifier (e.g. 'sonar', 'colon', 'leukemia', 'newsgroups20').
    cache_dir : str, default='data/cache'
        Target directory for cached preprocessed arrays.
    force_download : bool, default=False
        If True, ignores existing cache and refetches raw data.

    Returns
    -------
    X : np.ndarray of shape (N, D)
        Preprocessed feature matrix.
    y : np.ndarray of shape (N,)
        Integer cluster labels.
    metadata : dict
        Dataset descriptor properties.
    """

    info =get_dataset_info (name )


    if not os .path .isabs (cache_dir ):
        c_dir =os .path .abspath (os .path .join (_PROJECT_ROOT ,cache_dir ))
    else :
        c_dir =cache_dir 
    os .makedirs (c_dir ,exist_ok =True )


    if info .domain in ("acoustic","synthetic","genomics"):
        from .genomics import load_genomics_dataset 
        return load_genomics_dataset (name ,cache_dir =c_dir ,force_download =force_download )

    if info .domain =="text":
        from .text import load_20newsgroups ,load_rcv1 
        if name =="newsgroups20":
            n_features =info .expected_D if info .expected_D >0 else 10000 
            return load_20newsgroups (n_features =n_features ,cache_dir =c_dir ,force_download =force_download )
        elif name =="rcv1":
            return load_rcv1 (cache_dir =c_dir ,force_download =force_download )

    if info .domain =="image":
        from .image import load_coil20 ,load_yale_b 
        if name =="yale_b":
            return load_yale_b (cache_dir =c_dir ,force_download =force_download )
        elif name =="coil20":
            return load_coil20 (cache_dir =c_dir ,force_download =force_download )

    if info .domain =="hyperspectral":
        from .spectral import load_indian_pines 
        if name =="indian_pines":
            return load_indian_pines (cache_dir =c_dir ,force_download =force_download )

    if info .domain =="audio":
        from .audio import load_isolet 
        if name =="isolet":
            return load_isolet (cache_dir =c_dir ,force_download =force_download )

    if info .domain =="scrnaseq":
        from .scrnaseq import load_tabula_muris ,load_zheng68k 
        if name =="zheng68k":
            return load_zheng68k (cache_dir =c_dir ,force_download =force_download )
        elif name =="tabula_muris":
            return load_tabula_muris (cache_dir =c_dir ,force_download =force_download )

    raise NotImplementedError (
    f"Dataset '{name }' in domain '{info .domain }' is registered but has no active loader. "
    f"Enable in Phase 4."
    )
