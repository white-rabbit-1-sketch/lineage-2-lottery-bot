import pickle
import os
from typing import List

from Entity.AbstractHistoryRecord import AbstractHistoryRecord
from Model.AbstractModel import AbstractModel


class HistoryRepository:
    def __init__(self, var_path: str):
        self.var_path = var_path

    def get_records(self, model: AbstractModel) -> List[AbstractHistoryRecord]:
        result = []

        if os.path.exists(self.get_model_history_path(model)):
            with open(self.get_model_history_path(model), 'rb') as file:
                result = pickle.load(file)

        return result

    def save_records(self, model: AbstractModel, records: List[AbstractHistoryRecord]) -> None:
        with open(self.get_model_history_path(model), 'wb') as file:
            pickle.dump(records, file)

    def get_model_history_path(self, model: AbstractModel) -> str:
        return os.path.join(self.var_path, model.__class__.__name__ + ".history.pickle")

    def merge_records(self, file_paths: List[str], output_file: str) -> None:
        output_file = os.path.join(self.var_path, output_file)

        merged_records = []

        for file_path in file_paths:
            file_path = os.path.join(self.var_path, file_path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    records = pickle.load(file)
                    if isinstance(records, list):
                        merged_records.extend(records)
                    else:
                        print(f"Warning: {file_path} does not contain a list of records.")
            else:
                print(f"Warning: {file_path} does not exist.")

        with open(output_file, 'wb') as output:
            pickle.dump(merged_records, output)

        print(f"Merged {len(merged_records)} records into {output_file}.")