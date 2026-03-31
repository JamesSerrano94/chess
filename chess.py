from ast import Index
from concurrent.futures.process import _threads_wakeups
import pygame

import time

import sys
import copy

board = [['  ' for i in range(8)] for i in range(8)]
whitePassant = -10
blackPassant = -10
whiteCastle = False
blackCastle = False



## Creates a chess piece class that shows what team a piece is on, what type of piece it is and whether or not it can be killed by another selected piece.
class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image


## Creates instances of chess pieces, so far we got: pawn, king, rook and bishop
## The first parameter defines what team its on and the second, what type of piece it is
bp = Piece('b', 'p', 'b_pawn.png')
wp = Piece('w', 'p', 'w_pawn.png')
bk = Piece('b', 'k', 'b_king.png')
wk = Piece('w', 'k', 'w_king.png')
br = Piece('b', 'r', 'b_rook.png')
wr = Piece('w', 'r', 'w_rook.png')
bb = Piece('b', 'b', 'b_bishop.png')
wb = Piece('w', 'b', 'w_bishop.png')
bq = Piece('b', 'q', 'b_queen.png')
wq = Piece('w', 'q', 'w_queen.png')
bkn = Piece('b', 'kn', 'b_knight.png')
wkn = Piece('w', 'kn', 'w_knight.png')



