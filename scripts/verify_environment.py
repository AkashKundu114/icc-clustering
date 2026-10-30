import os
import platform
import sys

import psutil
import requests


def check_env():
    lines = []
    lines.append("# Computational Environment Verification (ENV.md)")
    lines.append("")
    lines.append("**Verification Date:** 2026-10-28")
    lines.append(f"**Host OS:** {platform.system()} {platform.release()} (Build {platform.version()})")
    lines.append(f"**Architecture:** {platform.machine()}")
    lines.append(f"**Processor:** {platform.processor()}")
    lines.append(f"**Logical CPU Cores:** {os.cpu_count()}")
    
    # RAM
    mem = psutil.virtual_memory()
    total_gb = mem.total / (1024**3)
    avail_gb = mem.available / (1024**3)
    lines.append(f"**Total RAM:** {total_gb:.2f} GB (Usable: {avail_gb:.2f} GB)")
    
    # Python
    lines.append(f"**Python Version:** {sys.version.split()[0]} ({sys.executable})")
    
    # PyTorch and GPU
    try:
        import torch
        lines.append(f"**PyTorch Version:** {torch.__version__}")
        cuda_avail = torch.cuda.is_available()
        lines.append(f"**CUDA Available:** {cuda_avail}")
        if cuda_avail:
            lines.append(f"**GPU Device:** {torch.cuda.get_device_name(0)}")
            lines.append(f"**GPU Count:** {torch.cuda.device_count()}")
            total_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            lines.append(f"**GPU VRAM:** {total_vram:.2f} GB")
        else:
            lines.append("**GPU Device:** CUDA not available in current torch build")
    except ImportError:
        lines.append("**PyTorch:** Not installed")

    # Network
    try:
        r = requests.get("https://api.crossref.org/works/10.1109/TPAMI.2023.3318603", timeout=10)
        if r.status_code == 200:
            lines.append(f"**Internet Connectivity (CrossRef API):** PASS (HTTP {r.status_code})")
        else:
            lines.append(f"**Internet Connectivity (CrossRef API):** FAIL (HTTP {r.status_code})")
    except Exception as e:
        lines.append(f"**Internet Connectivity (CrossRef API):** FAIL ({e})")

    # Git
    try:
        import subprocess
        git_res = subprocess.run(["C:\\Program Files\\Git\\cmd\\git.exe", "--version"], capture_output=True, text=True)
        lines.append(f"**Git Version:** {git_res.stdout.strip()}")
    except Exception as e:
        lines.append(f"**Git Version:** Error ({e})")

    # Tectonic LaTeX
    tectonic_path = os.path.abspath("tools/bin/tectonic.exe")
    if os.path.exists(tectonic_path):
        lines.append(f"**Tectonic Engine:** Present ({tectonic_path})")
    else:
        lines.append("**Tectonic Engine:** Missing")

    # Memory Limits and Policies
    lines.append("")
    lines.append("## Resource Limits & Safety Caps")
    lines.append("- **Max RAM per process:** 13.0 GB (hard abort threshold)")
    lines.append("- **Max time per single fit:** 30 minutes")
    lines.append("- **Max time per experiment battery:** 6.0 hours")
    lines.append("- **Disk space threshold:** 5.0 GB minimum")
    lines.append("")
    
    output = "\n".join(lines)
    print(output)
    
    os.makedirs("docs", exist_ok=True)
    with open("docs/ENV.md", "w", encoding="utf-8") as f:
        f.write(output + "\n")
    print("\nSaved to docs/ENV.md")

if __name__ == "__main__":
    check_env()
