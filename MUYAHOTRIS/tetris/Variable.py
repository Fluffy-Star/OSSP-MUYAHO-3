import pygame
import pygame_menu
import random
import os

class Error_Type:
    COLLIDE_ERROR = {'no_error': 0, 'right_wall': 1, 'left_wall': 2, 'bottom': 3, 'overlap': 4}

class Color:
    #               R    G    B
    WHITE = (255, 255, 255)
    GRAY = (185, 185, 185)
    BLACK = (0, 0, 0)
    RED = (155, 0, 0)
    LIGHTRED = (175, 20, 20)
    GREEN = (0, 155, 0)
    LIGHTGREEN = (20, 175, 20)
    BLUE = (0, 0, 155)
    LIGHTBLUE = (20, 20, 175)
    YELLOW = (155, 155, 0)
    LIGHTYELLOW = (175, 175, 20)

class Size:
    field_width = 10  # 맵의 좌에서 우로 사이즈
    field_height = 20  # 맵 위에서 아래로 사이즈
    block_size = 25 # 블록 사이즈(픽셀)
    next_block_ratio = 0.6 # 다음블록 사이즈(픽셀) 비율

class Set:
    init_score = 0 # 초기 점수 세팅
    init_level = 1 # 초기 레벨
    init_goal = 5 # 레벨업을 하기 위한 조건
    init_skill = 0 # q스킬 게이지
    empty_board = 0 # 블록이 없는 빈 상태
    create_location_x = 3 # 블록 생성 초기 x위치
    create_location_y = 0 # 블록 생성 초기 y위치
    left_wall_x = 0 # 왼쪽 벽 좌표
    keep_state = 0 # 블록 상태유지 상수
    plus_one = 1 # 블록 한칸 이동 상수
    plus_two = 2 # 블록 두칸 이동 상수
    hidden_lines = 2 # 맨위의 숨겨진 줄수
    first_line_index_y = 2 # 맨 윗줄 y 인덱스
    dummy_one = 1 # 범위를 맞춰주기 위한 1
    delete_score = 10 # 줄 삭제시 얻는 점수
    delete_goal = 1 # 줄 삭제시 지워지는 목표
    success_goal = 0 # 목표 달성 상수
    max_level = 10 # 최대 레벨
    plus_level = 1 # 레벨 1업
    board_first = 0 # 보드의 첫번째 줄(안보이는 줄, 블록 위치는 여기서부터)
    board_second = 1 # 보드의 두번째 줄(안보이는 줄)
    board_third = 2 # 보드의 세번째 줄(블록이 보이는 첫번째 줄)
    block_border_thickness = 1 # 블록 테두리 두께



