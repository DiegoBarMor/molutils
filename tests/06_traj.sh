#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi
if [ ! -d "tests/data" ]; then
    bash tests/_fetch.sh
fi

echo ">>> TEST MOLUTILS 06: TRAJ"

dir_in="tests/data/input/traj"
dir_out="tests/data/output/traj"

### [TODO] change input data to something that is not already aligned
python3 molutils traj align "$dir_in/7vki.pdb" "$dir_in/7vki.xtc" -o "$dir_out/7vki.align.xtc"
python3 molutils traj rmsd  "$dir_in/7vki.pdb" "$dir_in/7vki.xtc" > "$dir_out/rmsd.orig.txt"
python3 molutils traj rmsd  "$dir_in/7vki.pdb" "$dir_out/7vki.align.xtc" > "$dir_out/rmsd.align.txt"
cp "$dir_in/7vki.pdb" "$dir_out/"
