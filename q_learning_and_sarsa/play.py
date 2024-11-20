import argparse
import os
import pickle
import sys

from tictactoe.agent import Qlearner, SARSAlearner, ValueIterationAgent, PolicyIterationAgent
from tictactoe.teacher import Teacher
from tictactoe.game import Game


class GameLearning(object):
    def __init__(self, args, alpha=0.5, gamma=0.9, epsilon=0.1):
        if args.load:
            if not os.path.isfile(args.path):
                raise ValueError("Cannot load agent: file does not exist.")
            with open(args.path, 'rb') as f:
                agent = pickle.load(f)
        else:
            if os.path.isfile(args.path):
                print('An agent is already saved at {}.'.format(args.path))
                while True:
                    response = input("Are you sure you want to overwrite? [y/n]: ")
                    if response.lower() in ['y', 'yes']:
                        break
                    elif response.lower() in ['n', 'no']:
                        print("OK. Quitting.")
                        sys.exit(0)
                    else:
                        print("Invalid input. Please choose 'y' or 'n'.")
            if args.agent_type == "q":
                agent = Qlearner(alpha, gamma, epsilon)
            else:
                agent = SARSAlearner(alpha, gamma, epsilon)

        self.games_played = 0
        self.path = args.path
        self.agent = agent

    def beginPlaying(self):
        print("Welcome to Tic-Tac-Toe. You are 'X' and the computer is 'O'.")

        def play_again():
            print("Games played: %i" % self.games_played)
            while True:
                play = input("Do you want to play again? [y/n]: ")
                if play == 'y' or play == 'yes':
                    return True
                elif play == 'n' or play == 'no':
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
            game = Game(self.agent, teacher=teacher)
            game.start()
            self.games_played += 1
            if self.games_played % 1000 == 0:
                print("Games played: %i" % self.games_played)
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

    args = parser.parse_args()

    # Handle Value Iteration agent differently since it doesn't need training
    if args.agent in ['v', 'p']:
        # Create appropriate agent
        if args.agent == 'v':
            agent = ValueIterationAgent(gamma=0.9)
            print("Computing optimal policy using Value Iteration...")
            agent.compute_value_iteration()
        else:
            agent = PolicyIterationAgent(gamma=0.9)
            print("Computing optimal policy using Policy Iteration...")
            agent.compute_policy_iteration()
            
        print("Done! Starting game...")
        print("\nWelcome to Tic-Tac-Toe. You are 'X' and the computer is 'O'.")
        
        while True:
            game = Game(agent)
            game.start()
            
            while True:
                play = input("Do you want to play again? [y/n]: ")
                if play.lower() in ['y', 'yes']:
                    break
                elif play.lower() in ['n', 'no']:
                    print("OK. Quitting.")
                    sys.exit(0)
                else:
                    print("Invalid input. Please choose 'y' or 'n'.")
    else:
        # Original code for Q-learning and SARSA agents
        if args.path is None:
            args.path = 'q_agent.pkl' if args.agent == 'q' else 'sarsa_agent.pkl'

        gl = GameLearning(args)

        if args.teacher_episodes is not None:
            gl.beginTeaching(args.teacher_episodes)
        else:
            gl.beginPlaying()   

 