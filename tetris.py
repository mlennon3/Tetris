import sys, random, time, pygame

WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = ( 20, 20,  155)
LIGHTBLUE   = ( 30, 30,  175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

colors = (BLUE, GREEN, RED, YELLOW)
light_colors = {BLUE: LIGHTBLUE, GREEN: LIGHTGREEN, RED: LIGHTRED, YELLOW: LIGHTYELLOW}


BLANK = '.'
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5
LEFTBORDER = 217
RIGHTBORDER = 420
BOARDTOP = WINDOWHEIGHT-(BOXSIZE*BOARDHEIGHT)
BOXBORDER = 3


DROPEVENTINT = pygame.USEREVENT+1
DROPEVENT = pygame.event.Event(DROPEVENTINT)

SETEVENTINT = pygame.USEREVENT+2
SETEVENT = pygame.event.Event(SETEVENTINT)

SLIDERIGHTEVENTINT = pygame.USEREVENT+3
SLIDERIGHTEVENT = pygame.event.Event(SLIDERIGHTEVENTINT)

SLIDELEFTEVENTINT = pygame.USEREVENT+4
SLIDELEFTEVENT = pygame.event.Event(SLIDELEFTEVENTINT)



I_TEMPLATE =  [['.....', 
                '..O..', 
                '..O..', 
                '..O..', 
                '..O..'],

                ['.....',
                 '.....', 
                 '.OOOO', 
                 '.....', 
                 '.....']]

S_TEMPLATE =  [['.....', 
                '..OO.', 
                '.OO..', 
                '.....', 
                '.....'],

                ['.....', 
                '..O..', 
                '..OO.', 
                '...O.', 
                '.....']]


Z_TEMPLATE =  [['.....', 
                '.OO..', 
                '..OO.', 
                '.....', 
                '.....'],

                ['.....', 
                '..O..', 
                '.OO..', 
                '.O...', 
                '.....']]

O_TEMPLATE =  [['.....', 
                '.OO..', 
                '.OO..', 
                '.....', 
                '.....']]

J_TEMPLATE =  [['.....', 
                '.O...', 
                '.OOO.', 
                '.....', 
                '.....'],

                ['.....', 
                '..O..', 
                '..O..', 
                '.OO..', 
                '.....'],

                ['.....', 
                '.OOO.', 
                '...O.', 
                '.....', 
                '.....'],

                ['.....', 
                '..OO.', 
                '..O..', 
                '..O..', 
                '.....']]


L_TEMPLATE =  [['.....', 
                '...O.', 
                '.OOO.', 
                '.....', 
                '.....'],

                ['.....', 
                '.OO..', 
                '..O..', 
                '..O..', 
                '.....'],

                ['.....', 
                '.OOO.', 
                '.O...', 
                '.....', 
                '.....'],

                ['.....', 
                '..O..', 
                '..O..', 
                '..OO.', 
                '.....']]

T_TEMPLATE =  [['.....', 
                '..O..', 
                '.OOO.', 
                '.....', 
                '.....'],

                ['.....', 
                '..O..', 
                '.OO..', 
                '..O..', 
                '.....'],

                ['.....', 
                '.....', 
                '.OOO.', 
                '..O..', 
                '.....'],

                ['.....', 
                '..O..', 
                '..OO.', 
                '..O..', 
                '.....']]

PIECES =   {'I': I_TEMPLATE,
            'S': S_TEMPLATE,
            'Z': Z_TEMPLATE,
            'O': O_TEMPLATE,
            'J': J_TEMPLATE,
            'L': L_TEMPLATE,
            'T': T_TEMPLATE}

def get_light_color(color):
    colors = {BLUE:LIGHTBLUE, GREEN:LIGHTGREEN, RED:LIGHTRED, YELLOW:LIGHTYELLOW}
    return colors[color]

def get_new_piece():
    #a piece is a dict with a 'shape', 'rotation', 'color'
    shape = random.choice(list(PIECES.keys()))
    # piece['x'] and piece['y'] are the number of lines the piece is offset.
    # 'x' starts on the board's left side and is anchored in the pieces left
    # 'y' starts on the board's top line and is anchored in the piece's top
    piece = {'shape': shape,
            'rotation_num' : 0,
            'rotation': PIECES[shape][0],
            'color': random.choice(colors),
            'x': -8,
            'y': -2}
    return piece

def next_piece_to_board(piece):
    piece['x'] = 4
    piece['y'] = -1
    return piece

def read_piece_template(piece):
    rotation = piece['rotation']
    occupied_spaces = []
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if rotation[y][x] != BLANK:
                occupied_spaces.append((x,y))
    return occupied_spaces

def draw_piece(piece, next_piece=False):
    occupied_spaces = read_piece_template(piece)
    #print occupied_spaces
    for (x,y) in occupied_spaces:
        draw_box(piece['color'], piece['x'] + x, piece['y'] + y, next_piece)


def draw_box(color, x, y, next_piece=False):
    # The piece would be above the board, unless the function is passed
    # that the piece will be displayed in the next piece box
    if y <= -1 and not next_piece:
        return

    x,y = board_offset_to_window_pixels(x,y)

    light_color = light_colors[color]
    box_rect = pygame.Rect(x, y, BOXSIZE-BOXBORDER, BOXSIZE-BOXBORDER)
    pygame.draw.rect(DISPLAYSURF, light_color, box_rect)
    pygame.draw.rect(DISPLAYSURF, color, box_rect, BOXBORDER)

def board_offset_to_window_pixels(x, y):
    # Pieces' and board locations are stored as x,y, where x and y correspond
    # to the rows and columns of the tetris board.  This function inputs that
    # and outputs the pixel locations of those pieces or board locations
    x = LEFTBORDER - BOXSIZE + BOXBORDER + (x * BOXSIZE)
    y = BOARDTOP + (y * BOXSIZE)
    return x,y

def get_board_spaces(piece):
    # Outputs a list of a piece's box's locations on the board 
    board_spaces = []
    rotation_boxes = read_piece_template(piece)
    for (x, y) in rotation_boxes:
        board_spaces.append((piece['x'] + x-1, piece['y'] + y))
    #print board_spaces
    return board_spaces

def copy_piece(piece):
    newpiece = {'shape': piece['shape'],
        'rotation_num' : piece['rotation_num'],
        'rotation': piece['rotation'],
        'color': piece['color'],
        'x': piece['x'],
        'y': piece['y']}
    return newpiece


def is_valid_move(piece, board, move):
    # Check if space is within gameboard boundries
    if not piece:
        return False
    if not move:
        return True
    newpiece = copy_piece(piece)

    if move == 'right':
        newpiece['x'] += 1

    elif move == 'left':
        newpiece['x'] -= 1

    elif move == 'rot':
        newpiece['rotation_num'] = (newpiece['rotation_num']+1) %len(PIECES[newpiece['shape']])
        newpiece['rotation'] = PIECES[newpiece['shape']][newpiece['rotation_num']]
    else:
        #print 'first tree else'
        return False

    board_spaces = get_board_spaces(newpiece)

    for (x, y) in board_spaces:
        if x < 0:
            return False
        if x >= BOARDWIDTH:
            return False
        if y >= BOARDHEIGHT:
            return False
        # Needs to check if space is previously occupied
        if board[y][x] != BLANK:
            return False
    return True

def is_at_bottom(piece, board):
    # Returns whether a piece should be stopped from descending
    piece_spaces = get_board_spaces(piece)

    for x,y in piece_spaces:
        if y >= BOARDHEIGHT-1:
            return True

        #print board
        if board[y+1][x] != BLANK:
            #print board[y+1]
            return True
    return False

def are_lines_full(board):
    # Checks for lines completed across the board
    full_lines = []
    for y in range(len(board)):
        if BLANK not in board[y]:
            full_lines.append(y)
    if full_lines != []: return full_lines
    return False


def clear_lines(full_lines, board):
    # Clears lines from the gameboard
    for line in full_lines:
        board.remove(board[line])
        board.insert(0,['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'])
        #for above_line in range(line-1)[::-1]:
        #    print above_line
        #   board[line] = board[above_line]
    return board


def check_for_quit():
    if pygame.event.get(pygame.QUIT):
        terminate()

def play_again():
    # Displays "Game Over" and prompts the player to play again
    myfont = pygame.font.SysFont("monospace", 50)
    game_over = myfont.render("Game Over", 1, GRAY)
    DISPLAYSURF.blit(game_over, (200,20))
    again1 = myfont.render("Play again?", 1, GRAY)
    again2 = myfont.render("Any key for yes", 1, GRAY)
    DISPLAYSURF.blit(again1, (160,300))
    DISPLAYSURF.blit(again2, (100, 360))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return True
        check_for_quit()



def draw_board(board):
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH):
            color = board[y][x]
            if color != BLANK:
                draw_box(color, x+1, y)


