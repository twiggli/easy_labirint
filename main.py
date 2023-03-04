
from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_spped):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_spped

    def update(self):
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
            platforms_touched = sprite.spritecollide(self, barries, False)
            if self.x_speed > 0:
                for p in platforms_touched:
                    self.rect.right = min(self.rect.right, p.rect.left)
            elif self.x_speed < 0:
                for p in platforms_touched:
                    self.rect.left = max(self.rect.left, p.rect.right)
                
        if packman.rect.y <= win_width-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
            platforms_touched = sprite.spritecollide(self, barries, False)
            if self.y_speed > 0:
                for p in platforms_touched:
                    self.rect.bottom = min(self.rect.bottom, p.rect.top)
            elif self.y_speed < 0:
                for p in platforms_touched:
                    self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet-png-1024.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
        
class Enemy2(GameSprite):
    side = 'up'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.y <= 290:
            self.side = 'up'
        if self.rect.y >= 420:
            self.side = 'down'
        if self.side == 'down':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
     
        if self.rect.x > win_width+10:
            self.kill()

win_width = 700
win_height = 500
display.set_caption('Лабиринт')
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)

barries = sprite.Group()

bullets = sprite.Group()

monsters = sprite.Group()

monsters_up = sprite.Group()

w1 = GameSprite('bricks-wall-png-4.png', win_width / 2 - win_width / 3, win_height / 2, 270, 30)
w2 = GameSprite('bricks-wall-png-4.png', 370, 100, 30, 180)
w3 = GameSprite('bricks-wall-png-4.png', 370, 370, 30, 150)

barries.add(w1)
barries.add(w2)
barries.add(w3)

packman = Player('meme-6195988_1920.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('the-end-flag-arrival-destination-end-finish-svg-png-icon-2.png', win_width - 85, win_height - 100, 80, 80)

monster1 = Enemy('Monster-Energy-PNG-Photos.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('Monster-Energy-PNG-Photos.png', win_width - 80, 240, 80, 80, 5)
monster3 = Enemy2('Monster-Energy-PNG-Photos.png', win_width - 400, 280, 80, 80, 5)

monsters.add(monster1)
monsters.add(monster2)
monsters_up.add(monster3)

finish = False

run = True
while run:
    time.delay(50)

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
            elif e.key == K_SPACE:
                packman.fire()

    if not finish:
        window.fill(back)
        


        packman.update()
        bullets.update()

        packman.reset()

        bullets.draw(window)
        barries.draw(window)
        final_sprite.reset()

        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(monsters_up, bullets, True, True)

        monsters_up.update()
        monsters.update()

        monsters.draw(window)
        monsters_up.draw(window)

        sprite.groupcollide(bullets, barries, True, False)

        packman.update()
        if sprite.spritecollide(packman, monsters, monsters_up, False):
            finish = True

            img = image.load('360_F_312548010_JsXZ9vxIXTbgZlDr1IwlMTogrN84BN1L.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True

            img = image.load('e94364e95ec516ff4eebc9d2391e6aca.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

    display.update()

