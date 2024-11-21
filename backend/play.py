import argparse
import os
import pickle
import sys

from tictactoe.agent import Qlearner, SARSAlearner, ValueIterationAgent, PolicyIterationAgent
from tictactoe.teacher import Teacher
from tictactoe.game import Game


class GameLearning(object):
    def __init__(self, args, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.agent_type = args.agent_type
        self.path = args.path
        self.load = args.load
        self.teacher_episodes = args.teacher_episodes
        self.agent = self.load_or_create_agent(alpha, gamma, epsilon)
        self.games_played = 0

    def load_or_create_agent(self, alpha, gamma, epsilon):
        if self.load:
            if not os.path.isfile(self.path):
                raise ValueError("Cannot load agent: file does not exist.")
            with open(self.path, 'rb') as f:
                return pickle.load(f)
        else:
            if os.path.isfile(self.path):
                print(f'An agent is already saved at {self.path}.')
            if self.agent_type == "q":
                return Qlearner(alpha, gamma, epsilon)
            elif self.agent_type == "s":
                return SARSAlearner(alpha, gamma, epsilon)
            elif self.agent_type == "v":
                agent = ValueIterationAgent(gamma=gamma)
                print("Computing optimal policy using Value Iteration...")
                agent.compute_value_iteration()
                print("Done!")
                return agent
            elif self.agent_type == "p":
                agent = PolicyIterationAgent(gamma=gamma)
                print("Computing optimal policy using Policy Iteration...")
                agent.compute_policy_iteration()
                print("Done!")
                return agent
            else:
                raise ValueError("Unknown agent type")

    def beginPlaying(self):
        print("Welcome to Tic-Tac-Toe. You are 'X' and the computer is 'O'.")

        def play_again():
            print(f"Games played: {self.games_played}")
            while True:
                play = input("Do you want to play again? [y/n]: ")
                if play.lower() in ['y', 'yes']:
                    return True
                elif play.lower() in ['n', 'no']:
                    return False
                else:
                    print("Invalid input. Please choose 'y' or 'n'.")

        while True:
            game = Game(self.agent)
            game.start()
            self.games_played += 1
            self.agent.save(self.path)
            if not play_again():
                print("OK. Quitting.")
                break

    def beginTeaching(self, episodes):
        teacher = Teacher()
        while self.games_played < episodes:
            game = Game(self.agent, player=teacher, player_type='teacher')
            game.start()
            self.games_played += 1
            if self.games_played % 1000 == 0:
                print(f"Games played: {self.games_played}")
        
        self.agent.save(self.path)

    def beginSelfPlay(self, episodes):
        while self.games_played < episodes:
            game = Game(self.agent, self.agent, player_type='agent')
            game.start()
            self.games_played += 1
            if self.games_played % 1000 == 0:
                print(f"Games played: {self.games_played}")
        self.agent.save(self.path)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe.")
    parser.add_argument("-a", "--agent", type=str, choices=['q', 's', 'v', 'p'], 
                        default='q', help="Agent type (q=Q-Learning, s=SARSA, v=Value Iteration, p=Policy Iteration)")
    parser.add_argument("-p", "--path", type=str, required=False,
                        help="Specify the path for the agent pickle file.")
    parser.add_argument("-l", "--load", action="store_true",
                        help="whether to load trained agent")
    parser.add_argument("-t", "--teacher_episodes", default=None, type=int,
                        help="employ teacher agent who knows the optimal strategy")
    parser.add_argument("--self-play", default=None, type=int,
                        help="number of episodes for self-play training")

    args = parser.parse_args()

    if args.path is None:
        args.path = 'q_agent.pkl' if args.agent == 'q' else 'sarsa_agent.pkl' if args.agent == 's' else 'v_agent.pkl' if args.agent == 'v' else 'p_agent.pkl' 

    gl = GameLearning(args)

    if args.teacher_episodes is not None:
        gl.beginTeaching(args.teacher_episodes)
    elif args.self_play is not None:
        gl.beginSelfPlay(args.self_play)
    else:
        gl.beginPlaying()