def draw_border():
    pygame.draw.line(DISPLAYSURF, BLUE, (LEFTBORDER, BOARDTOP), (LEFTBORDER, WINDOWHEIGHT), 3)
    pygame.draw.line(DISPLAYSURF, BLUE, (RIGHTBORDER, BOARDTOP), (RIGHTBORDER, WINDOWHEIGHT), 3)
    pygame.draw.line(DISPLAYSURF, BLUE, (LEFTBORDER, BOARDTOP), (RIGHTBORDER, BOARDTOP), 3)

    pygame.draw.rect(DISPLAYSURF, BLUE, (35, 40, BOXSIZE*TEMPLATEWIDTH+8,
                                     BOXSIZE*TEMPLATEHEIGHT+8), 3)

def draw_score(score, lines, level):
    myfont = pygame.font.SysFont("monospace", 15)
    scoretext = myfont.render("Score:"+str(score), 1, GRAY)
    DISPLAYSURF.blit(scoretext, (WINDOWWIDTH - 100, 50))

    linestext = myfont.render("Lines:"+str(lines), 1, GRAY)
    DISPLAYSURF.blit(linestext, (WINDOWWIDTH - 100, 80))

    leveltext = myfont.render("Level:"+str(level), 1, GRAY)
    DISPLAYSURF.blit(leveltext, (WINDOWWIDTH-100, 110))


