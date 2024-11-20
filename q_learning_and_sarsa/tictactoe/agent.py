from abc import ABC, abstractmethod
import os
import pickle
import collections
import numpy as np
import random
from collections import defaultdict


class Learner(ABC):
    # Parent class for Q-learning and SARSA agents.
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))
        self.Q = {}
        for action in self.actions:
            self.Q[action] = collections.defaultdict(int)
        self.rewards = []

    def get_action(self, s):
        possible_actions = [a for a in self.actions if s[a[0]*3 + a[1]] == '-']
        if random.random() < self.eps:
            action = possible_actions[random.randint(0,len(possible_actions)-1)]
        else:
            values = np.array([self.Q[a][s] for a in possible_actions])
            ix_max = np.where(values == np.max(values))[0]
            if len(ix_max) > 1:
                ix_select = np.random.choice(ix_max, 1)[0]
            else:
                ix_select = ix_max[0]
            action = possible_actions[ix_select]
        self.eps *= (1.-self.eps_decay)
        return action

    def save(self, path):
        if os.path.isfile(path):
            os.remove(path)
        f = open(path, 'wb')
        pickle.dump(self, f)
        f.close()

    @abstractmethod
    def update(self, s, s_, a, a_, r):
        pass


class Qlearner(Learner):
    # A class to implement the Q-learning agent.
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def update(self, s, s_, a, a_, r):
        if s_ is not None:
            possible_actions = [action for action in self.actions if s_[action[0]*3 + action[1]] == '-']
            Q_options = [self.Q[action][s_] for action in possible_actions]
            self.Q[a][s] += self.alpha*(r + self.gamma*max(Q_options) - self.Q[a][s])
        else:
            self.Q[a][s] += self.alpha*(r - self.Q[a][s])
        self.rewards.append(r)


class SARSAlearner(Learner):
    # A class to implement the SARSA agent.
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def update(self, s, s_, a, a_, r):
        if s_ is not None:
            self.Q[a][s] += self.alpha*(r + self.gamma*self.Q[a_][s_] - self.Q[a][s])
        else:
            self.Q[a][s] += self.alpha*(r - self.Q[a][s])
        self.rewards.append(r)

