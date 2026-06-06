import pygame, sys, random, math

pygame.init()
CELL = 40
COLS, ROWS = 17, 11
W, H = COLS * CELL, ROWS * CELL
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 18)
big_font = pygame.font.SysFont("monospace", 32)

LANES = [
    {"y":1,"dir":1, "speed":1.2,"color":(239,68,68), "car_w":70},
    {"y":2,"dir":-1,"speed":1.5,"color":(249,115,22),"car_w":90},
    {"y":3,"dir":1, "speed":1.0,"color":(234,179,8), "car_w":60},
    {"y":4,"dir":-1,"speed":1.8,"color":(239,68,68), "car_w":80},
    {"y":5,"dir":1, "speed":1.3,"color":(249,115,22),"car_w":100},
    {"y":6,"dir":-1,"speed":1.6,"color":(234,179,8), "car_w":70},
    {"y":7,"dir":1, "speed":2.0,"color":(239,68,68), "car_w":55},
    {"y":8,"dir":-1,"speed":1.1,"color":(249,115,22),"car_w":85},
]

def spawn_cars(level):
    cars = []
    for lane in LANES:
        count = random.randint(2, 3)
        gap = W / count
        for i in range(count):
            x = i * gap + random.randint(0, 30)
            cars.append({
                "x": x, "y": lane["y"] * CELL + 4,
                "w": lane["car_w"] + (level-1)*5, "h": CELL - 8,
                "vx": lane["dir"] * (lane["speed"] + (level-1)*0.15),
                "color": lane["color"]
            })
    return cars

def reset():
    frog = {"x": COLS//2, "y": ROWS-1, "anim": 0}
    return frog, spawn_cars(1), 0, 3, 1, "playing", 0

frog, cars, score, lives, level, state, invincible = reset()

def move_frog(dx, dy):
    global score, level, cars, frog
    nx, ny = frog["x"] + dx, frog["y"] + dy
    if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS: return
    frog["x"], frog["y"] = nx, ny
    frog["anim"] = 8
    if frog["y"] == 0:
        score += 50 + lives * 10
        level = 1 + score // 200
        frog["x"], frog["y"] = COLS//2, ROWS-1
        cars = spawn_cars(level)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state != "playing":
                frog, cars, score, lives, level, state, invincible = reset()
            if state == "playing":
                if event.key in (pygame.K_UP, pygame.K_w):    move_frog(0,-1)
                if event.key in (pygame.K_DOWN, pygame.K_s):  move_frog(0,1)
                if event.key in (pygame.K_LEFT, pygame.K_a):  move_frog(-1,0)
                if event.key in (pygame.K_RIGHT, pygame.K_d): move_frog(1,0)

    if state == "playing":
        if invincible > 0: invincible -= 1
        if frog["anim"] > 0: frog["anim"] -= 1

        for c in cars:
            c["x"] += c["vx"]
            if c["vx"] > 0 and c["x"] > W + 10: c["x"] = -c["w"] - 10
            if c["vx"] < 0 and c["x"] < -c["w"] - 10: c["x"] = W + 10

        if invincible == 0 and 0 < frog["y"] < ROWS-1:
            fx = frog["x"]*CELL+4; fy = frog["y"]*CELL+4
            frect = pygame.Rect(fx, fy, CELL-8, CELL-8)
            for c in cars:
                crect = pygame.Rect(int(c["x"]), c["y"], c["w"], c["h"])
                if frect.colliderect(crect):
                    lives -= 1
                    invincible = 90
                    frog["x"], frog["y"] = COLS//2, ROWS-1
                    if lives <= 0: state = "dead"
                    break

    screen.fill((13,17,23))

    for r in range(ROWS):
        if r == 0 or r == ROWS-1:
            pygame.draw.rect(screen, (20,83,45), (0, r*CELL, W, CELL))
        else:
            c = (28,28,46) if r%2==0 else (22,22,42)
            pygame.draw.rect(screen, c, (0, r*CELL, W, CELL))

    for i in range(COLS):
        c = (22,163,74) if i%2==0 else (21,128,61)
        pygame.draw.rect(screen, c, (i*CELL+4, 4, CELL-8, CELL-8), border_radius=4)
    pygame.draw.rect(screen, (22,163,74), (0, (ROWS-1)*CELL, W, CELL))

    for c in cars:
        pygame.draw.rect(screen, c["color"], (int(c["x"]), c["y"], c["w"], c["h"]), border_radius=4)
        pygame.draw.rect(screen, (0,0,0,80), (int(c["x"])+4, c["y"]+c["h"]-8, 14, 7), border_radius=2)
        pygame.draw.rect(screen, (0,0,0,80), (int(c["x"])+c["w"]-18, c["y"]+c["h"]-8, 14, 7), border_radius=2)

    flash = invincible > 0 and (invincible // 6) % 2 == 0
    if not flash:
        fx = frog["x"]*CELL + CELL//2
        fy = frog["y"]*CELL + CELL//2 + (-4 if frog["anim"] > 0 else 0)
        pygame.draw.ellipse(screen, (74,222,128), (fx-10, fy-7, 20, 18))
        pygame.draw.ellipse(screen, (134,239,172), (fx-7, fy-9, 14, 12))
        pygame.draw.circle(screen, (255,255,255), (fx-4, fy-13), 4)
        pygame.draw.circle(screen, (255,255,255), (fx+4, fy-13), 4)
        pygame.draw.circle(screen, (26,26,46), (fx-4, fy-13), 2)
        pygame.draw.circle(screen, (26,26,46), (fx+4, fy-13), 2)

    screen.blit(font.render(f"Score: {score}   Lives: {'🐸'*lives}   Level: {level}", True, (255,255,255)), (10,12))

    if state == "dead":
        msg = big_font.render(f"Game Over! Score: {score}", True, (248,113,113))
        sub = font.render("Press SPACE to restart", True, (180,180,180))
        screen.blit(msg, (W//2 - msg.get_width()//2, H//2 - 20))
        screen.blit(sub, (W//2 - sub.get_width()//2, H//2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()