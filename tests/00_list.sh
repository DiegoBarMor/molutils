#!/bin/bash
set -euo pipefail

echo ">>> TEST MOLUTILS 00: LIST"

dir_in="tests/data/input"

python3 molutils list chains "$dir_in/prot_rna.pdb"
python3 molutils list residues "$dir_in/prot_rna.pdb"
