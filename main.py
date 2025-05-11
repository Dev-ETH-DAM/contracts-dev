#!/usr/bin/env python3

import asyncio
import uuid
from src.SubContract import (
    create_subcontract,add_crumb_TEE,add_crumb
)


async def async_main():
    contract = create_subcontract()
    # await add_crumb(
    #     address=contract,
    #     crumb_id="0x" + uuid.uuid4().hex,
    #     alias_name="SampleAliasName",
    #     price=30,
    #     setup_task="SampleSetupTask",
    #     setup_validation="SampleSetupValidation",
    #     max_run=5,
    # )
    await add_crumb_TEE(
        address=contract,
        crumb_id="0x"+uuid.uuid4().hex,
        alias_name="SampleAliasName",
        price=30,
        setup_task="SampleSetupTask",
        setup_validation="SampleSetupValidation",
        max_run=5,
    )

def main():
    """
    Entry point that runs the async main function
    """
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