starting_order = {(0, 0): pygame.transform.scale(pygame.image.load(br.image), (50, 50)), (1, 0): pygame.transform.scale(pygame.image.load(bkn.image), (50, 50)),
                  (2, 0): pygame.transform.scale(pygame.image.load(bb.image), (50, 50)), (3, 0): pygame.transform.scale(pygame.image.load(bq.image), (50, 50)),
                  (4, 0): pygame.transform.scale(pygame.image.load(bk.image), (50, 50)), (5, 0): pygame.transform.scale(pygame.image.load(bb.image), (50, 50)),
                  (6, 0): pygame.transform.scale(pygame.image.load(bkn.image), (50, 50)), (7, 0): pygame.transform.scale(pygame.image.load(br.image), (50, 50)),
                  (0, 1): pygame.transform.scale(pygame.image.load(bp.image), (50, 50)), (1, 1): pygame.transform.scale(pygame.image.load(bp.image), (50, 50)),
                  (2, 1): pygame.transform.scale(pygame.image.load(bp.image), (50, 50)), (3, 1): pygame.transform.scale(pygame.image.load(bp.image), (50, 50)),
                  (4, 1): pygame.transform.scale(pygame.image.load(bp.image), (50, 50)), (5, 1): pygame.transform.scale(pygame.image.load(bp.image), (50, 50)),
                  (6, 1): pygame.transform.scale(pygame.image.load(bp.image), (50, 50)), (7, 1): pygame.transform.scale(pygame.image.load(bp.image), (50, 50)),

                  (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                  (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                  (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                  (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                  (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                  (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                  (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                  (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

                  (0, 6): pygame.transform.scale(pygame.image.load(wp.image), (50, 50)), (1, 6): pygame.transform.scale(pygame.image.load(wp.image), (50, 50)),
                  (2, 6): pygame.transform.scale(pygame.image.load(wp.image), (50, 50)), (3, 6): pygame.transform.scale(pygame.image.load(wp.image), (50, 50)),
                  (4, 6): pygame.transform.scale(pygame.image.load(wp.image), (50, 50)), (5, 6): pygame.transform.scale(pygame.image.load(wp.image), (50, 50)),
                  (6, 6): pygame.transform.scale(pygame.image.load(wp.image), (50, 50)), (7, 6): pygame.transform.scale(pygame.image.load(wp.image), (50, 50)),
                  (0, 7): pygame.transform.scale(pygame.image.load(wr.image), (50, 50)), (1, 7): pygame.transform.scale(pygame.image.load(wkn.image), (50, 50)),
                  (2, 7): pygame.transform.scale(pygame.image.load(wb.image), (50, 50)), (3, 7): pygame.transform.scale(pygame.image.load(wq.image), (50, 50)),
                  (4, 7): pygame.transform.scale(pygame.image.load(wk.image), (50, 50)), (5, 7): pygame.transform.scale(pygame.image.load(wb.image), (50, 50)),
                  (6, 7): pygame.transform.scale(pygame.image.load(wkn.image), (50, 50)), (7, 7): pygame.transform.scale(pygame.image.load(wr.image), (50, 50)),}

# resized_order = {}

# # Iterate through the original dictionary to resize each image
# for position, image in starting_order.items():
#     if image is not None:  # Check if the image exists
#         resized_image = pygame.transform.scale(image, (50, 50))  # Resize to 50x50 pixels
#         resized_order[position] = resized_image  # Store the resized image in the new dictionary
#     else:
#         resized_order[position] = None  # If there's no image, store None

# Now the resized_order dictionary contains the resized images


def create_board(board):
    board[0] = [Piece('b', 'r', 'b_rook.png'), Piece('b', 'kn', 'b_knight.png'), Piece('b', 'b', 'b_bishop.png'), \
               Piece('b', 'q', 'b_queen.png'), Piece('b', 'k', 'b_king.png'), Piece('b', 'b', 'b_bishop.png'), \
               Piece('b', 'kn', 'b_knight.png'), Piece('b', 'r', 'b_rook.png')]

    board[7] = [Piece('w', 'r', 'w_rook.png'), Piece('w', 'kn', 'w_knight.png'), Piece('w', 'b', 'w_bishop.png'), \
               Piece('w', 'q', 'w_queen.png'), Piece('w', 'k', 'w_king.png'), Piece('w', 'b', 'w_bishop.png'), \
               Piece('w', 'kn', 'w_knight.png'), Piece('w', 'r', 'w_rook.png')]

    for i in range(8):
        board[1][i] = Piece('b', 'p', 'b_pawn.png')
        board[6][i] = Piece('w', 'p', 'w_pawn.png')
    return board


## returns the input if the input is within the boundaries of the board
def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True


## returns a string that places the rows and columns of the board in a readable manner
def convert_to_readable(board):
    output = ''

    for i in board:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output


## resets "x's" and killable pieces
def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass
    return convert_to_readable(board)


## Takes in board as argument then returns 2d array containing positions of valid moves
def highlight(board):
    highlighted = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x ':
                highlighted.append((i, j))
            else:
                try:
                    if board[i][j].killable:
                        highlighted.append((i, j))
                except:
                    pass
    return highlighted

def check_team(moves, index):
    row, col = index
    if moves%2 == 0:
        if board[row][col].team == 'w':
            return True
    else:
        if board[row][col].team == 'b':
            return True

## This takes in a piece object and its index then runs then checks where that piece can move using separately defined functions for each type of piece.
def select_moves(piece, index, moves):
    print("SELECT", moves, piece.team, piece.type, index)
    #print(convert_to_readable(board))
    if check_team(moves, index):
        if piece.type == 'p':
            if piece.team == 'b':
                return highlight(pawn_moves_b(index))
            else:
                return highlight(pawn_moves_w(index))

        if piece.type == 'k':
            return highlight(king_moves(index))

        if piece.type == 'r':
            return highlight(rook_moves(index))

        if piece.type == 'b':
            return highlight(bishop_moves(index))

        if piece.type == 'q':
            return highlight(queen_moves(index))

        if piece.type == 'kn':
            return highlight(knight_moves(index))

def select_moves_temp(piece, index, board):
        if piece.type == 'p':
            if piece.team == 'b':
                return highlight(pawn_moves_b_temp(index, board))
            else:
                return highlight(pawn_moves_w_temp(index, board))

        if piece.type == 'k':
            return highlight(king_moves_temp(index, board))

        if piece.type == 'r':
            return highlight(rook_moves_temp(index, board))

        if piece.type == 'b':
            return highlight(bishop_moves_temp(index, board))

        if piece.type == 'q':
            return highlight(queen_moves_temp(index, board))

        if piece.type == 'kn':
            return highlight(knight_moves_temp(index, board))

def dontPutKingInCheck(board, index, team):
    # print("IS THIS WORKING")
    for i in range(8):
        for j in range(8):
            copyBoard = copy.deepcopy(board)
            if copyBoard[i][j] == 'x ':
                copyBoard[i][j] = copyBoard[index[0]][index[1]]
                copyBoard[index[0]][index[1]] = '  '
                for a in range(8):
                    for b in range(8):
                        if copyBoard[a][b] != '  ' and copyBoard[a][b] != 'x ':
                            if team != copyBoard[a][b].team:
                                select_moves_temp(copyBoard[a][b], (a, b), copyBoard)
                                # print("A AND B ARE", a, b, team)
                                # print("YEAH", a, b, team)
                                # print(convert_to_readable(copyBoard))

                                for c in range(8):
                                    for d in range(8):
                                        if copyBoard[c][d] != '  ' and copyBoard[c][d] != 'x ':
                                            if copyBoard[c][d].team == team and copyBoard[c][d].type == 'k':
                                                if copyBoard[c][d].killable == True:
                                                    board[i][j] = '  '

                                

                                copyBoard = resetPotential(copyBoard)

 
def isItCheck(board, team):
    for i in range(8):
        for j in range(8):
            copyBoard = copy.deepcopy(board)
            if copyBoard[i][j] != '  ' and copyBoard[i][j] != 'x ':
                if team == copyBoard[i][j].team:
                    select_moves_temp(copyBoard[i][j], (i, j), copyBoard)
                    # print("FUCK YEAH", i, j, team)
                    # print(convert_to_readable(copyBoard))
                    for c in range(8):
                        for d in range(8):
                            if copyBoard[c][d] != '  ' and copyBoard[c][d] != 'x ':
                                if copyBoard[c][d].team != team and copyBoard[c][d].type == 'k':
                                    # print("TEAM IS ", team, c, d, i, j)
                                    if copyBoard[c][d].killable == True:
                                        return True
                    copyBoard = resetPotential(copyBoard)
    return False

def availableMoves(board, team):
    for i in range(8):
        for j in range(8):
            copyBoard = copy.deepcopy(board)
            if copyBoard[i][j] != '  ' and copyBoard[i][j] != 'x ':
                if team == copyBoard[i][j].team:
                    select_moves_temp(copyBoard[i][j], (i, j), copyBoard)
                    for c in range(8):
                        for d in range(8):
                            if copyBoard[c][d] == 'x ':
                                # print("C AND D ARE ", c, d, i, j, team)
                                copyBoard[c][d] = copyBoard[i][j]
                                copyBoard[i][j] = '  '
                                if team == 'w':
                                    if isItCheck(copyBoard, 'b') is False:
                                        return True
                                else:
                                    if isItCheck(copyBoard, 'w') is False:
                                        return True
                                copyBoard[i][j] = copyBoard[c][d]
                                copyBoard[c][d] = '  '
    return False



## Basically, check black and white pawns separately and checks the square above them. If its free that space gets an "x" and if it is occupied by a piece of the opposite team then that piece becomes killable.
def pawn_moves_b(index):
    # print("HEYYYYYYY")
    if index[0] == 1:
        if board[index[0] + 2][index[1]] == '  ' and board[index[0] + 1][index[1]] == '  ':
            board[index[0] + 2][index[1]] = 'x '
    bottom3 = [[index[0] + 1, index[1] + i] for i in range(-1, 2)]

    for positions in bottom3:
        if on_board(positions):
            if bottom3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'b':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
    if index[0] == 4 and abs(whitePassant - index[1]) == 1: # en passant
        board[positions[0]][whitePassant] = 'x '
    # print("OUTKAST")
    dontPutKingInCheck(board, index, 'b')
    return board


def pawn_moves_b_temp(index, board):
    if index[0] == 1:
        if board[index[0] + 2][index[1]] == '  ' and board[index[0] + 1][index[1]] == '  ':
            board[index[0] + 2][index[1]] = 'x '
    bottom3 = [[index[0] + 1, index[1] + i] for i in range(-1, 2)]

    for positions in bottom3:
        if on_board(positions):
            if bottom3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'b':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  '  or board[positions[0]][positions[1]] == 'x ':
                    board[positions[0]][positions[1]] = 'x '
    if index[0] == 4 and abs(whitePassant - index[1]) == 1: # en passant
        board[positions[0]][whitePassant] = 'x '
    #board = dontPutKingInCheck(board, index, 'b')
    return board


def pawn_moves_w(index):
    if index[0] == 6:
        if board[index[0] - 2][index[1]] == '  ' and board[index[0] - 1][index[1]] == '  ':
            board[index[0] - 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]

    


    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'w':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '

    if index[0] == 3 and abs(blackPassant - index[1]) == 1: # en passant
         board[positions[0]][blackPassant] = 'x '
    dontPutKingInCheck(board, index, 'w')
    return board


def pawn_moves_w_temp(index, board):
    if index[0] == 6:
        if board[index[0] - 2][index[1]] == '  ' and board[index[0] - 1][index[1]] == '  ':
            board[index[0] - 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]

    


    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'w':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ' or board[positions[0]][positions[1]] == 'x ':
                    board[positions[0]][positions[1]] = 'x '

    if index[0] == 3 and abs(blackPassant - index[1]) == 1: # en passant
         board[positions[0]][blackPassant] = 'x '
    return board

## This just checks a 3x3 tile surrounding the king. Empty spots get an "x" and pieces of the opposite team become killable.
def king_moves(index):
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 + x] == '  ':
                    board[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                        copyBoard = copy.deepcopy(board)
                        copyBoard[index[0] - 1 + y][index[1] - 1 + x] = copyBoard[index[0]][index[1]]
                        copyBoard[index[0]][index[1]] = '  '
                        #print("WHAT ARE TEAMS", copyBoard[index[0] - 1 + y][index[1] - 1 + x].team, board[index[0] - 1 + y][index[1] - 1 + x].team)
                        if isItCheck(copyBoard, board[index[0] - 1 + y][index[1] - 1 + x].team) is False:
                            #print("YES IT IS CHECK")
                            board[index[0] - 1 + y][index[1] - 1 + x].killable = True

    #Castle exception
    if board[index[0]][index[1]].team == 'w' and board[index[0]][index[1]].type == 'k' and index[0] == 7 and index[1] == 4 and not whiteCastle:
        if board[7][5] == 'x ' and board[7][6] == '  ' and board[7][7].team == 'w' and board[7][7].type == 'r':
            board[7][6] = 'x '
        if board[7][3] == 'x ' and board[7][2] == '  ' and board[7][1] == '  ' and board[7][0].team == 'w' and board[7][0].type == 'r':
            board[7][2] = 'x '

    elif board[index[0]][index[1]].team == 'b' and board[index[0]][index[1]].type == 'k' and index[0] == 0 and index[1] == 4 and not blackCastle:
        if board[0][5] == 'x ' and board[0][6] == '  ' and board[0][7].team == 'b' and board[0][7].type == 'r':
            board[0][6] = 'x '
        if board[0][3] == 'x ' and board[0][2] == '  ' and board[0][1] == '  ' and board[0][0].team == 'b' and board[0][0].type == 'r':

            board[0][2] = 'x '
    dontPutKingInCheck(board, index, board[index[0]][index[1]].team)
    return board

def king_moves_temp(index, board):
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 + x] == '  ' or board[index[0] - 1 + y][index[1] - 1 + x] == 'x ':
                    board[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                        board[index[0] - 1 + y][index[1] - 1 + x].killable = True

    #Castle exception
    if board[index[0]][index[1]].team == 'w' and board[index[0]][index[1]].type == 'k' and index[0] == 7 and index[1] == 4 and not whiteCastle:
        if board[7][5] == 'x ' and board[7][6] == '  ' and board[7][7].team == 'w' and board[7][7].type == 'r':
            board[7][6] = 'x '
        if board[7][3] == 'x ' and board[7][2] == '  ' and board[7][1] == '  ' and board[7][0].team == 'w' and board[7][0].type == 'r':
            board[7][2] = 'x '

    elif board[index[0]][index[1]].team == 'b' and board[index[0]][index[1]].type == 'k' and index[0] == 0 and index[1] == 4 and not blackCastle:
        if board[0][5] == 'x ' and board[0][6] == '  ' and board[0][7].team == 'b' and board[0][7].type == 'r':
            board[0][6] = 'x '
        if board[0][3] == 'x ' and board[0][2] == '  ' and board[0][1] == '  ' and board[0][0].team == 'b' and board[0][0].type == 'r':

            board[0][2] = 'x '
    return board


## This creates 4 lists for up, down, left and right and checks all those spaces for pieces of the opposite team. The list comprehension is pretty long so if you don't get it just msg me.
def rook_moves(index):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    dontPutKingInCheck(board, index, board[index[0]][index[1]].team)
    return board

def rook_moves_temp(index, board):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ' or board[positions[0]][positions[1]] == 'x ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board

## Same as the rook but this time it creates 4 lists for the diagonal directions and so the list comprehension is a little bit trickier.
def bishop_moves(index):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                 [[index[0] + i, index[1] - i] for i in range(1, 8)],
                 [[index[0] - i, index[1] + i] for i in range(1, 8)],
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    dontPutKingInCheck(board, index, board[index[0]][index[1]].team)
    return board

def bishop_moves_temp(index, board):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                 [[index[0] + i, index[1] - i] for i in range(1, 8)],
                 [[index[0] - i, index[1] + i] for i in range(1, 8)],
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                #print(convert_to_readable(board))
                if board[positions[0]][positions[1]] == '  ' or board[positions[0]][positions[1]] == 'x ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board


## applies the rook moves to the board then the bishop moves because a queen is basically a rook and bishop in the same position.
def queen_moves(index):
    board = rook_moves(index)
    board = bishop_moves(index)
    dontPutKingInCheck(board, index, board[index[0]][index[1]].team)
    return board

def queen_moves_temp(index, board):
    board = rook_moves_temp(index, board)
    board = bishop_moves_temp(index, board)
    return board


## Checks a 5x5 grid around the piece and uses pythagoras to see if if a move is valid. Valid moves will be a distance of sqrt(5) from centre
def knight_moves(index):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True
    dontPutKingInCheck(board, index, board[index[0]][index[1]].team)
    return board

def knight_moves_temp(index, board):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  '  or board[index[0] + i][index[1] + j] == 'x ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True
    #dontPutKingInCheck(board, index, board[index[0]][index[1]].team)
    return board


WIDTH = 400

WIN = pygame.display.set_mode((WIDTH, WIDTH))

""" This is creating the window that we are playing on, it takes a tuple argument which is the dimensions of the window so in this case 800 x 800px
"""

pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] == None:
                pass
            else:
                WIN.blit(starting_order[(self.row, self.col)], (self.x, self.y))

        """
        For now it is drawing a rectangle but eventually we are going to need it
        to use blit to draw the chess pieces instead
        """


def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY
    return grid
"""
This is creating the nodes thats are on the board(so the chess tiles)
I've put them into a 2d array which is identical to the dimesions of the chessboard
"""


def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

    """
    The nodes are all white so this we need to draw the grey lines that separate all the chess tiles
    from each other and that is what this function does"""


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)


def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE
        """
        Displays all the potential moves
        """


def Do_Move(OriginalPos, FinalPosition, WIN):
    starting_order[FinalPosition] = starting_order[OriginalPos]
    starting_order[OriginalPos] = None

    #en passant Exception
    if board[FinalPosition[1]][FinalPosition[0]].team == 'w':
        global blackPassant
        blackPassant = -10
    else:
        global whitePassant
        whitePassant = -10


def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid

"""this takes in 2 co-ordinate parameters which you can get as the position of the piece and then the position of the node it is moving to
you can get those co-ordinates using my old function for swap"""

create_board(board)
def resetPotential(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'x ':
                board[i][j] = '  '
    return board

def totalPoints(board):
    total = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] != 'x 'and board[i][j] != '  ':
                multipler = 1
                if board[i][j].team == 'b':
                    multipler = -1
                if board[i][j].type =='p':
                    total = total + (multipler * 1)
                elif board[i][j].type =='kn':
                    total = total + (multipler * 3)
                elif board[i][j].type =='b':
                    total = total + (multipler * 3)
                elif board[i][j].type =='r':
                    total = total + (multipler * 5)
                elif board[i][j].type =='q':
                    total = total + (multipler * 9)
    return total


def calculateMove(board, turnNum, flag):
    if turnNum % 2 == 0:
        team = 'w'
    else:
        team = 'b'
    moves = {}
    for i in range(8):
        for j in range(8):
            copyBoard = copy.deepcopy(board)
            if copyBoard[i][j] != 'x 'and copyBoard[i][j] != '  ':
                if copyBoard[i][j].team == team:
                    select_moves_temp(copyBoard[i][j], (i, j), copyBoard)
                    for c in range(8):
                        for d in range(8):
                            if copyBoard[c][d] == 'x ':
                                moves[((i, j), (c, d))] = 0
                            if copyBoard[c][d] != '  ' and copyBoard[c][d] != 'x ':
                                if copyBoard[c][d].killable == True:
                                    moves[((i, j), (c, d))] = 0
                    copyBoard = resetPotential(copyBoard)

    for move in moves:
        copyBoard[move[1][0]][move[1][1]] = copyBoard[move[0][0]][move[0][1]]
        copyBoard[move[0][0]][move[0][1]] = '  '
        if turnNum % 2 == 0:
            if availableMoves(copyBoard, 'w') is False:
                if isItCheck(copyBoard, 'b'):
                    moves[move] = -200
                moves[move] = 0
        else:
            if availableMoves(copyBoard, 'b') is False:
                if isItCheck(copyBoard, 'w'):
                    moves[move] = 200
                moves[move] = 0
        if flag > 0:
            moves[move] = calculateMove(copyBoard, turnNum + 1, flag - 1)
        else:
            moves[move] = totalPoints(copyBoard)
        copyBoard = copy.deepcopy(board)

    if team == 'w':
        return max(moves.values())
    else:
        return min(moves.values())

def computerTurn(board, turnNum):
    moves = {}
    for i in range(8):
        for j in range(8):
            copyBoard = copy.deepcopy(board)
            if copyBoard[i][j] != 'x 'and copyBoard[i][j] != '  ':
                if copyBoard[i][j].team == compPlayer:
                    select_moves_temp(copyBoard[i][j], (i, j), copyBoard)
                    for c in range(8):
                        for d in range(8):
                            if copyBoard[c][d] == 'x ':
                                moves[((i, j), (c, d))] = 0
                            if copyBoard[c][d] != '  ' and copyBoard[c][d] != 'x ':
                                if copyBoard[c][d].killable == True:
                                    moves[((i, j), (c, d))] = 0
                    copyBoard = resetPotential(copyBoard)

    for move in moves:
        copyBoard[move[1][0]][move[1][1]] = copyBoard[move[0][0]][move[0][1]]
        copyBoard[move[0][0]][move[0][1]] = '  '
        if turnNum % 2 == 0:
            if availableMoves(copyBoard, 'w') is False:
                if isItCheck(copyBoard, 'b'):
                    moves[move] = -200
                moves[move] = 0
        else:
            if availableMoves(copyBoard, 'b') is False:
                if isItCheck(copyBoard, 'w'):
                    moves[move] = 200
                moves[move] = 0
        moves[move] = calculateMove(copyBoard, turnNum + 1, 0)
        copyBoard = copy.deepcopy(board)
                    
    if compPlayer == 'w':
        return max(moves, key=moves.get)
    else:
        return min(moves, key=moves.get)

def main(WIN, WIDTH):
    print("HUMAN PLAYER IS ", humanPlayer, compPlayer)
    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(8, WIDTH)
    while True:
        pygame.time.delay(50) ##stops cpu dying
        if moves % 2 == 0 and compPlayer == 'w':
            ((row, col), (x, y)) = computerTurn(board, moves)
            board[x][y] = board[row][col]
            board[row][col] = '  '
            deselect()
            remove_highlight(grid)
            Do_Move((col, row), (y, x), WIN)
            moves += 1
            print(convert_to_readable(board))
            continue
        if moves % 2 == 1 and compPlayer == 'b':
            ((row, col), (x, y)) = computerTurn(board, moves)
            board[x][y] = board[row][col]
            board[row][col] = '  '
            deselect()
            remove_highlight(grid)
            Do_Move((col, row), (y, x), WIN)
            moves += 1
            print(convert_to_readable(board))
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """This quits the program if the player closes the window"""

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = Find_Node(pos, WIDTH)





                if selected == False:
                    try:
                        possible = select_moves((board[x][y]), (x,y), moves)
                        for positions in possible:
                            row, col = positions
                            grid[row][col].colour = BLUE
                        piece_to_move = x,y
                        selected = True
                    except:
                        piece_to_move = []
                        print('Can\'t select')
                    #print(piece_to_move)

                else:
                    try:
                        if board[x][y].killable == True:
                            row, col = piece_to_move ## coords of original piece
                            if board[row][col].type == 'p': 
                                if x == 0 or x == 7: # promote
                                    isValid = False
                                    while not isValid:
                                        newPiece = input("WHAT PIECE DO YOU WANT: ")
                                        if newPiece == "q" or newPiece == "r" or newPiece == "b" or newPiece == "kn":
                                            isValid = True
                                        else:
                                            print("THAT IS NOT A VALID PIECE! PLEASE CHOOSE AGAIN!")
                                    board[row][col].type = newPiece
                                    if board[row][col].team == 'w':
                                        if newPiece == "q":
                                            starting_order[(col, 1)] = pygame.transform.scale(pygame.image.load(wq.image), (50, 50))
                                        elif newPiece == "r":
                                            starting_order[(col, 1)] = pygame.transform.scale(pygame.image.load(wr.image), (50, 50))
                                        elif newPiece == "b":
                                            starting_order[(col, 1)] = pygame.transform.scale(pygame.image.load(wb.image), (50, 50))
                                        else:
                                            starting_order[(col, 1)] = pygame.transform.scale(pygame.image.load(wkn.image), (50, 50))
                                    else: 
                                        if newPiece == "q":
                                            starting_order[(col, 6)] = pygame.transform.scale(pygame.image.load(bq.image), (50, 50))
                                        elif newPiece == "r":
                                            starting_order[(col, 6)] = pygame.transform.scale(pygame.image.load(br.image), (50, 50))
                                        elif newPiece == "b":
                                            starting_order[(col, 6)] = pygame.transform.scale(pygame.image.load(bb.image), (50, 50))
                                        else:
                                            starting_order[(col, 6)] = pygame.transform.scale(pygame.image.load(bkn.image), (50, 50))
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)
                            Do_Move((col, row), (y, x), WIN)
                            moves += 1
                            print(convert_to_readable(board))
                        else: #click on same piece
                            deselect()
                            remove_highlight(grid)
                            selected = False
                            #board = resetPotential(board)
                            print("Deselected")
                    except:
                        if board[x][y] == 'x ':
                            row, col = piece_to_move

                            if board[row][col].type == 'p': #pawn exceptions
                                if abs(x - row) == 2: #en passant setup
                                    if board[row][col].team == 'w':
                                        global whitePassant
                                        whitePassant = col
                                    else: 
                                        global blackPassant
                                        blackPassant = col
                                
                                elif y != col and board[x][y] == 'x ': #remove pawn in case of en passant
                                    if board[row][col].team == 'w':
                                        board[x + 1][y] = '  '
                                        starting_order[(y, x+1)] = None
                                    else:
                                        board[x - 1][y] = '  '
                                        starting_order[(y, x-1)] = None
                                elif x == 0 or x == 7: # promote
                                    isValid = False
                                    while not isValid:
                                        newPiece = input("WHAT PIECE DO YOU WANT: ")
                                        if newPiece == "q" or newPiece == "r" or newPiece == "b" or newPiece == "kn":
                                            isValid = True
                                        else:
                                            print("THAT IS NOT A VALID PIECE! PLEASE CHOOSE AGAIN!")
                                    board[row][col].type = newPiece
                                    if board[row][col].team == 'w':
                                        if newPiece == "q":
                                            starting_order[(col, 1)] = pygame.transform.scale(pygame.image.load(wq.image), (50, 50))
                                        elif newPiece == "r":
                                            starting_order[(col, 1)] = pygame.transform.scale(pygame.image.load(wr.image), (50, 50))
                                        elif newPiece == "b":
                                            starting_order[(col, 1)] = pygame.transform.scale(pygame.image.load(wb.image), (50, 50))
                                        else:
                                            starting_order[(col, 1)] = pygame.transform.scale(pygame.image.load(wkn.image), (50, 50))
                                    else: 
                                        if newPiece == "q":
                                            starting_order[(col, 6)] = pygame.transform.scale(pygame.image.load(bq.image), (50, 50))
                                        elif newPiece == "r":
                                            starting_order[(col, 6)] = pygame.transform.scale(pygame.image.load(br.image), (50, 50))
                                        elif newPiece == "b":
                                            starting_order[(col, 6)] = pygame.transform.scale(pygame.image.load(bb.image), (50, 50))
                                        else:
                                            starting_order[(col, 6)] = pygame.transform.scale(pygame.image.load(bkn.image), (50, 50))
                            
                            elif board[row][col].type == 'k':
                                if abs(y -  col) == 2:
                                    if x == 7:
                                        global whiteCastle
                                        whiteCastle = True
                                        if y == 6:
                                            board[7][5] = board[7][7]
                                            board[7][7] = '  '
                                            starting_order[(7, 7)] = None
                                            starting_order[(5, 7)] = pygame.transform.scale(pygame.image.load(wr.image), (50, 50))
                                        elif y == 2:
                                            board[7][3] = board[7][0]
                                            board[7][0] = '  '
                                            starting_order[(0, 7)] = None
                                            starting_order[(3, 7)] = pygame.transform.scale(pygame.image.load(wr.image), (50, 50))
                                    elif x == 0:
                                        global blackCastle
                                        blackCastle = True
                                        if y == 6:
                                            board[0][5] = board[0][7]
                                            board[0][7] = '  '
                                            starting_order[(7, 0)] = None
                                            starting_order[(5, 0)] = pygame.transform.scale(pygame.image.load(br.image), (50, 50))
                                        elif y == 2:
                                            board[0][3] = board[0][0]
                                            board[0][0] = '  '
                                            starting_order[(0, 0)] = None
                                            starting_order[(3, 0)] = pygame.transform.scale(pygame.image.load(br.image), (50, 50))

                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)
                            Do_Move((col, row), (y, x), WIN)
                            moves += 1
                            #board = resetPotential(board)
                            print(convert_to_readable(board))
                        else:
                            deselect() #illegal move
                            remove_highlight(grid)
                            selected = False
                            print("Invalid move")
                    selected = False
                    
                    # print("TEAM IS ", board[x][y].team)
                    # for i in range(8):
                    #     for j in range(8):
                    #         if board[i][j] != '  ' and board[i][j] != 'x ':
                    #             if board[i][j].type == 'k':
                    #                 print("I AND J ARE", i, j)
                    #                 if board[i][j].killable == True:
                    #                     print("CHECK"
                if moves % 2 == 0:
                    if availableMoves(board, 'w') is False:
                        if isItCheck(board, 'b'):
                            print("BLACK WINS!")
                            return
                        print("STALEMATE!")
                        return
                else:
                    if availableMoves(board, 'b') is False:
                        if isItCheck(board, 'w'):
                            print("White WINS!")
                            return
                        print("STALEMATE!")
                        return
            
            update_display(WIN, grid, 8, WIDTH)
            

humanPlayer = sys.argv[1]
compPlayer = 'b'
if humanPlayer == 'b':
    compPlayer = 'w'


main(WIN, WIDTH)