<<<<<<< HEAD
import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
from Variable import *


class Board:

    def __init__(self, screen):
        self.screen = screen
        self.width = Size.field_width
        self.height = Size.field_height
        self.block_size = Size.block_size
        self.init_board()
        self.generate_piece()

    def init_board(self):
        self.board = []
        self.score = Set.init_score
        self.level = Set.init_level
        self.goal = Set.init_goal
        self.skill = Set.init_skill
        for _ in range(self.height):
            self.board.append([Set.empty_board]*self.width)

    def generate_piece(self):
        self.piece = Piece()
        self.next_piece = Piece()
        self.piece_x, self.piece_y = Set.create_location_x,Set.create_location_y

    def nextpiece(self):
        self.piece = self.next_piece
        self.next_piece = Piece()
        self.piece_x, self.piece_y = Set.create_location_x,Set.create_location_y

    def absorb_piece(self):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.nextpiece()
        self.score += self.level
        if self.skill < 100:
            self.skill += 2

    def block_collide_with_board(self, x, y):
        if x < 0:
            return Error_Type.COLLIDE_ERROR['left_wall']
        elif x >= self.width:
            return Error_Type.COLLIDE_ERROR['right_wall']
        elif y >= self.height:
            return Error_Type.COLLIDE_ERROR['bottom']
        elif self.board[y][x]:
            return Error_Type.COLLIDE_ERROR['overlap']
        return Error_Type.COLLIDE_ERROR['no_error']

    def collide_with_board(self, dx, dy):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return Error_Type.COLLIDE_ERROR['no_error']

    def can_move_piece(self, dx, dy):
        _dx = self.piece_x + dx
        _dy = self.piece_y + dy
        if self.collide_with_board(dx = _dx, dy = _dy):
            return False
        return True

    def can_drop_piece(self):
        return self.can_move_piece(dx=0, dy=1)

    def try_rotate_piece(self, clockwise=True):
        self.piece.rotate(clockwise)
        collide = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        if not collide:
            pass
        elif collide == Error_Type.COLLIDE_ERROR['left_wall']:
            if self.can_move_piece(dx=1, dy=0):
                self.move_piece(dx=1, dy=0)
            elif self.can_move_piece(dx=2, dy=0):
                self.move_piece(dx=2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        elif collide == Error_Type.COLLIDE_ERROR['right_wall']:
            if self.can_move_piece(dx=-1, dy=0):
                self.move_piece(dx=-1, dy=0)
            elif self.can_move_piece(dx=-2, dy=0):
                self.move_piece(dx=-2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        else:
            self.piece.rotate(not clockwise)

    def move_piece(self, dx, dy):
        if self.can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def drop_piece(self):
        if self.can_drop_piece():
            self.move_piece(dx=0, dy=1)
        else:
            self.absorb_piece()
            self.delete_lines()

    def full_drop_piece(self):
        while self.can_drop_piece():
            self.drop_piece()
        self.drop_piece()

    def rotate_piece(self, clockwise=True):
        self.try_rotate_piece(clockwise)

    def pos_to_pixel(self, x, y):
        return self.block_size*x, self.block_size*(y-2)

    def pos_to_pixel_next(self, x, y):
        return self.block_size*x*0.6, self.block_size*(y-2)*0.6

    def delete_line(self, y):
        for y in reversed(range(1, y+1)):
            self.board[y] = list(self.board[y-1])

    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        for y in remove:
            line_sound = pygame.mixer.Sound("assets/sounds/Line_Clear.wav")
            line_sound.play()
            self.delete_line(y)
            self.score += 10 * self.level
            self.goal -= 1
            if self.goal == 0:
                if self.level < 10:
                    self.level += 1
                    self.goal = 5 * self.level
                else:
                    self.goal = '-'
            if self.level <= 9:
                pygame.time.set_timer(pygame.USEREVENT, (500 - 50 * (self.level-1)))
            else:
                pygame.time.set_time(pygame.USEREVENT, 100)

    def game_over(self):
        return sum(self.board[0]) > 0 or sum(self.board[1]) > 0

    def draw_blocks(self, array2d, color=Color.WHITE, dx=0, dy=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)
                        tmp = 1
                        while self.can_move_piece(0, tmp):
                            tmp += 1
                        x_s, y_s = self.pos_to_pixel(x, y+tmp-1)

                        pygame.draw.rect(self.screen, self.piece.T_COLOR[block-1],
                                        (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Color.BLACK,
                                        (x_pix, y_pix, self.block_size, self.block_size), 1)

    def draw_shadow(self, array2d, dx, dy): #그림자 기능 함수 추가
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.height:
                for x, block in enumerate(row):
                    x += dx
                    if block:
                        tmp = 1
                        while self.can_move_piece(0,tmp):
                            tmp += 1
                        x_s, y_s = self.pos_to_pixel(x,y + tmp - 1)

                        pygame.draw.rect(self.screen, self.piece.T_COLOR[7],
                                         (x_s, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Color.BLACK,
                                         (x_s, y_s, self.block_size, self.block_size),1)

    def draw_next_piece(self, array2d, color=Color.WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, self.piece.T_COLOR[block-1],
                                    (x_pix+240, y_pix+65, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, Color.BLACK,
                                    (x_pix+240, y_pix+65, self.block_size * 0.5, self.block_size * 0.5),1)

    def draw(self):
        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M:%S')
        self.screen.fill(Color.BLACK)
        for x in range(self.width):
            for y in range(self.height):
                x_pix, y_pix = self.pos_to_pixel(x, y)
                pygame.draw.rect(self.screen, (26,26,26),
                 (x_pix, y_pix, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, Color.BLACK,
                 (x_pix, y_pix, self.block_size, self.block_size),1)
        self.draw_shadow(self.piece, dx=self.piece_x,dy=self.piece_y) #그림자 기능 추가
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.board)
        pygame.draw.rect(self.screen, Color.WHITE, Rect(250, 0, 350, 450)) # 게임시 옆에 흰색 바탕 관련 코드
        self.draw_next_piece(self.next_piece)
        next_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('NEXT', True, Color.BLACK)
        skill_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SKILL', True, Color.BLACK)
        skill_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.skill)+'%', True, Color.BLACK)
        score_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SCORE', True, Color.BLACK)
        score_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.score), True, Color.BLACK)
        level_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('LEVEL', True, Color.BLACK)
        level_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.level), True, Color.BLACK)
        goal_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('GOAL', True, Color.BLACK)
        goal_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.goal), True, Color.BLACK)
        time_text = pygame.font.Font('assets/Roboto-Bold.ttf', 14).render(str(nowTime), True, Color.BLACK)
        self.screen.blit(next_text, (255, 20))
        self.screen.blit(skill_text, (255, 120))
        self.screen.blit(skill_value, (255, 145))
        self.screen.blit(score_text, (255, 200))
        self.screen.blit(score_value, (255,225))
        self.screen.blit(level_text, (255, 275))
        self.screen.blit(level_value, (255,300))
        self.screen.blit(goal_text, (255, 350))
        self.screen.blit(goal_value, (255,375))
        self.screen.blit(time_text, (255, 430))

    def pause(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Paused', True, Color.GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press p to continue', True, Color.GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p:
                    running = False

    def GameOver(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Game over', True, Color.GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Color.GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False

    def newGame(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Tetris', True, Color.GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Color.GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.fill(Color.BLACK)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False

    def HS(self, txt="no"):
        if txt != "no":
            fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
            textSurfaceObj = fontObj.render('HighScore : '+txt, True, Color.GREEN)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (175, 185)
            fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
            textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Color.GREEN)
            textRectObj2 = textSurfaceObj2.get_rect()
            textRectObj2.center = (175, 235)
            self.screen.fill(Color.BLACK)
            self.screen.blit(textSurfaceObj, textRectObj)
            self.screen.blit(textSurfaceObj2, textRectObj2)
            pygame.display.update()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        running = False

    def ultimate(self):
        if self.skill == 100:
            bomb = pygame.image.load("assets/images/bomb.jpg")
            bomb = pygame.transform.scale(bomb, (350, 450))
            bomb_sound = pygame.mixer.Sound('assets/sounds/bomb.wav')
            self.screen.blit(bomb, (0, 0))
            pygame.display.update()
            bomb_sound.play()
            time.sleep(1)
            self.board = []
            self.skill = 0
            for _ in range(self.height):
                self.board.append([0]*self.width)
=======
import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
from Variable import *


class Board:

    def __init__(self, screen):
        self.screen = screen
        self.width = Size.field_width
        self.height = Size.field_height
        self.block_size = Size.block_size
        self.init_board()
        self.generate_piece()

    def init_board(self):
        self.board = []
        self.score = Set.init_score
        self.level = Set.init_level
        self.goal = Set.init_goal
        self.skill = Set.init_skill
        for _ in range(self.height):
            self.board.append([Set.empty_board]*self.width)

    def generate_piece(self):
        self.piece = Piece()
        self.next_piece = Piece()
        self.piece_x, self.piece_y = Set.create_location_x,Set.create_location_y

    def nextpiece(self):
        self.piece = self.next_piece
        self.next_piece = Piece()
        self.piece_x, self.piece_y = Set.create_location_x,Set.create_location_y

    def absorb_piece(self):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.nextpiece()
        self.score += self.level
        if self.skill < 100:
            self.skill += 2

    def block_collide_with_board(self, x, y):
        if x < Set.left_wall_x:
            return Error_Type.COLLIDE_ERROR['left_wall']
        elif x >= self.width:
            return Error_Type.COLLIDE_ERROR['right_wall']
        elif y >= self.height:
            return Error_Type.COLLIDE_ERROR['bottom']
        elif self.board[y][x]:
            return Error_Type.COLLIDE_ERROR['overlap']
        return Error_Type.COLLIDE_ERROR['no_error']

    def collide_with_board(self, dx, dy):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return Error_Type.COLLIDE_ERROR['no_error']

    def can_move_piece(self, dx, dy):
        _dx = self.piece_x + dx
        _dy = self.piece_y + dy
        if self.collide_with_board(dx = _dx, dy = _dy):
            return False
        return True

    def can_drop_piece(self):
        return self.can_move_piece(dx=Set.keep_state, dy=Set.plus_one)

    def try_rotate_piece(self, clockwise=True):
        self.piece.rotate(clockwise)
        collide = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        if not collide:
            pass
        elif collide == Error_Type.COLLIDE_ERROR['left_wall']:
            if self.can_move_piece(dx=Set.plus_one, dy=Set.keep_state):
                self.move_piece(dx=Set.plus_one, dy=Set.keep_state)
            elif self.can_move_piece(dx=Set.plus_two, dy=Set.keep_state):
                self.move_piece(dx=Set.plus_two, dy=Set.keep_state)
            else:
                self.piece.rotate(not clockwise)
        elif collide == Error_Type.COLLIDE_ERROR['right_wall']:
            if self.can_move_piece(dx=-Set.plus_one, dy=Set.keep_state):
                self.move_piece(dx=-Set.plus_one, dy=Set.keep_state)
            elif self.can_move_piece(dx=-Set.plus_two, dy=Set.keep_state):
                self.move_piece(dx=-Set.plus_two, dy=Set.keep_state)
            else:
                self.piece.rotate(not clockwise)
        else:
            self.piece.rotate(not clockwise)

    def move_piece(self, dx, dy):
        if self.can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def drop_piece(self):
        if self.can_drop_piece():
            self.move_piece(dx=Set.keep_state, dy=Set.plus_one)
        else:
            self.absorb_piece()
            self.delete_lines()

    def full_drop_piece(self):
        while self.can_drop_piece():
            self.drop_piece()
        self.drop_piece()

    def rotate_piece(self, clockwise=True):
        self.try_rotate_piece(clockwise)

    def pos_to_pixel(self, x, y):
        return self.block_size*x, self.block_size*(y-Set.hidden_lines)

    def pos_to_pixel_next(self, x, y):
        return self.block_size*x*Size.next_block_ratio, self.block_size*(y-Set.hidden_lines)*Size.next_block_ratio

    def delete_line(self, y):
        for y in reversed(range(Set.first_line_index_y, y+Set.dummy_one)):
            self.board[y] = list(self.board[y-1])

    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        for y in remove:
            line_sound = pygame.mixer.Sound("assets/sounds/Line_Clear.wav")
            line_sound.play()
            self.delete_line(y)
            self.score += Set.delete_score * self.level
            self.goal -= Set.delete_goal
            if self.goal == Set.success_goal:
                if self.level < Set.max_level:
                    self.level += Set.plus_level
                    self.goal = Set.init_goal * self.level
                else:
                    self.goal = '-'
            if self.level < Set.max_level:
                pygame.time.set_timer(pygame.USEREVENT, (500 - 50 * (self.level-1)))
            else:
                pygame.time.set_time(pygame.USEREVENT, 100)

    def game_over(self):
        return sum(self.board[Set.board_first]) > Set.empty_board or sum(self.board[Set.board_second]) > Set.empty_board

    def draw_blocks(self, array2d, color=Color.WHITE, dx=0, dy=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= Set.board_third and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)

                        pygame.draw.rect(self.screen, self.piece.T_COLOR[block-1],
                                        (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Color.BLACK,
                                        (x_pix, y_pix, self.block_size, self.block_size), Set.block_border_thickness)

    def draw_shadow(self, array2d, dx, dy): #그림자 기능 함수 추가
        for y, row in enumerate(array2d):
            y += dy
            if y >= Set.board_first and y < self.height:
                for x, block in enumerate(row):
                    x += dx
                    if block:
                        tmp = Set.plus_one
                        while self.can_move_piece(0,tmp):
                            tmp += Set.plus_one
                        x_s, y_s = self.pos_to_pixel(x,y + tmp - 1)

                        pygame.draw.rect(self.screen, self.piece.T_COLOR[7],
                                         (x_s, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Color.BLACK,
                                         (x_s, y_s, self.block_size, self.block_size),Set.block_border_thickness)

    def draw_next_piece(self, array2d, color=Color.WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, self.piece.T_COLOR[block-1],
                                    (x_pix+240, y_pix+65, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, Color.BLACK,
                                    (x_pix+240, y_pix+65, self.block_size * 0.5, self.block_size * 0.5),1)

    def draw(self):
        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M:%S')
        self.screen.fill(Color.BLACK)
        for x in range(self.width):
            for y in range(self.height):
                x_pix, y_pix = self.pos_to_pixel(x, y)
                pygame.draw.rect(self.screen, (26,26,26),
                 (x_pix, y_pix, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, Color.BLACK,

                 (x_pix, y_pix, self.block_size, self.block_size),1)

        self.draw_shadow(self.piece, dx=self.piece_x,dy=self.piece_y) #그림자 기능 추가
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.board)

        pygame.draw.rect(self.screen, Color.WHITE, Rect(250, 0, 350, 450)) # 게임시 옆에 흰색 바탕 관련 코드
        self.draw_next_piece(self.next_piece)
        next_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('NEXT', True, Color.BLACK)
        skill_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SKILL', True, Color.BLACK)
        skill_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.skill)+'%', True, Color.BLACK)
        score_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SCORE', True, Color.BLACK)
        score_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.score), True, Color.BLACK)
        level_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('LEVEL', True, Color.BLACK)
        level_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.level), True, Color.BLACK)
        goal_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('GOAL', True, Color.BLACK)
        goal_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.goal), True, Color.BLACK)
        time_text = pygame.font.Font('assets/Roboto-Bold.ttf', 14).render(str(nowTime), True, Color.BLACK)
        self.screen.blit(next_text, (255, 20))
        self.screen.blit(skill_text, (255, 120))
        self.screen.blit(skill_value, (255, 145))
        self.screen.blit(score_text, (255, 200))
        self.screen.blit(score_value, (255,225))
        self.screen.blit(level_text, (255, 275))
        self.screen.blit(level_value, (255,300))
        self.screen.blit(goal_text, (255, 350))
        self.screen.blit(goal_value, (255,375))
        self.screen.blit(time_text, (255, 430))

    def pause(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Paused', True, Color.GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press p to continue', True, Color.GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p:
                    running = False

    def GameOver(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Game over', True, Color.GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Color.GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False

    def newGame(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Tetris', True, Color.GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Color.GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.fill(Color.BLACK)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False

    def HS(self, txt="no"):
        if txt != "no":
            fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
            textSurfaceObj = fontObj.render('HighScore : '+txt, True, Color.GREEN)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (175, 185)
            fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
            textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Color.GREEN)
            textRectObj2 = textSurfaceObj2.get_rect()
            textRectObj2.center = (175, 235)
            self.screen.fill(Color.BLACK)
            self.screen.blit(textSurfaceObj, textRectObj)
            self.screen.blit(textSurfaceObj2, textRectObj2)
            pygame.display.update()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        running = False

    def ultimate(self):
        if self.skill == 100:
            bomb = pygame.image.load("assets/images/bomb.jpg")
            bomb = pygame.transform.scale(bomb, (350, 450))
            bomb_sound = pygame.mixer.Sound('assets/sounds/bomb.wav')
            self.screen.blit(bomb, (0, 0))
            pygame.display.update()
            bomb_sound.play()
            time.sleep(1)
            self.board = []
            self.skill = 0
            for _ in range(self.height):
                self.board.append([0]*self.width)
>>>>>>> 62d6f72fc4509bd3c6ef90c717586197b97b02c5
