#导入必要的库
import pygame
import sys
import random


from day02.my_snake_game import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, YELLOW

#初始化
pygame.init()
#创建游戏窗口
WIDTH=800
HEIGHT=600
GREEN_SIZE=20
GREEN_WIDTH=WIDTH//GREEN_SIZE
GREEN_HEIGHT=HEIGHT//GREEN_SIZE
screen=pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("会移动的方块")
#创建时钟对象
clock=pygame.time.Clock()
#定义颜色
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)
snake=[(GREEN_WIDTH//2),(GREEN_HEIGHT//2)]
direction=(1,0)
speed=10
food=(random.randint(0,GRID_WIDTH-1),random.randint(0,GRID_HEIGHT-1))
score=0
game_over=False
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    if game_over:
        screen.fill(BLACK)
        font=pygame.font.SysFont(None,72)
        game_over_text=font.render('游戏结束',True,RED)
        screen.blit(game_over_text,(WIDTH//2-150,HEIGHT//2-50))
        score_text=font.render(f'分数:{score}',True,YELLOW)
        screen.blit(score_text,(WIDTH//2-100,HEIGHT//2+50))
        pygame.display.flip()
        pygame.time.wait(3000)
        running=False
        continue
    keys=pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and direction!=(-1,0):
        direction=(1,0)
    elif keys[pygame.K_LEFT] and direction!=(1,0):
        direction=(-1,0)
    elif keys[pygame.K_UP] and direction!=(0,1):
        direction=(0,-1)
    elif keys[pygame.K_DOWN] and direction!=(0,-1):
        direction=(0,1)
    head_x,head_y=snake[0]
    dir_x,dir_y=direction
    new_head=(head_x+dir_x,head_y+dir_y)
    if (new_head[0]<0 or new_head[0]>=GRID_WIDTH or new_head[1]<0 or new_head[1]>=GRID_HEIGHT):
        print("撞墙了！游戏结束")
        game_over=True
    elif new_head in snake[1:]:
        print("撞到自己了！游戏结束")
        game_over=True
    if game_over:
        continue
    if new_head==food:
        snake.insert(0,new_head)
        food=(random.randint(0,GRID_WIDTH-1),random.randint(0,GRID_HEIGHT-1))
        score+=1
        print(f"吃到食物！分数:{score}")
    else:
        snake.insert(0,new_head)
        snake.pop()
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen,GREEN,segment[0]*GRID_SIZE,segment[1]*GRID_SIZE,GRID_SIZE,GRID_SIZE)

    pygame.draw.rect(screen,RED,food[0]*GRID_SIZE,food[1]*GRID_SIZE,GRID_SIZE,GRID_SIZE)
    font=pygame.font.SysFont(None,36)
    score_text=font.render(f'分数:{score}',True,WHITE)
    screen.blit(score_text,(10,10))
    status_text=font.render('小心边界和自己身体',True,YELLOW)
    screen.blit(status_text,(10,50))
    pygame.display.flip()
    clock.tick(speed)
#退出游戏
pygame.quit()
sys.exit()
#111
