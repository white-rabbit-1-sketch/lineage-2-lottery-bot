from Model.AbstractModel import AbstractModel

class CasinoColorModel(AbstractModel):
    def __init__(self):
        super(CasinoColorModel, self).__init__(input_size = 24, out_features = 2)