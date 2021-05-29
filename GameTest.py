import unittest

from Game import Game


class TicTacToeTest(unittest.TestCase):
    def test_game_draw(self):
        game = Game()
        board = [['x', 'o', 'x'],
                 ['o', 'x', 'o'],
                 ['o', 'x', 'o']]
        game.board = board
        self.assertEqual(game.game_state(), 'd')

    def test_game_won(self):
        game = Game()
        board = [['x', 'x', 'o'],
                 ['o', 'o', 'o'],
                 ['o', 'x', 'x']]
        game.board = board
        self.assertEqual(game.game_state(), 'w')

        board = [['x', 'x', 'o'],
                 ['o', 'x', 'o'],
                 ['o', 'o', 'x']]
        game.board = board
        self.assertEqual(game.game_state(), 'w')

    def test_game_ongoing(self):
        game = Game()
        board = [['x', 'x', 'o'],
                 ['o', '-', 'o'],
                 ['o', 'x', 'x']]
        game.board = board
        self.assertEqual(game.game_state(), None)


if __name__ == '__main__':
    unittest.main()
