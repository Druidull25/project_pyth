import pygame
import math
import random

pygame.init()

ecran_lungime = 800
ecran_inaltime = 600

clock = pygame.time.Clock()
FPS = 60

gravitatie = 0.75


fundal = pygame.image.load('7481714.jpg')
fundal = pygame.transform.scale(fundal, ((int(fundal.get_width() * 0.3), int(fundal.get_height()* 0.3))))
singleplayer = pygame.image.load('SINGLEPLAYER.png')
multiplayer = pygame.image.load('MULTIPLAYER.png')
star = pygame.image.load('start.png')
phantom = pygame.image.load('phantom.png')
sword = pygame.image.load('sword.png')
phantom = pygame.transform.scale(phantom, ((int(phantom.get_width() * 0.3), int(phantom.get_height()* 0.3))))
sword = pygame.transform.scale(sword, ((int(sword.get_width() * 0.3), int(sword.get_height()* 0.3))))
knight = pygame.image.load('fire_knight.png')
mauler = pygame.image.load('crystal_mauler.png')
knight = pygame.transform.scale(knight, ((int(knight.get_width() * 1.2), int(knight.get_height()* 1.2))))
mauler = pygame.transform.scale(mauler, ((int(mauler.get_width() * 0.8), int(mauler.get_height()* 0.8))))
bubble = pygame.image.load('bubble.png')
bubble = pygame.transform.scale(bubble, ((int(bubble.get_width() * 6), int(bubble.get_height()* 6))))
bubble.set_alpha(150)
pygame.display.set_icon(knight)
pygame.display.set_caption("Phantom Sword")

im1 = 'fire_knight'
im2 = 'Crystal_Mauler'
mm = True

ecran = pygame.display.set_mode((ecran_lungime,ecran_inaltime))

