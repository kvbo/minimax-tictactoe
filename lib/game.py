from .constants import EMPTY_SYMBOL, DRAW_SCORE, WIN_SCORE
from .board import Board
from .errors import InvalidMoveError, InvalidInputError, AlreadyPlayedError
from .controllers import HumanController, AIController
from random import randint
import os


def default_update_fn(game):
	if game.clear_console:
		os.system('cls' if os.name == 'nt' else 'clear')
	
	print('*' * 30)	
	for key, player in game.players.items():
		print(str(player['controller']).ljust(8," "), '->', player['mark'], ' | ', 'score: ', player['score'])

	print('Moves played: ', game.steps)
	print('*' * 30)	

	game.board.print()
	for i in game.messages:

		match i['type']:
			case 'error':
				color = "Error: "
			case _ :
				color = ''

		print(f"{color} {i['message']}")
	game.messages.clear()


class Game:
	def __init__(self, *args, **kwargs):
		self.players = {}
		self.messages = []
		self.turn = randint(0, 1)
		self.clear_console = kwargs.get('clear_console', False)
		self.update_fn = None


	def setup(self):
		self.won = False
		self.steps = 0
		self.board = Board()


	def play(self, row, col):
		if self.won == True or self.steps > 8:
			return 

		board = self.board.copy()
		try:
			self.board.play(self.current_player["mark"], row, col)
			self.steps += 1

			if self.board.check(row, col):
				self.won = True
				return 

			if self.steps > 8:
				return 

			else:
				self.next()
				self.current_player["controller"].play()


		except (InvalidMoveError, InvalidInputError, AlreadyPlayedError ) as e:
			if not isinstance(e, InvalidInputError):
				self.board.board = board
			
			self.messages.append({'type': 'error', 'message': e })
			self.current_player['controller'].play()


	def next(self, commit=True):
		turn = 0 if self.turn == 1 else 1

		if commit:
			self.turn = turn

		return turn


	@property
	def current_player(self):
		return self.players[str(self.turn)]

	@property
	def previous_player(self):
		return self.players[str(self.next(commit=False))]


	def loop(self, update_fn=default_update_fn):
		self.update_fn=update_fn
		self.setup()

		self.current_player["controller"].play()

		self.print()
		if self.won:
			print(self.current_player['controller'], 'wins')
			self.current_player['score'] += WIN_SCORE
			self.next()

		else:
			print('Game is a draw')
			self.current_player['score'] 	+= DRAW_SCORE
			self.previous_player['score'] += DRAW_SCORE


	def print(self):
		self.update_fn(game=self)


	def release(self):
		self.players = []


	def add_players(self, *args, **kwargs):
		human_count = 0
		player_count = 0
		marks = ['\U0001f600', '\U0001F616']
		# marks = ['x', 'o']


		for controller in args:
			add = False
			mark = marks[player_count]
			player_number = player_count

			
			if issubclass(controller, HumanController):
				add = True
				human_count += 1
				player_count += 1
				c = controller(game=self, name=f"Player {human_count}", **kwargs)

			elif issubclass(controller, AIController): 
				add = True
				c = controller(game=self, name=f"AI Bot", **kwargs)
				player_count += 1
				# mark = '\U0001f916'


			else:
				...


			if add and player_count <= 2:
				self.players[str(player_number)] = {
					"score": 0,
					"controller": c,
					"mark": mark
				}



