from copy import deepcopy

WIDTH = 3
HEIGHT = 3
AI_TURN_INDEX = 1
MAX = WIDTH * HEIGHT

CROSS_LENGTH = min([WIDTH,HEIGHT])

players = ["X","O"]
N_PLAYERS = len(players)

if WIDTH > HEIGHT:
	X_LARGER = True
elif WIDTH == HEIGHT:
	X_LARGER = False
else:
	X_LARGER = False

MAX = WIDTH * HEIGHT

horizontal_wins = []
vertical_wins = []

for player in players:
	horizontal_wins.append([])
	vertical_wins.append([])
# HORIZONTAL WINS
for x in range(WIDTH):
	player_index = 0
	for player in players:
		horizontal_wins[player_index] += player		
		player_index += 1
# VERTICAL WINS
for x in range(HEIGHT):
	player_index = 0
	for player in players:
		vertical_wins[player_index] += player
		player_index += 1
# CROSS WINS
if len(horizontal_wins) < len(vertical_wins):
	cross_wins = horizontal_wins
else:
	cross_wins = vertical_wins

free_squares = []
	
game_is_on = True

board = []

move_counter = 0

# GENERATES BOARD
for y in range(HEIGHT):
	board.append([])
	for x in range(WIDTH):
		board[y].append(" ")
		free_squares.append([y,x])
# PRINTS BOARD
def board_print(board):
	width = len(board[0])
	horiz = ""
	for w in range(width):
		horiz += " _"
	print(horiz)
	for row in board:
		printer = "|"
		for square in row:
			printer += str(square[0]) + "|"
		print(printer)
		print(horiz)

def announce(status,who):
	if status == 2:
		print(f"Player '{who}' has won!")
	else:
		print("The game was a draw!")

def move(move):
	height_index = move[0]
	width_index = move[1]
	# VALID MOVE?
	if height_index < HEIGHT and width_index < WIDTH and board[height_index][width_index] == " ":
		board[height_index][width_index] = players[player_index]
		board_print(board)

		free_squares.remove([height_index,width_index])
		return True
	else:
		print("INCORRECT MOVE YOU MORON")
		return False

def checker(board, turn_counter):
	current = turn_counter % N_PLAYERS
	# HORIZONTAL CHECK
	for row in board:
		if row in horizontal_wins:
			if row == horizontal_wins[current]:
				return 2 #WIN
			else:
				return -1 #LOSE
	# VERTICAL CHECK
	for col in range(WIDTH):
		column = []
		for row in board:
			column.append(row[col])
		if column in vertical_wins:
			if column == vertical_wins[current]:
				return 2 #WIN
			else:
				return -1 #LOSE
	# CROSS CHECK
	for check_index in range(abs(WIDTH-HEIGHT)+1):
		cross = []
		inv_cross = []
		for row in range(CROSS_LENGTH):
			if X_LARGER:
				cross.append(board[row][row + check_index])
				inv_cross.append(board[row][WIDTH-1-row + check_index])
			else:
				cross.append(board[row + check_index][row])
				inv_cross.append(board[row + check_index][WIDTH-1-row])	
		if cross in cross_wins or inv_cross in cross_wins:
			if cross == cross_wins[current] or inv_cross == cross_wins[current]:
				return 2 # WIN
			else:
				return -1 # LOSE
	if turn_counter >= MAX:
		return 1 # DRAW
	return 0 #GAME GOES ON, RETURNS FALSE

def add_move(board, square, depth):
	#print(board)
	board[square[0]][square[1]] = players[depth % N_PLAYERS]
	return board

def minimax_miner(board, free_squares, depth, original_depth):
	new_boards = [add_move(deepcopy(board), square, depth) for square in free_squares] #FUCKING LIST COMPREHENSION FAILED ON ME
	depth += 1
	evaluations = [checker(board, AI_TURN_INDEX) for board in new_boards]
	if depth < MAX:
		for board in range(len(new_boards)):
			if evaluations[board] == 0:
				new_free_squares = deepcopy(free_squares)
				new_free_squares.pop(board)
				evaluations[board] = minimax_miner(new_boards[board], new_free_squares, depth, original_depth)
	#print(depth, original_depth)
	if depth > original_depth:
		if depth % N_PLAYERS == AI_TURN_INDEX:
			return max(evaluations)
		else:
			return min(evaluations)
	else:
		return evaluations

def genius(board, free_squares, depth, original_depth):
	game_tree = minimax_miner(board, free_squares, depth, original_depth)
	return game_tree

# GAME
while game_is_on:
	player_index = move_counter % N_PLAYERS
	if player_index == AI_TURN_INDEX:
		print("Genius moves: ")
		moves = genius(board, free_squares, move_counter, move_counter+1)
		#print(moves)
		move_successful = move(free_squares[moves.index(max(moves))])
		if move_successful:
			move_counter += 1
	else:
		move_raw = input(f"Enter move for '{str(players[player_index])}': ")
		move_successful = move([int(move_raw[0]),int(move_raw[1])])
		if move_successful:
			move_counter += 1

	check = checker(board, move_counter)
	if check:
		game_is_on = False
		announce(check,players[player_index])
