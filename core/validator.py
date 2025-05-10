import json

validator_json_key = "VALIDATOR_SETUP"

class TaskValidator:
    params = None
    is_valid = False
    
    def set_params(self, configuration_json:str):
        """Sets the parameters for the validator, the default
        is to just save the json, but it is recommended
        to have your own parameter logic.

        Args:
            configuration_json (str): a json grabbed from 
            the task where the orchestrator can 
            add extra parameters. The orchestrator needs to
            provide only the validation part.
        """
        self.params = json.loads(configuration_json)

    def validate_work(self, given_params:dict, given_results:dict):
        """Validate that the results come from the 
        given parameters. In case they do is_valid becomes
        true, else remains false.

        Args:
            given_params (dict): the parameters that come from the
            work of a task
            given_results (dict): the results that come from the 
            work of a task
        """
        self.is_valid = False

    def item_is_valid(self) -> bool:
        """Aditional logic to validate the work, if needed.

        If the work is valid the orchestrator needs to close the
        item and assignd the reward to the wallet.

        Returns:
            bool: If the work item was valid or not.
        """
        return self.is_valid