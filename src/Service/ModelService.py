from Model.AbstractModel import AbstractModel
from Repository.ModelRepository import ModelRepository

class ModelService:
    def __init__(self, model_repository: ModelRepository):
        self.model_repository = model_repository

    def get_data(self, model: AbstractModel):
        return self.model_repository.get_data(model)

    def save_data(self, model: AbstractModel):
        self.model_repository.save_data(model)