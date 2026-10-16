import sys, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
sys.path.insert(0,'experiments/exp1_generalization/src')
from exp1_pseudolabel_generalization import run_pseudolabel_generalization
out='experiments/audit_controls/data/e5_exp1_pseudolabel_rerun.csv'
run_pseudolabel_generalization(noise_dims=[0,200,1000,3000], n_trials=10, output_csv=out)
