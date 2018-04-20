import numpy as np


#1==wall
#9==board_exit

def create_board_exit(board):
    #creating walls
    for i in range(np.shape(board)[0]):
        board[i][0]=1
        board[i][np.shape(board)[1]-1] = 1;
    for j in range(np.shape(board)[1]):
        board[0][j]=1
        board[np.shape(board)[0]-1][j] = 1;

    #creating exit
    board[int(np.floor(np.shape(board)[0]/2)-1)][np.shape(board)[1]-1] = 9

def create_room(height, width, board, start_point = [0,0]): #start(x,y) point is a upper-left corner of the room

    #creating walls
    for i in range(width):#x
        board[start_point[0]+i][start_point[1]] = 1
        board[start_point[0]+i][start_point[1]+height-1] = 1

    for i in range(height):#x
        board[start_point[0]][start_point[1]+i] = 1
        board[start_point[0]+width][start_point[1]+i] = 1

    #creating room door
    doors=[start_point[0]+height, int(start_point[1]+(np.floor(width/2)))]
    board[doors[0]][doors[1]] = 0;





height = 18
width = 18

actual_state = np.zeros((height, width))

create_room(8,8,actual_state,[0,0])
create_board_exit(actual_state)
print actual_state
