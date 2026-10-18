#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi
if [ ! -d "tests/data" ]; then
    bash tests/_fetch.sh
fi

echo ">>> TEST MOLUTILS 05: MERGE"

dir_in="tests/data/input"
dir_out="tests/data/output/merge"

python3 molutils merge "$dir_in/1aju.pdb" "$dir_in/6e9a.pdb" -o "$dir_out/merged.pdb"
