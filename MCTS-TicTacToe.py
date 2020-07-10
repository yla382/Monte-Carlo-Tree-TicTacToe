import copy
import random

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
player_piece = 'X'
ai_piece = 'O'

class Node: # A node to keep track of the score and its state and next available player's moves
	def __init__(self, state, parent):
		self.state = copy.deepcopy(state)  
		self.parent = parent
		self.children = []
		self.score = 0
		self.depth = 0

	def make_children(self, piece):  # Creates a children node containing state of opponent's possible moves
		for i in range(len(self.state)):
			for j in range(len(self.state)):
				if(self.state[i][j] == ' '):
					new_state = copy.deepcopy(self.state)
					new_state[i][j] = piece
					node = Node(new_state, self)
					node.depth = self.depth + 1
					self.children.append(node)


def is_board_full(current_board):  # Checks if the tic-tac-toe board is full or not
	count = 0
	for i in range(len(current_board)):
		for j in range(len(current_board[i])):
			if(current_board[i][j] == ' '):
				count += 1
	return (count == 0)


def board_score_mcst(check_node):  # Checks for the result of the board and gives the score based on win/loss/draw. Return -2 if AI loses, Return 1 if AI wins, and return 0 for draw
	current_board = check_node.state
	node_depth = check_node.depth
	player_win_condition = ['X', 'X', 'X']
	ai_win_condition = ['O', 'O', 'O']

	#horizontal check
	for i in range(len(current_board)):
		if(player_win_condition == current_board[i]):
			return -4

		if(ai_win_condition == current_board[i]):
			return 4 * (1 / node_depth)

	#vertical check
	for i in range(len(current_board)):
		list = []
		for j in range(len(current_board)):
			list.append(current_board[j][i])

		if(player_win_condition == list):
			return -4

		if(ai_win_condition == list):
			return 4 * (1 / node_depth)

	#diagonal check
	list = []
	for i in range(len(current_board)):
		list.append(current_board[i][i])

	if(player_win_condition == list):
		return -4
	if(ai_win_condition == list):
		return 4 * (1 / node_depth)

	list = []
	count = int(len(current_board)) - 1
	for i in range(len(current_board)):
		list.append(current_board[i][count])
		count -= 1

	if(player_win_condition == list):
		return -4

	if(ai_win_condition == list):
		return 4 * (1 / node_depth)
	
	return 0

def board_score(current_board):  # Checks for the result of the board and gives the score based on win/loss/draw. Return -2 if AI loses, Return 1 if AI wins, and return 0 for draw
	player_win_condition = ['X', 'X', 'X']
	ai_win_condition = ['O', 'O', 'O']

	#horizontal check
	for i in range(len(current_board)):
		if(player_win_condition == current_board[i]):
			return -4

		if(ai_win_condition == current_board[i]):
			return 4

	#vertical check
	for i in range(len(current_board)):
		list = []
		for j in range(len(current_board)):
			list.append(current_board[j][i])

		if(player_win_condition == list):
			return -4

		if(ai_win_condition == list):
			return 4

	#diagonal check
	list = []
	for i in range(len(current_board)):
		list.append(current_board[i][i])

	if(player_win_condition == list):
		return -4
	if(ai_win_condition == list):
		return 4

	list = []
	count = int(len(current_board)) - 1
	for i in range(len(current_board)):
		list.append(current_board[i][count])
		count -= 1

	if(player_win_condition == list):
		return -4

	if(ai_win_condition == list):
		return 4
	
	return 0


