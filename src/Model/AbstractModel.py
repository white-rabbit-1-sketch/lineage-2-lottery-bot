import torch
import torch.nn as nn
import torch.optim as optim

LEARNING_RATE = 0.001
LEARNING_STEP_SIZE = 20
DROPOUT = 0.3

INPUT_SIZE = 1
HIDDEN_SIZE = 100
NUM_LAYERS = 3
OUT_FEATURES = 1

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

if torch.cuda.is_available():
    torch.cuda.empty_cache()


class AbstractModel(nn.Module):
    def __init__(
            self,
            input_size: int = INPUT_SIZE,
            hidden_size: int = HIDDEN_SIZE,
            num_layers: int = NUM_LAYERS,
            dropout: float = DROPOUT,
            out_features: int = OUT_FEATURES,
    ):
        super(AbstractModel, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size

        self.lstm_results = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )

        self.fc_hidden = nn.Linear(hidden_size, hidden_size // 2)
        self.dropout = nn.Dropout(dropout)
        self.fc_combined = nn.Linear(hidden_size // 2, out_features)

        self.optimizer = optim.Adam(self.parameters(), lr=LEARNING_RATE, weight_decay=0.01)
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=LEARNING_STEP_SIZE, gamma=0.9)

        self.to(device)

    def forward(self, context):
        h_0 = torch.zeros(self.num_layers, context.size(0), self.hidden_size).to(device)
        c_0 = torch.zeros(self.num_layers, context.size(0), self.hidden_size).to(device)

        out_results, _ = self.lstm_results(context, (h_0, c_0))
        out_results = out_results[:, -1, :]

        out = self.fc_hidden(out_results)
        out = torch.relu(out)
        out = self.dropout(out)
        out = self.fc_combined(out)

        return out

    def get_prediction(self, context):
        context = torch.tensor(context, dtype=torch.float32).unsqueeze(0).to(device)
        if len(context) > 2:
            context = (context - context.mean()) / context.std()

        output = self.forward(context)
        probabilities = torch.softmax(output, dim=1)

        return output, probabilities

    def correct(self, output, corrected_result, base_weights = None):
        target = torch.tensor([corrected_result], dtype=torch.long).to(device)

        criterion = nn.CrossEntropyLoss()
        if base_weights is not None:
            weights = torch.tensor(base_weights, dtype = torch.float32).to(device)
            criterion = nn.CrossEntropyLoss(weight = weights)

        loss = criterion(output, target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.scheduler.step()

        return loss.item()