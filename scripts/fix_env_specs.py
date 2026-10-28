import os

with open("paper/main.tex", "r", encoding="utf-8") as f:
    text = f.read()

old_env = r"""    \item \textbf{Host Processor (CPU):} AMD Ryzen processor (AMD64 Family 25 Model 97 Stepping 2) featuring 16 physical cores and 32 logical threads operating at base clock 3.20~GHz.
    \item \textbf{Host Memory (RAM):} 15.21~GB usable system RAM (16.0~GB physical DDR5 installed).
    \item \textbf{GPU Acceleration:} NVIDIA GeForce RTX 5060 Laptop GPU (8.0~GB GDDR6 VRAM, CUDA capability 13.4 runtime).
    \item \textbf{Software Stack and Core Libraries:} Python 3.14.6 (64-bit AMD64 architecture), NumPy 2.4.6, SciPy 1.18.0, Scikit-learn 1.9.1, PyTorch 2.16.0.dev20261017+cu134, Numba 0.66.0, and Pandas 3.0.0."""

new_env = r"""    \item \textbf{Host Processor (CPU):} AMD Ryzen 9 8940HX with Radeon Graphics (16 physical cores, 32 logical threads, base clock 3.20~GHz).
    \item \textbf{Host Memory (RAM):} 15.21~GB usable system RAM (16.0~GB physical DDR5 installed).
    \item \textbf{GPU Acceleration:} NVIDIA GeForce RTX 5060 Laptop GPU (8.0~GB GDDR6 VRAM, compute capability 12.0, CUDA runtime version 13.4, Driver 617.14).
    \item \textbf{Software Stack and Core Libraries:} Python 3.14.6 (64-bit AMD64 architecture), NumPy 2.4.6, SciPy 1.18.0, Scikit-learn 1.9.1, PyTorch 2.16.0.dev20261017+cu134, Numba 0.66.0, and Pandas 3.0.5."""

assert old_env in text, "old_env not found"
text = text.replace(old_env, new_env, 1)

with open("paper/main.tex", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated Sec 5.1 environment specs successfully.")
