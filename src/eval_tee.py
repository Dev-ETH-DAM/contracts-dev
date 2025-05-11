from core.transformer_validator import TransformerValidator
from src.MainContract import get_in_progress_queue
from src.SubContract import get_crumbs_by_status, update_crumb_to_closed_validated


async def eval_done_crumbs(main_contract_address):

    sub_contracts = await get_in_progress_queue(main_contract_address)

    for sub_contract in sub_contracts:
        done_crumbs = await get_crumbs_by_status(sub_contract, 2)

        for crumb in done_crumbs:
            crumb_id, alias_name, price, status, setup_task, setup_validation, result, assignee, last_updated, max_run = crumb

            eval_task = TransformerValidator()
            eval_task.set_params(setup_validation)
            is_valid = eval_task.validate_work(None, None)

            if is_valid:
                await update_crumb_to_closed_validated(sub_contract, crumb_id)



