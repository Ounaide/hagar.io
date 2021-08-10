w=600
h=600

from random import choice
from time import sleep

def setup():
    size(w,h)
    background(255)

scl=1
baseR = 50
score=0
blobnumber = 150

class blob:
    def __init__(self,x,y,r,me):
        self.x=x
        self.y=y
        self.r=r
        self.me=me
        self.position = PVector(self.x,self.y)
        self.index=""
        self.vel = PVector(0,0)
        if not self.me:
            self.colors = (random(255),random(255),random(255))
                  
    def show(self,c):
        try:
            fill(*c)
        except:
            fill(c)
        ellipse(self.position.x,self.position.y,2*self.r,2*self.r)
        
    def update(self):
        if self.me:
            newvel = PVector(mouseX-w/2,mouseY-h/2)
            newvel.setMag(2)
            self.vel.lerp(newvel,1)
            self.position.add(self.vel)
        else:
            if random(0,100)>80:
                d=[-30,0,30]
                rand = PVector(choice(d),choice(d))
                newvel = self.vel.add(rand)
                #newvel.setMag(random(0,8))
                self.vel.lerp(newvel,0.01)
                self.vel.setMag(random(0,8))
                self.position.add(self.vel)
                
    def touch(self,other):
        global blobs
        if sqrt((self.position.x-other.position.x)**2 + (self.position.y-other.position.y)**2) <= self.r + other.r:
            return True
    def eat(self,other):
        if self.r > other.r:
            self.r = lerp(self.r,sqrt(self.r**2 + other.r**2),0.05)
            return True
        else:
            return False

        
me = blob(w/2,h/2,baseR,True)
blobs=[]

for _ in range(blobnumber):
    b = blob(random(-2*w,2*w),random(-2*h,2*h),random(10,75),False)
    blobs.append(b)
    b.index = str(_+1)
    
def draw():
    global score
    global scl
    global blobs
    
    translate(w/2,h/2)
    background(255)
    scale(scl)
    translate(-me.position.x,-me.position.y)

    
    for Blob in blobs:
        Blob.show(Blob.colors)
        Blob.update()
        """if Blob.r!=0: #show blob indexes for debugging purposes
            textSize(Blob.r)
            stroke(0)
            fill(255,0,0)
            textAlign(CENTER)
            text(str(Blob.index),Blob.position.x,Blob.position.y+0.5*Blob.r)"""

    me.show((255,0,0))
    
    textAlign(CENTER)
    fill(0)
    textSize(25)
    text(str(score),me.position.x,me.position.y+0.25*me.r)
    
    me.update()
    
    for Blob in blobs:
        if me.touch(Blob): #coliision with my own blob, adds a 3 sec immunity so that you don't die immediatly after spawning
            if Blob.r > me.r  and frameCount>=180: # me smaller = me dead
                print("game over")
                sleep(2)
                exit()
            elif Blob.r < me.r: #me bigger = me even bigger
                me.r = lerp(me.r,sqrt(me.r**2 + Blob.r**2),0.05)
                newscale= baseR/(lerp(me.r,sqrt(me.r**2 + Blob.r**2),0.05))
                scl = lerp(scl,newscale,0.1)
                blobs.remove(Blob)
                score+=1
                
                
    if me.r==0:
        blobs=[]
        
    if len(blobs)!=blobnumber: #if a blob is eaten, create a new one
        b=blob(random(-2*w,2*w),random(-2*h,2*h),random(10,75),False)
        blobs.append(b)

    for b1 in blobs: #check for collisions in between all the other blobs (makes the game run incredibly slower! if you remove this part, make sure to reduce me.vel's lerp speed)
        for b2 in blobs:
            if b1.touch(b2):
                if b1.eat(b2):
                    blobs.remove(b2)
                    

    


                
