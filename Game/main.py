import math
import random
import sys

import pygame

W, H = 960, 540
FPS = 60
DEMO = "--demo" in sys.argv

TITLE = "SPACE SHOOTER"
SUBTITLE = "Enemies fly in from the right - hold the line!"
TIPS = ("- Enemies fly in from the right side.",
        "- Grab the blue W orbs to upgrade your gun.",
        "- Green H repairs, yellow S gives a shield.",
        "- Touching an enemy hurts: shoot first!",
        "- Beat the boss and set a HIGH SCORE!")

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas,couriersnew,monospace", 20, bold=True)
big_font = pygame.font.SysFont("consolas,couriersnew,monospace", 64, bold=True)
small_font = pygame.font.SysFont("consolas,couriersnew,monospace", 16)


def make_ship(main, wing, accent, w=70, h=44):
    """Draw a ship facing RIGHT."""
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    cy = h // 2
    dark = (20, 20, 30)
                        
    for sign in (-1, 1):
        edge = 2 if sign < 0 else h - 3
        pts = [(w * 0.62, cy), (w * 0.34, cy), (w * 0.08, edge), (w * 0.30, edge)]
        pygame.draw.polygon(s, wing, pts)
        pygame.draw.polygon(s, dark, pts, 2)
                        
        pygame.draw.circle(s, accent, (int(w * 0.19), edge + (3 if sign < 0 else -3)), 3)
                  
    pygame.draw.rect(s, (60, 60, 75), (int(w * 0.02), cy - 7, int(w * 0.14), 14), border_radius=3)
              
    body = [(w - 2, cy), (w * 0.72, cy - 8), (w * 0.2, cy - 9), (w * 0.08, cy - 6),
            (w * 0.08, cy + 6), (w * 0.2, cy + 9), (w * 0.72, cy + 8)]
    pygame.draw.polygon(s, main, body)
    pygame.draw.polygon(s, dark, body, 2)
            
    pygame.draw.line(s, accent, (int(w * 0.22), cy), (int(w * 0.6), cy), 2)
             
    pygame.draw.ellipse(s, (120, 220, 255), (int(w * 0.48), cy - 5, int(w * 0.24), 10))
    pygame.draw.ellipse(s, dark, (int(w * 0.48), cy - 5, int(w * 0.24), 10), 1)
    return s


def glow(radius, color, alpha=255):
    s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        a = int(alpha * (1 - r / radius) ** 1.6)
        pygame.draw.circle(s, (*color, a), (radius, radius), r)
    return s


PLAYER_IMG = make_ship((190, 195, 205), (130, 140, 160), (255, 170, 40), 76, 48)
ENEMY_IMG = {
    "red": make_ship((205, 50, 60), (150, 40, 50), (255, 220, 80), 64, 42),
    "green": make_ship((110, 200, 60), (70, 150, 50), (255, 80, 80), 64, 42),
    "blue": make_ship((60, 130, 220), (40, 90, 170), (255, 220, 80), 68, 44),
    "boss": make_ship((130, 60, 170), (90, 40, 120), (255, 90, 90), 230, 150),
}
GLOW_ORANGE = glow(22, (255, 160, 40))
GLOW_RED = glow(14, (255, 60, 60))
GLOW_BLUE = glow(18, (80, 160, 255))
GLOW_GREEN = glow(18, (90, 255, 120))
GLOW_YELLOW = glow(18, (255, 230, 80))
SHIELD_IMG = pygame.Surface((110, 110), pygame.SRCALPHA)
pygame.draw.circle(SHIELD_IMG, (80, 200, 255, 40), (55, 55), 52)
pygame.draw.circle(SHIELD_IMG, (120, 220, 255, 170), (55, 55), 52, 3)


                                                                            
         
                                                                            
TAU = math.tau
_rot_cache = {}


def rotated(key, img, angle):
    """Rotate a RIGHT-facing sprite to `angle` (radians, screen coords). Cached."""
    q = int(round(-math.degrees(angle) / 4.0)) * 4
    k = (key, q)
    s = _rot_cache.get(k)
    if s is None:
        s = pygame.transform.rotate(img, q)
        _rot_cache[k] = s
    return s


