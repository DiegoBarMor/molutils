#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi
if [ ! -d "tests/data" ]; then
    bash tests/_fetch.sh
fi

echo ">>> TEST MOLUTILS 04: SELECT"

dir_in="tests/data/input"
dir_out="tests/data/output/select"

query_0="nucleic and not name H*"
query_1="resname U"

python3 molutils select "$query_0" "$dir_in/prot_rna.pdb" "$dir_out/rna_noH.pdb"
python3 molutils select "$query_1" "$dir_in/traj/7vki.pdb" "$dir_out/traj.pdb" \
    -t "$dir_in/traj/7vki.xtc" "$dir_out/traj.xtc"
