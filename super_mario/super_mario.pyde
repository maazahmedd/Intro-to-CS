add_library('minim')
import random, os
path = os.getcwd()
player = Minim(this)
WIDTH = 1280
HEIGHT = 720

class Creature:
    def __init__(self, x, y, r, g, img_name, img_w, img_h, num_frames):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        self.num_frames = num_frames
        self.frame = 0
        self.dir = RIGHT
        
    def gravity(self):
        if self.y + self.r >= self.g:
            self.vy = 0
        else:
            self.vy += 0.3
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        
        for p in game.platforms:
            if self.y + self.r <= p.y and self.x + self.r >= p.x and self.x - self.r <= p.x + p.w:
                self.g = p.y
                break
            else:
                self.g = game.g
    
    def update(self):
        self.gravity()
        
        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
        
        if self.dir == RIGHT:
            image(self.img, self.x - self.img_w//2 - game.x_shift, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
            image(self.img, self.x - self.img_w//2 - game.x_shift, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
            
        # fill(255, 0, 0)
        # stroke(255, 0, 0)
        # strokeWeight(5)
        # noFill()
        # ellipse(self.x, self.y, self.r * 2, self.r * 2)

class Gomba(Creature):
    def __init__(self, x, y, r, g, img_name, img_w, img_h, num_frames, xl, xr):
        # super().__init__(x, y, r, g)
        Creature.__init__(self, x, y, r, g, img_name, img_w, img_h, num_frames)
        self.xl = xl
        self.xr = xr
        self.vx = random.randint(1, 5)
        self.dir = random.choice([LEFT, RIGHT])
        if self.dir == LEFT:
            self.vx *= -1

    
    def update(self):
        self.gravity()
    
        if frameCount%10 == 0:
            self.frame = (self.frame + 1) % self.num_frames
        
        if self.x < self.xl:
            self.vx *= -1
            self.dir = RIGHT
        elif self.x > self.xr:
            self.vx *= -1
            self.dir = LEFT
        
        self.x += self.vx
        self.y += self.vy
    
    
class Mario(Creature):
    def __init__(self, x, y, r, g, img_name, img_w, img_h, num_frames):
        # super().__init__(x, y, r, g)
        Creature.__init__(self, x, y, r, g, img_name, img_w, img_h, num_frames)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.alive = True
        self.jump_sound = player.loadFile(path + "/sounds/jump.mp3")
        
    def update(self):
        self.gravity()
        
        if self.key_handler[LEFT] == True:
            self.vx = -10
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.vx = 10
            self.dir = RIGHT
        else:
            # if not self.key_handler[UP] and self.y + self.r == self.g:
            self.vx = 0
            
        if self.key_handler[UP] and self.y + self.r == self.g:
            self.jump_sound.rewind()
            self.jump_sound.play()
            self.vy = -10
        
        if frameCount%5 == 0 and self.vx != 0 and self.vy == 0:
            self.frame = (self.frame + 1) % self.num_frames
        elif self.vx == 0:
            self.frame = 0
        
        self.x += self.vx
        self.y += self.vy

        if self.x - self.r < 0:
            self.x = self.r

        for g in game.gombas:
            if self.distance(g) <= self.r + g.r:
                if self.vy > 0:
                    game.gombas.remove(g)
                    self.vy = -10
                else:
                    self.alive = False
        
        if self.x >= game.w//2:
            game.x_shift += self.vx
        elif self.x < game.w//2:
            game.x_shift = 0    
        
    def distance(self, target):
        return ((self.x - target.x)**2 + (self.y -target.y)**2) ** 0.5

class Platform:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/" + img)
    
    def display(self):
        # fill(0, 125, 0)
        # rect(self.x, self.y, self.w, self.h)
        image(self.img, self.x  - game.x_shift, self.y, self.w, self.h)
        
class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.x_shift = 0
        self.mario = Mario(100, 100, 35, self.g, "mario.png", 100, 70, 11)
        self.background_sound = player.loadFile(path + "/sounds/background.mp3")
        self.background_sound.rewind()
        self.background_sound.loop()
        self.platforms = []
        for i in range(3):
            # 200, 500
            # 500, 400
            # 800, 300
            self.platforms.append(Platform(200+i*300, 500-i*100, 200, 50, "platform.png"))
        
        self.platforms.append(Platform(1500, 500, 200, 50, "platform.png"))
    
        self.gombas = []
        for g in range(5):
            self.gombas.append(Gomba(random.randint(200, 800), 100, 35, self.g, "gomba.png", 70, 70, 5, 200, 800))
        
        self.backgrounds = []
        for i in range(5, 0, -1):
            self.backgrounds.append(loadImage(path + "/images/layer_0" + str(i) + ".png"))
        
    def display(self):
        
        if self.mario.alive == False:
            fill(0, 0, 0)
            textSize(20)
            text("Game over", 600, 350)
            return
            
        strokeWeight(0)
        fill(0, 125, 0)
        rect(0, self.g, self.w, self.h)
        
        x = 0
        cnt = 0 
        for b in self.backgrounds:
            if cnt == 0:
                x = self.x_shift//4
            elif cnt == 1:
                x = self.x_shift//3
            elif cnt == 2:
                x = self.x_shift//2
            else:
                x = self.x_shift
                
            width_right = x % self.w
            width_left = self.w - width_right
            
            image(b, 0, 0, width_left, self.h, width_right, 0, self.w, self.h)
            image(b, width_left, 0, width_right, self.h, 0, 0, width_right, self.h)
            cnt += 1
        
        for p in self.platforms:
            p.display()
        
        for g in self.gombas:
            g.display()
        
        self.mario.display()

game = Game(WIDTH, HEIGHT, 585)

def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255, 255, 255)
    game.display()

def keyPressed():
    if keyCode == LEFT:
        game.mario.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.mario.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.mario.key_handler[UP] = True
    
def keyReleased():
    if keyCode == LEFT:
        game.mario.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.mario.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.mario.key_handler[UP] = False

def mouseClicked():
    global game
    if game.mario.alive == False:
        game.background_sound.pause()
        game = Game(WIDTH, HEIGHT, 585)
    
    
    
