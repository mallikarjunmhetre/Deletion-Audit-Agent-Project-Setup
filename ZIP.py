"""
make_zip.py — Create code.zip for HackerRank submission
Excludes: dataset/, .cache/, output/, __pycache__, .pytest_cache, .env, *.pyc
"""
import zipfile, os
from pathlib import Path

ROOT = Path(r"C:\Users\Mallikarjun\OneDrive\Desktop\ARJUN\ghost-audit")
OUT  = ROOT / "code.zip"

EXCLUDE_DIRS  = {"dataset", ".cache", "output", "__pycache__", ".pytest_cache",
                 ".git", "venv", ".venv", "env"}
EXCLUDE_FILES = {".env", "code.zip", "generate_dataset.py"}
EXCLUDE_EXT   = {".pyc", ".pyo"}

included = []
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(ROOT.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(ROOT)
        parts = rel.parts
        # Skip excluded dirs (any part of path)
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        # Skip excluded filenames
        if path.name in EXCLUDE_FILES:
            continue
        # Skip excluded extensions
        if path.suffix.lower() in EXCLUDE_EXT:
            continue
        zf.write(path, rel)
        included.append(str(rel))

print(f"Created: {OUT}")
print(f"Size   : {OUT.stat().st_size / 1024:.1f} KB")
print(f"Files  : {len(included)}")
print()
for f in included:
    print(f"  {f}")
