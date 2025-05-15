# defichain_scripts
Scripts to get stuff from the blockchain

source your venv or generate a new one:
python -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate

install the package into venv:
pip install -e .

generate your .evn file containing the path to defi-cli as well as login credentials from defi.conf
]$ cat .env
USERNAME=YOUR_DEFI_RPC_USER
PASSWORD=YOUR_DEFI_RPC_PASSWORD
CLI="defi-cli command"


use provided commands as defined in pyproject.toml
defichain_*
