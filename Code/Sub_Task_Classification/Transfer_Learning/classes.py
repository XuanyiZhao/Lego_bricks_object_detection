import torch
import torch.nn as nn

# define logistic regression
class LogisticRegression(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(LogisticRegression, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, output_size)

    def forward(self, x):
        batch_size = x.shape[0]
        x = x.view(batch_size, -1)
        x = self.fc1(x)
        return x

"""## Naive neural network

"""

class SimpleNetwork(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(SimpleNetwork, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, output_size)
        )

    def forward(self, x):
        batch_size = x.shape[0]
        x = x.view(batch_size, -1)
        x = self.layers(x)
        return x
