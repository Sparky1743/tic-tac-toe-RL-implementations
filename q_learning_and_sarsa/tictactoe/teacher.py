import random

class Teacher:

    def __init__(self, level=0.9):
        self.ability_level = level

    def win(self, board, key='X'):
        for i in range(3):
            row = [board[i][0], board[i][1], board[i][2]]
            col = [board[0][i], board[1][i], board[2][i]]
            if row.count(key) == 2 and row.count('-') == 1:
                return i, row.index('-')
            if col.count(key) == 2 and col.count('-') == 1:
                return col.index('-'), i

        diag1 = [board[0][0], board[1][1], board[2][2]]
        diag2 = [board[0][2], board[1][1], board[2][0]]
        if diag1.count(key) == 2 and diag1.count('-') == 1:
            return diag1.index('-'), diag1.index('-')
        if diag2.count(key) == 2 and diag2.count('-') == 1:
            return diag2.index('-'), 2 - diag2.index('-')

        return None

    def blockWin(self, board):
        return self.win(board, key='O')

    def fork(self, board):
        for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if board[i][j] == '-' and (
                (board[1][0] == 'X' and board[1][2] == 'X') or 
                (board[0][1] == 'X' and board[2][1] == 'X') or 
                (board[1][1] == 'X')
            ):
                return i, j
        return None

    def blockFork(self, board):
        return self.fork(board)

    def center(self, board):
        if board[1][1] == '-':
            return 1, 1
        return None

    def corner(self, board):
        for i, j in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if board[i][j] == '-':
                return i, j
        return None

    def sideEmpty(self, board):
        for i, j in [(0, 1), (1, 0), (1, 2), (2, 1)]:
            if board[i][j] == '-':
                return i, j
        return None

    def randomMove(self, board):
        possibles = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '-']
        return random.choice(possibles)

    def makeMove(self, board):
        if random.random() > self.ability_level:
            return self.randomMove(board)

        move = self.win(board)
        if move: return move
        move = self.blockWin(board)
        if move: return move
        move = self.fork(board)
        if move: return move
        move = self.blockFork(board)
        if move: return move
        move = self.center(board)
        if move: return move
        move = self.corner(board)
        if move: return move
        move = self.sideEmpty(board)
        if move: return move

        return self.randomMove(board)
