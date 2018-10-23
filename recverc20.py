"""erc20kit receiver python

Usage:
  recverc20.py <contract_address> <to_address>
  recverc20.py (-h | --help)
  recverc20.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

import sys
from time import sleep
import decimal
import json
import erc20token
from docopt import docopt

from config import contract_abi, RPC_PROVIDER


tx_statuses = {}
accepted_tx_statuses = {}
def txCallback(tx_id, status, from_address, to_address, amount):
    tx_statuses[tx_id] = status
  

def recvErc20(contract_address, to_address):
    """Receive ERC20 token

    Args:
        contract_address(str): The address for ERC20 token.
        to_address(str): The address to be sent tokens to.
    """
    token_sdk = erc20token.SDK(provider_endpoint_uri=RPC_PROVIDER, 
                       contract_address=contract_address, 
                       contract_abi=json.loads(contract_abi))

    # Monitor token transactions from me 
    token_sdk.monitor_token_transactions(txCallback, to_address=to_address)

    print(f"Waiting for receiving tokens - balance: {token_sdk.get_address_token_balance(to_address)}")
    
    while True:
        for tx_id in tx_statuses:
            tx_status = tx_statuses[tx_id]
            if tx_status == erc20token.TransactionStatus.PENDING:
                if not(tx_id in accepted_tx_statuses):
                    accepted_tx_statuses[tx_id] = erc20token.TransactionStatus.PENDING
                    print(f"Pending transation {tx_id}...")
            if tx_status == erc20token.TransactionStatus.SUCCESS:
                tx_data = token_sdk.get_transaction_data(tx_id)
                print(f"Received {tx_data.token_amount} tokens from {tx_data.from_address} - balance: {token_sdk.get_address_token_balance(to_address)}")
                tx_statuses.pop(tx_id, None)
                accepted_tx_statuses.pop(tx_id, None)
                break
        sleep(1)


if __name__ == "__main__":
    arguments = docopt(__doc__, version='erc20kit receiver python 0.1')

    contract_address = arguments["<contract_address>"]
    to_address = arguments["<to_address>"]

    recvErc20(contract_address, to_address)
    