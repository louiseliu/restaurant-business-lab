#!/usr/bin/env python3
"""Reproduce the sample locally. No uploads, model APIs or network access."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for script in ['generate_sample.py','analyze.py','test_analysis.py']:
 subprocess.run([sys.executable,str(ROOT/'src'/script)],cwd=ROOT,check=True)