class ValueIterationAgent(Learner):
    """
    Value Iteration agent for Tic-tac-toe.
    
    This agent uses the Value Iteration algorithm to compute the optimal policy
    for playing Tic-tac-toe. Unlike Q-learning and SARSA, this is a model-based
    approach that requires knowledge of state transitions and rewards.
    
    Parameters
    ----------
    gamma : float
        Discount factor for future rewards (default: 0.9)
    theta : float
        Convergence criterion - threshold for value function updates (default: 0.001)
    """
    
    def __init__(self, gamma=0.9, theta=0.001):
        # Note: We pass None for alpha and 0 for eps since VI doesn't use these
        super().__init__(alpha=None, gamma=gamma, eps=0, eps_decay=0)
        self.theta = theta
        
        # State values V(s)
        self.V = defaultdict(float)
        
        # Optimal policy π*(s) -> a
        self.policy = {}
        
        # Store rewards for visualization (inherited from Learner)
        self.rewards = []
        
        # Initialize possible actions (same as parent class)
        self.actions = [(i, j) for i in range(3) for j in range(3)]

    def get_state_value(self, state):
        """Get value of a state."""
        return self.V[state]

    def get_action(self, state):
        """
        Get the optimal action for the given state based on computed policy.
        
        Parameters
        ----------
        state : str
            Current game state representation
            
        Returns
        -------
        tuple
            (row, col) action to take
        """
        # If state not in policy (shouldn't happen after training), return random action
        if state not in self.policy:
            possible_actions = [a for a in self.actions if state[a[0]*3 + a[1]] == '-']
            if possible_actions:
                return possible_actions[np.random.randint(len(possible_actions))]
            return self.actions[0]  # Fallback
            
        return self.policy[state]

    def compute_value_iteration(self):
        """
        Run the value iteration algorithm to compute optimal value function and policy.
        """
        iteration = 0
        while True:
            delta = 0  # Keep track of maximum value change
            
            # Iterate through all states
            for state in self.get_all_states():
                old_value = self.V[state]
                
                # Skip terminal states (they have fixed values)
                if self.is_terminal_state(state):
                    continue
                
                # Compute new value using Bellman equation
                max_value = float('-inf')
                for action in self.get_valid_actions(state):
                    value = 0
                    # Consider all possible next states
                    next_state = self.get_next_state(state, action)
                    reward = self.get_reward(state, action, next_state)
                    value = reward + self.gamma * self.V[next_state]
                    max_value = max(max_value, value)
                
                # Update state value
                self.V[state] = max_value
                
                # Update maximum change
                delta = max(delta, abs(old_value - self.V[state]))
            
            iteration += 1
            
            # Check convergence
            if delta < self.theta:
                break
        
        # Compute optimal policy after value iteration converges
        self.compute_policy()
        
        return iteration

    def compute_policy(self):
        """
        Compute optimal policy based on the computed value function.
        """
        for state in self.get_all_states():
            if self.is_terminal_state(state):
                continue
                
            best_action = None
            best_value = float('-inf')
            
            # For each action, compute expected value
            for action in self.get_valid_actions(state):
                next_state = self.get_next_state(state, action)
                value = self.get_reward(state, action, next_state) + \
                       self.gamma * self.V[next_state]
                
                if value > best_value:
                    best_value = value
                    best_action = action
            
            self.policy[state] = best_action

    def is_terminal_state(self, state):
        """
        Check if the given state is terminal (game over).
        To be implemented.
        """
        # Check for wins
        for i in range(3):
            # Check rows
            if state[i*3:(i+1)*3] in ['XXX', 'OOO']:
                return True
            # Check columns
            if state[i] + state[i+3] + state[i+6] in ['XXX', 'OOO']:
                return True
        
        # Check diagonals
        if state[0] + state[4] + state[8] in ['XXX', 'OOO']:
            return True
        if state[2] + state[4] + state[6] in ['XXX', 'OOO']:
            return True
        
        # Check for draw (no empty spaces)
        if '-' not in state:
            return True
            
        return False

    def get_valid_actions(self, state):
        """
        Get list of valid actions for the given state.
        """
        return [(i//3, i%3) for i in range(9) if state[i] == '-']

    def get_next_state(self, state, action):
        """
        Get the next state after taking an action.
        Returns the state string after applying the action.
        """
        pos = action[0] * 3 + action[1]
        return state[:pos] + 'X' + state[pos+1:]

    def get_reward(self, state, action, next_state):
        """
        Get the reward for taking an action in a state.
        Returns:
            1.0 for a win
            0.0 for a draw
            -1.0 for a loss
            Small negative value for non-terminal moves to encourage shorter paths
        """
        if self.is_terminal_state(next_state):
            if self.check_win(next_state, 'X'):
                return 1.0
            elif self.check_win(next_state, 'O'):
                return -1.0
            else:
                return 0.0  # Draw
        return -0.01  # Small negative reward for non-terminal moves

    def check_win(self, state, player):
        """Check if the specified player has won."""
        win_patterns = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]            # Diagonals
        ]
        
        for pattern in win_patterns:
            if all(state[i] == player for i in pattern):
                return True
        return False

    def get_all_states(self):
        """
        Generate all possible game states.
        This is a simplified version - you might want to optimize this.
        """
        states = set()
        states.add('-' * 9)  # Empty board
        
        # Generate states (this is a simplified version)
        # In practice, you'd want to generate only valid game states
        for i in range(9):
            new_states = set()
            for state in states:
                if state[i] == '-':
                    new_states.add(state[:i] + 'X' + state[i+1:])
                    new_states.add(state[:i] + 'O' + state[i+1:])
            states.update(new_states)
        
        return states

    def update(self, s, s_, a, a_, r):
        """
        Required by parent class but not used in Value Iteration.
        Value Iteration is model-based and doesn't use online updates.
        """
        pass

