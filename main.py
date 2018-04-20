import numpy as np
import cv2
from time import sleep
from copy import deepcopy


#1==wall
#9==board_exit

def create_board_exit(board):
    #creating walls
    for i in range(np.shape(board)[0]):
        board[i][0]='#'
        board[i][np.shape(board)[1]-1] = '#';
    for j in range(np.shape(board)[1]):
        board[0][j]='#'
        board[np.shape(board)[0]-1][j] = '#';

    #creating exit
    board[int(np.floor(np.shape(board)[0]/2)-1)][np.shape(board)[1]-1] = '#'

def create_room(height, width, board, start_point = [0,0]): #start(x,y) point is a upper-left corner of the room

    #creating walls
    for i in range(width):#x
        board[start_point[0]+i][start_point[1]] = '#'
        board[start_point[0]+i][start_point[1]+height-1] = '#'

    for i in range(height):#x
        board[start_point[0]][start_point[1]+i] = '#'
        board[start_point[0]+width][start_point[1]+i] = '#'

    #creating room door
    doors=[start_point[0]+height, int(start_point[1]+(np.floor(width/2)))]
    board[doors[0]][doors[1]] = '0';

def smallest_neighbour(y,x, board):
    k = 999
    if board[y-1][x] != '0' and board[y-1][x] != '#' and board[y-1][x] != '/' and int(board[y-1][x])< k:
        k = int(board[y-1][x])

    if board[y-1][x+1] != '0' and board[y-1][x+1] != '#' and board[y-1][x+1] != '/' and int(board[y-1][x+1])< k:
        k = int(board[y-1][x+1])

    if  board[y][x-1] != '0' and board[y][x-1] != '#' and board[y][x-1] != '/' and int(board[y][x-1])< k:
        k = int(board[y][x-1])

    if board[y][x+1] != '0' and board[y][x+1] != '#' and board[y][x+1] != '/' and int(board[y][x+1])< k:
        k = int(board[y][x+1])

    if board[y+1][x] != '0' and board[y+1][x] != '#' and board[y+1][x] != '/' and int(board[y+1][x])< k:
        k = int(board[y+1][x])

    if board[y+1][x+1] != '0' and board[y+1][x+1] != '#' and board[y+1][x+1] != '/' and int(board[y+1][x+1])<k:
        k = int(board[y+1][x+1])
    return k

def calculate_distance_matrix(board, exit):
    stack = []
    board[exit[0],exit[1]] = '1'
    stack.append([exit[0],exit[1], 1])
    while len(stack)!=0:   #tutaj
        stack.reverse()
        P = stack.pop()
        stack.reverse()


        if(board[P[0]-1][P[1]]=='0'):
            stack.append([P[0]-1,P[1],P[2]+1])
            board[P[0]-1][P[1]] = str(int(smallest_neighbour(P[0]-1, P[1], board))+1)
        if(board[P[0]-1][P[1]+1]=='0'):
            stack.append([P[0]-1,P[1]+1,P[2]+1])
            board[P[0]-1][P[1]+1] = str(int(smallest_neighbour(P[0]-1, P[1]+1, board))+1)
        if(board[P[0]][P[1]-1]=='0'):
            stack.append([P[0],P[1]-1,P[2]+1])
            board[P[0]][P[1]-1] = str(int(smallest_neighbour(P[0], P[1]-1, board))+1)
        if(board[P[0]][P[1]+1]=='0'):
            stack.append([P[0],P[1]+1,P[2]+1])
            board[P[0]][P[1]+1] = str(int(smallest_neighbour(P[0], P[1]+1, board))+1)
        if(board[P[0]+1][P[1]+1]=='0'):
            stack.append([P[0]+1,P[1]+1,P[2]+1])
            board[P[0]+1][P[1]+1] = str(int(smallest_neighbour(P[0]+1, P[1]+1, board))+1)
        if(board[P[0]+1][P[1]]=='0'):
            stack.append([P[0]+1,P[1],P[2]+1])
            board[P[0]+1][P[1]] = str(int(smallest_neighbour(P[0]+1, P[1], board))+1)

        print '=============================================='
        print board

height = 11
width = 11

actual_state = np.chararray((height, width))
actual_state[:,:] = '0'

create_room(4,4,actual_state,[0,0])
create_board_exit(actual_state)
print actual_state
calculate_distance_matrix(actual_state, [5,9])
print "final", "==========================================="
print actual_state
