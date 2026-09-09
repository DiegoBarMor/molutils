#!/bin/bash
set -euo pipefail

if [ ! -d "tests" ]; then
    echo "This script must be run from the root of the repository (where the 'tests' directory is located)."
    exit 1
fi
if [ ! -d "tests/data" ]; then
    bash tests/_fetch.sh
fi

echo ">>> TEST MOLUTILS 00: LIST"

dir_in="tests/data/input"

python3 molutils list chains "$dir_in/prot_rna.pdb" # expected: H R
python3 molutils list residues "$dir_in/prot_rna.pdb" # expected: H.100 H.101 H.102 H.103 H.104 H.105 H.106 H.107 H.108 H.109 H.110 H.111 H.112 H.113 H.114 H.115 H.116 H.117 H.118 H.119 H.120 H.121 H.122 H.123 H.124 H.125 H.126 H.127 H.128 H.129 H.130 H.131 H.132 H.133 H.134 H.135 H.136 H.137 H.138 H.139 H.140 H.141 H.142 H.143 H.144 H.145 H.146 H.147 H.148 H.149 H.150 H.151 H.152 H.153 H.154 H.155 H.156 H.157 H.158 H.159 H.160 H.161 H.162H.163 H.164 H.165 H.166 H.167 H.168 H.169 H.170 H.171 H.172 H.173 H.174 H.175 H.176 H.177 H.178 H.179 H.180 H.181 H.182 H.183 H.184 H.185 H.186 H.187 H.188 H.189 H.190 H.191 H.192 H.193 H.194 H.195 H.196 H.197 H.198 H.199 H.200 H.201 H.202 H.203 H.204 H.205 H.206 H.207 H.208 H.35 H.36 H.37 H.38 H.39 H.40 H.41 H.42 H.43 H.44 H.45 H.46 H.47 H.48 H.49 H.50 H.51 H.52 H.53 H.54 H.55 H.56 H.57 H.58 H.59 H.60 H.61 H.62 H.63 H.64 H.65 H.66 H.67 H.68 H.69 H.70 H.71 H.72 H.73 H.74 H.75 H.76 H.77 H.78 H.79 H.80 H.81 H.82 H.83 H.84 H.85 H.86 H.87 H.88 H.89 H.90 H.91 H.92 H.93 H.94 H.95 H.96 H.97 H.98 H.99 R.0 R.1 R.2 R.3 R.4 R.5 R.6 R.7 R.8 R.9
