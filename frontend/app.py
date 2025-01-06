# frontend/app.py
from flask import Flask, Response, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import logging

# Add both project root and backend to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'backend'))

from tictactoe.game import Game, getStateKey
from tictactoe.agent import Qlearner, SARSAlearner, ValueIterationAgent, PolicyIterationAgent
from tictactoe.teacher import Teacher
from play import GameLearning  # Import GameLearning class
import pickle

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Add secret key for SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for WebSocket

# Load agents
def load_agent(agent_type):
    """Load or create a new agent"""
    path = os.path.join(PROJECT_ROOT, 'backend', 
                       'q_agent.pkl' if agent_type == 'q' else 'sarsa_agent.pkl' if agent_type == 's' else 'v_agent.pkl' if agent_type == 'v' else 'p_agent.pkl')
    try:
        if os.path.isfile(path):
            logger.debug(f"Loading agent from {path}")
            with open(path, 'rb') as f:
                return pickle.load(f)
    except Exception as e:
        logger.warning(f"Could not load agent: {e}")
    
    logger.debug(f"Creating new {agent_type} agent")
    if agent_type == 'q':
        return Qlearner(0.5, 0.9, 0.1)
    elif agent_type == 's':
        return SARSAlearner(0.5, 0.9, 0.1)
    elif agent_type == 'v':
        agent = ValueIterationAgent(gamma=0.9)
        agent.compute_value_iteration()
        return agent
    elif agent_type == 'p':
        agent = PolicyIterationAgent(gamma=0.9)
        agent.compute_policy_iteration()
        return agent
    else:
        raise ValueError("Unknown agent type")

current_game = None

@app.route('/')
def index():
    try:
        global current_game
        current_game = Game(load_agent("q"))
        return render_template('game.html')
    except Exception as e:
        logger.error(f"Error rendering game page: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/train')
def train():
    try:
        return render_template('train.html')
    except Exception as e:
        logger.error(f"Error rendering train page: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/rewards')
def rewards():
    return render_template('rewards.html')

@socketio.on('player_move')
def handle_move(data):
    try:
        logger.debug(f"Received player move: {data}")
        global current_game
        if current_game is None:
            logger.debug("Creating new game")
            current_game = Game(load_agent(data['agent']))
        
        # Process player move
        row, col = data['row'], data['col']
        logger.debug(f"Player move at position ({row}, {col})")
        current_game.board[row][col] = 'X'
        
        # print(current_game.checkForEnd('X'))
        if current_game.checkForEnd('X') == 1:
            emit('agent_move', {
                'game_over': True,
                'winner': 'X',
                'message': 'You win!'
            })
            return
        elif current_game.checkForDraw():
            emit('agent_move', {
                'game_over': True,
                'winner': None,
                'message': "It's a draw!"
            })
            return
        
        # Get agent move
        state = getStateKey(current_game.board)  # Use the imported function
        action = current_game.agent.get_action(state)
        current_game.agentMove(action)
        
        response = {
            'row': action[0],
            'col': action[1],
            'game_over': False
        }
        
        if current_game.checkForEnd('O') == 1:
            response.update({
                'game_over': True,
                'winner': 'O',
                'message': 'Agent wins!'
            })
        elif current_game.checkForDraw():
            response.update({
                'game_over': True,
                'winner': None,
                'message': "It's a draw!"
            })
            
        emit('agent_move', response)
        
    except Exception as e:
        logger.error(f"Error in handle_move: {str(e)}")
        emit('error', {'message': str(e)})

@socketio.on('new_game')
def new_game(data):
    global current_game
    current_game = Game(load_agent(data['agent']))
    emit('game_reset')

@socketio.on('start_training')
def handle_training(data):
    try:
        logger.debug(f"Starting training with parameters: {data}")
        agent_type = data['agent_type']
        method = data.get('method', None)
        episodes = data.get('episodes', None)
        load_existing = data.get('load_existing', False)
        
        # Prepare arguments for GameLearning
        class Args:
            def __init__(self, agent_type, path, load, teacher_episodes):
                self.agent_type = agent_type
                self.path = path
                self.load = load
                self.teacher_episodes = teacher_episodes
        
        args = Args(
            agent_type=agent_type,
            path=os.path.join(PROJECT_ROOT, 'backend', f'{"sarsa" if agent_type=="s" else agent_type }_agent.pkl'),
            load=load_existing,
            teacher_episodes=episodes if method == 'teacher' else None
        )
        
        # Initialize GameLearning
        game_learning = GameLearning(args)
        
        if method == 'teacher' and (agent_type == 'q' or agent_type == 's'):
            game_learning.beginTeaching(episodes)
        else:
            game_learning.beginSelfPlay(episodes)
        
        emit('training_complete')
        
    except Exception as e:
        logger.error(f"Error in training: {str(e)}")
        emit('training_error', {'message': str(e)})

@app.route('/get_rewards/<agent_type>')
def get_rewards(agent_type):
    try:
        logger.debug(f"Fetching rewards for agent type: {agent_type}")
        agent = load_agent(agent_type)
        if not agent.rewards:
            return jsonify({'error': 'No rewards data available'})
        
        # Plot in memory
        plt.figure(figsize=(10, 6))
        plt.plot(np.cumsum(agent.rewards))
        plt.title('Agent Cumulative Reward vs. Episode')
        plt.xlabel('Episode')
        plt.ylabel('Cumulative Reward')
        
        # Save plot to memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        
        # Return image directly as response
        return Response(buf.getvalue(), mimetype='image/png')
    
    except Exception as e:
        logger.error(f"Error getting rewards: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True)