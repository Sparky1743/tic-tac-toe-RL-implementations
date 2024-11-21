# Tic-Tac-Toe Reinforcement Learning Project

This project implements various reinforcement learning agents to play the game of Tic-Tac-Toe. The agents use algorithms such as Q-Learning, SARSA, Value Iteration, and Policy Iteration to learn optimal strategies through self-play and interaction with human players. A web interface is provided for easy interaction with the agents, allowing users to play against them, train them, and visualize their learning progress.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Using the Web Interface](#using-the-web-interface)
    - [Play Against the AI Agents](#play-against-the-ai-agents)
    - [Train the Agents](#train-the-agents)
    - [View Agent Rewards](#view-agent-rewards)
- [Project Structure](#project-structure)
- [Agents Implemented](#agents-implemented)
- [Using Terminal](#using-terminal)
    - [Manual Training](#manual-training)
    - [Training with a Teacher](#training-with-a-teacher)
    - [Self-Play Training](#self-play-training)
    - [Loading and Continuing Training](#loading-and-continuing-training)
    - [Playing](#playing)
    - [Plotting Rewards](#plotting-rewards)
- [License](#license)

## Features

- **Play Tic-Tac-Toe**: Play against AI agents powered by reinforcement learning algorithms directly in your browser.
- **Train Agents**: Train the agents using different algorithms and methods through the web interface.
- **Visualize Rewards**: View the cumulative rewards of the agents to understand their learning progress.
- **Multiple Algorithms**: Supports Q-Learning, SARSA, Value Iteration, and Policy Iteration agents.
- **Interactive Web Interface**: User-friendly web interface built with Flask and Socket.IO.
- **Self-Play Training**: Agents can train by playing against themselves, accelerating the learning process.

## Getting Started

### Prerequisites

- **Python 3.6 or higher**
- **pip** package manager

### Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/Sparky1743/tic-tac-toe-RL-implementations
    cd tic-tac-toe-RL-implementations
    ```

2. **Install Required Packages**

    Install the necessary Python packages using `pip`:

    ```sh
    pip install -r requirements.txt
    ```

    Ensure that the `requirements.txt` file includes all necessary dependencies, such as `Flask`, `Flask-SocketIO`, `NumPy`, `Matplotlib`, etc.

## Using the Web Interface

To interact with the agents using the web interface, follow these steps:

1. **Run the Flask Application**

    Navigate to the `frontend` directory and start the Flask app:

    ```sh
    cd frontend
    python app.py
    ```

    The server will start running at `http://localhost:5000`.

2. **Access the Web Interface**

    Open your web browser and go to `http://localhost:5000` to access the main page.

### Play Against the AI Agents

1. **Navigate to the Play Page**

    From the homepage or navigation bar, select the **Play** option.

2. **Select an Agent**

    Use the dropdown menu to select the type of agent you want to play against:

    - **Q-Learning Agent**
    - **SARSA Agent**
    - **Value Iteration Agent**
    - **Policy Iteration Agent**

3. **Start Playing**

    Click on the cells to make your move. You are 'X', and the AI agent is 'O'. The game status will be displayed above the board.

4. **Start a New Game**

    Click the **New Game** button to reset the board and play again.

### Train the Agents

1. **Navigate to the Train Page**

    Click on the **Train** option in the navigation bar.

2. **Select Agent Type**

    Choose the agent you want to train:

    - **Q-Learning**
    - **SARSA**
    - **Value Iteration**
    - **Policy Iteration**

3. **Configure Training Parameters**

    For **Q-Learning** and **SARSA** agents:

    - **Training Method**: Choose between **Teacher Training** and **Self-Play Training**.
    - **Training Episodes**: Enter the number of episodes for training (e.g., 5000).
    - **Load Existing Agent**: Check this box to continue training an existing agent.

    For **Value Iteration** and **Policy Iteration** agents:

    - No additional parameters are needed as these are model-based methods.

4. **Start Training**

    Click the **Start Training** button. Training progress will be displayed, and a status message will inform you when training is complete.

### View Agent Rewards

1. **Navigate to the Rewards Page**

    Select the **Rewards** option from the navigation bar.

2. **Select an Agent**

    Choose the agent whose rewards you want to view from the dropdown menu.

3. **View Rewards Plot**

    A plot of the cumulative rewards versus episodes will be displayed, showing the agent's learning progress.

## Project Structure

```
tic-tac-toe-RL-implementations/
├── frontend/
│   ├── app.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── game.js
│   │       ├── rewards.js
│   │       └── train.js
│   ├── templates/
│   │   ├── base.html
│   │   ├── game.html
│   │   ├── rewards.html
│   │   └── train.html
├── backend/
│   ├── play.py
│   ├── plot_agent_reward.py
│   └── tictactoe/
│       ├── agent.py
│       ├── game.py
│       └── teacher.py
├── LICENSE
├── README.md
└── requirements.txt
```

## Agents Implemented

- **Q-Learning Agent**: Learns the optimal policy by maximizing the expected value of the total reward over any and all successive steps, starting from the current state.
- **SARSA Agent**: On-policy algorithm that updates the Q-value based on the action actually taken.
- **Value Iteration Agent**: Computes the optimal state-value function by iteratively improving the estimate of V(s).
- **Policy Iteration Agent**: Iteratively evaluates and improves a policy until reaching the optimal policy.

## Using Terminal 

### Playing

To play against a trained agent, use the `--load` option to load the trained model:

- **Q-Learning**:
        ```sh
        python backend/play.py -a q --path q_agent.pkl --load
        ```

- **SARSA**:
        ```sh
        python backend/play.py -a s --path sarsa_agent.pkl --load
        ```

- **Value Iteration**:
        ```sh
        python backend/play.py -a v --path v_agent.pkl --load
        ```

- **Policy Iteration**:
        ```sh
        python backend/play.py -a p --path p_agent.pkl --load
        ```

In this mode, the game will proceed interactively, and you will play against the agent. The agent will make decisions based on its learned strategy.

### Manual Training

When training an agent manually, you can specify a path to save the agent's state using the `-p` option:

- **Q-Learning**:
        ```sh
        python backend/play.py -a q -p my_agent_path.pkl
        ```

- **SARSA**:
        ```sh
        python backend/play.py -a s -p my_agent_path.pkl
        ```

### Training with a Teacher

You can also train an agent automatically using a teacher agent. This is done by specifying the `-t` option followed by the number of training episodes:

- **Q-Learning**:
        ```sh
        python backend/play.py -a q -t 5000
        ```

- **SARSA**:
        ```sh
        python backend/play.py -a s -t 5000
        ```

This will train the agent automatically and save its progress to the specified pickle file.

### Self-Play Training

Agents can also be trained through self-play, where they play against themselves to improve their strategies. This is done by specifying the `--self-play` option followed by the number of training episodes:

- **Q-Learning**:
        ```sh
        python backend/play.py -a q --self-play 5000
        ```

- **SARSA**:
        ```sh
        python backend/play.py -a s --self-play 5000
        ```

This method allows agents to learn by playing against themselves, accelerating the learning process.

### Loading and Continuing Training

To load an existing agent and continue training, use the `-l` option:

- **Q-Learning** (load and train manually):
        ```sh
        python backend/play.py -a q -l
        ```

- **SARSA** (load and train manually):
        ```sh
        python backend/play.py -a s -l
        ```

You can also continue training with a teacher:

- **Q-Learning** (load and train with teacher):
        ```sh
        python backend/play.py -a q -l -t 5000
        ```

- **SARSA** (load and train with teacher):
        ```sh
        python backend/play.py -a s -l -t 5000
        ```

The agent will continue learning and its state will be saved, overwriting the previous pickle file.

### Plotting Rewards

To plot the cumulative rewards of a trained agent, use the `plot_agent_reward.py` script:

```sh
python backend/plot_agent_reward.py -p q_agent.pkl
```

