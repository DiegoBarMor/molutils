#!/bin/bash
set -euo pipefail

bash tests/00_list.sh
bash tests/01_count.sh
bash tests/02_extract.sh
bash tests/03_remove.sh
bash tests/04_select.sh
bash tests/05_merge.sh
