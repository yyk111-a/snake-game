import pygame
import sys
import random
import math

# 初始化pygame
pygame.init()

# 游戏设置
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇 - 特效版")
clock = pygame.time.Clock()

# 颜色定义
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 120, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)


# 特效粒子系统 - 简化版本
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = 1.0

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 0.02
        self.size -= 0.1
        return self.life > 0 and self.size > 0

    def draw(self, surface):
        # 简化绘制，不使用透明度
        alpha = self.life
        r, g, b = self.color
        # 根据生命周期调整亮度
        adjusted_color = (int(r * alpha), int(g * alpha), int(b * alpha))
        pygame.draw.circle(surface, adjusted_color, (int(self.x), int(self.y)), int(self.size))


particles = []


def create_particles(x, y, color, count=10):
    for _ in range(count):
        particles.append(Particle(x, y, color))


def update_particles():
    global particles
    particles = [p for p in particles if p.update()]


def draw_particles(surface):
    for particle in particles:
        particle.draw(surface)


# 蛇身渐变效果
def get_snake_color(index, total_length):
    # 从绿色渐变到蓝色
    r = int(0 + (0 - 0) * index / total_length)
    g = int(255 + (120 - 255) * index / total_length)
    b = int(0 + (255 - 0) * index / total_length)
    return (r, g, b)


# 食物发光效果 - 简化版本
def draw_glowing_food(x, y):
    # 绘制食物主体
    food_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, RED, food_rect)

    # 简单的脉动效果
    time = pygame.time.get_ticks() // 100
    pulse = math.sin(time * 0.5) * 0.3 + 0.7
    highlight_size = int(GRID_SIZE * 0.6 * pulse)

    # 高光效果
    highlight_rect = pygame.Rect(
        x * GRID_SIZE + (GRID_SIZE - highlight_size) // 2,
        y * GRID_SIZE + (GRID_SIZE - highlight_size) // 2,
        highlight_size, highlight_size
    )
    pygame.draw.rect(screen, (255, 100, 100), highlight_rect, border_radius=3)


