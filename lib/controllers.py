import time		
import random
import math
from .board import Board
from .errors import InvalidInputError, InvalidMoveError


class Controller:
	def __init__(self, game, name):
		self.name = name
		self.game = game

	def play(self, *args, **kwargs):
		self.game.print() 


	def __str__(self):
		return self.name



class HumanController(Controller):
	def play(self, **kwargs):
		super().play()

		_move = str(input(f"{self}\'s turn. Enter move: ")).strip()
		move = _move.split(' ')

		if len(move) != 2:
			raise InvalidInputError(_move)

		for i in move:
			if not i.isdigit():
				raise InvalidInputError(_move)


		move = [ int(i) for i in move ]
		self.game.play(*move)



class AIController(Controller):
	def play(self, **kwargs):
		super().play()
		print(f"Wait as ai {self} is thinking")

		self.game.play(*self._make_best_move())


	def _make_best_move(self, **kwargs):
		b = Board()
		if(self.game.previous_player['controller'] != self):
			ai_mark = self.game.current_player['mark']
			other_mark = self.game.previous_player['mark']

		else:
			ai_mark = self.game.previous_player['mark']
			other_mark = self.game.current_player['mark']

		b.board = self.game.board.copy()
		playable = b.get_empty_squares() 
		time.sleep(1)

		if self.game.steps < 1:
			weights = [
				0.25, 0.1, 0.25,
				0.1,  0.6, 0.1,
				0.25, 0.1, 0.25
			]

			print(random.choices(playable, weights))
			return playable[random.randint(0, len(playable) - 1)]

		best_move = None
		best_val = -math.inf
		
		for row, col in playable:
			b.play(ai_mark, row, col)
			move_val = self._minimax(False, b, ai_mark=ai_mark, opponent_mark=other_mark, max = -math.inf, min = math.inf)

			if move_val > best_val:
				best_val = move_val
				best_move = [row, col]

			b.unset(row, col)

		return best_move


	def _minimax(self, is_max, board, depth=0, **kwargs):
		if len(board.get_empty_squares()) == 0:
			return 0

		score = self._evaluate(board, **kwargs)

		if abs(score) == 10:
			return score

		arr = []
		for row, col in board.get_empty_squares():
			board.play(kwargs["ai_mark"] if is_max else kwargs['opponent_mark'], row, col)

			arr.append(self._minimax(not is_max, board, depth + 1, **kwargs))
			board.unset(row, col)
		
		return max(arr) if is_max else min(arr)


	def _evaluate(self, board_obj, **kwargs):
		diagonals = [[0, 0], [1, 1], [2, 2]]

		win_pos = None
		for pos in diagonals:
			result = board_obj.check(*pos)

			if result:
				win_pos = pos
				break

		if win_pos:
			char = board_obj.get_value_at(*win_pos)

			if char == kwargs['opponent_mark']:
				return -10

			elif char == kwargs['ai_mark']:
				return 10

		return 0

