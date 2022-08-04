# importing the random module
import random
# creating global constants for width and height of the game, and the number of rows and columns (these can directly be changed if the user wants to play differently)
NUM_ROWS = 20
NUM_COLS = 10
WIDTH = 400
HEIGHT = 800
# creating a list called colors which stores all possible colors which the blocks can have
colors = [[255, 51, 52], [12, 150, 228], [30, 183, 66], [246, 187, 0], [76, 0, 153], [255, 255, 255], [0, 0, 0]]
# creating a list called blocks which will store all blocks which have been instantiated; initially this list is empty
blocks = []

# creating a Block class
class Block:
    def __init__(self):
        # each block has a colour attribute which is randomly generated
        self.colour = random.randint(0, 6)
        
        # the while loop below generates a random column for each block and checks if the block can take that column.
        # if there is already a block in the list of blocks which is at row = 0 and column = random column generated, then another random column is generated
        valid_col = False
        while valid_col == False:
            count = 0
            self.column = random.randint(0, NUM_COLS - 1)
            for block in blocks:
                if block.row == 0 and self.column == block.column:
                    count += 1
            # if no block in the list of blocks has row = 0 and column = random column generated, then valid_col is set to True and the random column is assigned to the new block
            if count == 0:
                valid_col = True
                
        self.row = 0
        # self.x = x coordinate of the top left corner of the block and self.y = y coordinate of the top left corner of the block 
        self.x = self.column * WIDTH/NUM_COLS
        self.y = 0
        # since the block moves down row by row, self.vy is the speed with which the block falls, i.e one row for every call of the display() method of the block class
        self.vy = HEIGHT/NUM_ROWS
        # a dictionary, self.key_handler stores the possible directions in which the blocks can move through key presses
        self.key_handler = {LEFT:False, RIGHT:False}
    
    def fall(self):
        # the for loop below iterates through all previous blocks in the blocks list (not the current block) and checks if the current block is one row above any of the previous blocks
        # if the case above is true, then the current block stops at its position, self.vy is set to 0 and the block will not fall below
        # this allows stacking of the blocks on top of each other
        for i in range(len(blocks) - 1):
            if self.x == blocks[i].x and self.y + self.vy == blocks[i].y:
                self.vy = 0
                
        # the if condition below checks if the block will go beyond the grid if self.vy is added. If so, it stops moving and self.vy is set to 0 again
        if self.y + self.vy == HEIGHT:
            self.vy = 0
            self.y = HEIGHT - (HEIGHT/NUM_ROWS)
            self.row = NUM_ROWS - 1
            
        # if self.vy is not 0 yet, then the block can move further below
        if self.vy != 0:
            self.y += self.vy
            self.row += 1
            
    def update(self):
        # the update() method will first call the fall() method where the block can fall
        self.fall()
        
        # the if condition below first checks if the left arrow key is pressed
        if self.key_handler[LEFT] == True:
            # the if condition below now checks if going left will allow the block to remain within the grid dimensions. The block can not go behind the 0th column.
            if self.x - WIDTH/NUM_COLS >= 0:
                # if the left arrow key is pressed but there is already a block present in that location, the block will not move because of the if condition below.
                # the current block is checked only against the previous blocks (not against itself)
                for i in range(len(blocks) - 1):
                    if self.column == blocks[i].column + 1 and (self.row == blocks[i].row):
                        self.key_handler[LEFT] = False
                        break
                    
                # if the block is able to move left (i.e not colliding with any other block), it will move one column to the left
                # note: holding down the key will make the block 'drift' to the left; i.e: it will move more than one column to the left
                if self.key_handler[LEFT] == True and self.vy != 0:
                    self.x -= WIDTH/NUM_COLS
                    self.column -= 1
                    self.key_handler[LEFT] = False
                    
            else:
                self.key_handler[LEFT] = False
        
        # the if condition below checks if the right arrow key has been pressed
        elif self.key_handler[RIGHT] == True:
            # the if condition now checks if adding one row to the right side of the block will allow it to remain within the grid dimensions as block can't go beyond the last column.
            if self.x + 2*(WIDTH/NUM_COLS) <= WIDTH:
                # if the right arrow key is pressed but there is already a block present in that location, the block will not move because of the if condition below.
                # the current block is only checked against previous blocks in the blocks list (not against itself)
                for i in range(len(blocks) - 1):
                    if self.column == blocks[i].column - 1 and (self.row == blocks[i].row):
                        self.key_handler[RIGHT] = False
                        break
                    
                # if the block is able to move right (i.e not colliding with any other block), it will move one column to the right
                # note: holding down the key will make the block 'drift' to the right; i.e: it will move more than one column to the right
                if self.key_handler[RIGHT] == True and self.vy != 0:
                    self.x += WIDTH/NUM_COLS
                    self.column += 1
                    self.key_handler[RIGHT] = False
                    
            else:
                self.key_handler[RIGHT] = False
   
    # the display() method will call the update() method first and then display the block with its colors using the colors list 
    def display(self):
        self.update()
        fill(colors[self.colour][0], colors[self.colour][1], colors[self.colour][2])
        rect(self.x, self.y, WIDTH/NUM_COLS, HEIGHT/NUM_ROWS)
    