def terminate():
    pygame.quit()
    sys.exit()

def main():
    global DISPLAYSURF
    pygame.init()
    pygame.font.init()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    while True:
        check_for_quit()
        run_game()

        if play_again():
            continue
        else:
            terminate()


def run_game():

    def slide_right(falling_piece):
        if is_valid_move(falling_piece, board, 'right'):
            falling_piece['x'] += 1
            DISPLAYSURF.fill(BLACK)
            draw_piece(falling_piece)
        else:
            sliding_right = False


    def slide_left(falling_piece):
        if is_valid_move(falling_piece, board, 'left'):
            falling_piece['x'] -= 1
            DISPLAYSURF.fill(BLACK)
            draw_piece(falling_piece)
        else:
            sliding_left = False

    #must simply return when game is over
    check_for_quit()
    falling_piece = next_piece_to_board(get_new_piece())
    next_piece = get_new_piece()
    draw_piece(falling_piece)

    drop_time = 500
    score = 0
    lines = 0
    level = 1
    sliding_right = False
    sliding_left = False
    board = []

    for x in range(BOARDHEIGHT):
        board.append(['.']*BOARDWIDTH)

    # Lets the pieces start falling
    pygame.time.set_timer(DROPEVENTINT, drop_time)

    while True:
        check_for_quit()

        if not falling_piece:
            falling_piece = next_piece_to_board(next_piece)
            next_piece = get_new_piece()
            DISPLAYSURF.fill(BLACK)
            draw_piece(falling_piece)
            if is_at_bottom(falling_piece, board):
                draw_border()
                draw_board(board)
                pygame.display.update()
                # Game Over
                return


        for event in pygame.event.get():

            if event.type == SLIDERIGHTEVENT:
                slide_right(falling_piece)

            if event.type == SLIDELEFTEVENT:
                slide_left(falling_piece)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    sliding_right = False
                    # Disable the slide timer
                    pygame.time.set_timer(SLIDERIGHTEVENTINT, 0)
                if event.key == pygame.K_LEFT:
                    sliding_left = False
                    # Disable the slide timer
                    pygame.time.set_timer(SLIDELEFTEVENTINT, 0)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    sliding_right = True
                    slide_right(falling_piece)

                elif event.key == pygame.K_LEFT:
                    sliding_left = True
                    slide_left(falling_piece)

                elif event.key == pygame.K_DOWN:
                    # Reset drop time to prevent doubles
                    pygame.time.set_timer(DROPEVENTINT, drop_time)
                    pygame.event.post(DROPEVENT)

                
                elif event.key == pygame.K_UP:
                    if is_valid_move(falling_piece, board, 'rot'):
                        falling_piece['rotation_num'] = (falling_piece['rotation_num']+1) %len(PIECES[falling_piece['shape']])
                        falling_piece['rotation'] = PIECES[falling_piece['shape']][falling_piece['rotation_num']]
                        DISPLAYSURF.fill(BLACK)
                        draw_piece(falling_piece)
            elif event.type == DROPEVENTINT:
                if not is_at_bottom(falling_piece, board):
                    falling_piece['y'] += 1
                    DISPLAYSURF.fill(BLACK)
                    draw_piece(falling_piece)


                else:    
                    # Sets the piece into the board
                    pygame.event.post(SETEVENT)

            elif event.type == SETEVENTINT:
                for (x,y) in get_board_spaces(falling_piece):
                    board[y][x] = falling_piece['color']

                full_lines = are_lines_full(board)
                if full_lines:
                    if len(full_lines) == 4:
                        score += level * 100
                    score += level * 10 *len(full_lines)
                    board = clear_lines(full_lines, board)
                    lines += len(full_lines)
                    if lines % 10 == 0:
                        level += 1
                        drop_time *- 0.9
                falling_piece = None

            elif event.type == SLIDERIGHTEVENTINT:
                slide_right(falling_piece)

            elif event.type == SLIDELEFTEVENTINT:
                slide_left(falling_piece)

            if sliding_right:
                pygame.time.set_timer(SLIDERIGHTEVENTINT, 150)

            if sliding_left:
                pygame.time.set_timer(SLIDELEFTEVENTINT, 150)


        draw_piece(next_piece, True)
        draw_border()
        draw_board(board)
        draw_score(score, lines, level)
        pygame.display.update()



main()

