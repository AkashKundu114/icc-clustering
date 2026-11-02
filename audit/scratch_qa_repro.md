Created At: 2026-11-01T21:31:21+05:30
Completed At: 2026-11-01T21:31:21+05:30
File Path: `file:///D:/icc-clustering/src/icc/utils/helpers.py`
Total Lines: 78
Total Bytes: 1807
Showing lines 1 to 78
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: """
2: Shared utilities for ICC: seed control, timing, memory measurement, and logging.
3: """
4: 
5: import contextlib
6: import logging
7: import os
8: import random
9: import time
10: from typing import Dict, Generator
11: 
12: import numpy as np
13: 
14: 
15: def set_seed(seed: int = 42) -> None:
16:     """
17:     Set random seeds across Python, NumPy, and optional libraries for reproducibility.
18: 
19:     Parameters
20:     ----------
21:     seed : int
22:         Integer random seed.
23:     """
24:     random.seed(seed)
25:     np.random.seed(seed)
26:     os.environ["PYTHONHASHSEED"] = str(seed)
27: 
28:     # Optional torch seeding
29:     try:
30:         import torch
31: 
32:         torch.manual_seed(seed)
33:         if torch.cuda.is_available():
34:             torch.cuda.manual_seed_all(seed)
35:     except ImportError:
36:         pass
37: 
38: 
39: @contextlib.contextmanager
40: def Timer() -> Generator[Dict[str, float], None, None]:
41:     """
42:     Context manager for measuring elapsed execution time in seconds.
43: 
44:     Yields
45:     ------
46:     Dict[str, float]
47:         Dictionary with key 'elapsed' updated when context exits.
48:     """
49:     state: Dict[str, float] = {"elapsed": 0.0}
50:     start = time.perf_counter()
51:     try:
52:         yield state
53:     finally:
54:         state["elapsed"] = time.perf_counter() - start
55: 
56: 
57: def configure_logging(level: int = logging.INFO) -> logging.Logger:
58:     """
59:     Configure and return a standard logger for ICC.
60: 
61:     Parameters
62:     ----------
63:     level : int
64:         Logging level (e.g. logging.INFO).
65: 
66:     Returns
67:     -------
68:     logging.Logger
69:     """
70:     logger = logging.getLogger("icc")
71:     if not logger.handlers:
72:         handler = logging.StreamHandler()
73:         formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S")
74:         handler.setFormatter(formatter)
75:         logger.addHandler(handler)
76:     logger.setLevel(level)
77:     return logger
78: 
The above content shows the entire, complete file contents of the requested file.
