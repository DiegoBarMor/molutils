#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi
if [ ! -d "tests/data" ]; then
    bash tests/_fetch.sh
fi

echo ">>> TEST MOLUTILS 03: REMOVE"

dir_in="tests/data/input"

# python3 molutils remove altlocs "$dir_in/6e9a.pdb"
