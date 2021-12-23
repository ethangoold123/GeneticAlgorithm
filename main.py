import random
import numpy as np
import pygame

pygame.init()

#Pygame setup stuff

#Window size
windowWidth = 2000
windowHeight = 1000
testWindow = pygame.display.set_mode((windowWidth,windowHeight))

#Window title
pygame.display.set_caption("Genetic Algorithm Testing")
#Ant Icon
aliveAnt = pygame.image.load('beeAlive.png')
deadAnt = pygame.image.load('beeDead.png')
activeFood = pygame.image.load('foodActive.png')
inactiveFood = pygame.image.load('foodInactive.png')
aliveBird = pygame.image.load('birdAlive.png')
deadBird = pygame.image.load('birdDead.png')

pngPixelSize = 32

#pygame.display.set_icon(AliveAnt)

def distanceBetweenPoints(pos1, pos2):
    distance = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    return abs(distance)

class Population:
    def __init__(self, antList, foodDeposits, birdList, maxMovement = 1):
        self.antList = antList
        self.foodDeposits = foodDeposits
        self.birdList = birdList
        self.maxMovement = maxMovement

    def antsEat(self):
        for ant in self.antList:
            for food in self.foodDeposits:
                if (distanceBetweenPoints(ant.currentPos, food.currentPos) <= 20):
                    ant.eats()
                    food.eaten()

    def birdEatsAnt(self):
        for bird in birdList:
            if(bird.isHungry):
                for ant in antList:
                    if (distanceBetweenPoints(ant.currentPos, bird.currentPos) <= 20):
                        ant.dies()
                        bird.eats()

    def drawAnts(self):
        for ant in self.antList:
            if (ant.isAlive):
                testWindow.blit(aliveAnt, ant.currentPos)
            else:
                testWindow.blit(deadAnt, ant.currentPos)
            energyBarRed = pygame.Rect(ant.currentPos[0], ant.currentPos[1] - pngPixelSize/2, pngPixelSize, 10)
            energyBarGreen = pygame.Rect(ant.currentPos[0], ant.currentPos[1] - pngPixelSize/2,
                                         (pngPixelSize*(ant.energy)/ant.energyCapacity), 10)
            pygame.draw.rect(testWindow, (255,0,0), energyBarRed)
            pygame.draw.rect(testWindow, (0, 255, 0), energyBarGreen)

    def drawBirds(self):
        for bird in self.birdList:
            if (bird.isAlive):
                testWindow.blit(aliveBird, bird.currentPos)
            else:
                testWindow.blit(deadBird, bird.currentPos)
            energyBarRed = pygame.Rect(bird.currentPos[0], bird.currentPos[1] - pngPixelSize / 2, pngPixelSize, 10)
            energyBarGreen = pygame.Rect(bird.currentPos[0], bird.currentPos[1] - pngPixelSize / 2,
                                         (pngPixelSize * (bird.energy) / bird.energyCapacity), 10)
            pygame.draw.rect(testWindow, (255, 0, 0), energyBarRed)
            pygame.draw.rect(testWindow, (0, 255, 0), energyBarGreen)

    def drawFoods(self):
        for food in self.foodDeposits:
            if (food.isEatable):
                testWindow.blit(activeFood, food.currentPos)
            else:
                testWindow.blit(inactiveFood, food.currentPos)

    def regrowFood(self):
        for food in foodDeposits:
            if(not food.isEatable):
                food.regrowing()

    def makeAntMoves(self):
        for ant in self.antList:
            if (ant.isAlive):
                for food in foodDeposits:
                    if(distanceBetweenPoints(ant.currentPos, food.currentPos) <= ant.detectionRadius and food.isEatable):
                        #moves with a bias towards the food
                        xmove = ((food.currentPos[0] - ant.currentPos[0]))
                        ymove = ((food.currentPos[1] - ant.currentPos[1]))
                        if(xmove < -self.maxMovement):
                            xmove = -self.maxMovement
                        if (xmove > self.maxMovement):
                            xmove = self.maxMovement
                        if (ymove < -self.maxMovement):
                            ymove = -self.maxMovement
                        if (ymove > self.maxMovement):
                            ymove = self.maxMovement
                        ant.moveAnimal(xmove * ant.speed, -ymove * ant.speed)
                    else: #move randomly
                        xmove = random.randint(-self.maxMovement, self.maxMovement) * ant.speed
                        ymove = random.randint(-self.maxMovement, self.maxMovement) * ant.speed
                        ant.moveAnimal(xmove, ymove)
            ant.checkLife()

    def makeBirdMoves(self):
        for bird in self.birdList:
            if(bird.isAlive):
                if(bird.isHungry):
                    lowestMass = 10
                    posOfSmallestAnt = -1
                    for i, ant in enumerate(antList):
                        if (ant.isAlive):
                            if(distanceBetweenPoints(ant.currentPos, bird.currentPos) <= bird.detectionRadius):
                                if (ant.mass <= lowestMass):
                                    posOfSmallestAnt = i
                                    lowestMass = ant.mass
                            else:  # move randomly
                                xmove = random.randint(-self.maxMovement, self.maxMovement) * bird.speed
                                ymove = random.randint(-self.maxMovement, self.maxMovement) * bird.speed
                                bird.moveAnimal(xmove, ymove)

                    #moves with a bias towards the food
                    xmove = (antList[posOfSmallestAnt].currentPos[0] - bird.currentPos[0])
                    ymove = (antList[posOfSmallestAnt].currentPos[1] - bird.currentPos[1])
                    if (xmove < -self.maxMovement):
                        xmove = -self.maxMovement
                    if (xmove > self.maxMovement):
                        xmove = self.maxMovement
                    if (ymove < -self.maxMovement):
                        ymove = -self.maxMovement
                    if (ymove > self.maxMovement):
                        ymove = self.maxMovement
                    bird.moveAnimal(xmove * bird.speed, -ymove  * bird.speed)

                else: #move randomly less scouting if not hungry
                    xmove = random.randint(-self.maxMovement, self.maxMovement) * bird.speed/2
                    ymove = random.randint(-self.maxMovement, self.maxMovement) * bird.speed/2
                    bird.moveAnimal(xmove, ymove)
                bird.checkHunger()
                bird.checkLife()


