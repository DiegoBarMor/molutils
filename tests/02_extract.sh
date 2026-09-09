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

# python3 molutils extract models # [TODO]
# python3 molutils extract chains # [TODO]
# python3 molutils extract residue # [TODO]
# python3 molutils extract frames # [TODO]
