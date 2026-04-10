#!/bin/bash
set -eu

### Re-install the package locally

pip uninstall molutils -y || true
pip install .
rm -rf build molutils.egg-info
