#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi
if [ ! -d "tests/data" ]; then
    bash tests/_fetch.sh
fi

echo ">>> TEST MOLUTILS 01: COUNT"

dir_in="tests/data/input"

python3 molutils count models "$dir_in/1aju.pdb" # expected: 20
python3 molutils count chains "$dir_in/prot_rna.pdb" # expected: 2
python3 molutils count residues "$dir_in/prot_rna.pdb" # expected: 184
# python3 molutils count frames # [TODO] # expected:
python3 molutils count altlocs "$dir_in/6e9a.pdb" # expected: 267
