# Tic-Tac-Toe Reinforcement Learning Implementations

This project implements reinforcement learning agents to play the game of Tic-Tac-Toe. The agents use Q-learning and SARSA algorithms to learn optimal strategies through self-play and interaction with a human player.

## Usage

### Training

To train an agent using Q-learning or SARSA, run the `play.py` script with the appropriate arguments:

- Q-learning:
    ```sh
    python play.py -a q -t 10000
    ```

- SARSA:
    ```sh
    python play.py -a s -t 10000
    ```

The `-t` argument specifies the number of training episodes.

### Playing

To play against a trained agent, use the `--load` option to load the trained model:

- Q-learning:
    ```sh
    python play.py -a q --path q_agent.pkl --load
    ```

- SARSA:
    ```sh
    python play.py -a s --path sarsa_agent.pkl --load
    ```

### Plotting Rewards

To plot the cumulative rewards of a trained agent, use the `plot_agent_reward.py` script:

```sh
python plot_agent_reward.py -p q_agent.pkl
