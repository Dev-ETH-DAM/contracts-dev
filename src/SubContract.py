from typing import Optional
from src.ContractUtility import ContractUtility
from src.utils import get_contract
import subprocess
import aiohttp
import json

async def add_crumb(
    address: str,
    crumb_id: str,
    alias_name: str,
    price: int,
    setup_task: str,
    setup_validation: str,
    max_run: int,
    network_name: Optional[str] = "sapphire-testnet"
):
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    gas_price = await contract_utility.w3.eth.gas_price
    tx_hash = await contract.functions.addCrumb(
        crumb_id, alias_name, price, setup_task, setup_validation, max_run
    ).transact({"gasPrice": gas_price})
    tx_receipt = await contract_utility.w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"addCrumb transaction: {tx_receipt.transactionHash.hex()}")

async def update_crumb_to_queued(
    address: str,
    crumb_id: str,
    network_name: Optional[str] = "sapphire-testnet"
):
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    gas_price = await contract_utility.w3.eth.gas_price
    tx_hash = await contract.functions.updateCrumbToQueued(crumb_id).transact({"gasPrice": gas_price})
    tx_receipt = await contract_utility.w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"updateCrumbToQueued transaction: {tx_receipt.transactionHash.hex()}")

async def update_crumb_to_closed(
    address: str,
    crumb_id: str,
    result: str,
    network_name: Optional[str] = "sapphire-testnet"
):
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    gas_price = await contract_utility.w3.eth.gas_price
    tx_hash = await contract.functions.updateCrumbToClosed(crumb_id, result).transact({"gasPrice": gas_price})
    tx_receipt = await contract_utility.w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"updateCrumbToClosed transaction: {tx_receipt.transactionHash.hex()}")

async def update_crumb_to_closed_validated(
    address: str,
    crumb_id: str,
    network_name: Optional[str] = "sapphire-testnet"
):
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    gas_price = await contract_utility.w3.eth.gas_price
    tx_hash = await contract.functions.updateCrumbToClosedValidated(crumb_id).transact({"gasPrice": gas_price})
    tx_receipt = await contract_utility.w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"updateCrumbToClosedValidated transaction: {tx_receipt.transactionHash.hex()}")

async def get_crumb(
    address: str,
    crumb_id: str,
    network_name: Optional[str] = "sapphire-testnet"
):
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    crumb = await contract.functions.getCrumb(crumb_id).call()
    print(f"Crumb: {crumb}")
    return crumb

async def get_crumb_count(address: str, network_name: Optional[str] = "sapphire-testnet"):
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    count = await contract.functions.getCrumbCount().call()
    print(f"Number of crumbs: {count}")
    return count

async def get_crumbs_by_status(
    address: str,
    status: int,
    network_name: Optional[str] = "sapphire-testnet"
):
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    crumbs = await contract.functions.getCrumbsByStatus(status).call()
    print(f"Crumbs by status {status}: {crumbs}")
    return crumbs

async def get_all_crumbs(
    address: str,
    network_name: Optional[str] = "sapphire-testnet"
):
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    crumbs = await contract.functions.getAllCrumbs().call()
    print(f"All crumbs: {crumbs}")
    return crumbs


def create_subcontract(requester = "0xF4906b5F6D8D6f0f0512187C826729f027ADcb4B",
                       requestName = "SampleRequestName",
                       roflAppID = "00eac11dbccf10c68be35adf2fcf5ed09fecace79c",
                       private_key = "951ce0377a4cec5d2312b45396784ca75227098d414f704b25b601a33af96e27",):
    try:
        p = subprocess.run(
            [   
                "forge create src/SubContract.sol:SubContract "+
                "--evm-version paris --broadcast --json --rpc-url https://testnet.sapphire.oasis.dev "+
                f"--private-key {private_key} "+
                f"--constructor-args {requestName} {requester} {roflAppID}"
            ],
            shell=True,
            text=True,
            check=True,
            capture_output=True
        )

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Output:", e.stdout)
        print("Error:", e.stderr)
        return
    
    output = json.loads(p.stdout)
    return output['deployedTo']


async def exec_function_general(
    address: str,
    args: list,
    network_name: Optional[str] = "sapphire-testnet",
    rofl_socket_path: str = "/run/rofl-appd.sock",
    contract_name: str = "SubContract",
    method_name: str = "addCrumb",
):
    # Prepare the contract call data
    # Assume get_contract and ContractUtility usage remains the same for ABI encoding
    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract(contract_name)
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)
    # Build the encoded data payload for addCrumb
    data_hex = contract.encode_abi(
        method_name,
        args=args
    )

    # Estimate gas limit if desired
    gas_limit = await contract_utility.w3.eth.estimate_gas({
        "to": address,
        "data": data_hex,
        "value": 0
    })

    # Build JSON-RPC payload for /rofl/v1/tx/sign-submit
    tx_payload = {
        "tx": {
            "kind": "eth",
            "data": {
                "to": address.lstrip("0x"),
                "value": 0,
                "data": str(data_hex).lstrip("0x"),
                "gas_limit": gas_limit
            }
        }
    }

    print(json.dumps(tx_payload))

    # Send the transaction via the UNIX socket endpoint
    # Use aiohttp with UnixConnector
    connector = aiohttp.UnixConnector(path=rofl_socket_path)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(
            "http://localhost/rofl/v1/tx/sign-submit",
            json=tx_payload
        ) as resp:
            resp.raise_for_status()
            result = await resp.json()

    # The response typically includes the transaction hash
    tx_hash = result.get("tx_hash") or result.get("hash")
    print(f"Submitted addCrumb tx, hash: {tx_hash}")
    return tx_hash
    