class MCS_Tree:  # Monte carlo tree search class for the AI to make a move
	def __init__(self, root, max_sim=100):
		self.root = root
		self.current_node = root # Node in the tree that is the current state of the game
		self.max_sim = max_sim

	def expand(self, piece): # Creates children for the current node
		self.current_node.make_children(piece)

	def simulate_helper(self, node, piece, finish_condition, score_func): # Recursively make a random move until the state/board is full and returns the score
		if(finish_condition(node.state) or score_func(node) != 0):
			return score_func(node)
		else:
			new_piece = ' '
			if(piece == player_piece):
				new_piece = ai_piece
				node.make_children(ai_piece)
			else:
				new_piece = player_piece
				node.make_children(player_piece)

			random_node = random.choice(node.children)
			return 0 + self.simulate_helper(random_node, new_piece, finish_condition, score_func)

	
	def simulate(self, piece, finish_condition, score_func): # Simulate the games on current node's children to update scores
		for node in self.current_node.children:
			score = 0
			sim_node = copy.deepcopy(node)
			for i in range(self.max_sim):
				score += self.simulate_helper(sim_node, piece, finish_condition, score_func)
			node.score = score
		return

	def select(self): # Select the current node's children with the highest score and make it has the current node
		selected_node = None
		for node in self.current_node.children:
			if(selected_node == None):
				selected_node = node
			else:
				if(selected_node.score < node.score):
					selected_node = node

		self.current_node = selected_node
		return self.current_node.state

	def update_current_node(self, state): # Search for the matching board in current node's children and make it as the current node. Used after player makes a move
		if(len(self.current_node.children) != 0):
			for node in self.current_node.children:
				if(node.state == state):
					self.current_node = node


def user_input(current_board): # Gets row and column location and add player's move into the board
	row = input('Enter row index: ')
	col = input('Enter column index: ')
	is_valid_move = False

	while(is_valid_move == False):
		try:
			row = int(row)
			col = int(col)

			if(row >=1 and col >= 1 and row <= 3 and col <= 3):
				if(current_board[row - 1][col - 1] == ' '):
					is_valid_move = True
				else:
					print('Location already filled. Try again')
					row = int(input('Enter row index: '))
					col = int(input('Enter column index: '))
			else:	
				print('Invalid location. Try again')
				row = int(input('Enter row index: '))
				col = int(input('Enter column index: '))
		except ValueError:
			print('Invalid type. Try again')
			row = input('Enter row index: ')
			col = input('Enter column index: ')
	
	current_board[row - 1][col - 1] = 'X'


def display(current_board): #Displays the board
	print('   ' + '1 | 2 | 3')
	print('--------------')
	print('1| ' + current_board[0][0] + ' | ' + current_board[0][1] + ' | ' + current_board[0][2] + ' |')
	print('--------------')
	print('2| ' + current_board[1][0] + ' | ' + current_board[1][1] + ' | ' + current_board[1][2] + ' |')
	print('--------------')
	print('3| ' + current_board[2][0] + ' | ' + current_board[2][1] + ' | ' + current_board[2][2] + ' |')


def play_a_new_game():
	global board, player_piece, ai_piece # Global declaration to avoid UnboundLocalError

	print('Ready for a Tic-Tac-Toe match?')
	print('You will be X and the AI will be O in the game')
	display(board)

	root = Node(copy.deepcopy(board), None) # Add empty board into the root_node for MCST
	mcst = MCS_Tree(root, 300) # MCST initialization
	turn = input('Enter who goes first (you: 1, AI: 2)? ')
	while(True):
		try:
			turn = int(turn)
			if(turn == 1 or turn == 2):
				break
			else:
				print("Enter either 1 or 2")
				turn = input('Enter who goes first (you: 1, AI: 2)? ')
		except ValueError:
			print("Enter integer value of 1 or 2")
			turn = input('Enter who goes first (you: 1, AI: 2)? ')

	while(True):
		if(turn == 1): # Player's turn
			print('Your move')
			user_input(board)
			mcst.expand(player_piece)
			display(board)
			turn += 1
		else: # AI's turn
			print('AI\' move')
			mcst.update_current_node(board)
			mcst.expand(ai_piece)
			mcst.simulate(ai_piece, is_board_full, board_score_mcst)
			board = copy.deepcopy(mcst.select())
			display(board)
			turn -= 1

		if(is_board_full(board)): # Ends the loop when board is full
			break

		if(board_score(board) != 0): # Ends the loop when someone wins
			break

		print('')

	if(board_score(board) == 0): # Prints the result of the game
		print('It\'s a draw')
	elif(board_score(board) > 0):
		print('You lost. AI wins.')
	else:
		print('You win. AI lost!')


if __name__ == '__main__':
	play_a_new_game()
