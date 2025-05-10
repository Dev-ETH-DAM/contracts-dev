#!/usr/bin/env python3

import asyncio
from src.ContractUtility import ContractUtility
from src.MainContract import add_to_request_queue, get_request_queue, get_in_progress_queue, get_completed_queue
from src.SubContract import *
from src.MessageBox import set_message, get_message
import argparse

from tee.mover import process_request_queue


async def async_main():
    """
    Main method for the Python CLI tool.

    :return: None
    """

    # await process_request_queue('0x123f578600F8B64B235ba9D627F121c619731275')
    # return
    #
    # a = await get_crumbs_by_requester("0xf0f07F649bAD04Bf3956bdcac4ad8e3f616B80DF")
    #
    # print(a)
    #
    # return

    # await add_to_request_queue('0x123f578600F8B64B235ba9D627F121c619731275', 'JsonB', 10, 1)
    # a = await get_request_queue('0x123f578600F8B64B235ba9D627F121c619731275')
    # print(a)
    #
    # a = await get_in_progress_queue('0x123f578600F8B64B235ba9D627F121c619731275')
    # print(a)
    #
    # a = await get_completed_queue('0x123f578600F8B64B235ba9D627F121c619731275')
    # print(a)
    # return

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

    # Subparser for set message
    set_message_parser = subparsers.add_parser(
        "setMessage", help="Interact with a deployed contract"
    )
    set_message_parser.add_argument(
        "--address", help="Contract address to call", required=True
    )
    set_message_parser.add_argument(
        "--message", help="Message to store in the contract", required=True
    )
    set_message_parser.add_argument(
        "--network",
        help="Chain name to connect to "
        "(sapphire, sapphire-testnet, sapphire-localnet)",
        required=True,
    )

    # Subparser for get message
    get_message_parser = subparsers.add_parser(
        "message", help="Interact with a deployed contract"
    )
    get_message_parser.add_argument(
        "--address", help="Contract address to call", required=True
    )
    get_message_parser.add_argument(
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
        case "setMessage":
            await set_message(
                arguments.address,
                arguments.message,
                arguments.network
                )
        case "message":
            await get_message(arguments.address, arguments.network)
        case _:
            parser.print_help()


def main():
    """
    Entry point that runs the async main function
    """
    # asyncio.run(add_crumb("0xf0f07F649bAD04Bf3956bdcac4ad8e3f616B80DF",
    #                         b'1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x33',
    #                         "test",
    #                         3,
    #                         """{
    #                           "task_type": "sentiment-analysis",
    #                           "model_name": "",
    #                           "dataset_url": "",
    #                           "id_dict": {},
    #                           "label_dict": {},
    #                           "batch_size": 32,
    #                           "train_ds_url": "",
    #                           "test_ds_url": "",
    #                           "ds_text_column": "text",
    #                           "ds_id_column": "id",
    #                           "predict_ds_url": "https://raw.githubusercontent.com/AskingAlexander/Datasets/refs/heads/master/sample.csv"
    #                         }""",
    #                         "{}",
    #                         4
    #                       ))
    # asyncio.run(update_crumb_to_queued("0xf0f07F649bAD04Bf3956bdcac4ad8e3f616B80DF",
    #                         b'1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x33'))
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
