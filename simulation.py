import random
import time
import threading
import pygame
import sys
import config as c
from Vehicle import Vehicle
# Default values of signal timers

signals = []
noOfSignals = 4
currentGreen = 0   # Indicates which signal is green currently
nextGreen = (currentGreen+1)%noOfSignals    # Indicates which signal will turn green next
currentYellow = 0   # Indicates whether yellow signal is on or off

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""

# Initialization of signals with default values
def initialize():
    ts1 = TrafficSignal(0, c.defaultYellow, c.defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, c.defaultYellow, c.defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(c.defaultRed, c.defaultYellow, c.defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(c.defaultRed, c.defaultYellow, c.defaultGreen[3])
    signals.append(ts4)
    repeat()

def repeat():
    global currentGreen, currentYellow, nextGreen
    while(signals[currentGreen].green>0):   # while the timer of current green signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 1   # set yellow signal on
    # reset stop coordinates of lanes and vehicles 
    for i in range(0,3):
        for vehicle in c.vehicles[c.directionNumbers[currentGreen]][i]:
            vehicle.stop = c.defaultStop[c.directionNumbers[currentGreen]]
    while(signals[currentGreen].yellow>0):  # while the timer of current yellow signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 0   # set yellow signal off
    
     # reset all signal times of current signal to default times
    signals[currentGreen].green = c.defaultGreen[currentGreen]
    signals[currentGreen].yellow = c.defaultYellow
    signals[currentGreen].red = c.defaultRed
       
    currentGreen = nextGreen # set next signal as green signal
    nextGreen = (currentGreen+1)%noOfSignals    # set next green signal
    signals[nextGreen].red = signals[currentGreen].yellow+signals[currentGreen].green    # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat()  

# Update values of the signal timers after every second
def updateValues():
    for i in range(0, noOfSignals):
        if(i==currentGreen):
            if(currentYellow==0):
                signals[i].green-=1
            else:
                signals[i].yellow-=1
        else:
            signals[i].red-=1

# Generating vehicles in the simulation
def get_direction():
    temp = random.randint(0, 99)
    direction_number = 0
    dist = [25, 50, 75, 100]
    if (temp < dist[0]):
        direction_number = 0
    elif (temp < dist[1]):
        direction_number = 1
    elif (temp < dist[2]):
        direction_number = 2
    elif (temp < dist[3]):
        direction_number = 3
    return direction_number
    #return 0

def generateVehicles():
    while(True):
        vehicle_id = random.randint(0,3)
        lane_number = 0 if vehicle_id == 2 else random.randint(1,2)
        direction_number = get_direction()
        vehicle = Vehicle(lane_number, vehicle_id, direction_number)
        simulation.add(vehicle.get_object())
        time.sleep(1)

class Main:
    thread1 = threading.Thread(name="initialization",target=initialize, args=())    # initialization
    thread1.daemon = True
    thread1.start()

    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize 
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/intersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())    # Generating vehicles
    thread2.daemon = True
    thread2.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))   # display background in simulation
        for i in range(0,noOfSignals):  # display signal and set timer according to current status: green, yello, or red
            if(i==currentGreen):
                if(currentYellow==1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, c.signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, c.signalCoods[i])
            else:
                if(signals[i].red<=10):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, c.signalCoods[i])
        signalTexts = ["","","",""]

        # display signal timer
        for i in range(0,noOfSignals):  
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],c.signalTimerCoods[i])

        # display the vehicles
        for vehicle in simulation:  
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move(currentGreen, currentYellow)
            if vehicle.isEmergency():
                vehicle.update()
        pygame.display.update()
Main()