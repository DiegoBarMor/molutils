#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi

git clone --depth 1 --branch molutils https://github.com/DiegoBarMor/volgrids-testdata/ tests/data
