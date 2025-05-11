import ast
import json

from core.transformer_validator import TransformerValidator
from src.MainContract import get_in_progress_queue
from src.SubContract import get_crumbs_by_status, update_crumb_to_closed_validated


async def eval_done_crumbs(main_contract_address='0x885cA90bD752A682dD1883614edA0C0557c973a6'):


    in_progress_items = await get_in_progress_queue(main_contract_address)

    for item in in_progress_items:
        done_crumbs = await get_crumbs_by_status(item[5], 2)

        for crumb in done_crumbs:

            res_tuple = ast.literal_eval(crumb.result)
            eval_task = TransformerValidator()
            eval_task.set_params(crumb.setup_validation)
            is_valid = eval_task.validate_work(res_tuple[0], res_tuple[1])

            if is_valid:
                await update_crumb_to_closed_validated(item[5], crumb.id)



