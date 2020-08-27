import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import torch.optim as optim
import copy

class AI(object):
  def __init__(self, discount=0.95, buffer_size=10000, batch_size=32, nbatches=10, epsilon=0.05):
    self.pred_network = Net()
    self.targ_network = Net()
    self.replay_buffer = []
    self.epsilon = epsilon
    self.buffer_size = buffer_size
    self.nbatches = nbatches
    self.batch_size = batch_size
    self.discount = discount

    self.criterion = nn.MSELoss()
    self.optimizer = optim.Adam(self.pred_network.parameters(), lr=0.0001)

  def to_tensor_state(self, state):
    return torch.Tensor([[state]])

  def index_to_action(self, idx):
    actions = [1, 0, -1]
    return actions[idx]

  def action_to_index(self, a):
    indexes = [1, 0, 2]
    return indexes[a]

  def action(self, state): # 1 for left, 0 for nothing, -1 for right
    out = self.pred_network(self.to_tensor_state(state))

    if np.random.uniform() < self.epsilon:
      action_idx = np.random.randint(0, out.size()[1])
    else:
      action_idx = out.max(1)[1][0]

    return self.index_to_action(action_idx)

  def store_transition(self, state, action, reward, next_state, terminal):
    self.replay_buffer.append((torch.Tensor([state]),
                              action, reward,
                              torch.Tensor([next_state]),
                              terminal))
    if len(self.replay_buffer) > self.buffer_size:
      self.replay_buffer = self.replay_buffer[1:]

  def extract_learning_base(self):
    indexes = np.random.choice(range(len(self.replay_buffer)), self.batch_size * self.nbatches)
    lb = [self.replay_buffer[i] for i in indexes]

    X = torch.split(torch.stack([t[0] for t in lb]), self.batch_size)
    a = torch.split(torch.tensor([t[1] for t in lb]), self.batch_size)
    r = torch.split(torch.tensor([t[2] for t in lb]), self.batch_size)
    Xn = torch.split(torch.stack([t[3] for t in lb]), self.batch_size)
    nt = torch.split(torch.tensor([not t[4] for t in lb]), self.batch_size)

    return X, a, r, Xn, nt

  def experience_replay(self):
    X, a, r, Xn, nt = self.extract_learning_base()
    
    for i,xbatch in enumerate(X):
      abatch = a[i]
      idxbatch = torch.tensor([self.action_to_index(a) for a in abatch])

      rbatch = r[i]
      tbatch = nt[i].int()
      Xnbatch = Xn[i]
      targets = rbatch + self.discount * self.targ_network(Xnbatch).max(1)[0] * tbatch
      
      self.optimizer.zero_grad()
      outputs = self.pred_network(xbatch)
      predicted = outputs[torch.arange(outputs.size(0)), idxbatch]
      
      loss = self.criterion(predicted, targets)
      loss.backward()
      self.optimizer.step()

  def transfer_to_target_network(self):
    self.targ_network = copy.deepcopy(self.pred_network)


class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.conv1 = nn.Conv2d(1, 3, 3)
    # self.pool = nn.MaxPool2d(4, 4)
    self.conv2 = nn.Conv2d(3, 6, 3)
    self.pool2 = nn.MaxPool2d(2, 2)
    self.conv3 = nn.Conv2d(6, 9, 3)
    self.conv4 = nn.Conv2d(9, 12, 3)
    self.fc1 = nn.Linear(12 * 23 * 35, 84)
    self.fc2 = nn.Linear(84, 3)

  def forward(self, x):
    x = self.pool2(F.relu(self.conv1(x)))
    x = self.pool2(F.relu(self.conv2(x)))
    x = self.pool2(F.relu(self.conv3(x)))
    x = self.pool2(F.relu(self.conv4(x)))
    x = x.view(-1, 12 * 23 * 35)
    x = F.relu(self.fc1(x))
    x = self.fc2(x)
    return x