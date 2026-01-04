import pygame
import math
import random
import os
import sys

pygame.init()

WIDTH, HEIGHT = 900, 650
RADIUS = 18
ROWS = 7
FPS = 60

SHOTS_BEFORE_DROP = 5
DROP_DISTANCE = RADIUS * 2
DANGER_LINE = HEIGHT - 100

COLORS = [
    (255, 90, 90),
    (90, 255, 90),
    (90, 90, 255),
    (255, 255, 90),
    (255, 90, 255),
    (90, 255, 255)
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Shooter")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 40)

def load_scores():
    if not os.path.exists("data.txt"):
        return []
    with open("data.txt") as f:
        return [(x.split(",")[0], int(x.split(",")[1])) for x in f.read().splitlines()]

def save_score(name, score):
    scores = load_scores()
    scores.append((name, score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    with open("data.txt", "w") as f:
        for n, s in scores:
            f.write(f"{n},{s}\n")

class Bubble:
    def __init__(self, x, y, color):
        self.x, self.y, self.color = x, y, color

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), RADIUS)
        pygame.draw.circle(screen, (0,0,0), (int(self.x), int(self.y)), RADIUS, 2)

class ShooterBubble(Bubble):
    def __init__(self, color):
        super().__init__(WIDTH//2, HEIGHT-60, color)
        self.vx = 0
        self.vy = 0
        self.active = False

    def shoot(self, angle):
        self.vx = math.cos(angle) * 12
        self.vy = -math.sin(angle) * 12
        self.active = True

    def move(self):
        if not self.active:
            return
        self.x += self.vx
        self.y += self.vy
        if self.x <= RADIUS or self.x >= WIDTH - RADIUS:
            self.vx *= -1

class Game:
    def __init__(self):
        self.bubbles = []
        self.score = 0
        self.shots = 0
        self.state = "PLAYING"
        self.score_saved = False
        self.current = ShooterBubble(random.choice(COLORS))
        self.next_color = random.choice(COLORS)
        self.create_grid()

    def create_grid(self):
        cols = WIDTH // (RADIUS * 2)
        for r in range(ROWS):
            for c in range(cols):
                self.bubbles.append(
                    Bubble(c*RADIUS*2+RADIUS, r*RADIUS*2+RADIUS, random.choice(COLORS))
                )

    def drop_bubbles(self):
        for b in self.bubbles:
            b.y += DROP_DISTANCE

    def update(self):
        if self.state != "PLAYING":
            return
        if self.current.active:
            self.current.move()
            self.check_collision()

    def check_collision(self):
        for b in self.bubbles:
            if math.hypot(b.x-self.current.x, b.y-self.current.y) <= RADIUS*2:
                self.snap()
                return
        if self.current.y <= RADIUS:
            self.snap()

    def snap(self):
        self.current.active = False
        placed = Bubble(self.current.x, self.current.y, self.current.color)
        self.bubbles.append(placed)
        self.clear_matches(placed)

        self.shots += 1
        if self.shots % SHOTS_BEFORE_DROP == 0:
            self.drop_bubbles()

        self.current = ShooterBubble(self.next_color)
        self.next_color = random.choice(COLORS)
        self.check_game_over()

    def get_cluster(self, start):
        stack = [start]
        cluster = []
        visited = set()
        while stack:
            b = stack.pop()
            if b in visited:
                continue
            visited.add(b)
            cluster.append(b)
            for o in self.bubbles:
                if o.color == start.color and math.hypot(o.x-b.x, o.y-b.y) <= RADIUS*2.2:
                    stack.append(o)
        return cluster

    def clear_matches(self, placed):
        cluster = self.get_cluster(placed)
        if len(cluster) >= 3:
            for b in cluster:
                self.bubbles.remove(b)
            self.score += len(cluster)*15

    def check_game_over(self):
        for b in self.bubbles:
            if b.y + RADIUS >= DANGER_LINE:
                self.state = "GAME_OVER"

    def draw(self):
        for b in self.bubbles:
            b.draw()

        pygame.draw.line(screen, (200,50,50), (0,DANGER_LINE), (WIDTH,DANGER_LINE), 2)

        if self.state == "PLAYING" and not self.current.active:
            mx,my = pygame.mouse.get_pos()
            pygame.draw.line(screen,(200,200,200),(self.current.x,self.current.y),(mx,my),2)

        self.current.draw()
        pygame.draw.circle(screen, self.next_color, (WIDTH-50, HEIGHT-40), RADIUS)
        screen.blit(font.render(f"Score: {self.score}", True, (255,255,255)), (20, HEIGHT-40))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH,HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))

        screen.blit(big_font.render("GAME OVER", True, (255,80,80)), (WIDTH//2-120, HEIGHT//2-120))
        screen.blit(big_font.render(f"Score: {self.score}", True, (255,255,255)), (WIDTH//2-110, HEIGHT//2-60))
        screen.blit(font.render("Press R to Replay", True, (200,200,200)), (WIDTH//2-90, HEIGHT//2))
        screen.blit(font.render("Press Q to Quit", True, (200,200,200)), (WIDTH//2-80, HEIGHT//2+30))

def input_name():
    name=""
    while True:
        screen.fill((20,20,20))
        screen.blit(big_font.render("Enter Player Name", True,(255,255,255)),(270,240))
        pygame.draw.rect(screen,(255,255,255),(250,300,400,50).2)
        screen.blit(big_font.render(name+"|",True,(255,255,90)),(260,305))
        for e in pygame.event.get():
            if e.type==pygame.QUIT: sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN and name: return name
                elif e.key==pygame.K_BACKSPACE: name=name[:-1]
                elif len(name)<12: name+=e.unicode
        pygame.display.flip()
        clock.tick(30)

def main():
    player = input_name()
    game = Game()
    running = True

    while running:
        clock.tick(FPS)
        screen.fill((30,30,30))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_score(player, game.score)
                pygame.quit()
                sys.exit()
                
            if game.state == "PLAYING":
                if e.type == pygame.MOUSEBUTTONDOWN and not game.current.active:
                    mx,my = pygame.mouse.get_pos()
                    angle = math.aten2(game.current.y-my, mx-game.current.x)
                    game.current.shoot(angle)

            if game.state == "GAME_OVER":
                if not game.score_saved:
                    save_score(player, game.score)
                    game.score_saved = True
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r: