# Tic-Tac-Toe Reinforcement Learning Implementations

This project implements reinforcement learning agents to play the game of Tic-Tac-Toe. The agents use Q-learning and SARSA algorithms to learn optimal strategies through self-play and interaction with a human player.

## Usage

### Manual Training

When training an agent manually, you can specify a path to save the agent's state using the `-p` option:

- **Q-learning**:
    ```sh
    python play.py -a q -p my_agent_path.pkl
    ```

- **SARSA**:
    ```sh
    python play.py -a s -p my_agent_path.pkl
    ```

If the file already exists, you will be prompted to overwrite it.

### Training with a Teacher

You can also train an agent automatically using a teacher agent. This is done by specifying the `-t` option followed by the number of training episodes:

- **Q-learning**:
    ```sh
    python play.py -a q -t 5000
    ```

- **SARSA**:
    ```sh
    python play.py -a s -t 5000
    ```

This will train the agent automatically and save its progress to the specified pickle file.

### Loading and Continuing Training

To load an existing agent and continue training, use the `-l` option:

- **Q-learning** (load and train manually):
    ```sh
    python play.py -a q -l
    ```

- **SARSA** (load and train manually):
    ```sh
    python play.py -a s -l
    ```

You can also continue training with a teacher:

- **Q-learning** (load and train with teacher):
    ```sh
    python play.py -a q -l -t 5000
    ```

- **SARSA** (load and train with teacher):
    ```sh
    python play.py -a s -l -t 5000
    ```

The agent will continue learning and its state will be saved, overwriting the previous pickle file.

### Playing

To play against a trained agent, use the `--load` option to load the trained model:

- **Q-learning**:
    ```sh
    python play.py -a q --path q_agent.pkl --load
    ```

- **SARSA**:
    ```sh
    python play.py -a s --path sarsa_agent.pkl --load
    ```

In this mode, the game will proceed interactively, and you will play against the agent. The agent will make decisions based on its learned strategy.

### Plotting Rewards

To plot the cumulative rewards of a trained agent, use the `plot_agent_reward.py` script:

```sh
python plot_agent_reward.py -p q_agent.pkl
