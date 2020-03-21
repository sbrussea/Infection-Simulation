from cmu_112_graphics import *
from tkinter import *
import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np


#All credit for graphics pack to Carnegie Mellon University: 
#http://www.kosbie.net/cmu/fall-19/15-112/notes/notes-animations-part2.html


def distance(x1,y1,x2,y2):
    return int(((((x2 - x1)**2) + ((y2-y1)**2))**.5))


class person(object):
    def __init__(self,status,x,y):
        self.status = status
        self.x = x
        self.y = y
        self.angle = random.randrange(0,6)
        self.speed = 4
        self.time = 0
        self.age = random.randint(0,100)
        self.realAge = 0
        self.chance = random.randint(0,100)
        self.string = f'{self.age} {self.chance} {self.angle}'
        self.daysInfected = 0
        self.moving = True
        

    def __hash__(self): 
        return hash(self.string)
    
    def __eq__(self,other):
        return (isinstance(other,person) and (self.string == other.string))


class infectMode(Mode):
    def appStarted(mode):
        mode.slowMode = False
        mode.infectionAgeGroup = dict()
        mode.amount = 300
        mode.infected = 0
        mode.cured = 0
        mode.healthy = 0
        mode.died = 0
        mode.allDead = []
        mode.people = []
        mode.width = 900
        mode.height = 600
        mode.insertPeople()
        mode.timeCount = 0
        mode.day = 0
        mode.graphX = []
        mode.graphY = []
        mode.graphX2 = []
        mode.graphY2 = []
        mode.wall = False
        
        
    
    def insertPeople(mode):
        for i in range(mode.amount):
            x = random.randint(20,mode.width-20)
            y = random.randint(20,mode.height-20)
            mode.people.append(person("healthy", x, y))
        mode.countStatus()
        if mode.app.proposal == True:
            for p in mode.people:
                if 11 <= p.age < 29:
                    p.x = random.randint(0, mode.width/3 - 20)
                else:
                    p.x = random.randint(mode.width/3 + 20, mode.width - 20)
            
        for p in mode.people:
            if 0 <= p.age and p.age < 11.5:
                p.realAge = "50's"
            if 11.5 <= p.age and p.age < 19.5:
                p.realAge = "60's"
            if 20 <= p.age and p.age < 24.5:
                p.realAge = "70's"
            if 24.5 <= p.age and p.age < 29:
                p.realAge = "80's"
            mode.infectionAgeGroup[p.realAge] = 0
        
            

    def checkCollision(mode):
        hits = set()
        for p1 in mode.people:
            for p2 in mode.people:
                if distance(p1.x, p1.y, p2.x, p2.y) < 10:
                    if ((p1 != p2 )and (p1 not in hits)):
                        mode.collision(p1,p2)
                        mode.changeStatus(p1,p2)
                        hits.add(p1)
                        hits.add(p2)
            if (p1.x > mode.width - 8) or (p1.x < 8):
                #p1.speed = -1 * p1.speed
                p1.angle += math.pi
            if mode.wall == True:
                if (mode.width/4 - 10 < p1.x and p1.x < mode.width/4 + 10):
                    p1.speed = -1 * p1.speed
                if (2*mode.width/3 - 10 < p1.x and p1.x < 2*mode.width/3 + 10):
                    p1.speed = -1 * p1.speed
                if (mode.height/2 - 10 < p1.y and p1.y < mode.height/2 + 10):
                    p1.speed = -1 * p1.speed
            if mode.app.proposal == True:
                #if (mode.width/3 - 5 < p1.x and p1.x < mode.width/3 + 5):
                #    p1.speed = -1 * p1.speed
                if (mode.width/3 - 15 < p1.x and p1.x < mode.width/3 + 5):
                    p1.speed = -1 * p1.speed


            if (p1.y > mode.height - 10) or (p1.y < 10):
                #p1.speed = -1 * p1.speed
                p1.angle += math.pi
    
    def changeStatus(mode,a, b):
        if a.status == "sick" and b.status != "recovered":
            b.status = "sick"
            mode.infectionAgeGroup[b.realAge] += 1
        if b.status == "sick" and a.status != "recovered":
            a.status = "sick"
            mode.infectionAgeGroup[a.realAge] += 1
        
        

    #From http://archive.petercollingridge.co.uk/sites/files/peter/particle_tutorial_8.txt
    def collision(mode,a, b):
        dx = a.x - b.x
        dy = a.y - b.y
        tangent = math.atan2(dy, dx)
        angleA = 2*tangent - a.angle
        angleB = 2*tangent - b.angle
        a.angle = angleA
        b.angle = angleB
        angle = 0.5 * math.pi + tangent
        a.x += math.sin(angle)
        a.y -= math.cos(angle)
        b.x -= math.sin(angle)
        b.y += math.cos(angle)
    
    def moveAll(mode):
        for person in mode.people:
            if person.moving == True:
                if person.status == "sick":
                    person.time += 1
                    person.daysInfected += 1
                    if person.realAge != 0 and mode.slowMode == True:
                        person.speed = .5
                if person.time >= random.randint(140,200):
                    person.status = "recovered"
                    person.speed = 4
                person.x += math.sin(person.angle) * person.speed
                person.y -= math.cos(person.angle) * person.speed

    def countStatus(mode):
        healthy = 0
        sick = 0
        cured = 0
        
        for person in mode.people:
            if person.status == "healthy":
                healthy += 1
            if person.status == "sick":
                sick += 1
                
            if person.status == "recovered":
                cured += 1
        mode.infected = sick
        mode.cured = cured
        mode.healthy = healthy

    def timerFired(mode):
        mode.timeCount += 1
        mode.checkCollision()
        mode.moveAll()
        mode.countStatus()
        if mode.timeCount % 10 == 0:
            mode.checkDeaths()
            mode.day += 1
            mode.graphX.append(mode.day)
            mode.graphY.append(mode.infected)
            
            mode.graphX2.append(mode.day)
            mode.graphY2.append(mode.cured)

    def checkDeaths(mode):
        for p in mode.people:
            if p.status == "sick":
                if 0 <= p.age and p.age < 11.5:
                    #https://www.census.gov/prod/cen2010/briefs/c2010br-03.pdf
                    #corresponding to census numbers on percentage of population
                    #50-60
                    if p.chance == 50:
                        if p.daysInfected > 8:
                            p.status = "dead"
                if 11.5 <= p.age and p.age < 19.5:
                    #60-70
                    if p.chance <= 3:
                        if p.daysInfected > 8:
                            p.status = "dead"
                if 20 <= p.age and p.age < 24.5:
                    if p.chance <= 6:
                        if p.daysInfected > 8:
                            p.status = "dead"
                if 24.5 <= p.age and p.age < 29:
                    if p.chance < 11:
                        if p.daysInfected > 8:
                            p.status = "dead"
            if p.status == "dead":
                mode.died += 1
                mode.allDead.append(p.realAge)
                mode.people.remove(p)
                print(f'Died : {mode.allDead}')
                
            

    def keyPressed(mode,event):
        if event.key == "g":
            plt.title('Infected and Recovered vs. Time')
            plt.xlabel('Day')
            plt.ylabel('Infected')
            plt.plot(mode.graphX, mode.graphY, label = 'Infected')
            plt.plot(mode.graphX2,mode.graphY2, label = 'Cured')
            plt.legend()
            print(f'Infected: {mode.infectionAgeGroup}')
            plt.show()
        if event.key == "w":
            mode.wall = not mode.wall
        if event.key == "p":
            mode.app.proposal = not mode.app.proposal
            mode.appStarted()
        if event.key == "s":
            mode.slowMode = not mode.slowMode
        if event.key == "h":
            mode.app.setActiveMode(mode.app.helpMode)
            
        
    def mousePressed(mode,event):
        newPerson = person("sick", event.x, event.y)
        mode.people.append(newPerson)
        mode.sickStart = True

    def redrawAll(mode,canvas):
        r = 5
        string = f'Healthy {mode.healthy}, Sick {mode.infected}, Recovered {mode.cured}, Died {mode.died}'
        for p in mode.people:
            if p.status == "healthy":
                color = "green"
            if p.status == "recovered":
                color = "pink"
            if p.status == "sick":
                color = "red"
            canvas.create_oval(p.x - r, p.y - r, p.x + r, p.y + r, fill = color)
            if p.realAge != 0:
                canvas.create_text(p.x, p.y, text = p.realAge)
        canvas.create_text(mode.width/2, 40, text = string)
        canvas.create_text(10, mode.height-20,text = "Press \'h\' for help", anchor = "nw")
        canvas.create_text(10, 20, text = f' Day : {mode.day}', anchor = "nw")
        if mode.slowMode:
            canvas.create_text(mode.width - 40, 40, text = "SlowMode")
        if mode.wall == True:
            canvas.create_line(mode.width/4, 0, mode.width/4, mode.height)
            canvas.create_line(2*mode.width/3, 0, 2*mode.width/3, mode.height)
            canvas.create_line(0, mode.height/2, mode.width, mode.height/2)
        if mode.app.proposal == True:
            canvas.create_line(mode.width/3-10, 0, mode.width/3 - 10, mode.height)
            canvas.create_line(mode.width/3-5, 0, mode.width/3 - 5, mode.height)
        

class helpMode(Mode):
    def appStarted(mode):
        mode.width = 900
        mode.height = 600
        mode.app.proposal = False

    def keyPressed(mode,event):
        mode.app.setActiveMode(mode.app.infectMode)

    def redrawAll(mode,canvas):
        string = f'This is the infection simulator \n \'p\' will be proposal mode, where we wall off all 60+ year olds to the rest of the public and let everyone else get infected'
        string2 = f'\'w\' will bring up several walls,\n people may be able to slip out of these walls through an unintentional bug that helps prove the point of this program'
        string3 = f'\'g\' will be the graph where you can see in days, how long it takes for a disease to spread and finish its cycle'
        string6 = f'\'s\' will be slow Mode, where sick people over 50 will slow to almost a halt'
        string4 = f'Clicking anywhere will introduce an infected person to the population'  
        string5 = f' Press any button to get back to the main infection mode'
        canvas.create_text(30, mode.height /10, text = f' {string} \n\n {string2} \n\n {string3} \n\n {string6} \n\n {string4} \n\n {string5}',anchor = "nw")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.infectMode = infectMode()
        app.helpMode = helpMode()
        app.setActiveMode(app.helpMode)
        app.timerDelay = 100

#Every second is 1 day


MyModalApp(width=900, height=600)