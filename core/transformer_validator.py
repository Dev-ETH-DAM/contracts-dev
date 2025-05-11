from core.validator import TaskValidator
from core.constants import *

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from os.path import join
from pathlib import Path
from os import getcwd
from scipy.special import softmax

import pandas as pd
import pickle

class TransformerValidator(TaskValidator):
    task_type = None
    model_name = None
    text_key = None
    text_id_key = None
    predict_ds_url = None
    model_path = None

    def set_params(self, configuration_json:str):
        super().set_params(configuration_json)
        
        self.task_type = self.params[task_type_key]
        self.model_name = self.params[model_name_key]
        self.text_key = self.params[ds_text_key]
        self.text_id_key = self.params[ds_text_id_key]
        self.predict_ds_url = self.params[predict_ds_url_key]

        if len(self.model_name) == 0:
            self.model_name = None
        else:            
            self.model_path = join(getcwd(), "models", self.task_type, self.model_name)
            path = Path(self.model_path)     
            path.mkdir(parents=True, exist_ok=True)

    def validate_work(self, given_params:dict, given_results:dict):
        to_predict = pd.read_csv(self.predict_ds_url)

        if given_params[model_name_key] == None:
            for _, row in to_predict.iterrows():
                text = row[self.text_key]
                text_id = row[self.text_id_key]  
                output = pipeline(self.task_type, model=None)(text)[0]["label"]

                if given_results[text_id] != output:
                    self.is_valid = False
                    return
        else:
            model = AutoModelForSequenceClassification.from_pretrained(
                self.model_path,
                ignore_mismatched_sizes=True,
                problem_type=self.model_type)
            tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            model = pickle.loads(given_params[model_name_key])

            for _, row in to_predict.iterrows():
                text = row[self.text_key]
                text_id = row[self.text_id_key]
                inputs = tokenizer(text, return_tensors="pt")
                outputs = model(**inputs)

                probabilities = softmax(
                        outputs[0].cpu().detach().numpy(), axis=1)[0]
                
                output = int(probabilities.argmax())

                if given_results[int(text_id)] != output:
                    self.is_valid = False
                    return
                
        self.is_valid = True
        return True

