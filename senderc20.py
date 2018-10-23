"""erc20kit python

Usage:
  senderc20.py <contract_address> <from_privatekey> <to_address> <amount>
  senderc20.py (-h | --help)
  senderc20.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from time import sleep
import decimal
import json
import erc20token
from docopt import docopt

from config import contract_abi, RPC_PROVIDER


tx_statuses = {}
def txCallback(tx_id, status, from_address, to_address, amount):
    tx_statuses[tx_id] = status
  

def sendErc20(contract_address, from_privatekey, to_address, amount):
    """Send ERC20 token

    Args:
        contract_address(str): The address for ERC20 token.
        from_privatekey(str): Private Key for from address.
        to_address(str): The address to send tokens to.
        amount(Decimal): The amount of tokens to transfer.
    """
    token_sdk = erc20token.SDK(provider_endpoint_uri=RPC_PROVIDER, 
                       private_key=from_privatekey,
                       contract_address=contract_address, 
                       contract_abi=json.loads(contract_abi))
    print(f"Balance: {token_sdk.get_token_balance()}")

    # Monitor token transactions from me 
    token_sdk.monitor_token_transactions(txCallback, from_address=token_sdk.get_address())

    # Send tokens
    tx_id = token_sdk.send_tokens(to_address, amount)

    print(f"Sending {amount} tokens to {to_address} - {tx_id}...")
    
    # In a short while, the transaction enters the pending queue
    for wait in range(0, 5000):
        if (tx_id in tx_statuses) and (tx_statuses[tx_id] > erc20token.TransactionStatus.UNKNOWN):
            break
        sleep(0.003)
    assert (tx_id in tx_statuses) and (tx_statuses[tx_id] >= erc20token.TransactionStatus.PENDING)
    print(f"\tPending transation...")

    # Wait until transaction is confirmed
    for wait in range(0, 90):
        if (tx_id in tx_statuses) and (tx_statuses[tx_id] > erc20token.TransactionStatus.PENDING):
            break
        sleep(1)
    assert (tx_id in tx_statuses) and (tx_statuses[tx_id] == erc20token.TransactionStatus.SUCCESS)
    print(f"\tSent {amount} tokens")

    print(f"Balance: {token_sdk.get_token_balance()}")


if __name__ == "__main__":
    arguments = docopt(__doc__, version='erc20kit sender python 0.1')

    contract_address = arguments["<contract_address>"]
    from_privatekey = arguments["<from_privatekey>"]
    to_address = arguments["<to_address>"]
    amount = decimal.Decimal(arguments["<amount>"])

    sendErc20(contract_address, from_privatekey, to_address, amount)
    