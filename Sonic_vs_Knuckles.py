# Finishing Touches & Next Steps
import pygame
pygame.init()

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 350

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Sonic vs Knuckles")

background = pygame.transform.scale(pygame.image.load('./Assets/Images/neo_green_hill_BG.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()

quill_Sound = pygame.mixer.Sound('./Assets/Sound/Quill_Attack_Sound.wav')
knuckles_hit = pygame.mixer.Sound('./Assets/Sound/Knuckles_Hit.wav')
death_sound = pygame.mixer.Sound('./Assets/Sound/Knuckles_Death.wav')
jump_sound = pygame.mixer.Sound('./Assets/Sound/Sonic_Jump.wav')
sonic_hit = pygame.mixer.Sound('./Assets/Sound/Sonic_Hit.wav')

bgm = pygame.mixer.music.load('./Assets/Sound/Beach_Music.mp3')
pygame.mixer.music.play(-1)

hits = 0

class Player(object):
    walk_right = []
    walk_left = []
    for index in range(0, 9):
        load_frame_right = pygame.image.load('./Assets/Images/Sonic_R_' + str(index + 1) + '.png')
        walk_right.append(pygame.transform.scale(load_frame_right, (60, 64)))
        load_frame_left = pygame.image.load('./Assets/Images/Sonic_L_' + str(index + 1) + '.png')
        walk_left.append(pygame.transform.scale(load_frame_left, (60, 64)))
    jump_sprite = pygame.transform.scale(pygame.image.load('./Assets/Images/Sonic_Jump.png'), (60, 64))
    face_forward = pygame.transform.scale(pygame.image.load('./Assets/Images/Sonic_Face_Forward.png'), (60, 64))
    downward = pygame.transform.scale(pygame.image.load('./Assets/Images/Sonic_Down.png'), (60, 64))
    def __init__(self, x_coord, y_coord, CHAR_WIDTH, CHAR_HEIGHT):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.CHAR_WIDTH = CHAR_WIDTH
        self.CHAR_HEIGHT = CHAR_HEIGHT
        self.velocity = 5
        self.jumping = False
        self.jump_Count = 10
        self.LEFT = False
        self.RIGHT = False
        self.walk_Count = 0
        self.stand = True
        self.down = False
        self.hitbox = (self.x_coord + 15, self.y_coord + 10, 34, 49)

    def draw_Player(self, window):
        if self.walk_Count + 1 >= 27:
            self.walk_Count = 0
        if not (self.stand) and not (self.jumping):
            if self.LEFT:
                window.blit(self.walk_left[self.walk_Count//3], (self.x_coord, self.y_coord))
                self.walk_Count += 1
            elif self.RIGHT:
                window.blit(self.walk_right[self.walk_Count//3], (self.x_coord, self.y_coord))
                self.walk_Count += 1
        elif self.jumping:
            window.blit(self.jump_sprite, (self.x_coord, self.y_coord))
        elif self.down:
            window.blit(self.downward, (self.x_coord, self.y_coord))
        else:
            if self.RIGHT:
                window.blit(self.walk_right[0], (self.x_coord, self.y_coord))
            elif self.LEFT:
                window.blit(self.walk_left[0], (self.x_coord, self.y_coord))
            else:
               window.blit(self.face_forward, (self.x_coord, self.y_coord))
        
        self.hitbox = (self.x_coord + 15, self.y_coord + 10, 34, 49)
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
    def hit(self):
        self.x_coord = 50
        self.y_coord = 270
        self.walk_Count = 0
        font1 = pygame.font.SysFont('calibri', 100)
        text = font1.render('-5', 1, (225, 0, 0))
        window.blit(text, (WINDOW_WIDTH/2 - (text.get_width()/2), WINDOW_HEIGHT/2 - (text.get_height()/2)))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class Projectile(object):
    def __init__(self, x_coord, y_coord, radius, color, direction):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.radius = radius
        self.color = color
        self.direction = direction
        self.velocity = 8 * direction

    def draw_projectile(self, window):
        pygame.draw.circle(window, self.color, (self.x_coord, self.y_coord), self.radius)

class Enemy(object):
    walk_right = []
    walk_left = []
    for index in range(0, 11):
        load_frame_right = pygame.image.load('./Assets/Images/Knux_R_' + str(index + 1) + '.png')
        walk_right.append(pygame.transform.scale(load_frame_right, (60, 64)))
        load_frame_left = pygame.image.load('./Assets/Images/Knux_L_' + str(index + 1) + '.png')
        walk_left.append(pygame.transform.scale(load_frame_left, (60, 64)))
    def __init__(self, x_coord, y_coord, CHAR_WIDTH, CHAR_HEIGHT, end):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.CHAR_WIDTH = CHAR_WIDTH
        self.CHAR_HEIGHT = CHAR_HEIGHT
        self.end = end
        self.path = [self.x_coord, self.end]
        self.walk_Count = 0
        self.velocity = 3
        self.hitbox = (self.x_coord + 15, self.y_coord + 10, 36, 57)
        self.health = 20
        self.visible = True
    
    def draw_enemy(self, window):
        self.move()
        if self.visible:
            if self.walk_Count + 1 >= 33:
                self.walk_Count = 0
            
            if self.velocity > 0:
                window.blit(self.walk_right[self.walk_Count // 3], (self.x_coord, self.y_coord))
                self.walk_Count += 1
            else:
                window.blit(self.walk_left[self.walk_Count // 3], (self.x_coord, self.y_coord))
                self.walk_Count += 1
            pygame.draw.rect(window, (10, 10, 10), (self.hitbox[0] - 8, self.hitbox[1] - 21, 52, 12))
            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0] - 7, self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 255, 0), (self.hitbox[0] - 7, self.hitbox[1] - 20, 50 - ((50/20) * (20 - self.health)), 10))
            self.hitbox = (self.x_coord + 15, self.y_coord + 10, 34, 49)
            # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.velocity > 0:
            if self.x_coord + self.velocity < self.path[1]:
                self.x_coord += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walk_Count = 0
        else:
            if self.x_coord - self.velocity > self.path[0]:
                self.x_coord += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walk_Count = 0
    
    def hit(self):
        if self.health > 1:
            self.health -= 1
        elif self.health == 1:
            death_sound.play()
            self.visible = False
            self.health -= 1
        print('hit')


def redraw_game_window():
    window.blit(background, (0, 0))
    text = font.render('Score: ' + str(hits), 1, (0, 0, 100))
    window.blit(text, (370, 10))
    Sonic.draw_Player(window)
    Knuckles.draw_enemy(window)
    for quill in quills:
        quill.draw_projectile(window)
    pygame.display.update()

# main loop
font = pygame.font.SysFont('calibri', 30, True)
Sonic = Player(50, 270, 60, 64)
Knuckles = Enemy(100, 270, 60, 64, 450)
quill_charge = 0
quills = []
run = True
while run:
    clock.tick(27)

    if Sonic.hitbox[1] < Knuckles.hitbox[1] + Knuckles.hitbox[3] and Sonic.hitbox[1] + Sonic.hitbox[3] > Knuckles.hitbox[1] and Knuckles.visible:
        if Sonic.hitbox[0] + Sonic.hitbox[2] > Knuckles.hitbox[0] and Sonic.hitbox[0] < Knuckles.hitbox[0] + Knuckles.hitbox[2]:
            sonic_hit.play()
            Sonic.hit()
            hits -= 5

    if quill_charge > 0:
        quill_charge += 1;
    if quill_charge > 3:
        quill_charge = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for quill in quills:
        if quill.y_coord - quill.radius < Knuckles.hitbox[1] + Knuckles.hitbox[3] and quill.y_coord + quill.radius > Knuckles.hitbox[1] and Knuckles.visible:
            if quill.x_coord + quill.radius > Knuckles.hitbox[0] and quill.x_coord - quill.radius < Knuckles.hitbox[0] + Knuckles.hitbox[2]:
                Knuckles.hit()
                if Knuckles.health > 1:
                    knuckles_hit.play()
                hits += 1
                quills.pop(quills.index(quill))

        if quill.x_coord < 500 and quill.x_coord > 0:
            quill.x_coord += quill.velocity
        else:
            quills.pop(quills.index(quill))

    KEYS = pygame.key.get_pressed()

    if KEYS[pygame.K_SPACE] and quill_charge == 0:
        if Sonic.LEFT:
            direction = -1
        else:
            direction = 1
        if len(quills) < 5:
            quill_Sound.play()
            quills.append(Projectile((Sonic.x_coord + Sonic.CHAR_WIDTH // 2), round(Sonic.y_coord + Sonic.CHAR_HEIGHT // 2), 6, (0, 0, 255), direction))
        quill_charge = 1

    if KEYS[pygame.K_LEFT] and Sonic.x_coord > Sonic.velocity:
        Sonic.x_coord -= Sonic.velocity
        Sonic.LEFT = True
        Sonic.RIGHT = False
        Sonic.stand = False

    elif KEYS[pygame.K_RIGHT] and Sonic.x_coord < WINDOW_WIDTH - Sonic.CHAR_WIDTH - Sonic.velocity:
        Sonic.x_coord += Sonic.velocity
        Sonic.RIGHT = True
        Sonic.LEFT = False
        Sonic.stand = False

    elif KEYS[pygame.K_DOWN]:
        Sonic.down = True

    elif Sonic.jumping == True:
        Sonic.stand = False
    else:
        Sonic.stand = True
        Sonic.down = False
        Sonic.walk_Count = 0

    if not(Sonic.jumping):
        if KEYS[pygame.K_UP]:
            Sonic.jumping = True
            jump_sound.play()
            Sonic.RIGHT = False
            Sonic.LEFT = False
            Sonic.walk_Count = 0
    else:
        if Sonic.jump_Count >= -10:
            neg = 1
            if Sonic.jump_Count < 0:
                neg = -1
            Sonic.y_coord -= (Sonic.jump_Count ** 2) * 0.5 * neg
            Sonic.jump_Count -= 1 
        else:
            Sonic.jumping = False
            Sonic.stand = True
            Sonic.jump_Count = 10
    redraw_game_window()

pygame.quit()