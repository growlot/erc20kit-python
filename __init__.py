import sys
import erc20token
import json
import docopt

# from config import contract_abi, contract_address, RPC_PROVIDER



# def getEvents(start_block, end_block):
#     """Get only 'Birth' events from start_block to end_block

#     Args:
#         start_block(int):
#         end_block(int):
#     """
#     event_filter = contract.events.Birth.createFilter(
#         fromBlock=start_block,
#         toBlock=end_block
#     )
#     events = event_filter.get_all_entries()

#     return events


# def analyzeEvent(event):
#     """Analyze a event
    
#     Args:
#         event (dict): An event object to analyze

#     Returns:
#         dict: Analysis data which contains kittyId, txHash ...
#     """
#     txHash = event['transactionHash']
#     kittyId = event['args']['kittyId']
    
#     tx = web3.eth.getTransaction(txHash)
#     block = web3.eth.getBlock(event['blockNumber'])
    
#     fromAddress = tx['from']
#     toAddress = tx['to']
#     timestamp = block['timestamp']

#     return {
#         'kittyId': kittyId,
#         'txHash': txHash.hex(),
#         'from': fromAddress,
#         'to': toAddress,
#         'timestamp': timestamp
#     }


# def writeToCSV(data, fileName='events.csv'):
#     """Write array of dict data to csv

#     Args:
#         data (array): Array of dictionaries to write into a csv
#         fileName(str): A csv file name
#     """
#     keys = data[0].keys()
#     with open(fileName, 'w') as output_file:
#         dict_writer = csv.DictWriter(output_file, keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(data)


# def runAnalyzer(start_block=DEFAULT_START_BLOCK, end_block=DEFAULT_END_BLOCK):
#     """Start analyzing the events

#     Args:
#         start_block(int): Height of the starting block to analyze
#         end_block(int): Height of the ending block to analyze
#     """
#     events = getEvents(start_block, end_block)
#     print("--------- Read {} events -----------".format(len(events)))

#     eventsData = []
#     for event in events:
#         data = analyzeEvent(event)
#         eventsData.append(data)

#     print("--------- Processed {} events ----------".format(len(eventsData)))

#     writeToCSV(eventsData)


tx_statuses = {}
def txCallback(tx_id, status, from_address, to_address, amount):
    tx_statuses[tx_id] = status
  

def sendErc20(contract_address, from_address, from_privatekey, to_address, amount):
    """Send ERC20 token

    Args:
        contract_address(string): Ethereum address for ERC20 token
        from_address(string): Ethereum address for account from
        from_privatekey(string): Private Key for the fromAddress
        to_address(string): Ethereum address for account to
        amount(int64): Wei amount to send
    """
    token_sdk = erc20token.SDK(provider_endpoint_uri=RPC_PROVIDER, 
                       private_key=from_privatekey,
                       contract_address=contract_address, 
                       contract_abi=json.loads(contract_abi))
    token_balance = token_sdk.get_token_balance()
    print("Balance: {}".format(token_balance))

    # Monitor token transactions from me 
    token_sdk.monitor_token_transactions(txCallback, from_address=token_sdk.get_address())

    # Send tokens
    tx_id = token_sdk.send_tokens(to_address, amount)

    # In a short while, the transaction enters the pending queue
    for wait in range(0, 5000):
        if tx_statuses[tx_id] > erc20token.TransactionStatus.UNKNOWN:
            break
        sleep(0.001)
    assert tx_statuses[tx_id] >= erc20token.TransactionStatus.PENDING

    # Wait until transaction is confirmed 
    for wait in range(0, 90):
        if tx_statuses[tx_id] > erc20token.TransactionStatus.PENDING:
            break
        sleep(1)
    assert tx_statuses[tx_id] == erc20token.TransactionStatus.SUCCESS
    print("Sent {}".format(amount))


if __name__ == "__main__":
    arguments = docopt(__doc__, version='erc20kit python 0.1')
    print(arguments)

    sendErc20("","","","",1)
    