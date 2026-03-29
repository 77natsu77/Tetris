import pygame as pg
from copy import deepcopy
from random import randrange, choice
import sys

W, H = 10, 15
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 700  #Check this sze in future
FPS = 60

pg.init()
pg.display.set_caption("Tetris")
sc = pg.display.set_mode(RES)
game_sc = pg.Surface(GAME_RES)
clock = pg.time.Clock()

bg = pg.image.load('img/bg.jpg').convert()
game_bg = pg.image.load('img/bg2.jpg').convert()

grid = [
    pg.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)
]
#can inc the prob of getting a blocjk by adding it in here more
figure_pos = [
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],  #I block
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],  #0 block
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],  #s block
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],  #z block
    [(0, 0), (0, -1), (0, 1), (-1, -1)],  # p block
    [(0, 0), (0, -1), (0, 1), (1, -1)],  #l block
    [(0, 0), (0, -1), (0, 1), (1, -1)]
]  #t block

figures = [[pg.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos]
           for fig_pos in figure_pos]
figure_rect = pg.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

main_font = pg.font.SysFont('Font/font.ttf', 65)
font = pg.font.SysFont('Font/font.ttf', 45)

anim_count, anim_speed, anim_limit = 0, 60, 2000

title_tetris = main_font.render('TETRIS', True, pg.Color('darkorange'))
title_score = font.render('Score:', True, pg.Color('green'))
title_record = font.render('Record:', True, pg.Color('purple'))

get_color = lambda: (randrange(30, 240), randrange(30, 240), randrange(
    30, 240))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
  if figure[i].x < 0 or figure[i].x > W - 1:
    return False
  elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
    return False
  return True


def get_record():
  try:
    with open('record') as f:
      return f.readline()
  except FileNotFoundError:
    with open('record', 'w') as f:
      f.write('0')


def set_record(record, score):
  rec = max(int(record), score)
  with open('record', 'w') as f:
    f.write(str(rec))


while True:
  record = get_record()

  sc.blit(bg, (0, 0))
  sc.blit(game_sc, (20, 20))
  game_sc.blit(game_bg, (0, 0))

  dx, rotate = 0, False
  for i in range(lines):
    pg.time.wait(200)

  
  for event in pg.event.get():
    if event.type == pg.QUIT:
      exit()
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_LEFT:
        dx = -1
      elif event.key == pg.K_RIGHT:
        dx = 1
      elif event.key == pg.K_DOWN:
        anim_limit = 100
      elif event.key == pg.K_UP:
        rotate = True
        
  center = figure[0]
  figure_old = deepcopy(figure)
  if rotate:
    for i in range(4):
      x = figure[i].y - center.y
      y = figure[i].x - center.x
      figure[i].x = center.x - x
      figure[i].y = center.y + y
      if not check_borders():
        figure = deepcopy(figure_old)
        break

  
  line, lines = H - 1, 0
  for row in range(H - 1, -1, -1):
    count = 0
    for i in range(W):
      if field[row][i]:
        count += 1
        field[line][i] = field[row][i]
    if count < W:
      line -= 1
    else:
      anim_speed += 3
      lines += 1
      for i in range(W):
        field[row][i] = 0
  score += scores[lines]

  figure_old = deepcopy(figure)
  for i in range(4):
    figure[i].x += dx
    if not check_borders():
      figure = deepcopy(figure_old)
      break

  anim_count += anim_speed
  if anim_count > anim_limit:
    anim_count = 0

  
    figure_old = deepcopy(figure)
    for i in range(4):
      figure[i].y += 1
      if not check_borders():
        figure = deepcopy(figure_old)
        for i in range(4):
          field[figure_old[i].y][figure_old[i].x] = color
        figure, color = next_figure, next_color
        next_figure, next_color = deepcopy(choice(figures)), get_color()
        anim_limit = 2000
        break
  [pg.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

  for i in range(4):
    figure_rect.x = figure[i].x * TILE
    figure_rect.y = figure[i].y * TILE
    pg.draw.rect(game_sc, color, figure_rect)

  for i in range(4):
    figure_rect.x = next_figure[i].x * TILE + 380
    figure_rect.y = next_figure[i].y * TILE + 180
    pg.draw.rect(sc, next_color, figure_rect)

  for y, raw in enumerate(field):
    for x, col in enumerate(raw):
      if col:
        figure_rect.x, figure_rect.y = x * TILE, y * TILE
        pg.draw.rect(game_sc, col, figure_rect)

  sc.blit(title_tetris, (485, 0))
  sc.blit(title_score, (535, 540))

  sc.blit(font.render(str(score), True, pg.Color('green')), (600, 580))
  sc.blit(title_record, (535, 430))
  sc.blit(font.render(str(record), True, pg.Color('purple')), (600, 470))

  for i in range(W):
    if field[0][i]:
      set_record(record, score)
      field = [[0 for i in range(W)] for j in range(H)]
      anim_count, anim_speed, anim_limit = 0, 60, 2000
      score = 0
      for i_rect in grid:
        pg.draw.rect(game_sc, get_color(), i_rect, 1)
        sc.blit(game_sc, (20, 20))
        pg.display.flip()
        clock.tick(200)
      
  
  pg.display.flip()
  clock.tick(FPS)
