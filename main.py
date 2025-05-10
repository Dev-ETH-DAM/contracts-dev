#!/usr/bin/env python3

import asyncio
from src.ContractUtility import ContractUtility
from src.MainContract import add_to_request_queue, get_request_queue, get_in_progress_queue, get_completed_queue
from src.SubContract import *
from src.MessageBox import set_message, get_message
import argparse

from tee.mover import process_request_queue


async def aggregate_contract_results():
    pass


async def validate_crumb_results():
    pass


async def async_main():
    """
    Main method for the Python CLI tool.

    :return: None
    """

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


def main():
    """
    Entry point that runs the async main function
    """

    asyncio.run(async_main())


if __name__ == "__main__":
    main()
