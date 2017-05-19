#!/usr/bin/python3
import pygame
import time
import random
pygame.init()
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,191,255)
display_width = 800
display_height = 600



FPS = 5#Frame per second
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Slither")

icon = pygame.image.load('snake_logo.jpg')
pygame.display.set_icon(icon)
img = pygame.image.load('snake.jpg')#填入待放置的圖片
pen_img = pygame.image.load('pen.jpg')
apple_img = pygame.image.load('apple.jpg')
pineApple_img = pygame.image.load('pineapple.jpg')

things_img = [pen_img,pineApple_img,apple_img]
block_size = 20
pygame.display.update()
#只要做完pygame模組中函式的使用，必須加上上面的語句更新

clock = pygame.time.Clock()

thingsThickness = 30

direction = "right"
#蛇初始化向右移動

smallfont = pygame.font.SysFont('SimHei',25)
medfont = pygame.font.SysFont('SimHei',50)
largefont = pygame.font.SysFont('SimHei',80)

def randThingGen():
    randThingX = random.randrange(0, display_width -  block_size, block_size)#因為蘋果寬10，然後x數值從左往又遞增，因此當display_width==800的時候，蘋果最右側會在810處
    randThingY = random.randrange(0, display_height - block_size, block_size)#目的要讓Apple髓機出現在場景中，竊為了被蛇能剛好通過(覆蓋)，所以蘋果的X和Y座標都必須是蛇的整數倍，就能完全對齊
    
    return randThingX,randThingY
    
def pause():

    paused = True
    message_to_screen("Paused",
                          black,
                          -100,
                          size="large")

    message_to_screen("Press C to continue or Q to quit.",
                        black,
                        25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        #gameDisplay.fill(white)
        
clock.tick(5)
def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])



def game_intro():
    
    intro =True
    
    while intro:
        
        for event in pygame.event.get():
            #如果有人進去遊戲後，直接按右上角關閉鍵，則可讓他順利關閉，否則會當掉。
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_n:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome to NHCC Slither",
                        blue,
                         -100,
                         "medium")
        message_to_screen("Make the snake eat Pineapple ,Pen ,Apple",
                         blue,
                         -50,
                         "medium")
        message_to_screen("Go",
                         blue,
                         0,
                         "medium")
        pygame.display.update()
        clock.tick(15)
def snake(block_size, snakelist):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
        
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    
    if direction == "up":
        head = img
    
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))#此時head是旋轉過的img
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay,green,[XnY[0],XnY[1],block_size,block_size])


def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
        
    return textSurface, textSurface.get_rect()
    
def message_to_screen(msg,color,y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    global direction
    global snakeLength
    direction = 'right'
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 0
    lead_y_change = 0

    randThingX,randThingY = randThingGen()

    snakeList = []
    snakeLength = 1
    
    things = random.choice(things_img)
    
   
    while not gameExit:
        
        if gameOver == True:
            #gameDisplay.fill(white)
            message_to_screen("Game Over",
                              red,
                              y_displace=-50,
                              size = "large")#若K_q按q則無法離開
            message_to_screen("press c to play again or press q to quit a game",
                              green)
            pygame.display.update()
        while gameOver == True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    gameExit = True
                    gameOver = False
                    
                    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                    #現在往向左方向移動，但目前垂直方向還有數值，因此要設為0，若未設為0，則會水平垂直同時移動，變成斜向
                    #lead_x -= 10
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                    #lead_x += 10
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                    #lead_x -= 10
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                    #lead_x += 10
                elif event.key == pygame.K_p:
                    pause()
        
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y <0:
                gameOver = True
            #如果只有>，則方塊可以部份跑出邊界，要等到整塊出去遊戲才結束；但加了>=，只要方塊碰觸邊界，就遊戲結束

                '''
                if event.type == pygame.KEY_UP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        lead_x_change = 0
                '''

        lead_x += lead_x_change#預設情況是電腦狀況每秒鐘會產生幾千到幾萬個frame，(每產生一個frame就會減一次)所以要用到clock.tick(FPS)控制
        lead_y += lead_y_change

        gameDisplay.fill(white)
        
        gameDisplay.blit(things, (randThingX, randThingY)) 

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        
       
        #此行實測不可能發生
        if len(snakeList) > snakeLength:
            del snakeList[0]#因為每次移動都會新增一筆座標，如果滿的話要刪除最老的(x,y)，也就是索引值為0的座標直
            
        
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
                
        snake(block_size,snakeList)
        score(snakeLength-1)
        pygame.display.update()
        
       
        if lead_x > randThingX and lead_x < randThingX + thingsThickness or lead_x + block_size > randThingX and  lead_x + block_size < randThingX + thingsThickness:
            if lead_y > randThingY and lead_y <randThingY + thingsThickness:
                randThingX,randThingY = randThingGen()
                things = random.choice(things_img)
                gameDisplay.blit(things, (randThingX, randThingY))
                snakeLength += 1
            elif lead_y + block_size > randThingY and lead_y + block_size < randThingY + thingsThickness:
                randThingX,randThingY = randThingGen()
                snakeLength += 1
                things = random.choice(things_img)
                gameDisplay.blit(things, (randThingX, randThingY))
        clock.tick(FPS)
    #當gameExit = True時，回接著執行到此
    message_to_screen("bye bye",red)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()
    
game_intro()
gameLoop()
