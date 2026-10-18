#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi
if [ ! -d "tests/data" ]; then
    bash tests/_fetch.sh
fi

echo ">>> TEST MOLUTILS 02: EXTRACT"

dir_in="tests/data/input"
dir_traj="$dir_in/traj"
dir_out="tests/data/output"

python3 molutils extract models "$dir_in/1aju.pdb" "$dir_out/models_all"
python3 molutils extract models "$dir_in/1aju.pdb" "$dir_out/models_1" -f

python3 molutils extract chains "$dir_in/prot_rna.pdb" "$dir_out/chains_all"
python3 molutils extract chains "$dir_in/prot_rna.pdb" "$dir_out/chains_1" -f

python3 molutils extract residue "$dir_in/prot_rna.pdb" "H.42" -o "$dir_out/residues"
python3 molutils extract residue "$dir_in/prot_rna.pdb" "R.3" -o "$dir_out/residues"

python3 molutils extract frames "$dir_traj/7vki.pdb" "$dir_traj/7vki.xtc" -o "$dir_out/frames_one" -f 42
python3 molutils extract frames "$dir_traj/7vki.pdb" "$dir_traj/7vki.xtc" -o "$dir_out/frames_some" -f 20 40 60
python3 molutils extract frames "$dir_traj/7vki.pdb" "$dir_traj/7vki.xtc" -o "$dir_out/frames_some_u" -f 20 40 60 -u