# 蛇头特效
def draw_snake_head(x, y, direction):
    # 基础蛇头
    head_rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, GREEN, head_rect)

    # 眼睛
    eye_size = GRID_SIZE // 5
    if direction == (1, 0):  # 向右
        eye_pos1 = (head_rect.right - eye_size - 2, head_rect.top + eye_size + 2)
        eye_pos2 = (head_rect.right - eye_size - 2, head_rect.bottom - eye_size - 2)
    elif direction == (-1, 0):  # 向左
        eye_pos1 = (head_rect.left + eye_size + 2, head_rect.top + eye_size + 2)
        eye_pos2 = (head_rect.left + eye_size + 2, head_rect.bottom - eye_size - 2)
    elif direction == (0, 1):  # 向下
        eye_pos1 = (head_rect.left + eye_size + 2, head_rect.bottom - eye_size - 2)
        eye_pos2 = (head_rect.right - eye_size - 2, head_rect.bottom - eye_size - 2)
    else:  # 向上
        eye_pos1 = (head_rect.left + eye_size + 2, head_rect.top + eye_size + 2)
        eye_pos2 = (head_rect.right - eye_size - 2, head_rect.top + eye_size + 2)

    pygame.draw.circle(screen, WHITE, eye_pos1, eye_size)
    pygame.draw.circle(screen, WHITE, eye_pos2, eye_size)
    pygame.draw.circle(screen, BLACK, eye_pos1, eye_size // 2)
    pygame.draw.circle(screen, BLACK, eye_pos2, eye_size // 2)


# 背景网格特效 - 简化版本
def draw_animated_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(0, HEIGHT, GRID_SIZE):
            # 简单的网格点
            pygame.draw.rect(screen, (40, 40, 60),
                             (x + GRID_SIZE // 2 - 1, y + GRID_SIZE // 2 - 1, 2, 2))


# 分数显示特效
def draw_animated_score(score, high_score):
    font = pygame.font.SysFont(None, 36)

    # 分数显示
    score_text = font.render(f'分数: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # 最高分显示
    high_score_text = font.render(f'最高分: {high_score}', True, BLUE)
    screen.blit(high_score_text, (10, 50))


def init_game():
    """初始化游戏状态"""
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
    score = 0
    game_over = False
    return snake, direction, food, score, game_over


def show_game_over_screen(score, high_score):
    """显示游戏结束画面"""
    screen.fill(BLACK)

    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)

    # 游戏结束文字
    game_over_text = font_large.render('游戏结束!', True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 120))

    # 分数显示
    score_text = font_medium.render(f'本次分数: {score}', True, YELLOW)
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))

    # 最高分显示
    high_score_text = font_medium.render(f'最高分数: {high_score}', True, BLUE)
    screen.blit(high_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))

    # 操作提示
    restart_text = font_small.render('按 R 键重新开始', True, GREEN)
    screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 80))

    quit_text = font_small.render('按 Q 键退出游戏', True, WHITE)
    screen.blit(quit_text, (WIDTH // 2 - 120, HEIGHT // 2 + 120))

    pygame.display.flip()

    # 等待玩家选择
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
        clock.tick(30)

    return False


# 初始化游戏
snake, direction, food, score, game_over = init_game()
speed = 10
high_score = 0

print("游戏开始！使用方向键控制")

# 游戏主循环
game_running = True
while game_running:
    # 单局游戏循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False

        # 游戏结束处理
        if game_over:
            # 更新最高分
            if score > high_score:
                high_score = score

            # 显示结束画面
            restart = show_game_over_screen(score, high_score)
            if restart:
                # 重新开始游戏
                snake, direction, food, score, game_over = init_game()
                particles.clear()
                break
            else:
                running = False
                game_running = False
                break

        # 键盘控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and direction != (-1, 0):
            direction = (1, 0)
        elif keys[pygame.K_LEFT] and direction != (1, 0):
            direction = (-1, 0)
        elif keys[pygame.K_DOWN] and direction != (0, -1):
            direction = (0, 1)
        elif keys[pygame.K_UP] and direction != (0, 1):
            direction = (0, -1)

        # 蛇的移动逻辑
        head_x, head_y = snake[0]
        dir_x, dir_y = direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # 碰撞检测
        # 1. 撞墙检测
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            print("撞墙了！游戏结束")
            # 创建碰撞粒子效果
            for _ in range(20):
                create_particles(new_head[0] * GRID_SIZE + GRID_SIZE // 2,
                                 new_head[1] * GRID_SIZE + GRID_SIZE // 2,
                                 RED)
            game_over = True

        # 2. 撞自己检测
        elif new_head in snake[1:]:
            print("撞到自己了！游戏结束")
            # 创建碰撞粒子效果
            for _ in range(20):
                create_particles(new_head[0] * GRID_SIZE + GRID_SIZE // 2,
                                 new_head[1] * GRID_SIZE + GRID_SIZE // 2,
                                 PURPLE)
            game_over = True

        # 如果游戏结束，跳过后续逻辑
        if game_over:
            continue

        # 吃食物检测
        if new_head == food:
            # 吃到食物，蛇变长
            snake.insert(0, new_head)
            # 创建吃食物粒子效果
            for _ in range(15):
                create_particles(food[0] * GRID_SIZE + GRID_SIZE // 2,
                                 food[1] * GRID_SIZE + GRID_SIZE // 2,
                                 YELLOW)
            # 生成新食物，确保不在蛇身上
            while True:
                food = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
                if food not in snake:
                    break
            score += 1
            print(f"吃到食物！分数: {score}")
        else:
            # 正常移动
            snake.insert(0, new_head)
            snake.pop()

            # 创建移动轨迹粒子
            if random.random() < 0.3:
                create_particles(snake[-1][0] * GRID_SIZE + GRID_SIZE // 2,
                                 snake[-1][1] * GRID_SIZE + GRID_SIZE // 2,
                                 BLUE, 2)

        # 🎨 绘制游戏画面 - 添加特效
        screen.fill(BLACK)

        # 绘制动态背景网格
        draw_animated_grid()

        # 绘制蛇身 - 渐变颜色效果
        for i, segment in enumerate(snake):
            if i == 0:  # 蛇头
                draw_snake_head(segment[0], segment[1], direction)
            else:  # 蛇身
                color = get_snake_color(i, len(snake))
                pygame.draw.rect(screen, color,
                                 (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE))

        # 绘制食物 - 发光效果
        draw_glowing_food(food[0], food[1])

        # 更新和绘制粒子
        update_particles()
        draw_particles(screen)

        # 显示游戏信息
        draw_animated_score(score, high_score)

        # 控制提示
        font = pygame.font.SysFont(None, 36)
        control_text = font.render('方向键控制 | 撞墙/撞身结束 | R重新开始', True, YELLOW)
        screen.blit(control_text, (10, 90))

        # 控制游戏速度
        clock.tick(speed)

        # 更新显示
        pygame.display.flip()

# 退出游戏
pygame.quit()
sys.exit()