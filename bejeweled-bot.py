#!/usr/bin/python
# -*- coding: ascii -*-
'''
Plays a game of Bejeweled Blitz on Facebook.

Created on 24.12.2012
@author: adrianus
'''

import autopy as ap
import time
import sys
import pygame

### constants ###
    SLEEPING_TIME = 0.02
    MAX_MOVES = 5

### input helpers ###

def left_down():
    ap.mouse.toggle(True, ap.mouse.LEFT_BUTTON)
    time.sleep(SLEEPING_TIME)

def left_up():
    ap.mouse.toggle(False, ap.mouse.LEFT_BUTTON)
    time.sleep(SLEEPING_TIME)

def move_mouse(x, y):
    x, y = board_to_pixel(x, y)
    ap.mouse.move(int(x), int(y))
    time.sleep(SLEEPING_TIME)

def click(x, y):
    move_mouse(x, y)
    left_down()
    left_up()
    
def move_fields(x0, y0, x1, y1):
    global moves
    move_mouse(x0, y0)
    left_down()
    move_mouse(x1, y1)
    left_up()
    moves += 1

### screen helpers ###

def get_pixel(x, y):
    return ap.color.hex_to_rgb(ap.screen.get_color(x, y))

def get_field(x, y):
    x, y = board_to_pixel(x, y)
    return ap.color.hex_to_rgb(ap.screen.get_color(x, y))

def get_board():
    board = []
    for y in range(0, 8):
        board.append([])
        for x in range(0, 8):
            pix = get_field(x, y)
            color = match_color(pix)
            board[y].append(color)
    return board
    
def match_color(pix):
    names = ['y', 'w', 'r', 'o', 'p', 'g', 'b', 'X', 'g', 'y', 
             'y', 'g', 'b', 'w', 'g', 'r', 'p', 'p', 'o', 'p', 'b']
    colors = [(254, 254, 38), (254, 254, 254), (254, 29, 59),
              (254, 254, 137), (250, 10, 250), (98, 254, 156),
              (20, 112, 232), (114, 186, 112), (0, 168, 10),
              (254, 247, 67), (255, 255, 102), (206, 255, 255), 
              (44, 156, 252), (211, 211, 211),  (0, 94, 6),
              (215, 17, 30), (185, 16, 184), (217, 19, 216),
              (252, 126, 44), (255, 73, 255), (21, 74, 120)]
    c = 0
    for color in colors:
        diff = 0
        for i in range(3):
            diff += abs(color[i]-pix[i])
        if diff < 60:
            return names[c]
        c += 1
    return '.'

def board_to_pixel(x, y):
    x = x*40 + 195 + anchor[0]
    y = y*40 + 70 + anchor[1]
    return x, y

def same_gem(x0, y0, x1, y1):
    m = 7 # max row
    if x0 < 0 or y0 < 0 or x1 < 0 or y1 < 0 or x0 > m or y0 > m or x1 > m or y1 > m:
        return False
    elif board[y0][x0] == '.' or board[y1][x1] == '.':
        return False
    elif board[y0][x0] == 'X' or board[y1][x1] == 'X':
        return True
    else:
        return board[y0][x0] == board[y1][x1]

def board_valid(board):
    whites = 0
    for line in board:
        for field in line:
            if field == 'w':
                whites += 1
    if whites >= 20:
        return False
    else:
        return True

### canvas helpers ###
    
def draw_board():
    board_size = [320, 320]
    colors = {'y': (254, 254, 38), 'w': (254, 254, 254), 'r': (254, 29, 59),
              'o': (254, 128, 0),  'p': (250, 10, 250),  'g': (50, 254, 50),
              'b': (20, 112, 232), 'X': (114, 186, 112), '.': (0, 0, 0)}
    signs = []
    for line in board:
        for sign in line:
            signs.append(sign)
    
    for y in range(8):
        for x in range(8):
            col = colors[board[y][x]]
            pygame.draw.rect(disp, col, (x*40, y*40, 40, 40))
    pygame.display.flip()

### main ###
    
def main():
    global anchor
    global disp 
    global rects
    global moves
    global board
	
    # detect anchors
    screen = ap.screen.get_size()
    x = y = 0
    for i in range(screen[0]):
        if x == 0 and get_pixel(i, screen[1]/2) == (199, 199, 199):
            x = i
        if y == 0 and get_pixel(screen[0]/3, i) == (215, 215, 215):
            y = i
        if x != 0 and y != 0:
            anchor = (x, y)
            break
    print "Detected anchor:", anchor
    
    # preparing canvas
    pygame.init()
    disp = pygame.display.set_mode([320, 320])
    pygame.display.set_caption("Bejeweled Blitz Demo")

	# play
    print "Starting game!"
    time.sleep(5)
    click(2, 7) # "play now"
    time.sleep(1)

    while True:
        if get_field(2, 4) == (60, 109, 118) or not board_valid(board):
            break # "time up"
        board = get_board()
        draw_board()
        
        # calculate possible moves
        moves = 0
        for y in range(0, 8):
            if moves >= MAX_MOVES: break
            for x in range(0, 8):
                if moves >= MAX_MOVES: break
                if same_gem(x, y, x-1, y): # two gems next to each other, horizontal
                    if same_gem(x, y, x+1, y-1): move_fields(x+1, y, x+1, y-1, 'a') # right
                    if same_gem(x, y, x+2, y): move_fields(x+1, y, x+2, y, 'b')
                    if same_gem(x, y, x+1, y+1): move_fields(x+1, y, x+1, y+1, 'c')
                    if same_gem(x, y, x-2, y-1): move_fields(x-2, y, x-2, y-1, 'd') # left
                    if same_gem(x, y, x-2, y+1): move_fields(x-2, y, x-2, y+1, 'e')
                    if same_gem(x, y, x-3, y): move_fields(x-2, y, x-3, y, 'f')
                if same_gem(x, y, x, y-1): # two gems next to each other, vertical
                    if same_gem(x, y, x+1, y+1): move_fields(x, y+1, x+1, y+1, 'g') # below
                    if same_gem(x, y, x, y+2): move_fields(x, y+1, x, y+2, 'h')
                    if same_gem(x, y, x-1, y+1): move_fields(x, y+1, x-1, y+1, 'i')
                    if same_gem(x, y, x-1, y-2): move_fields(x, y-2, x-1, y-2, 'j') # above
                    if same_gem(x, y, x+1, y-2): move_fields(x, y-2, x+1, y-2, 'k')
                    if same_gem(x, y, x, y-3): move_fields(x, y-2, x, y-3, 'l')
                if same_gem(x, y, x-2, y): # gem in the middle is missing, horizontal
                    if same_gem(x, y, x-1, y-1): move_fields(x-1, y, x-1, y-1, 'm')
                    if same_gem(x, y, x-1, y+1): move_fields(x-1, y, x-1, y+1, 'n')
                if same_gem(x, y, x, y-2): # gem in the middle is missing, vertical
                    if same_gem(x, y, x-1, y-1): move_fields(x, y-1, x-1, y-1, 'o')
                    if same_gem(x, y, x+1, y-1): move_fields(x, y-1, x+1, y-1, 'p')
					
    print "Game ended."
    
if __name__ == "__main__":
    main()