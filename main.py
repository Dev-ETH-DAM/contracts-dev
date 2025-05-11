#!/usr/bin/env python3

import asyncio
import uuid
import random
from src.SubContract import (
    create_subcontract,exec_function_general,add_crumb
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
    for i in range(5):    
        await exec_function_general(
            address=contract,
            args=["0x"+uuid.uuid4().hex,
            "SampleAliasName",
            random.randint(1, 100),
            "SampleSetupTask",
            "SampleSetupValidation",
            random.randint(1, 100)],
        )

def main():
    """
    Entry point that runs the async main function
    """
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
