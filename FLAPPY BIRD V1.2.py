import pygame as pg
import random
import math
import time


def drawpipe(pipesizes,pipex):
    
    display.blit(pipe_bottom,[pipex,pipesizes[0]])
    display.blit(pipe_top,[pipex,pipesizes[1]])

def drawbird(birdx,inpain):      
    if not godmode:
        display.blit(bird,[birdx,birdy])
    else:
        if not inpain:
            display.blit(birdjesus,[birdx,birdy])
        else:
            display.blit(birdsuffering,[birdx,birdy])
            inpain = False
    return inpain


def drawcoin(coinx,coiny):
    
    display.blit(coin,[coinx,coiny])


    
pg.init()
debuggreen = (255,255,255)
displayH = 960
displayW = 640
clockspeed = 70
birdx = 250
birdy = 50
gapsize = 120
coinpercentage = 50
backgroundscrollspeed = 0.5
jumpstrength = 10
pipespeed = 5
font = "Prestige Elite Std"

hs = open("data/highscore.txt")
highscore = hs.readline()
totalcoins = hs.readline()

debug = False
godmode = False

if godmode:
    bird_color = (255,0,255)
else:
    bird_color = (255,255,0)
gravity = 0.8
pipe_cleared = True
inpain = False
got_coin = False
isthereacoin = True
pipex = displayH
coinx = 2*displayW+birdx
coiny = 100
birdvel = 0
font = pg.font.SysFont(font,45)
clock = pg.time.Clock()
display = (displayH,displayW)
display = pg.display.set_mode(display)
pg.display.set_caption("Flappi berd")
backgroundx = 0
background  = pg.image.load("images/background.png")
bird = pg.image.load("images/bird.png")
birdjesus = pg.image.load("images/birdjesus.png")
birdsuffering = pg.image.load("images/birdsuffering.png")
pipe_bottom = pg.image.load("images/pipe_bottom.png")
pipe_top = pg.image.load("images/pipe_top.png")
coin = pg.image.load("images/coin.png")
display.blit(background,[0,0])







started = False
while not started:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                started = True

    
    display.blit(background,(0,0))
    startrender = font.render("PRESS SPACE TO START!",True,(0,0,0))
    display.blit(startrender,(displayH/2-170,displayW/2))
    pg.display.update()
    clock.tick(clockspeed)

coins = 0
score = 0


dead = False

while not dead:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            dead = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE or event.key == pg.K_UP or event.key == pg.K_w:
                birdvel = -jumpstrength

            if event.key == pg.K_g:
                if godmode:
                    godmode = False
                    print("you are now no longer Jesus")
                    bird_color = (255,255,0)
                else:
                    godmode = True
                    print("you are now jesus")
                    bird_color = (255,0,255)

            if event.key == pg.K_ESCAPE:
                dead = True


    birdvel += gravity
    birdy += birdvel


#bottom death detection
    if not godmode:
        if birdy > displayW:
            print("haha loser")
            dead = True
    else:
        if birdy > displayH:
            birdy = 0
            print("Woosh!")
            birdvel = 0
            inpain = True


    if pipex < -90:
        pipe_cleared = True
        pipex = displayH+90
        print("pipe cleared!")
        score +=1

    if pipe_cleared:
        
        bottomheight = random.randint(gapsize,displayW-30)
        topheight = bottomheight-2*displayW+gapsize
        pipesizes = (bottomheight,topheight)
        pipe_cleared = False
        print(pipesizes)


    if coinx < -48:
        print("coin passed")
        coinx = pipex + displayH/2 + birdx/2
        isthereacoin = False
        chance = random.randint(0,100)
        if chance <= coinpercentage:
            isthereacoin = True
            coiny = random.randint(gapsize - 50 ,displayW - 50)
        
    
            
#roof collision handling
    if birdy < 0:
        birdvel = 0
        birdy = 0

#bottom pipe collision handling
        
    if birdy+20 >= pipesizes[0]:
        for pipexdif in range(0,90):
            for birdxdif in range(0,75):    
                if birdx + birdxdif == pipex + pipexdif:
                    if not godmode:
                        dead = True
                    else:
                        inpain = True
                     
        


#top pipe collision handling
    if birdy-8 <= pipesizes[1]+displayH-10:
    
        for pipexdif in range(0,90):
            for birdxdif in range(0,75):
                if birdx + birdxdif == pipex + pipexdif:
                    if not godmode:
                        dead= True
                    else:
                        inpain = True

#coin collision handling

    if coinx >= birdx and coinx <= birdx + 75 and isthereacoin:
        if coiny >= birdy and coiny <= birdy + 60:
            isthereacoin = False
            coins += 1

    
    elif coinx+48 >= birdx and coinx+48 <= birdx + 75 and isthereacoin:
        if coiny >= birdy and coiny <= birdy + 60:
            isthereacoin = False
            coins += 1

    elif coinx >= birdx and coinx <= birdx + 75 and isthereacoin:
        if coiny+48 >= birdy and coiny+48 <= birdy + 60:
            isthereacoin = False
            coins += 1
            
    elif coinx+48 >= birdx and coinx+48 <= birdx + 75 and isthereacoin:
        if coiny+48 >= birdy and coiny+48 <= birdy + 60:
            isthereacoin = False
            coins += 1



    display.blit(background,[backgroundx,0])
    drawpipe(pipesizes,pipex)
    inpain = drawbird(birdx,inpain)
    if isthereacoin:
        drawcoin(coinx,coiny)
    scorender = font.render("SCORE: "+str(score)+"/"+str(highscore),True,debuggreen)
    coinsrender = font.render("COINS: "+str(coins),True,debuggreen)
    display.blit(coinsrender,(15,displayW-60))
    display.blit(scorender,(15,displayW-30))

    if debug:
        pg.draw.rect(display,debuggreen,[birdx,birdy,10,10])
        pg.draw.rect(display,debuggreen,[pipex,pipesizes[0],90,10])
        pg.draw.rect(display,debuggreen,[pipex,pipesizes[1],90,10])
        pg.draw.rect(display,debuggreen,[coinx,coiny,10,10])
        
    pipex -=pipespeed
    coinx -=pipespeed
    
        

#background looping
    if backgroundx >= -displayH:
        backgroundx -= backgroundscrollspeed
        
    else:
        backgroundx = 0
        print("background looped")


    pg.display.update()
    clock.tick(clockspeed)





    



if score > int(highscore):
    highscore = score
totalcoins = int(totalcoins) +  coins


hs.close()
hs = open("data/highscore.txt","w")
hs.write(str(highscore))
hs.write(str(totalcoins))




hs.close()
pg.quit()
quit()