class PolicyIterationAgent(Learner):
    """
    Policy Iteration agent for Tic-tac-toe.
    
    This agent uses the Policy Iteration algorithm to compute the optimal policy
    for playing Tic-tac-toe. Like Value Iteration, this is a model-based
    approach that requires knowledge of state transitions and rewards.
    
    Parameters
    ----------
    gamma : float
        Discount factor for future rewards (default: 0.9)
    theta : float
        Convergence criterion - threshold for value function updates (default: 0.001)
    """
    
    def __init__(self, gamma=0.9, theta=0.001):
        # Note: We pass None for alpha and 0 for eps since PI doesn't use these
        super().__init__(alpha=None, gamma=gamma, eps=0, eps_decay=0)
        self.theta = theta
        
        # State values V(s)
        self.V = defaultdict(float)
        
        # Current policy π(s) -> a
        self.policy = {}
        
        # Store rewards for visualization (inherited from Learner)
        self.rewards = []
        
        # Initialize possible actions (same as parent class)
        self.actions = [(i, j) for i in range(3) for j in range(3)]

    def get_action(self, state):
        """
        Get the optimal action for the given state based on computed policy.
        
        Parameters
        ----------
        state : str
            Current game state representation
            
        Returns
        -------
        tuple
            (row, col) action to take
        """
        # If state not in policy (shouldn't happen after training), return random action
        if state not in self.policy:
            possible_actions = [a for a in self.actions if state[a[0]*3 + a[1]] == '-']
            if possible_actions:
                return possible_actions[np.random.randint(len(possible_actions))]
            return self.actions[0]  # Fallback
            
        return self.policy[state]

    def compute_policy_iteration(self):
        """
        Run the policy iteration algorithm to compute optimal policy.
        Returns the number of iterations taken to converge.
        """
        iteration = 0
        
        # Initialize random policy
        for state in self.get_all_states():
            if not self.is_terminal_state(state):
                valid_actions = self.get_valid_actions(state)
                if valid_actions:
                    self.policy[state] = valid_actions[np.random.randint(len(valid_actions))]
        
        while True:
            iteration += 1
            
            # 1. Policy Evaluation
            self.policy_evaluation()
            
            # 2. Policy Improvement
            policy_stable = self.policy_improvement()
            
            # 3. Check if policy has converged
            if policy_stable:
                break
                
        return iteration

    def policy_evaluation(self):
        """
        Evaluate current policy until convergence.
        """
        while True:
            delta = 0
            # Iterate through all states
            for state in self.get_all_states():
                if self.is_terminal_state(state):
                    continue
                    
                old_value = self.V[state]
                
                # Get action from current policy
                action = self.policy.get(state)
                if action is None:
                    continue
                
                # Compute new value based on current policy
                next_state = self.get_next_state(state, action)
                reward = self.get_reward(state, action, next_state)
                self.V[state] = reward + self.gamma * self.V[next_state]
                
                # Track maximum change in value
                delta = max(delta, abs(old_value - self.V[state]))
            
            # Check if value function has converged
            if delta < self.theta:
                break

    def policy_improvement(self):
        """
        Improve policy for all states and check if policy is stable.
        Returns True if policy is stable (no changes made).
        """
        policy_stable = True
        
        for state in self.get_all_states():
            if self.is_terminal_state(state):
                continue
                
            old_action = self.policy.get(state)
            
            # Find best action under current values
            best_action = None
            best_value = float('-inf')
            
            for action in self.get_valid_actions(state):
                next_state = self.get_next_state(state, action)
                value = self.get_reward(state, action, next_state) + \
                       self.gamma * self.V[next_state]
                       
                if value > best_value:
                    best_value = value
                    best_action = action
            
            if best_action is not None:
                self.policy[state] = best_action
            
            if old_action != best_action:
                policy_stable = False
                
        return policy_stable

    def is_terminal_state(self, state):
        """
        Check if the given state is terminal (game over).
        """
        # Check for wins
        for i in range(3):
            # Check rows
            if state[i*3:(i+1)*3] in ['XXX', 'OOO']:
                return True
            # Check columns
            if state[i] + state[i+3] + state[i+6] in ['XXX', 'OOO']:
                return True
        
        # Check diagonals
        if state[0] + state[4] + state[8] in ['XXX', 'OOO']:
            return True
        if state[2] + state[4] + state[6] in ['XXX', 'OOO']:
            return True
        
        # Check for draw (no empty spaces)
        if '-' not in state:
            return True
            
        return False

    def get_valid_actions(self, state):
        """
        Get list of valid actions for the given state.
        """
        return [(i//3, i%3) for i in range(9) if state[i] == '-']

    def get_next_state(self, state, action):
        """
        Get the next state after taking an action.
        Returns the state string after applying the action.
        """
        pos = action[0] * 3 + action[1]
        return state[:pos] + 'X' + state[pos+1:]

    def get_reward(self, state, action, next_state):
        """
        Get the reward for taking an action in a state.
        Returns:
            1.0 for a win
            0.0 for a draw
            -1.0 for a loss
            Small negative value for non-terminal moves to encourage shorter paths
        """
        if self.is_terminal_state(next_state):
            if self.check_win(next_state, 'X'):
                return 1.0
            elif self.check_win(next_state, 'O'):
                return -1.0
            else:
                return 0.0  # Draw
        return -0.01  # Small negative reward for non-terminal moves

    def check_win(self, state, player):
        """Check if the specified player has won."""
        win_patterns = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]            # Diagonals
        ]
        
        for pattern in win_patterns:
            if all(state[i] == player for i in pattern):
                return True
        return False

    def get_all_states(self):
        """
        Generate all possible game states.
        This is a simplified version - you might want to optimize this.
        """
        states = set()
        states.add('-' * 9)  # Empty board
        
        # Generate states (this is a simplified version)
        # In practice, you'd want to generate only valid game states
        for i in range(9):
            new_states = set()
            for state in states:
                if state[i] == '-':
                    new_states.add(state[:i] + 'X' + state[i+1:])
                    new_states.add(state[:i] + 'O' + state[i+1:])
            states.update(new_states)
        
        return states

    def update(self, s, s_, a, a_, r):
        """
        Required by parent class but not used in Policy Iteration.
        Policy Iteration is model-based and doesn't use online updates.
        """
        pass
  