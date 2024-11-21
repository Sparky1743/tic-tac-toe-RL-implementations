import random


class Game:
    """ The game class. New instance created for each new game. """
    def __init__(self, agent, player=None, player_type=None):
        self.agent = agent
        self.player = player
        self.player_type = player_type
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def playerMove(self):
        
        if self.player is None:
            printBoard(self.board)
            while True:
                move = input("Your move! Please select a row and column from 0-2 "
                             "in the format row,col: ")
                print('\n')
                try:
                    row, col = int(move[0]), int(move[2])
                except ValueError:
                    print("INVALID INPUT! Please use the correct format.")
                    continue
                if row not in range(3) or col not in range(3) or not self.board[row][col] == '-':
                    print("INVALID MOVE! Choose again.")
                    continue
                self.board[row][col] = 'X'
                break

        elif self.player_type == "teacher":
            action = self.player.makeMove(self.board)
            self.board[action[0]][action[1]] = 'X'
        else: # self.player_type == "agent"
            state = getStateKey(self.board)
            action = self.player.get_action(state)
            self.board[action[0]][action[1]] = 'X'


    def agentMove(self, action):
        self.board[action[0]][action[1]] = 'O'

    def checkForWin(self, key):
        a = [self.board[0][0], self.board[1][1], self.board[2][2]]
        b = [self.board[0][2], self.board[1][1], self.board[2][0]]
        if a.count(key) == 3 or b.count(key) == 3:
            return True
        for i in range(3):
            col = [self.board[0][i], self.board[1][i], self.board[2][i]]
            row = [self.board[i][0], self.board[i][1], self.board[i][2]]
            if col.count(key) == 3 or row.count(key) == 3:
                return True
        return False

    def checkForDraw(self):
        draw = True
        for row in self.board:
            for elt in row:
                if elt == '-':
                    draw = False
        return draw

    def checkForEnd(self, key):
        if self.checkForWin(key):
            if self.agent is None:
                printBoard(self.board)
                if key == 'X':
                    print("Player wins!")
                else:
                    print("RL agent wins!")
            return 1
        elif self.checkForDraw():
            if self.agent is None:
                printBoard(self.board)
                print("It's a draw!")
            return 0
        return -1

    def playGame(self, player_first):
        if player_first:
            self.playerMove()
        prev_state = getStateKey(self.board)
        prev_action = self.agent.get_action(prev_state)

        while True:
            self.agentMove(prev_action)
            check = self.checkForEnd('O')
            if not check == -1:
                reward = check
                break
            self.playerMove()
            check = self.checkForEnd('X')
            if not check == -1:
                reward = -1*check
                break
            else:
                reward = 0
            new_state = getStateKey(self.board)
            new_action = self.agent.get_action(new_state)
            self.agent.update(prev_state, new_state, prev_action, new_action, reward)
            prev_state = new_state
            prev_action = new_action

        self.agent.update(prev_state, None, prev_action, None, reward)

    def start(self):
        if self.agent is not None:
            if random.random() < 0.5:
                self.playGame(player_first=False)
            else:
                self.playGame(player_first=True)
        else:
            while True:
                response = input("Would you like to go first? [y/n]: ")
                print('')
                if response == 'n' or response == 'no':
                    self.playGame(player_first=False)
                    break
                elif response == 'y' or response == 'yes':
                    self.playGame(player_first=True)
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

def printBoard(board):
    print('    0   1   2\n')
    for i, row in enumerate(board):
        print('%i   ' % i, end='')
        for elt in row:
            print('%s   ' % elt, end='')
        print('\n')

def getStateKey(board):
    key = ''
    for row in board:
        for elt in row:
            key += elt
    return key