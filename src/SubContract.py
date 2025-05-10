from typing import Optional
from src.ContractUtility import ContractUtility
from src.utils import get_contract

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

async def get_crumbs_by_requester(
    address: str,
    network_name: Optional[str] = "sapphire-testnet"
):
    from src.ContractUtility import ContractUtility
    from src.utils import get_contract

    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    crumbs = await contract.functions.getCrumbsByRequester().call()
    print(f"Crumbs by requester: {crumbs}")
    return crumbs


async def update_results(
    address: str,
    results: str,
    network_name: Optional[str] = "sapphire-testnet"
):
    from src.ContractUtility import ContractUtility
    from src.utils import get_contract

    contract_utility = ContractUtility(network_name)
    abi, _ = get_contract("SubContract")
    contract = contract_utility.w3.eth.contract(address=address, abi=abi)

    gas_price = await contract_utility.w3.eth.gas_price
    tx_hash = await contract.functions.updateResults(results).transact({"gasPrice": gas_price})
    tx_receipt = await contract_utility.w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"updateResults transaction: {tx_receipt.transactionHash.hex()}")