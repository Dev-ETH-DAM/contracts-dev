import ast
import json

from core.transformer_validator import TransformerValidator
from src.MainContract import get_in_progress_queue
from src.SubContract import get_crumbs_by_status, update_crumb_to_closed_validated


async def eval_done_crumbs(main_contract_address='0x123f578600F8B64B235ba9D627F121c619731275'):


    in_progress_items = await get_in_progress_queue(main_contract_address)

    for item in in_progress_items:
        done_crumbs = await get_crumbs_by_status(item[5], 0)

        for crumb in done_crumbs:
            crumb_id, alias_name, price, status, setup_task, setup_validation, result, assignee, last_updated, max_run = crumb

            res_tuple = ast.literal_eval(result)
            eval_task = TransformerValidator()
            eval_task.set_params(setup_validation)
            is_valid = eval_task.validate_work(json.loads(res_tuple[0]), json.loads(res_tuple[1]))

            if is_valid:
                await update_crumb_to_closed_validated(item[5], crumb_id)



