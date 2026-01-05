import pygame, random, sys

pygame.init()
W, H = 500, 600
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dodge the Blocks")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

player = pygame.Rect(225, 540, 50, 50)
blocks = []
score = 0

difficulty = "Easy"
speed = 4
spawn_rate = 40

def set_difficulty(level):
    global speed, spawn_rate, difficulty
    difficulty = level

    if level == "Easy":
        speed = 4
        spawn_rate = 40
    elif level == "Medium":
        speed = 6
        spawn_rate = 25
    elif level == "Hard":
        speed = 8
        spawn_rate = 15

def reset():
    global blocks, score
    blocks = []
    score = 0
    player.x = 225
    set_difficulty("Easy")

set_difficulty("Easy")

while True:
    clock.tick(60)
    win.fill((20, 20, 30))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 6
    if keys[pygame.K_RIGHT] and player.x < W - 50:
        player.x += 6

    # CHANGE LEVEL BASED ON SCORE
    if score >= 20 and difficulty != "Hard":
        set_difficulty("Hard")
    elif score >= 10 and difficulty != "Medium":
        set_difficulty("Medium")

    # Spawn blocks
    if random.randint(1, spawn_rate) == 1:
        blocks.append(pygame.Rect(random.randint(0, W - 50), -50, 50, 50))

    for b in blocks[:]:
        b.y += speed
        if b.y > H:
            blocks.remove(b)
            score += 1
        if b.colliderect(player):
            reset()

    pygame.draw.rect(win, (100, 200, 255), player)
    for b in blocks:
        pygame.draw.rect(win, (255, 90, 90), b)

    score_txt = font.render(f"Score: {score}", True, (230, 230, 230))
    level_txt = font.render(f"Level: {difficulty}", True, (230, 230, 230))

    win.blit(score_txt, (10, 10))
    win.blit(level_txt, (10, 40))

    pygame.display.update()