# creating a Game class
class Game:
    def __init__(self):
        # game speed and score is set to zero whenever the game is started
        self.speed = 0
        self.score = 0
        # when the game starts, a block is instantiated and appended to the blocks list
        self.block = Block()
        blocks.append(self.block)
            
    def update(self):
        # the if condition below checks if the current block has stopped moving
        if self.block.vy == 0: 
            count = 0
            # a list called consecutive initially has rubbish values, but this will store the blocks below the current block if they have the same color
            consecutive = [0, 1, 2]
            # now the current block is compared to the 3 blocks below it (if they exist) to check for the same color
            for i in range(1, 4):
                for j in range(len(blocks) - 1):
                    if blocks[j].column == self.block.column and blocks[j].row == self.block.row + i:
                        if blocks[j].colour == self.block.colour:
                            consecutive[i - 1] = blocks[j]
                            count += 1
            # if all three blocks below the current block have the same color as the current block, then the 4 blocks are removed from the blocks list
            # the score is also incremented by 1 and game.speed is set back to 0
            if count == 3:
                self.score += 1
                self.speed = 0
                blocks.remove(self.block)
                for i in range(3):
                    blocks.remove(consecutive[i])
            
            # if the current block is not moving AND the grid is not filled, then a new block is instantiated and appended to the blocks list and game speed is increased
            if len(blocks) < NUM_ROWS * NUM_COLS:
                self.block = Block()
                self.speed += 0.25
                blocks.append(self.block)
        
    def display(self):
        # the display() method first calls the update() method above
        self.update()
        
        # the display() method then displays all the rectangles created and adds grid lines
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                noFill()
                stroke(180)
                rect(col * WIDTH/NUM_COLS, row * HEIGHT/NUM_ROWS, WIDTH/NUM_COLS, HEIGHT/NUM_ROWS)
        
        # the display() method goes over all the blocks in the blocks list and displays them
        for block in blocks:
            block.display()
            
        # over the course of the game, the score is shown at the top right of the grid
        # the text size and position will change if the HEIGHT and WIDTH of the grid is changed
        textSize(15 * HEIGHT/400)
        fill(0)
        text("Score: " + str(self.score), 130 * WIDTH/200, 15 * HEIGHT/400)
        
        # if the grid is completely filled with blocks, the game shows 'game over' and shows the final score
        # the text size and position will change if the HEIGHT and WIDTH of the grid is changed
        if len(blocks) == NUM_ROWS * NUM_COLS:
            textSize(25 * HEIGHT/400)
            fill(0)
            text("GAME OVER\nYour score: " + str(self.score) + "\nClick to restart", 15 * WIDTH/200, 200 * HEIGHT/400)

# a variable called game creates an instance of the game class
game = Game()

def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    # slow down the game by not displaying every frame
    if frameCount%(max(1, int(8 - game.speed))) == 0 or frameCount == 1:
        background(210)
        # this calls the display method of the game class
        game.display()
    
def keyPressed():
    # the keyPressed function changed the status of the left and right keys in the key_handler dictionary of the block
    if keyCode == LEFT:
        game.block.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.block.key_handler[RIGHT] = True
        
def mouseClicked():
    # if the grid has been filled (game over) and the mouse is clicked on the screen, the blocks list is cleared and the game is restarted by creating another instance of the game class
    if len(blocks) == NUM_ROWS * NUM_COLS:
        del blocks[0: (NUM_ROWS * NUM_COLS)]
        global game
        game = Game()
