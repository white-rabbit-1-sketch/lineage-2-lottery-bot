from typing import List

from Entity.AbstractHistoryRecord import AbstractHistoryRecord
from Model.AbstractModel import AbstractModel
from Repository.HistoryRepository import HistoryRepository

class HistoryService:
    def __init__(
            self,
            history_repository: HistoryRepository
    ):
        self.history_repository = history_repository

    def get_records(self, model: AbstractModel) -> List[AbstractHistoryRecord]:
        return self.history_repository.get_records(model)

    def save_records(self, model: AbstractModel, records: List[AbstractHistoryRecord]) -> None:
        self.history_repository.save_records(model, records)

    def merge_records(self, file_paths: List[str], output_file: str) -> None:
        self.history_repository.merge_records(file_paths, output_file)