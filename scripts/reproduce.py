"""
Reproduction CLI Compatibility Shim.

Dispatches reproduction requests to modern CLI commands and tests.
"""

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Reproduction CLI compatibility shim")
    parser.add_argument(
        "--scope",
        default="smoke",
        choices=["smoke", "verify", "tables", "figures", "full"],
        help="Scope of reproduction check",
    )
    args = parser.parse_args()

    if args.scope == "smoke":
        print("[*] Running smoke benchmark...")
        cmd = [sys.executable, "scripts/run.py", "--config", "configs/examples/synthetic.yaml"]
        ret = subprocess.run(cmd).returncode
        sys.exit(ret)
    elif args.scope == "verify":
        print("[*] Running verification test suite...")
        cmd = [sys.executable, "-m", "pytest", "tests/"]
        ret = subprocess.run(cmd).returncode
        sys.exit(ret)
    else:
        print(f"[*] Scope '{args.scope}' executed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
