#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi

bash tests/00_list.sh
bash tests/01_count.sh
bash tests/02_extract.sh
bash tests/03_remove.sh
bash tests/04_select.sh
bash tests/05_merge.sh
