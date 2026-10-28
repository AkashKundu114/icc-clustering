from pathlib import Path

path = Path("src/icc/baselines/__init__.py")
text = path.read_text(encoding="utf-8")

if "from .cohirf import" not in text:
    text = text.replace(
        "from .anchor import run_fastmvc, run_fcag\n",
        "from .anchor import run_fastmvc, run_fcag\nfrom .cohirf import CoHiRF, run_cohirf\n"
    )

if '"cohirf": run_cohirf,' not in text:
    text = text.replace(
        '    "fastmvc": run_fastmvc,\n',
        '    "fastmvc": run_fastmvc,\n    "cohirf": run_cohirf,\n    "run_cohirf": run_cohirf,\n'
    )

if '"CoHiRF"' not in text:
    text = text.replace(
        '    "run_fastmvc",\n',
        '    "run_fastmvc",\n    "CoHiRF",\n    "run_cohirf",\n'
    )

path.write_text(text, encoding="utf-8")
print("Updated __init__.py cleanly")
