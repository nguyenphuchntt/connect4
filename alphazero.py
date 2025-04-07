import numpy as np
import math
import random
import torch
import torch.nn as nn
import torch.nn.functional as F

import config
from board import Board
from resnet import ResNet
from mcts import MCTS

from tqdm.notebook import trange

class AlphaZero:
    def __init__(self, model, optimizer, board:Board):
        self.model = model
        self.optimizer = optimizer
        self.board = board
        self.mcts = MCTS(board, model)
        
    def selfPlay(self):
        "Perform one episode of self-play."
        memory = []
        player = 1
        state = self.board.reset()
        
        while True:
            neutral_state = state if player==1 else self.board.flip(state)
            action_probs = self.mcts.search(neutral_state)
            
            memory.append((state, action_probs, player))
            
            # The more the 'TEMPERATURE' get higher to infinity, the more random will the probs get
            # which mean we want to do the exploration
            # On the other hand if 'TEMPERATURE' got lower to zero, we will eventually get the max action of the prob
            # which mean we want to do the exploitation
            temperature_action_probs = action_probs ** (1 / config.TEMPERATURE)
            action = np.random.choice(config.ACTION_SIZE, p=temperature_action_probs/sum(temperature_action_probs))
            
            state = self.board.get_next_state(state, action, player)
            
            value = self.board.evaluate(state)
            is_terminal = self.board.is_terminal_node(state)

            if is_terminal:
                returnMemory = []
                for hist_neutral_state, hist_action_probs, hist_player in memory:
                    hist_outcome = value if hist_player == player else self.board.get_opponent_value(value)
                    returnMemory.append((
                        self.board.get_encoded_state(hist_neutral_state),
                        hist_action_probs,
                        hist_outcome
                    ))
                return returnMemory
            
            player *= -1
                
            
    
    def train(self, memory):
        "Train the AlphaZero agent for 1 epoch"
        random.shuffle(memory)
        for batchIdx in range(0, len(memory), config.BATCH_SIZE):
            sample = memory[batchIdx : min(batchIdx+config.BATCH_SIZE, len(memory)-1)]
            # Currently we have a tuple of (state, policy, value)
            # By using zip, we have a list of state, list of policy, list of target and transpose
            state, policy_targets, value_targets = zip(*sample)

            state = np.array(state)
            policy_targets = np.array(policy_targets)
            # We want each value to be its own subarray so change it into a 2darray with 1 column
            value_targets = np.array(value_targets).reshape(-1, 1)

            state = torch.tensor(state, dtype=torch.float32, device=self.model.device)
            policy_targets = torch.tensor(policy_targets, dtype=torch.float32, device=self.model.device)
            value_targets = torch.tensor(value_targets, dtype=torch.float32, device=self.model.device)

            # Getting the loss, we will try to minimize this value
            out_policy, out_value = self.model(state)
            policy_loss = F.cross_entropy(out_policy, policy_targets)
            value_loss = F.mse_loss(out_value, value_targets)
            loss = policy_loss + value_loss


            self.optimizer.zero_grad()  # Reset the gradient to 0 before calculate new gradient
            loss.backward()             # Calculate new gradient by using backpropagation
            self.optimizer.step()       # Update weights by optimizer (Adam)

    def learn(self):
        "Update the neural network"
        for iteration in range(config.N_ITER):
            memory = []
            
            # Some layer like BatchNorm will work stabilily without updating
            # We do this to stability maintain the selfPlay progress
            self.model.eval()
            for selfPlay_iteration in trange(config.N_SELFPLAY_ITER):
                memory += self.selfPlay()
                
            self.model.train()
            for epoch in trange(config.N_EPOCHS):
                self.train(memory)
            
            # Save weights
            torch.save(self.model.state_dict(), f"model_{iteration}.pt")
            # Save the state of optimizer
            torch.save(self.optimizer.state_dict(), f"optimizer_{iteration}.pt")



board = Board()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ResNet(device)
optimizer = torch.optim.Adam(model.parameters(), lr=config.LEANRING_RATE, weight_decay=config.WEIGHT_DECAY)

alphaZero = AlphaZero(model, optimizer, board)
alphaZero.learn()