class button():
    def __init__(self,x,y,img,scara):
        lungime = img.get_width()
        inaltime = img.get_height()
        self.image = pygame.transform.scale(img, (int(lungime * scara), int(inaltime * scara)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self, check, check2):
        ecran.blit(self.image, (self.rect.x, self.rect.y))

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                return True
        if pygame.mouse.get_pressed()[0] == 0:
            return False

class fighter (pygame.sprite.Sprite):
    def __init__(self, x, y, scara, speed, imm):
        pygame.sprite.Sprite.__init__(self)
        self.animations = []
        self.ind = 0
        self.action = 0
        aux = []
        for i in range(1,9):
            img = pygame.image.load(f'{imm}/png/{imm}/01_idle/idle_{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scara), int (img.get_height() * scara)))
            aux.append(img)
        self.animations.append(aux)
        aux = []
        for i in range(1,9):
            img = pygame.image.load(f'{imm}/png/{imm}/02_run/run_{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scara), int (img.get_height() * scara)))
            aux.append(img)
        self.animations.append(aux)

        aux = []
        for i in range(1,8):
            img = pygame.image.load(f'{imm}/png/{imm}/05_1_atk/1_atk_{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scara), int (img.get_height() * scara)))
            aux.append(img)
        self.animations.append(aux)  

        aux = []
        for i in range(1,11):
            img = pygame.image.load(f'{imm}/png/{imm}/11_death/death_{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scara), int (img.get_height() * scara)))
            aux.append(img)
        self.animations.append(aux)  

        self.image = self.animations[self.action][self.ind]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed=speed
        self.flip = False
        self.jump = False
        self.grav = 0
        self.is_jumping = False
        self.update_anim = pygame.time.get_ticks()
        self.attack = 0
        self.is_attacking = 0 
        self.health = 150
        self.alive = True
        self.is_attacked = False
        self.horvel = 0
        self.hitpoint = 0
        self.push = False
        self.shield = False
        self.energy = 100
        self.damage = 20

    def move(self, moving_left,moving_right):
        dx = 0
        dy = 0
        if self.shield == False:
            if self.is_attacked == True:
                self.horvel = 16 * self.hitpoint
                self.is_attacked = False
                self.push = True

            if moving_left and moving_right == False and self.push == False:
                self.flip = True
                dx -= self.speed
            if moving_right and self.push == False:
                self.flip = False
                dx += self.speed
            elif moving_left == False and moving_right == False and self.is_attacking == 0:
                self.action = 0


            if self.push == True:
                dx += self.horvel
                self.horvel -= 2*self.hitpoint
            if self.horvel == 0:
                self.push = False
            if self.jump == True:
                self.grav = -17
                self.jump = False
                self.is_jumping = True
        

            if self.is_jumping == True:

                self.grav += gravitatie

                if self.grav > 10:
                    self.grav

                dy += self.grav
                if self.rect.bottom + dy > 600:
                    dy = 600 - self.rect.bottom
                    self.is_jumping = False
            if self.rect.x + dx < -290:
                dx = 0
                self.health = 0
            if self.rect.x + dx > 450:
                dx = 450 - self.rect.x
                self.health = 0
            self.rect.x += dx
            self.rect.y += dy


    def update_anima (self, moving_left, moving_right):

        anim = 100

        if self.attack == 1 and self.action != 3:
            self.action = 2
            self.ind = 0
            self.attack = 0
            self.is_attacking = 1

        self.image = self.animations [self.action][self.ind]
        if pygame.time.get_ticks() - self.update_anim > anim:
            self.update_anim = pygame.time.get_ticks()
            self.ind += 1
        if self.ind >= len(self.animations[self.action]) and self.action != 3:
            if self.action == 2:
                if moving_left == False and moving_right == False:
                    self.action =0
                else:
                    self.action = 1
                self.is_attacking = 0
            self.ind = 0
        elif self.action == 3 and self.ind ==  len(self.animations[self.action]):
            self.ind = len(self.animations[self.action]) - 1



    def check_alive(self):
        
        if self.health <= 0:
            self.alive = False
            self.speed = 0
            self.action = 3
            self.index = 0


        

    def draw(self):
        ecran.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
        if self.shield == True:
            ecran.blit(bubble,(self.rect.x+240,self.rect.y+150))


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self. max_health = max_health

    def draw(self, health):
        self.health = health

        ratio = self.health / self.max_health

        pygame.draw.rect(ecran, (255, 0, 0), (self.x, self.y, 150, 20))
        pygame.draw.rect(ecran, (0, 255, 0), (self.x, self.y, 150  * ratio, 20))

class EnergyBar():
    def __init__(self, x, y, energy, max_energy):
        self.x = x
        self.y = y
        self.energy = energy
        self. max_energy = max_energy

    def draw(self, energy):
        self.energy = energy

        ratio = self.energy / self.max_energy

        pygame.draw.rect(ecran, (255, 0, 0), (self.x, self.y, 100, 10))
        pygame.draw.rect(ecran, (0, 0, 255), (self.x, self.y, 100  * ratio, 10))


def attack(self,other):
    if self.attack== 1 and (math.sqrt((self.rect.x - other.rect.x) * (self.rect.x - other.rect.x) + (self.rect.y -other.rect.y) * (self.rect.y -other.rect.y)) <= 140) and ((self.flip == False and self.rect.x <= other.rect.x) or (self.flip == True and self.rect.x >= other.rect.x)):
        if other.shield == False:
            other.health -= self.damage
            other.is_attacked = True
            if other.rect.x > self.rect.x:
                other.hitpoint = 1
            else:
                other.hitpoint = -1
        else:
            other.energy -= 10
            self.is_attacked = True
            if other.rect.x > self.rect.x:
                self.hitpoint = -1
            else:
                self.hitpoint = 1
            if other.energy <= 0:
                other.shield= False

inrange = False
inrange2 = False

att = 200
update_att = pygame.time.get_ticks()

start=button(335, 420, star, 0.3)
single=button(335, 390, singleplayer, 0.3)
multi=button(335, 450, multiplayer, 0.3)

menu1 = False
mode = False



r = True


while mm:
    clock.tick(FPS)
    ecran.fill((0,0,0))
    ecran.blit(phantom,(300,100))
    ecran.blit(sword,(325,150))
    ecran.blit(knight,(100,100))
    if menu1 == False:
        if start.draw(menu1,r) == True:
            menu1 = True
    else:
        if single.draw(mm,r) == True:
            mm = False
            mode = True
        elif multi.draw(mm,r) == True:
            mm= False
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r=False
            mm = False



player1 = fighter(100,460,2.2,5, im1)
player2 = fighter(750,460,2.2,5, im2)
player2.flip = True

if mode == True:
    player2.health = 130
    player2.energy = 60
    player1.damage = 25

healt_bar1 = HealthBar(10, 80, player1.health, player1.health)
energy_bar1= EnergyBar(10,100,player1.energy,player1.energy)
moving_left1 = False
moving_right1 = False
jumping1 = False

healt_bar2 = HealthBar(635, 80, player2.health, player2.health)
energy_bar2= EnergyBar(685,100,player2.energy,player2.energy)
moving_left2 = False
moving_right2 = False
jumping2 = False


while r:

    if r:
        ecran.blit(fundal,(0,0))
        clock.tick(FPS)
        hel = player2.health
        attack(player1,player2)
        attack(player2,player1)
        ecran.blit(knight,(10,15))
        ecran.blit(mauler,(730,30))
        healt_bar1.draw(player1.health)
        energy_bar1.draw(player1.energy)
        healt_bar2.draw(player2.health)
        energy_bar2.draw(player2.energy)

        player1.update_anima(moving_left1,moving_right1)
        player1.draw()
        player1.move(moving_left1, moving_right1)
        player1.check_alive()

        player2.update_anima(moving_left2,moving_right2)
        player2.draw()
        player2.move(moving_left2, moving_right2)
        player2.check_alive()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r=False
            if event.type == pygame.KEYDOWN:
                if player1.alive == True:
                    if event.key == pygame.K_f:
                        if player1.is_attacking == 0 and player1.shield == False and player1.is_jumping == False:
                            player1.attack = 1
                    if event.key == pygame.K_a and player1.shield == False:
                        moving_left1 = True
                        if moving_right1 == True:
                            moving_right1 = False
                        if player1.is_attacking ==0:
                            player1.action = 1
                    if event.key == pygame.K_d and player1.shield == False:
                        if player1.is_attacking == 0 :
                            player1.action = 1
                        moving_right1 = True
                        if moving_left1 == True:
                            moving_left1 = False
                    if event.key == pygame.K_w and player1.is_jumping == False and player1.shield == False and player1.is_attacking == 0:
                        player1.jump = True
                    if event.key == pygame.K_e and player1.is_jumping == False and player1.action < 1 and player1.energy > 0:
                        player1.shield = True
                if player2.alive == True and mode == False:
                    if event.key == pygame.K_l:
                        if player2.is_attacking == 0 and player2.shield == False and player2.is_jumping == False:
                            player2.action = 1
                        moving_right2 = True
                        moving_left2 = False
                    if event.key == pygame.K_j and player2.shield == False:
                        moving_left2 = True
                        moving_right2 = False
                        if player2.is_attacking == 0:
                            player2.action = 1
                    if event.key == pygame.K_i and player2.is_jumping == False and player2.shield == False and player2.is_attacking == 0:
                        player2.jump = True
                    if event.key == pygame.K_p and player2.shield == False:
                        if player2.is_attacking == 0:
                            player2.attack = 1
                    if event.key == pygame.K_o and player2.is_jumping == False and player2.action < 1 and player2.energy >0:
                        player2.shield = True
        if mode == True:
            player1.speed = 6
            player2.damage = 15
            if math.sqrt((player1.rect.x - player2.rect.x) * (player1.rect.x - player2.rect.x) + (player1.rect.y -player2.rect.y) * (player1.rect.y -player2.rect.y)) > 70 and player2.health > 0:
                inrange = False
                inrange2 = False
                player2.shield = False
                if player2.rect.x > player1.rect.x:
                    if player2.is_attacking == 0:
                        player2.action = 1
                    moving_left2 = True
                    moving_right2 = False
                else:
                    if player2.is_attacking == 0:
                        player2.action = 1
                    moving_left2 = False
                    moving_right2 = True
            elif player2.health > 0:
                if inrange == False:
                    inrange = True
                    update_att = pygame.time.get_ticks()
                else:
                    moving_left2 = False
                    moving_right2 = False 
                    if random.randrange(1,11) == 1 and player2.health > 0 and player1.health > 0:
                        if inrange2 == False:
                            player2.shield = True
                            inrange2 = True
                            update_att = pygame.time.get_ticks()
                        else:
                            if update_att - pygame.time.get_ticks() > att or update_att - pygame.time.get_ticks() < (-1)*att:
                                inrange2 = False
                                player2.shield = False

                    if update_att - pygame.time.get_ticks() > att or update_att - pygame.time.get_ticks() < (-1)*att and player2.shield == False:
                        update_att = pygame.time.get_ticks()
                        if player2.is_attacking == 0:
                            if player2.rect.x > player1.rect.x:
                                player2.flip = True
                            else:
                                player2.flip = False
                            if player2.shield == False:
                                player2.attack = 1
            if player1.health <= 0:
                player2.action = 0
                player2.speed = 0



    if event.type == pygame.KEYUP:
        if event.key == pygame.K_e:
            player1.shield = False
        if event.key == pygame.K_a:
            moving_left1 = False
        if event.key == pygame.K_d:
            moving_right1 = False
        if event.key == pygame.K_j and mode == False:
            moving_left2 = False
        if event.key == pygame.K_l and mode == False:
            moving_right2 = False
        if event.key == pygame.K_o:
            player2.shield = False
        
    pygame.display.update()

pygame.quit()