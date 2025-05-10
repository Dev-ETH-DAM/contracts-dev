# Oasis Starter dApp in Python

This is a skeleton for confidential Oasis dApps in Python.

## Prerequisites

This project was tested on python 3.12, but should work with most
python3 versions. 
Use pyenv to handle multiple python installations.

## Installation

1. Initialize an environment using preferred environment manager 
   (venv, pipx...) ```python3 -m venv my_env```.
2. Install the [`oasis-sapphire-py`](https://pypi.org/project/oasis-sapphire-py/) client library and
   other dependencies from requirements.txt ```pip install -r requirements.txt```.

## Setup

1. If running sapphire-localnet make sure to launch the 
[local node](https://github.com/oasisprotocol/oasis-web3-gateway/tree/main/docker).

2. Add your deployer private key to the environment variables 
```export PRIVATE_KEY=<my_private_key>```. Make sure you have 
enough funds to cover the gas fees.

## Running

The **./src** folder contains the .py files which are used to compile, 
deploy and interact with the contracts inside 
**./contracts** folder. 
It also contains the ```main.py``` for command line development. 
Again make sure to follow the setup 
[instructions](#Setup) before running scripts.
Open main.py which contains a simple starter example.

### Initialization

The `ContractUtility` class is used to compile and deploy the contracts, 
based on the network name (sapphire, sapphire-testnet, sapphire-localnet).
The private key used to deploy the contract is fetched from the PRIVATE_KEY 
environment variable.

```python
contract_utility = ContractUtility("sapphire-localnet")
```

### Compiling the contract

After saving the .sol contract in **./contracts** folder, 
we can continue with compilation step.

To compile use class method ```setup_and_compile_contract()``` 
from **ContractUtility.py**.

```python
from src.ContractUtility import ContractUtility

ContractUtility.setup_and_compile_contract("MessageBox")
```

### Deploying the contract

```python
await contract_utility.deploy_contract("MessageBox)
```
Provide the contract name, in the starter example case 
we use the provided **MessageBox** without the .sol extension.

### Interacting with the contract

To help you get started with development,  ```main.py``` 
contains some functionality that showcases web3.py 
contract abstraction interaction.
It contains ```set_message()``` and ```get_message()``` 
functions that set message and query the contract view function 
```message()``` respectively. Message is fetched using the [EIP-712 signed queries](https://docs.oasis.io/build/sapphire/develop/authentication/) which allows for 
private data retrieval (msg.sender == author access control).

### Run example

To run: ```python3 main.py```

### CLI development

To compile, deploy and call the interact_with_contract() 
function from the terminal:
```shell
python3 main.py compile
python3 main.py deploy --network sapphire-localnet
python3 main.py setMessage --address <contract_address> --message "Hello world" --network sapphire-localnet
python3 main.py message --address <contract_address> --network  sapphire-localnet
```

## Testing

Some inital unit tests are located in **./tests** folder. 
Run ```pytest``` in the terminal. 
End-to-end tests are set to ```sapphire-localnet```, 
check ```tests/test_ContractUtility.py``` if you want to change the network.