def draw_flame(surf, x, y, angle, length, width, c1=(255, 120, 30), c2=(255, 235, 150)):
    bx, by = -math.cos(angle), -math.sin(angle)              
    px, py = -math.sin(angle), math.cos(angle)              
    pygame.draw.polygon(surf, c1, [(x + px * width, y + py * width),
                                   (x + bx * length, y + by * length),
                                   (x - px * width, y - py * width)])
    pygame.draw.polygon(surf, c2, [(x + px * width * 0.5, y + py * width * 0.5),
                                   (x + bx * length * 0.6, y + by * length * 0.6),
                                   (x - px * width * 0.5, y - py * width * 0.5)])


                                                                            
                                               
                                                                            
def make_nebula():
    surf = pygame.Surface((W, H), pygame.SRCALPHA)
    rnd = random.Random(7)
    palette = [(70, 30, 140), (30, 60, 160), (140, 30, 100), (20, 110, 140)]
    for _ in range(9):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        r = rnd.randint(90, 200)
        g = glow(r, rnd.choice(palette), 110)
        for dx in (-W, 0, W):                                                      
            for dy in (-H, 0, H):
                surf.blit(g, (x - r + dx, y - r + dy))
    return surf


NEBULA = make_nebula()
STAR_LAYERS = [
    [[random.uniform(0, W), random.uniform(0, H), 0.25 + random.random() * 0.15, 1] for _ in range(90)],
    [[random.uniform(0, W), random.uniform(0, H), 0.6 + random.random() * 0.2, 2] for _ in range(50)],
    [[random.uniform(0, W), random.uniform(0, H), 1.1 + random.random() * 0.3, 2] for _ in range(25)],
]
PLANETS = [
    {"x": 700.0, "y": 140.0, "r": 46, "c": (70, 110, 200), "f": 0.35},
    {"x": 200.0, "y": 420.0, "r": 28, "c": (200, 120, 70), "f": 0.5},
]
neb = [0.0, 0.0]


def update_background(vx, vy):
    neb[0] = (neb[0] - vx * 0.15 - 0.15) % W
    neb[1] = (neb[1] - vy * 0.15) % H
    for layer in STAR_LAYERS:
        for st in layer:
            st[0] = (st[0] - vx * st[2] * 0.6 - 0.35 * st[2]) % W
            st[1] = (st[1] - vy * st[2] * 0.6) % H
    for p in PLANETS:
        p["x"] -= vx * p["f"] + 0.1
        p["y"] -= vy * p["f"]
        if p["x"] < -150:
            p["x"] += W + 300
        elif p["x"] > W + 150:
            p["x"] -= W + 300
        if p["y"] < -150:
            p["y"] += H + 300
        elif p["y"] > H + 150:
            p["y"] -= H + 300


