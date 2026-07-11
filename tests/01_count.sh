#!/bin/bash
set -euo pipefail

echo ">>> TEST MOLUTILS 01: COUNT"

dir_in="tests/data/input"

python3 molutils count models "$dir_in/1aju.pdb"
python3 molutils count chains "$dir_in/prot_rna.pdb"
python3 molutils count residues "$dir_in/prot_rna.pdb"
# python3 molutils count frames # [TODO]
python3 molutils count altlocs "$dir_in/6e9a.pdb"
