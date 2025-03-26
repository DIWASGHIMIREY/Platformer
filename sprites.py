# Sprite classes for platform game
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.running = False
        self.game = game
        self.idle = []
        self.run_img_r = []
        self.run_img_l = []


        self.load_img()



        self.image = self.idle[0]


        # self.image = pg.Surface((30, 40))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.last_update = 0

        self.current_frame = 0

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0: self.running = True
        else: self.running = False
        if not self.running:
            if now - self.last_update > 500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.idle)
                self.image = self.idle[self.current_frame]
                self.rect = self.image.get_rect()
        if self.running:
            if now - self.last_update > 500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.idle)
                self.image = self.run_img_r[self.current_frame]
                self.rect = self.image.get_rect()
    def load_img(self):
        for i in range(1,4):
            filename = f"Sprites/idle{i}.png"
            img = pg.image.load(filename)
            img = pg.transform.scale(img, (50,70))
            self.idle.append(img)

        for i in range(1,7):
            filename = f"Sprites/run{i}.png"
            img_r = pg.image.load(filename)
            img_r = pg.transform.scale(img_r, (50,70))
            self.run_img_r.append(img_r)

        for frame in self.run_img_r:
            self.run_img_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC

        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y