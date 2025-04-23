# Sprite classes for platform game
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.running = False
        self.jumping = False
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
        if int(self.vel.x) != 0: self.running = True
        else: self.running = False
        if not self.running and not self.jumping:
            if now - self.last_update > 500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.idle)
                self.image = self.idle[self.current_frame]
                self.rect = self.image.get_rect()
        if self.jumping:
            self.image = pg.image.load("Sprites/idle3.png")
            self.rect = self.image.get_rect()
        if self.running:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.idle)
                self.image = self.run_img_r[self.current_frame]
                if self.vel.x < 0:
                    self.image = self.run_img_l[self.current_frame]

                self.rect = self.image.get_rect()
    def load_img(self):
        for i in range(1,4):
            filename = f"Sprites/idle{i}.png"
            img = pg.image.load(filename)
            # img = pg.transform.scale(img, (50,70))
            self.idle.append(img)

        for i in range(1,7):
            filename = f"Sprites/run{i}.png"
            img_r = pg.image.load(filename)
            # img_r = pg.transform.scale(img_r, (50,70))
            self.run_img_r.append(img_r)

        for frame in self.run_img_r:
            self.run_img_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.jumping = True
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
        # self.plat_img = []
        # self.image = pg.Surface((w, h))
        # self.image.fill(GREEN)

        self.image = pg.image.load("Sprites/Platforms/platform.png")

        # self.load_img()
        # self.image = ran.choice(self.plat_img)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # def load_img(self):
    #     for i in range(1,5):
    #         filename = f"Sprites/Platforms/platform{i}.png"
    #         img = pg.image.load(filename)
    #         # img = pg.transform.scale(img, (50,70))
    #         self.plat_img.append(img)



# class SpriteSheet():
#   def __init__(self, image):
#     self.sheet = image
#   def get_image(self, frame,framey, width, height, scale, color):
#     width_use = int(width*scale)
#     height_use = int(height*scale)
#     image = pg.Surface((width, height)).convert_alpha()
#     image.blit(self.sheet, (0, 0), ((frame * width), (framey*height), width, height))
#     image = pg.transform.scale(image, (width_use, height_use))
#     image.set_colorkey(color)
#
# sprite_sheet_image = pg.image.load('spritesheet.png')
# sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
# # size = 1
# for x in range(25):
#     for y in range(32):
#         #426X629
#         # if x == 6 and y==0:
#         plats.append(sprite_sheet.get_image(x, y, 17.04, 17.03,SCALE, BLACK))
#
#         image = sprite_sheet.get_image(x, y, 17.04, 17.03,SCALE, BLACK)
#         image.set_colorkey(BLACK)