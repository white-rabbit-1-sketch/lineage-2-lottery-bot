import torch
import os

from Model.AbstractModel import AbstractModel

class ModelRepository:
    def __init__(self, var_path: str):
        self.var_path = var_path

    def get_data(self, model: AbstractModel):
        if os.path.exists(self.get_model_data_path(model)):
            data = torch.load(self.get_model_data_path(model))
            model.load_state_dict(data['model_state_dict'])
            #model.set_h_0(data['h_0'])
            #model.set_c_0(data['c_0'])

    def save_data(self, model: AbstractModel):
        torch.save({
            'model_state_dict': model.state_dict(),
            #'h_0': model.get_h_0(),
            #'c_0': model.get_c_0()
        }, self.get_model_data_path(model))

    def get_model_data_path(self, model: AbstractModel) -> str:
        return os.path.join(self.var_path, model.__class__.__name__ + ".model.tbh")