# Send and receive ERC20 tokens kits 

## Requirements

Make sure you have Python 3 >=3.6.6

## Installation 

```
sudo apt update
sudo apt install build-essential automake libtool pkg-config libcurl4-openssl-dev curl libssl-dev

pip3 install -r requirements.txt
```

## Usage

### Send

```
python3 senderc20.py <contract_address> <from_privatekey> <to_address> <amount>
python3 senderc20.py (-h | --help)
python3 senderc20.py --version
python3 senderc20.py 0x61fadb0417c6b2252775790379dc96035a3c49c2 <from_privatekey> 0xc419f76dbf00C094eAF1F4F5399DB7785BaFD82e 0.1
```

### Receive

```
python3 recverc20.py <contract_address> <to_address>
python3 recverc20.py (-h | --help)
python3 recverc20.py --version
python3 recverc20.py 0x61fadb0417c6b2252775790379dc96035a3c49c2 0xc419f76dbf00C094eAF1F4F5399DB7785BaFD82e
```
