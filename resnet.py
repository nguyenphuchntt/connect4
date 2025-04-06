import numpy as np
import math
import torch
import config
from board import Board


import torch.nn as nn
import torch.nn.functional as F

import matplotlib.pyplot as plt

class ResNet(nn.Module):
    "Residual neural network model."
    def __init__(self, device):
        super().__init__()
        self.device = device
        n_filters = config.N_FILTERS

        self.startBlock = nn.Sequential(
            nn.Conv2d(3, n_filters, kernel_size=3, padding=1),
            nn.BatchNorm2d(n_filters),
            nn.ReLU()
        )
        
        self.backBone = nn.ModuleList(
            [ResBlock() for i in range(config.N_RES_BLOCKs)]
        )
        
        # Policy head for choosing actions
        self.policyHead = nn.Sequential(
            nn.Conv2d(n_filters, n_filters//4, kernel_size=3, padding=1),
            nn.BatchNorm2d(n_filters//4),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(n_filters//4 * config.BOARD_ROWS * config.BOARD_COLUMNS, config.ACTION_SIZE)
        )
        
        # Value head for evaluating board states
        self.valueHead = nn.Sequential(
            nn.Conv2d(n_filters, n_filters//32, kernel_size=3, padding=1),
            nn.BatchNorm2d(n_filters//32),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(n_filters//32 * config.BOARD_ROWS * config.BOARD_COLUMNS, 1),
            nn.Tanh()
        )

        self.to(device)
        
    def forward(self, x):
        x = self.startBlock(x)
        for resBlock in self.backBone:
            x = resBlock(x)
        policy = self.policyHead(x)
        value = self.valueHead(x)
        return policy, value
    
class ResBlock(nn.Module):
    "Residual block, the backbone of a ResNet."
    def __init__(self):
        super().__init__()
        n_filters = config.N_FILTERS

        # Two convolutional layers, both with batch normalization
        self.conv1 = nn.Conv2d(n_filters, n_filters, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(n_filters)
        self.conv2 = nn.Conv2d(n_filters, n_filters, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(n_filters)
        
    def forward(self, x):
        # Pass x through layers and add skip connection
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual
        x = F.relu(x)
        return x



# my_board = Board()
# state = my_board.create_new_board()
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# state = my_board.get_next_state(state, 3, 1)
# state = my_board.get_next_state(state, 2, -1)
# print(state)

# encoded_state = my_board.get_encoded_state(state)
# print(encoded_state)

# tensor_state = torch.tensor(encoded_state).unsqueeze(0)
# model = ResNet(device)

# policy, value = model(tensor_state)
# value = value.item()
# policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()

# print(value, policy)

# plt.bar(range(config.BOARD_COLUMNS), policy)
# plt.show()