def draw_background():
    screen.fill((4, 4, 14))
    for i in (0, 1):
        for j in (0, 1):
            screen.blit(NEBULA, (neb[0] - W + i * W, neb[1] - H + j * H))
    for p in PLANETS:
        x, y, r = int(p["x"]), int(p["y"]), p["r"]
        pygame.draw.circle(screen, p["c"], (x, y), r)
        shade = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(shade, (0, 0, 20, 120), (r + r // 3, r + r // 3), r)
        screen.blit(shade, (x - r, y - r))
        pygame.draw.circle(screen, (255, 255, 255), (x - r // 3, y - r // 3), max(2, r // 8))
    for layer in STAR_LAYERS:
        for sx, sy, f, size in layer:
            c = min(255, int(110 + f * 120))
            pygame.draw.rect(screen, (c, c, c), (int(sx), int(sy), size, size))


                                                                            
                        
                                                                            
particles = []


def explode(x, y, scale=1.0, colors=None):
    colors = colors or [(255, 220, 90), (255, 140, 40), (255, 70, 40), (200, 200, 200)]
    for _ in range(int(26 * scale)):
        ang = random.random() * TAU
        sp = random.random() * 5 * scale + 0.5
        particles.append({
            "x": x, "y": y, "vx": math.cos(ang) * sp, "vy": math.sin(ang) * sp,
            "life": random.randint(20, 45), "max": 45,
            "size": random.randint(2, int(4 + 3 * scale)),
            "c": random.choice(colors),
        })
    particles.append({"x": x, "y": y, "vx": 0, "vy": 0, "life": 14, "max": 14,
                      "size": int(30 * scale), "c": (255, 240, 200), "ring": True})


def update_particles():
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vx"] *= 0.96
        p["vy"] *= 0.96
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)


def draw_particles():
    for p in particles:
        k = p["life"] / p["max"]
        if p.get("ring"):
            r = int(p["size"] * (1.5 - k))
            if r > 1:
                pygame.draw.circle(screen, p["c"], (int(p["x"]), int(p["y"])), r, 2)
        else:
            s = max(1, int(p["size"] * k))
            pygame.draw.circle(screen, p["c"], (int(p["x"]), int(p["y"])), s)


                                                                            
         
                                                                            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, friendly=True, dmg=1):
        super().__init__()
        self.friendly = friendly
        self.dmg = dmg
        if friendly:
            base = pygame.Surface((18, 6), pygame.SRCALPHA)
            pygame.draw.ellipse(base, (255, 190, 60), (0, 0, 18, 6))
            pygame.draw.ellipse(base, (255, 255, 200), (4, 1, 11, 4))
            self.image = pygame.transform.rotate(base, -math.degrees(angle))
        else:
            self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 70, 70), (6, 6), 6)
            pygame.draw.circle(self.image, (255, 230, 230), (6, 6), 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.fx, self.fy = float(x), float(y)
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed

    def update(self):
        self.fx += self.vx
        self.fy += self.vy
        self.rect.center = (int(self.fx), int(self.fy))
        if not screen.get_rect().inflate(120, 120).colliderect(self.rect):
            self.kill()

    def draw(self, surf):
        g = GLOW_ORANGE if self.friendly else GLOW_RED
        surf.blit(g, g.get_rect(center=self.rect.center))
        surf.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.fx, self.fy = 90.0, H / 2
        self.rect = PLAYER_IMG.get_rect(center=(self.fx, self.fy))
        self.hitbox = pygame.Rect(0, 0, 30, 30)
        self.hitbox.center = self.rect.center
        self.speed = 6
        self.hp = 100
        self.lives = 3
        self.weapon = 1
        self.last_shot = 0
        self.invuln_until = 0
        self.shield_until = 0
        self.tick = 0

    def shoot(self, now, bullets):
        if now - self.last_shot < 150:
            return
        self.last_shot = now
        mx, my = self.fx + 34, self.fy
        patterns = {
            1: [(0, 0)],
            2: [(-8, 0), (8, 0)],
            3: [(0, 0), (0, -0.2), (0, 0.2)],
            4: [(-6, 0), (6, 0), (0, -0.32), (0, 0.32)],
        }[self.weapon]
        for off, ao in patterns:
            bullets.add(Bullet(mx, my + off, ao, 13))

    def update(self, dx, dy):
        self.tick += 1
        n = math.hypot(dx, dy)
        if n > 1:
            dx, dy = dx / n, dy / n
        self.fx = max(40, min(W * 0.65, self.fx + dx * self.speed))
        self.fy = max(30, min(H - 30, self.fy + dy * self.speed))
        self.rect.center = (int(self.fx), int(self.fy))
        self.hitbox.center = self.rect.center

    def draw(self, surf, now):
        if now < self.invuln_until and (now // 80) % 2:
            return
        fl = 14 + random.randint(0, 10) + 4 * math.sin(self.tick * 0.6)
        draw_flame(surf, self.fx - 32, self.fy, 0.0, fl, 6)
        surf.blit(PLAYER_IMG, PLAYER_IMG.get_rect(center=(int(self.fx), int(self.fy))))
        if now < self.shield_until:
            if self.shield_until - now > 1200 or (now // 100) % 2:
                surf.blit(SHIELD_IMG, SHIELD_IMG.get_rect(center=self.rect.center))


class Enemy(pygame.sprite.Sprite):
    pending = []                                                                

    def __init__(self, kind, diff, pos):
        super().__init__()
        self.kind = kind
        self.base = ENEMY_IMG[kind]
        self.fx, self.fy = float(pos[0]), float(pos[1])
        self.heading = math.pi                                      
        self.rect = self.base.get_rect(center=pos)
        size = 130 if kind == "boss" else 40
        self.hitbox = pygame.Rect(0, 0, size, size)
        self.hitbox.center = pos
        self.t = random.random() * 6
        self.shoot_t = pygame.time.get_ticks() + random.randint(900, 2000)
        self.hp = {"red": 1, "green": 2, "blue": 3, "boss": 60 + diff * 10}[kind]
        self.max_hp = self.hp
        self.speed = {"red": 4.2 + diff * 0.2, "green": 2.6 + diff * 0.1, "blue": 2.2, "boss": 1.5}[kind]
        self.score = {"red": 10, "green": 25, "blue": 40, "boss": 1000}[kind]
        self.dir = random.choice([-1, 1])
        self.base_y = self.fy
        self.stop_x = W - 200 - random.randint(0, 150)

    def update(self, player, ebullets, diff):
        now = pygame.time.get_ticks()
        px, py = player.fx, player.fy
        self.t += 0.05
        if self.kind == "red":
            self.fx -= self.speed
            self.fy += max(-1.2, min(1.2, (py - self.fy) * 0.01))                                
        elif self.kind == "green":
            self.fx -= self.speed
            self.fy = max(40, min(H - 40, self.base_y + math.sin(self.t * 1.6) * 90))
        elif self.kind == "blue":
            if self.fx > self.stop_x:
                self.fx -= self.speed
            else:
                self.fy += self.dir * 1.6
                if self.fy < 50 or self.fy > H - 50:
                    self.dir *= -1
            if now > self.shoot_t and self.fx < W - 20:
                self.shoot_t = now + max(700, 1700 - diff * 100)
                self.fire(6, base=math.atan2(py - self.fy, px - self.fx))
        else:         
            if self.fx > W - 170:
                self.fx -= self.speed
            else:
                self.fy = H / 2 + math.sin(self.t * 0.8) * (H / 2 - 100)
                if now > self.shoot_t:
                    self.shoot_t = now + 850
                    self.fire(6, spread=(-0.35, 0, 0.35), base=math.atan2(py - self.fy, px - self.fx))
                    Enemy.pending.append((self.fx - 60, self.fy - 45, math.pi, 5))
                    Enemy.pending.append((self.fx - 60, self.fy + 45, math.pi, 5))
        self.rect.center = (int(self.fx), int(self.fy))
        self.hitbox.center = self.rect.center
        if self.rect.right < -20:
            self.kill()

    def fire(self, speed, spread=(0,), base=None):
        b = self.heading if base is None else base
        for off in spread:
            Enemy.pending.append((self.fx, self.fy, b + off, speed))

    def draw(self, surf):
        a = self.heading
        w = self.base.get_width()
        if self.kind == "boss":
            for off in (-30, 0, 30):
                bx = self.fx - math.cos(a) * (w / 2 - 4) - math.sin(a) * off
                by = self.fy - math.sin(a) * (w / 2 - 4) + math.cos(a) * off
                draw_flame(surf, bx, by, a, 20 + random.randint(0, 14), 9, (255, 90, 200), (255, 230, 255))
        else:
            bx = self.fx - math.cos(a) * (w / 2 - 6)
            by = self.fy - math.sin(a) * (w / 2 - 6)
            draw_flame(surf, bx, by, a, 10 + random.randint(0, 8), 5)
        img = rotated(self.kind, self.base, a)
        surf.blit(img, img.get_rect(center=(int(self.fx), int(self.fy))))


class PowerUp(pygame.sprite.Sprite):
    KINDS = {"W": (GLOW_BLUE, (80, 160, 255)), "H": (GLOW_GREEN, (90, 255, 120)), "S": (GLOW_YELLOW, (255, 230, 80))}

    def __init__(self, x, y, kind):
        super().__init__()
        self.kind = kind
        self.rect = pygame.Rect(0, 0, 26, 26)
        self.rect.center = (x, y)
        self.fx, self.fy = float(x), float(y)
        self.t = 0
        self.life = 60 * 12

    def update(self):
        self.t += 0.1
        self.life -= 1
        self.fx -= 1.4
        self.rect.center = (int(self.fx), int(self.fy + math.sin(self.t) * 6))
        if self.fx < -20 or self.life <= 0:
            self.kill()

    def draw(self, surf):
        if self.life < 120 and (self.life // 6) % 2:
            return                          
        g, col = self.KINDS[self.kind]
        surf.blit(g, g.get_rect(center=self.rect.center))
        pygame.draw.circle(surf, col, self.rect.center, 11)
        pygame.draw.circle(surf, (255, 255, 255), self.rect.center, 11, 2)
        txt = small_font.render(self.kind, True, (10, 10, 30))
        surf.blit(txt, txt.get_rect(center=self.rect.center))


def right_spawn():
    """A spawn position just outside the right edge of the screen."""
    return (W + 60, random.randint(40, H - 40))


                                                                            
            
                                                                            
class Game:
    def __init__(self, high=0):
        self.high = high
        self.reset()

    def reset(self):
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.ebullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        particles.clear()
        self.score = 0
        self.over = False
        self.paused = False
        self.next_spawn = pygame.time.get_ticks() + 1500
        self.boss_score = 1500
        self.shake = 0
        self.banner = ("GET READY", pygame.time.get_ticks() + 1800)

    @property
    def diff(self):
        return 1 + self.score // 400

    @property
    def boss_alive(self):
        return any(e.kind == "boss" for e in self.enemies)

    def new_enemy(self, kind, pos):
        e = Enemy(kind, self.diff, pos)
        self.enemies.add(e)
        return e

    def spawn(self, now):
        if now < self.next_spawn:
            return
        d = self.diff
        cap = min(22, 6 + d * 2)
        if self.boss_alive:
            self.next_spawn = now + 2600
            if len(self.enemies) < 6 and random.random() < 0.6:
                self.new_enemy("red", right_spawn())
            return
        self.next_spawn = now + max(380, 1200 - d * 60)
        if len(self.enemies) >= cap:
            return
        r = random.random()
        if r < 0.45:
            self.new_enemy("red", right_spawn())
        elif r < 0.75:
            y = random.randint(120, H - 120)
            for i in range(3):                                      
                e = self.new_enemy("green", (W + 60 + i * 70, y))
                e.t -= i * 0.55
        else:
            self.new_enemy("blue", right_spawn())

    def hurt_player(self, dmg, now):
        p = self.player
        if now < p.invuln_until or now < p.shield_until:
            return
        p.hp -= dmg
        self.shake = 12
        explode(p.fx, p.fy, 0.5)
        if p.hp <= 0:
            explode(p.fx, p.fy, 2.2)
            p.lives -= 1
            if p.lives <= 0:
                self.over = True
                self.high = max(self.high, self.score)
            else:
                p.hp = 100
                p.weapon = max(1, p.weapon - 1)
                p.invuln_until = now + 2500
                p.fx, p.fy = 90.0, H / 2
                self.ebullets.empty()

    def kill_enemy(self, e):
        self.score += e.score
        explode(e.fx, e.fy, 2.6 if e.kind == "boss" else 1.0)
        if e.kind == "boss":
            self.shake = 25
            self.banner = ("BOSS DESTROYED!", pygame.time.get_ticks() + 2000)
            self.boss_score = self.score + 2000
            for k in ("W", "H", "S"):
                self.powerups.add(PowerUp(int(e.fx) + random.randint(-50, 50), int(e.fy) + random.randint(-50, 50), k))
        elif random.random() < 0.12:
            self.powerups.add(PowerUp(int(e.fx), int(e.fy), random.choices("WHS", [5, 3, 2])[0]))
        e.kill()

    def update(self, inp, now):
        dx, dy, fire = inp
        p = self.player
        if self.paused or self.over:
            update_background(0, 0)
            update_particles()
            return
        p.update(dx, dy)
        update_background(5.0, 0.0)                                     
        if fire:
            p.shoot(now, self.bullets)

        if self.score >= self.boss_score and not self.boss_alive:
            self.new_enemy("boss", right_spawn())
            self.boss_score = 10 ** 9
            self.banner = ("WARNING: BOSS", now + 2200)

        self.spawn(now)
        self.bullets.update()
        self.ebullets.update()
        self.powerups.update()
        Enemy.pending = []
        for e in self.enemies:
            e.update(p, self.ebullets, self.diff)
        for x, y, ang, sp in Enemy.pending:
            self.ebullets.add(Bullet(x, y, ang, sp, False))

                                   
        for b in list(self.bullets):
            for e in self.enemies:
                if e.hitbox.colliderect(b.rect):
                    e.hp -= b.dmg
                    explode(b.rect.centerx, b.rect.centery, 0.2)
                    b.kill()
                    if e.hp <= 0:
                        self.kill_enemy(e)
                    break

                                          
        for b in list(self.ebullets):
            if p.hitbox.colliderect(b.rect):
                b.kill()
                self.hurt_player(12, now)
        for e in list(self.enemies):
            if p.hitbox.colliderect(e.hitbox):
                if e.kind != "boss":
                    self.kill_enemy(e)
                    self.score -= e.score                                 
                self.hurt_player(25, now)

                 
        for pu in list(self.powerups):
            if p.hitbox.colliderect(pu.rect.inflate(10, 10)):
                if pu.kind == "W":
                    p.weapon = min(4, p.weapon + 1)
                elif pu.kind == "H":
                    p.hp = min(100, p.hp + 40)
                else:
                    p.shield_until = now + 6000
                explode(pu.rect.centerx, pu.rect.centery, 0.4, [(255, 255, 255), (150, 220, 255)])
                pu.kill()
        update_particles()

    def draw_hud(self, now):
        p = self.player
        screen.blit(font.render(f"SCORE {self.score:06d}", True, (255, 255, 255)), (16, 12))
        screen.blit(small_font.render(f"HIGH {self.high:06d}", True, (160, 170, 200)), (16, 38))
        pygame.draw.rect(screen, (40, 40, 60), (W - 230, 14, 210, 18), border_radius=4)
        col = (90, 220, 100) if p.hp > 50 else (240, 190, 60) if p.hp > 25 else (230, 60, 60)
        pygame.draw.rect(screen, col, (W - 228, 16, int(206 * max(0, p.hp) / 100), 14), border_radius=3)
        pygame.draw.rect(screen, (200, 200, 220), (W - 230, 14, 210, 18), 2, border_radius=4)
        for i in range(max(0, p.lives)):
            screen.blit(pygame.transform.smoothscale(PLAYER_IMG, (32, 20)), (W - 230 + i * 38, 40))
        screen.blit(small_font.render(f"WEAPON LV {p.weapon}", True, (120, 190, 255)), (W - 230, 66))
        screen.blit(small_font.render(f"WAVE {self.diff}", True, (200, 200, 120)), (W // 2 - 30, 12))
        for e in self.enemies:
            if e.kind == "boss":
                bw = 400
                x = W // 2 - bw // 2
                pygame.draw.rect(screen, (40, 20, 50), (x, H - 30, bw, 14), border_radius=4)
                pygame.draw.rect(screen, (200, 70, 220), (x + 2, H - 28, int((bw - 4) * max(0, e.hp) / e.max_hp), 10), border_radius=3)
                pygame.draw.rect(screen, (230, 200, 240), (x, H - 30, bw, 14), 2, border_radius=4)
        text, until = self.banner
        if now < until:
            surf = big_font.render(text, True, (255, 230, 120))
            surf.set_alpha(255 if until - now > 400 else int(255 * (until - now) / 400))
            screen.blit(surf, surf.get_rect(center=(W // 2, H // 3)))

    def draw(self, now):
        draw_background()
        for pu in self.powerups:
            pu.draw(screen)
        for b in self.bullets:
            b.draw(screen)
        for b in self.ebullets:
            b.draw(screen)
        for e in self.enemies:
            e.draw(screen)
        if not self.over:
            self.player.draw(screen, now)
        draw_particles()
        self.draw_hud(now)

        if self.paused:
            t = big_font.render("PAUSED", True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=(W // 2, H // 2)))
            h = font.render("Press P to resume", True, (200, 200, 220))
            screen.blit(h, h.get_rect(center=(W // 2, H // 2 + 50)))
        if self.over:
            dim = pygame.Surface((W, H), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 150))
            screen.blit(dim, (0, 0))
            t = big_font.render("GAME OVER", True, (255, 90, 90))
            screen.blit(t, t.get_rect(center=(W // 2, H // 2 - 40)))
            s = font.render(f"Score {self.score}   High {self.high}", True, (255, 255, 255))
            screen.blit(s, s.get_rect(center=(W // 2, H // 2 + 20)))
            r = font.render("R = restart     M = main menu", True, (200, 200, 220))
            screen.blit(r, r.get_rect(center=(W // 2, H // 2 + 60)))
        if self.shake > 0:
            self.shake -= 1
            ox, oy = random.randint(-4, 4), random.randint(-4, 4)
            copy = screen.copy()
            screen.fill((0, 0, 0))
            screen.blit(copy, (ox, oy))


                                                                            
                                                     
                                                                            
def read_input(game):
    p = game.player
    if DEMO:
        near, best = None, 1e9
        for e in game.enemies:
            if e.fx < p.fx:
                continue
            d = math.hypot(e.fx - p.fx, e.fy - p.fy)
            if d < best:
                best, near = d, e
        if near is None:
            return (110 - p.fx) * 0.02, (H / 2 - p.fy) * 0.01, True
        dy = max(-1.0, min(1.0, (near.fy - p.fy) * 0.05))
        if best < 150:                                              
            dy = -dy
        return (110 - p.fx) * 0.02, dy, True
    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
    fire = keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]
    return dx, dy, fire


                                                                            
                                    
                                                                            
def panel(rect, title):
    s = pygame.Surface(rect.size, pygame.SRCALPHA)
    s.fill((10, 12, 30, 195))
    screen.blit(s, rect.topleft)
    pygame.draw.rect(screen, (90, 110, 190), rect, 2, border_radius=8)
    t = font.render(title, True, (255, 220, 110))
    screen.blit(t, (rect.x + 16, rect.y + 10))
    pygame.draw.line(screen, (70, 85, 150), (rect.x + 14, rect.y + 38), (rect.right - 14, rect.y + 38))


def keycap(text, x, y):
    t = small_font.render(text, True, (235, 240, 255))
    r = pygame.Rect(x, y, t.get_width() + 14, 24)
    pygame.draw.rect(screen, (45, 52, 85), r, border_radius=5)
    pygame.draw.rect(screen, (165, 175, 215), r, 2, border_radius=5)
    screen.blit(t, t.get_rect(center=r.center))
    return r.right + 5


def label(text, x, y, color=(215, 220, 240), f=None):
    screen.blit((f or small_font).render(text, True, color), (x, y))


def draw_menu(tick, high):
    draw_background()
    t = tick / 60.0

                                                                         
    pulse = 0.5 + 0.5 * math.sin(t * 2)
    title = big_font.render(TITLE, True, (255, 235, 140))
    shadow = big_font.render(TITLE, True, (200, 90, 40))
    cx = W // 2
    screen.blit(shadow, shadow.get_rect(center=(cx + 3, 56 + 3)))
    screen.blit(title, title.get_rect(center=(cx, 56)))
    sub = font.render(SUBTITLE, True, (150 + int(80 * pulse), 200, 255))
    screen.blit(sub, sub.get_rect(center=(cx, 100)))
    bob = math.sin(t * 2.2) * 6
    screen.blit(PLAYER_IMG, PLAYER_IMG.get_rect(center=(80, 58 + bob)))
    draw_flame(screen, 80 - 34, 58 + bob, 0.0, 14 + random.randint(0, 8), 6)
    foe = rotated("red", ENEMY_IMG["red"], math.pi)
    screen.blit(foe, foe.get_rect(center=(W - 80, 58 - bob)))
    draw_flame(screen, W - 80 + 28, 58 - bob, math.pi, 10 + random.randint(0, 8), 5)

                                                                           
    left = pygame.Rect(30, 128, 470, 316)
    panel(left, "HOW TO PLAY")
    y = left.y + 50
    dx = left.x + 285
    x = left.x + 16
    for c in ("W", "A", "S", "D"):
        x = keycap(c, x, y)
    label("or", x, y + 4, (150, 160, 190))
    keycap("ARROWS", x + 24, y)
    label("Move ship", dx, y + 4)
    y += 32
    x = keycap("LEFT CLICK", left.x + 16, y)
    label("or", x, y + 4, (150, 160, 190))
    keycap("SPACE", x + 24, y)
    label("Shoot (hold)", dx, y + 4)
    y += 32
    keycap("P", left.x + 16, y)
    label("Pause", left.x + 56, y + 4)
    keycap("ESC", left.x + 160, y)
    label("Back to menu", left.x + 212, y + 4)
    y += 40
    pygame.draw.line(screen, (70, 85, 150), (left.x + 14, y - 8), (left.right - 14, y - 8))
    for line in TIPS:
        label(line, left.x + 16, y, (190, 200, 225))
        y += 19

                                                                            
    right = pygame.Rect(520, 128, 410, 316)
    panel(right, "ENEMIES & POWER-UPS")
    y = right.y + 52
    rows = [
        ("red", "RED", (240, 90, 100), "Fast, flies straight at you", "10"),
        ("green", "GREEN", (130, 220, 80), "Wavy squad of 3", "25"),
        ("blue", "BLUE", (90, 160, 240), "Hovers & shoots at you", "40"),
        ("boss", "BOSS", (200, 110, 240), "Every ~2000 pts", "1000"),
    ]
    for kind, name, col, desc, pts in rows:
        img = ENEMY_IMG[kind]
        sw = 62 if kind != "boss" else 70
        sh = int(img.get_height() * sw / img.get_width())
        spr = pygame.transform.smoothscale(img, (sw, sh))
        spr = pygame.transform.flip(spr, True, False)
        screen.blit(spr, spr.get_rect(center=(right.x + 48, y + 12)))
        label(name, right.x + 94, y - 2, col, font)
        label(desc, right.x + 94, y + 18, (205, 210, 230))
        label(f"+{pts}", right.right - 70, y + 4, (255, 230, 120), font)
        y += 44
    pygame.draw.line(screen, (70, 85, 150), (right.x + 14, y - 4), (right.right - 14, y - 4))
    y += 8
    for letter, col, desc in (("W", (80, 160, 255), "Weapon upgrade (up to Lv 4)"),
                              ("H", (90, 255, 120), "Repair: +40 health"),
                              ("S", (255, 230, 80), "Shield for 6 seconds")):
        g = PowerUp.KINDS[letter][0]
        c = (right.x + 34, y + 9)
        screen.blit(g, g.get_rect(center=c))
        pygame.draw.circle(screen, col, c, 11)
        pygame.draw.circle(screen, (255, 255, 255), c, 11, 2)
        lt = small_font.render(letter, True, (10, 10, 30))
        screen.blit(lt, lt.get_rect(center=c))
        label(desc, right.x + 62, y + 1, (215, 220, 240))
        y += 27

                                                                                 
    if (tick // 30) % 2 == 0:
        s = font.render("PRESS  ENTER  OR  CLICK  TO  START", True, (255, 255, 255))
        screen.blit(s, s.get_rect(center=(cx, 482)))
    label(f"HIGH SCORE {high:06d}", cx - 85, 507, (160, 170, 200))


def main():
    state = "play" if DEMO else "menu"
    pygame.mouse.set_visible(state == "menu")
    game = Game()
    frames = 0
    menu_tick = 0
    while True:
        now = pygame.time.get_ticks()
        start = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if state == "menu":
                    if ev.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        start = True
                else:
                    if ev.key == pygame.K_ESCAPE:
                        game.high = max(game.high, game.score)
                        state = "menu"
                        pygame.mouse.set_visible(True)
                    if ev.key == pygame.K_p and not game.over:
                        game.paused = not game.paused
                    if ev.key == pygame.K_r and game.over:
                        game = Game(game.high)
                    if ev.key == pygame.K_m and game.over:
                        state = "menu"
                        pygame.mouse.set_visible(True)
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and state == "menu":
                start = True

        if state == "menu":
            menu_tick += 1
            update_background(1.2, 0.3)
            draw_menu(menu_tick, game.high)
            if start:
                game = Game(game.high)
                state = "play"
                pygame.mouse.set_visible(False)
        else:
            inp = read_input(game)
            game.update(inp, now)
            game.draw(now)

        pygame.display.flip()
        clock.tick(FPS)
        frames += 1
        if DEMO and "--frames" in sys.argv and frames > int(sys.argv[sys.argv.index("--frames") + 1]):
            if "--shot" in sys.argv:
                pygame.image.save(screen, sys.argv[sys.argv.index("--shot") + 1])
            break


if __name__ == "__main__":
    main()