#!/usr/bin/env python3

import asyncio
from asyncio import sleep
import asyncio.tasks
import os
from src.ContractUtility import ContractUtility
from src.MainContract import ComputeTask, move_to_completed_queue, add_to_request_queue, get_request_queue, get_in_progress_queue, get_completed_queue, get_in_progress_queue_t
from src.SubContract import *
from src.MessageBox import set_message, get_message
import argparse

from src.eval_tee import eval_done_crumbs
from tee.mover import process_request_queue


async def aggregate_contract_results():
    MAIN_CONTRACT_ADDRESS = "0x123f578600F8B64B235ba9D627F121c619731275"
    # Get all contracts from in progress queue
    print("Getting in progress queue...")
    in_progress_queue: list[ComputeTask] = await get_in_progress_queue_t(
        MAIN_CONTRACT_ADDRESS
    )
    for task in in_progress_queue:
        # Get the contract address
        contract_address: str = task.subContractAddress

        # Get the crumbs from the contract
        crumbs: list[Crumb] = await get_all_crumbs_t(contract_address)

        # Get the results from the crumbs
        is_complete = True
        for crumb in crumbs:
            if crumb.status != CrumbStatus.CLOSED_VALIDATED.value:
                is_complete = False
                break

        print(f'Is complete: {is_complete}')
        if is_complete:
            await move_to_completed_queue(MAIN_CONTRACT_ADDRESS, task.id)

        await sleep(30)


async def aggregate_task():
    """
    Aggregate the task from the request queue and move it to the in progress queue.
    """

    while True:
        await aggregate_contract_results()

        await sleep(30)


async def validate_crumb_results():
    while True:
        await eval_done_crumbs()
        await sleep(30)


async def mover():
    while True:
        await process_request_queue()
        await sleep(30)
async def async_main():
    """
    Main method for the Python CLI tool.

    :return: None
    """
    await eval_done_crumbs()
    return
    parser = argparse.ArgumentParser(
        description="""A Python CLI tool for compiling,
                    deploying, and interacting with smart contracts."""
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subparser for compile
    compile_parser = subparsers.add_parser(
        "compile",
        help="Compile the source code"
    )
    compile_parser.add_argument(
        "--contract",
        help="Name of the contract to compile",
        default="MessageBox"
    )

    # Subparser for deploy
    deploy_parser = subparsers.add_parser(
        "deploy",
        help="Deploy the smart contract"
    )
    deploy_parser.add_argument(
        "--contract",
        help="Name of the contract to deploy",
        default="MessageBox"
    )
    deploy_parser.add_argument(
        "--network",
        help="Chain name to connect to "
        "(sapphire, sapphire-testnet, sapphire-localnet)",
        required=True,
    )

    arguments = parser.parse_args()

    # Run aggregate_contract_results in the background every 30 seconds
    # and validate_crumb_results in the background every 30 seconds
    # using asyncio.create_task
    task = asyncio.create_task(aggregate_contract_results())
    task2 = asyncio.create_task(validate_crumb_results())
    task3 = asyncio.create_task(mover())

    match arguments.command:
        case "compile":
            # Use class method which does not
            # require an instance of ContractUtility.
            # This is to avoid setting up the Web3 instance
            # which requires the PRIVATE_KEY.
            ContractUtility.setup_and_compile_contract(arguments.contract)
        case "deploy":
            contract_utility = ContractUtility(arguments.network)
            await contract_utility.deploy_contract(arguments.contract)
        case _:
            parser.print_help()
    await task
    await task2
    await task3


def main():
    """
    Entry point that runs the async main function
    """

    asyncio.run(async_main())


if __name__ == "__main__":
    main()
