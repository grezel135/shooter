from pygame import *
from random import *
mixer.init()
font.init()
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')
win_w = 700
win_h = 500
lost = 0
killed = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.size_x = size_x
        self.size_y = size_y
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullet.add(bullets)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_h:
            self.rect.y = 0
            self.rect.x = randint(80, win_w - 80)
            self.speed = randint(1, 5)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -50:
            self.kill()

window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700,500))
run = True
clock = time.Clock()
FPS = 60

player = Player("rocket.png", 300, 400, 80, 100, 5)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_w - 80), -50, 80, 50, randint(1, 5))
    monsters.add(monster)
font1 = font.SysFont(None, 40)
font2 = font.SysFont(None, 70)

bullets = sprite.Group()
win = font2.render('YOU WIN!', True, (255, 215, 0))
losee = font2.render('YOU LOSE', True, (200, 0, 0))



mixer.music.play()
finish = False
while run:
    window.blit(background, (0, 0))
    player.reset()
    player.update()
    monsters.update()
    monsters.draw(window)
    

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire.play()

    
    bullets.update()
    bullets.draw(window)
    
    if finish != True:
        if sprite.groupcollide(bullets, monsters, True, True):
            killed += 1
            monster = Enemy("ufo.png", randint(80, win_w - 80), -50, 80, 50, randint(1, 3))
            monsters.add(monster)
            if killed >= 100:
                window.blit(win, (200, 200))
                finish = True
        elif lost >= 10:
            window.blit(losee, (200,200))
            finish = True
        elif sprite.spritecollide(player, monsters, False, False):
            window.blit(losee, (200,200))
            finish = True
                
        lose = font1.render('Пропущено:' + str(lost), True, (255, 255, 255))
        kill = font1.render('Счёт:' + str(killed), True, (255, 255, 255))        
        window.blit(lose, (0, 30))
        window.blit(kill, (0, 0))


        clock.tick(FPS)
        display.update()