class Animal:
    def __init__(self,isAlive = True, speed = 1, mass = 1, detectionRadius = 300, currentPos = [0,0], energy = 10000):
        self.isAlive = isAlive
        self.speed = speed
        self.mass = mass
        self.detectionRadius = detectionRadius
        self.currentPos = currentPos
        self.energyCapacity = energy
        self.energy = energy

    def moveAnimal(self,xMove,yMove):
        self.currentPos[0] += xMove
        #minus equals because I want a positive y move to represent going upwards not downwards
        self.currentPos[1] -= yMove
        #Preventing ants from moving out of the screen
        if(self.currentPos[0]< 0):
            self.currentPos[0] = 0
        if (self.currentPos[0] > windowWidth - pngPixelSize):
            self.currentPos[0] = windowWidth - pngPixelSize
        if (self.currentPos[1] < 0):
            self.currentPos[1] = 0
        if (self.currentPos[1] > windowHeight - pngPixelSize):
            self.currentPos[1] = windowHeight - pngPixelSize
        #moving costs energy somewhat proportional to your mass and speed, heavier and faster = more energy used to move
        self.energy -= np.sqrt(xMove**2 + yMove**2)*(self.speed*0.2 + self.mass*0.1 + self.detectionRadius*0.0005)

    def checkLife(self):
        if self.energy <= 0:
            self.dies()

    def dies(self):
        self.isAlive = False

    def eats(self):
        self.energy = self.energyCapacity

class Ant(Animal):
    def __init__(self,isAlive = True, speed = 1, mass = 1, detectionRadius = 300, currentPos = [0,0], energy = 10000):
        super().__init__(isAlive, speed, mass, detectionRadius, currentPos, energy)


class Bird(Animal):
    def __init__(self,isAlive = True, speed = 5, mass = 500, detectionRadius = 1000, currentPos = [0,0], energy = 1000000, isHungry = True):
        super().__init__(isAlive, speed, mass, detectionRadius, currentPos, energy)
        self.isHungry = isHungry

    def eats(self):
        self.energy = self.energyCapacity
        self.isHungry = False

    def checkHunger(self):
        if (self.energy <= self.energyCapacity*3/4):
            self.isHungry = True



class FoodDeposit:
    def __init__(self, currentPos = [0,0], timeToRegrow = 1000, isEatable = True):
        self.currentPos = currentPos
        self.timeToRegrow = timeToRegrow
        self.isEatable = isEatable

    def eaten(self):
        self.isEatable = False

    def regrowing(self):
        self.timeToRegrow -= 1
        if (self.timeToRegrow <= 0):
            self.isEatable = True
            self.timeToRegrow = 1000



def generateFoodDeposits(numDeposits):
    foodDeposits = []
    for i in range(numDeposits):
        xpos = random.randint(pngPixelSize, windowWidth - pngPixelSize)
        ypos = random.randint(pngPixelSize, windowHeight - pngPixelSize)
        newFood = FoodDeposit(currentPos=[xpos, ypos])
        foodDeposits.append(newFood)
    return foodDeposits

def generateAnts(numAnts):
    antList = []
    for i in range(numAnts):
        speed = random.uniform(0,1)
        mass = random.uniform(0,1.5)
        detectionRadius = random.randint(100,500)
        newAnt = Ant(speed = speed, mass = mass, detectionRadius = detectionRadius, currentPos=[1000, 900])
        antList.append(newAnt)
    return antList

def generateBirds(numBirds):
    birdList = []
    for i in range(numBirds):
        #speed = random.uniform(0,1)
        #mass = random.uniform(0,1.5)
        #detectionRadius = random.randint(100,500)
        newBird = Bird()
        birdList.append(newBird)
    return birdList

testRunning = True

numAnts = 10
numDeposits = 50
numBirds = 1



foodDeposits = generateFoodDeposits(numDeposits)
antList = generateAnts(numAnts)
birdList = generateBirds(numBirds)

population = Population(antList, foodDeposits, birdList)

delayInMs = 50
startTime = pygame.time.get_ticks()

while testRunning:
    currentTime = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            testRunning = False

    testWindow.fill((255,255,255))

    if(currentTime - startTime >= delayInMs):
        population.drawAnts()
        population.drawFoods()
        population.drawBirds()
        population.birdEatsAnt()
        population.antsEat()
        population.regrowFood()
        population.makeAntMoves()
        population.makeBirdMoves()
        pygame.display.update()
        startTime = currentTime

