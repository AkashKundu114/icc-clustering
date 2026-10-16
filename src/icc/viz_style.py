"""
Centralized Academic & Scientific Visualization Style for ICC Publications.
Adheres strictly to IEEE Transactions (TKDE, TPAMI), Nature, and NeurIPS standards.

Provides:
- set_academic_style(): Configures matplotlib rcParams (serif typography, CM mathtext, clean grid).
- MODEL_PALETTE: Consistent, colorblind-friendly colors across all baselines and ICC.
- MODEL_MARKERS: Distinct marker shapes for every algorithm.
- clean_spines(): Eliminates visual clutter (despines top and right borders).
- add_subfig_label(): Standardized subfigure enumeration (a), (b), (c)...
"""

import matplotlib.pyplot as plt

MODEL_PALETTE = {
    "ICC_v2": "#d62728",
    "ICC-v2": "#d62728",
    "ICC_v2 (Ours)": "#d62728",
    "ICC_v2_exact": "#1f77b4",
    "ICC_v1": "#e377c2",
    "ICC-v1": "#e377c2",
    "FCAG": "#17becf",
    "FastMVC": "#bcbd22",
    "DEC": "#9467bd",
    "IDEC": "#8c564b",
    "Standard_Consensus": "#ff7f0e",
    "Standard Consensus": "#ff7f0e",
    "Li_et_al_2019": "#8c564b",
    "Li et al. (2019)": "#8c564b",
    "Li et al.": "#8c564b",
    "K-Means": "#1f77b4",
    "kmeans": "#1f77b4",
    "Spectral": "#2ca02c",
    "spectral": "#2ca02c",
    "Ward": "#7f7f7f",
    "ward": "#7f7f7f",
    "FCM": "#393b79",
    "fcm": "#393b79",
    "GMM": "#ffbb78",
    "gmm": "#ffbb78",
    "ALL_POOLED": "#222222",
}


MODEL_MARKERS = {
    "ICC_v2": "*",
    "ICC-v2": "*",
    "ICC_v2 (Ours)": "*",
    "ICC_v1": "o",
    "ICC-v1": "o",
    "FCAG": "s",
    "FastMVC": "D",
    "DEC": "^",
    "Standard_Consensus": "v",
    "Standard Consensus": "v",
    "Li_et_al_2019": "P",
    "Li et al. (2019)": "P",
    "K-Means": "o",
    "kmeans": "o",
    "Spectral": "X",
    "spectral": "X",
    "Ward": "<",
    "ward": "<",
    "FCM": ">",
    "fcm": ">",
    "GMM": "d",
    "gmm": "d",
    "ALL_POOLED": "h",
}

MODEL_LINESTYLES = {
    "ICC_v2": "-",
    "ICC-v2": "-",
    "ICC_v2 (Ours)": "-",
    "ICC_v1": "--",
    "ICC-v1": "--",
    "FCAG": "-.",
    "FastMVC": ":",
    "DEC": "-",
    "Standard_Consensus": "--",
    "Standard Consensus": "--",
    "Li_et_al_2019": ":",
    "Li et al. (2019)": ":",
    "K-Means": "-",
    "kmeans": "-",
    "Spectral": "-.",
    "spectral": "-.",
    "Ward": ":",
    "ward": ":",
    "FCM": "--",
    "fcm": "--",
}


def set_academic_style():
    """
    Applies publication-grade typography, line widths, and axes formatting
    meeting IEEE Transactions on Knowledge and Data Engineering (TKDE) requirements.
    """
    plt.style.use("default")
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "Times", "Computer Modern Roman"],
            "mathtext.fontset": "cm",
            "font.size": 11.5,
            "axes.labelsize": 13.0,
            "axes.titlesize": 13.5,
            "xtick.labelsize": 11.5,
            "ytick.labelsize": 11.5,
            "legend.fontsize": 11.0,
            "figure.titlesize": 15.0,
            "lines.linewidth": 2.4,
            "lines.markersize": 7.0,
            "lines.markeredgewidth": 1.0,
            "axes.facecolor": "#ffffff",
            "figure.facecolor": "#ffffff",
            "axes.edgecolor": "#333333",
            "axes.linewidth": 0.9,
            "axes.axisbelow": True,
            "axes.grid": True,
            "grid.color": "#e0e0e0",
            "grid.linestyle": "--",
            "grid.linewidth": 0.65,
            "grid.alpha": 0.7,
            "legend.frameon": True,
            "legend.framealpha": 0.92,
            "legend.facecolor": "#ffffff",
            "legend.edgecolor": "#d0d0d0",
            "legend.fancybox": True,
            "legend.borderaxespad": 0.6,
            "legend.borderpad": 0.5,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
        }
    )


def clean_spines(ax, keep=("left", "bottom")):
    """
    Removes visual clutter by despining specified borders (typically top and right).
    """
    for spine in ["top", "right", "left", "bottom"]:
        if spine not in keep:
            ax.spines[spine].set_visible(False)
        else:
            ax.spines[spine].set_visible(True)
            ax.spines[spine].set_color("#333333")
            ax.spines[spine].set_linewidth(0.9)


def add_subfig_label(ax, label: str, loc: str = "top_left", pad: float = 0.02):
    """
    Adds clean, standardized academic subfigure labels like (a), (b), (c).
    """
    if loc == "top_left":
        ax.text(
            pad,
            1.0 - pad,
            label,
            transform=ax.transAxes,
            fontsize=11.5,
            fontweight="bold",
            va="top",
            ha="left",
            bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none", alpha=0.85),
        )
