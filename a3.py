board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
player_piece = 'X'
ai_piece = 'O'

def display(board):
	print('   ' + '1 | 2 | 3')
	print('--------------')
	print('1| ' + board[0][0] + ' | ' + board[0][1] + ' | ' + board[0][2] + ' |')
	print('--------------')
	print('2| ' + board[1][0] + ' | ' + board[1][1] + ' | ' + board[1][2] + ' |')
	print('--------------')
	print('3| ' + board[2][0] + ' | ' + board[2][1] + ' | ' + board[2][2] + ' |')

def user_input():
	row = int(input('Enter row index: '))
	col = int(input('Enter column index: '))
	is_valid_move = False

	while(is_valid_move == False):
		if(row >=1 and col >= 1 and row <= 3 and col <= 3):
			if(board[row - 1][col - 1] == ' '):
				is_valid_move = True
			else:
				print('Location already filled. Try again')
				row = int(input('Enter row index: '))
				col = int(input('Enter column index: '))
		else:	
			print('Invalid location. Try again')
			row = int(input('Enter row index: '))
			col = int(input('Enter column index: '))
	
	board[row - 1][col - 1] = 'X'


if __name__ == '__main__':
  #play_a_new_game()
  while(True):
  	display(board)
  	user_input()