import numpy as np
import cv2
from time import sleep
import random
from copy import deepcopy


#1==wall
#9==board_exit

def create_board_exit(board):
    #creating walls
    for i in range(np.shape(board)[0]):
        board[i][0]=-1
        board[i][np.shape(board)[1]-1] = -1;
    for j in range(np.shape(board)[1]):
        board[0][j]=-1
        board[np.shape(board)[0]-1][j] = -1;

    #creating exit
    board[int(np.floor(np.shape(board)[0]/2))][np.shape(board)[1]-1] = -2

def create_room(height, width, board, start_point = [0,0]): #start(x,y) point is a upper-left corner of the room

    #creating walls
    for i in range(width):#x
        board[start_point[0]+i][start_point[1]] = -1
        board[start_point[0]+i][start_point[1]+height-1] = -1

    for i in range(height):#x
        board[start_point[0]][start_point[1]+i] = -1
        board[start_point[0]+width][start_point[1]+i] = -1

    #creating room door
    doors=[start_point[0]+height, int(start_point[1]+(np.floor(width/2)))]
    board[doors[0]][doors[1]] = 0;

def create_random_dwellers(amount, board):
    w,h = np.shape(board)
    while amount > 0:
        x = random.randint(1,w-1)
        y = random.randint(1,h-1)
        if board[x][y] == 0:
            board[x][y] = -8
            amount -= 1


def smallest_neighbour_for_cost_matrix(y,x, board):
    k = 999
    if board[y-1][x]  > 0 and board[y-1][x]< k:
        k = board[y-1][x]

    if board[y-1][x+1] > 0 and board[y-1][x+1]< k:
        k = board[y-1][x+1]

    if  board[y][x-1] > 0 and board[y][x-1]< k:
        k = board[y][x-1]

    if board[y][x+1] > 0 and board[y][x+1]< k:
        k = board[y][x+1]

    if board[y+1][x] > 0 and board[y+1][x]< k:
        k = board[y+1][x]

    if board[y+1][x+1] >0 and board[y+1][x+1]<k:
        k = board[y+1][x+1]
    return k

def smallest_neighbour_for_iteration(y,x, board, board2):
    k = 999
    coords = [0,0]
    if board[y-1][x] > 0 and board[y-1][x]< k and board2[y-1][x] == 0:
        k = board[y-1][x]
        coords = [y-1,x]

    if board[y-1][x+1] > 0 and board[y-1][x+1]< k and board2[y-1][x-1] == 0:
        k = board[y-1][x+1]
        coords = [y-1, x+1]

    if  board[y][x-1] > 0 and board[y][x-1]< k and board2[y][x-1] == 0:
        k = board[y][x-1]
        coords = [y, x-1]

    if board[y][x+1] > 0 and board[y][x+1]< k and board2[y][x+1] == 0:
        k = board[y][x+1]
        coords = [y, x+1]
    if board[y+1][x] > 0 and board[y+1][x]< k and board2[y+1][x] == 0:
        k = board[y+1][x]
        coords = [y+1,x]

    if board[y+1][x+1] >0 and board[y+1][x+1]<k and board2[y+1][x+1] == 0:
        k = board[y+1][x+1]
        coords = [y+1, x+1]

    return coords

def calculate_distance_matrix(board, exit):
    stack = []
    board[exit[0],exit[1]] = 1
    stack.append([exit[0],exit[1]])
    while len(stack)!=0:

        P = stack.pop(0)

        if(board[P[0]-1][P[1]]==0):
            stack.append([P[0]-1,P[1]])
            board[P[0]-1][P[1]] = smallest_neighbour_for_cost_matrix(P[0]-1, P[1], board)+1
        if(board[P[0]-1][P[1]+1]==0):
            stack.append([P[0]-1,P[1]+1])
            board[P[0]-1][P[1]+1] = smallest_neighbour_for_cost_matrix(P[0]-1, P[1]+1, board)+1
        if(board[P[0]][P[1]-1]==0):
            stack.append([P[0],P[1]-1])
            board[P[0]][P[1]-1] = smallest_neighbour_for_cost_matrix(P[0], P[1]-1, board)+1
        if(board[P[0]][P[1]+1]==0):
            stack.append([P[0],P[1]+1])
            board[P[0]][P[1]+1] = smallest_neighbour_for_cost_matrix(P[0], P[1]+1, board)+1
        if(board[P[0]+1][P[1]+1]==0):
            stack.append([P[0]+1,P[1]+1])
            board[P[0]+1][P[1]+1] = smallest_neighbour_for_cost_matrix(P[0]+1, P[1]+1, board)+1
        if(board[P[0]+1][P[1]]==0):
            stack.append([P[0]+1,P[1]])
            board[P[0]+1][P[1]] = smallest_neighbour_for_cost_matrix(P[0]+1, P[1], board)+1

        # print '============================================'
        # # sleep(0.5)
        # print board
        # print 'stack length:   ', len(stack)

def iterate(board, cost_matrix):
    w,h = np.shape(board)
    arr = []

    for i in range(w):
        for j in range(h):
            if board[i][j] == -8:
                if cost_matrix[i][j] == 1:
                    board[i][j] = 0 #delete if standing next to entrance
                else:
                    arr.append([i,j, cost_matrix[i][j]])
    arr.sort(key=lambda x: x[2])


    for i in range(0, len(arr)):
        coords = smallest_neighbour_for_iteration(int(arr[i][0]), int(arr[i][1]), cost_matrix, board)
        if coords != [0,0]:
            board[int(arr[i][0])][int(arr[i][1])] = 0
            board[coords[0]][coords[1]] = -8

        #debug
        print board
        sleep(0.4)

    print len(arr), ' dwellers left.'



if __name__ == "__main__":
    height = 11
    width = 11


    actual_state = np.ndarray((height, width))
    actual_state[:,:] = 0
    #
    create_room(4,4,actual_state,[0,0])
    create_room(4,4,actual_state,[0,3])
    create_room(4,4,actual_state,[0,6])
    create_board_exit(actual_state)
    #board is prepared
    cost_matrix = deepcopy(actual_state)
    calculate_distance_matrix(cost_matrix, [5,9])
    create_random_dwellers(15,actual_state)

    while 1:
        print "new iteration:"
        iterate(actual_state, cost_matrix)
        print actual_state
        k = raw_input('continue? n stops, s shows costs matrix ')
        if k == 'n':
            break
        elif k == 's':
            print cost_matrix
