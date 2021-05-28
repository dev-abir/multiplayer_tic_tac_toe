class Game:
    def __init__(self):
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]  # don't use [['-'] * 3] * 3
        self._last_character_turned = None

    def reset_board(self):
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def game_state(self):
        for i in range(0, 3):
            row_sum = ord(self.board[i][0]) + ord(self.board[i][1]) + ord(self.board[i][2])
            if (row_sum == (ord('x') * 3)) or (row_sum == (ord('o') * 3)):
                return 'w'  # won

            column_sum = ord(self.board[0][i]) + ord(self.board[1][i]) + ord(self.board[2][i])
            if (column_sum == (ord('x') * 3)) or (column_sum == (ord('o') * 3)):
                return 'w'  # won

        diagonal_sum = ord(self.board[0][0]) + ord(self.board[1][1]) + ord(self.board[2][2])
        if (diagonal_sum == (ord('x') * 3)) or (diagonal_sum == (ord('o') * 3)):
            return 'w'  # won
        diagonal_sum = ord(self.board[0][2]) + ord(self.board[1][1]) + ord(self.board[2][0])
        if (diagonal_sum == (ord('x') * 3)) or (diagonal_sum == (ord('o') * 3)):
            return 'w'  # won

        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == '-':
                    return  # ongoing

        return 'd'  # draw

    def add_turn_internal(self, character, posX, posY):
        if self._last_character_turned == character:
            return "Please wait for your opponent!"
        elif self.board[posX][posY] != '-':
            return "Illegal turn!"
        else:
            self.board[posX][posY] = character
            self._last_character_turned = character
