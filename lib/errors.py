class InvalidMoveError(BaseException):
	def __init__(self, row=None, column=None):
		super().__init__()

		self.row = row
		self.column = column


	def __str__(self):
		msg = "The move is invalid. "
		rowValid = 0 >= self.row and self.row < 3 
		columnValid = 0 >= self.column and self.column < 3
		
		if self.row is None:
			msg = f"Row value missing"

		elif not rowValid:
			msg += f"Row value ({self.row}) must be integer between 0 and 2. "

		if self.column is None:
			msg = f"Column value missing"

		elif not columnValid:
			msg += f"Column value ({self.column}) must be an integer between 0 and 2. "
		return msg


class InvalidInputError(BaseException):
	def __init__(self, value ):
		super().__init__()

		self.value = value


	def __str__(self):
		return f'Value ({self.value}) is not a valid input. Input must be of format (1 0) or (2 0). '



class AlreadyPlayedError(BaseException):
	def __init__(self, row, column):
		self.row =  row
		self.column = column

	def __str__(self):
		return f'({self.row} {self.column}) has already being played'

