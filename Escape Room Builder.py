# This file contains the main code and modes for the project.
# Imports
# cmu_112_graphics is originally downloaded and modified from 
# www.cs.cmu.edu/~112/notes/notes-animations-part2.html
from cmu_112_graphics import *
from tkinter import *
import tkinter as tk
# I cite where I learnt how to use filedialog and pygame above the 
# functions I used these modules.
from tkinter import filedialog
import pygame
# Learnt how to use Pickle Module on the website: 
# https://pythonprogramming.net/python-pickle-module-save-objects-serialization/#:~:targetText=First%2C%20import%20pickle%20to%20use,into%20opened%20file%2C%20then%20close.&targetText=Use%20pickle.,-load()%20to
import pickle
import os
from Classes import Door, Containers, Keys, Hints, Rooms, KeyPads

# Copied, Modified and learnt how to use from
# https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
# not in MVP
def askFileName():
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(filetypes = (("Data Files", ".dat"), ("All Files", "*.*")))
    return filename

# learnt how to use os.path.expanduser from 
# https://stackoverflow.com/questions/3324486/finding-a-files-directory-address-on-a-mac
# not in mvp
def findFile(path = os.path.expanduser("~/Desktop/CS HW/Term Project"), suffix = ".dat"):
    for filename in os.listdir(path):
        if suffix in filename:
            return filename
    return False

# learnt how to use os.path.expanduser from 
# https://stackoverflow.com/questions/3324486/finding-a-files-directory-address-on-a-mac
# not in mvp
def removeDat(path = os.path.expanduser("~/Desktop/CS HW/Term Project")):
    if findFile() == ".dat":
        os.remove(path + "/" + ".dat")

# Modes
class SplashScreenMode(Mode):
    def appStarted(mode):
        # This image is downloaded from Google Image and is originally from 
        # bathescape.co.uk.
        mode.image = mode.loadImage("live-escape-rooms-bg.jpg")
        mode.Color = "gray"
        mode.titleSize = 0
        mode.appear = False
        mode.timerDelay = 1

    def timerFired(mode):
        if mode.titleSize < 150:
            mode.titleSize += 10
        else:
            mode.appear = True
    
    def keyPressed(mode, event):
        if event.key == "h":
            mode.app.setActiveMode(mode.app.HelpMode)

    def mouseReleased(mode, event):
        if mode.titleSize == 150:
            if (mode.width / 4 <= event.x <= 3 * mode.width / 4):
                if mode.height / 2 <= event.y <= 19 * mode.height / 32:
                    mode.app.IsNew = True
                    mode.app.setActiveMode(mode.app.DesignerMode)
                elif 5 * mode.height / 8 <= event.y <= 23 * mode.height / 32:
                    mode.app.IsNew = False
                    mode.app.setActiveMode(mode.app.DesignRoomMode)
                elif 3 * mode.height / 4 <= event.y <= 27 * mode.height / 32:
                    mode.app.setActiveMode(mode.app.PlayerMode)
                elif 7 * mode.height / 8 <= event.y <= 31 * mode.height / 32:
                    # Learnt how to use pygame.mixer.music on 
                    # https://www.pygame.org/docs/ref/music.html
                    pygame.mixer.music.fadeout(1000)
                    mode.app.quit()

    def redrawAll(mode, canvas):
        ratio = 1440 / 1280
        mode.ScaledImage = mode.scaleImage(mode.image, ratio)
        canvas.create_image(mode.width / 2, mode.height / 2, 
                            image = ImageTk.PhotoImage(mode.ScaledImage))
        canvas.create_text(mode.width / 2, mode.height / 4,
                            text = "Escape Room Builder", fill = "white",
                            font = ("Frank Knows", mode.titleSize))
        if mode.appear == True:
            # New design
            canvas.create_rectangle(mode.width / 4, mode.height / 2, 
                                    3 * mode.width / 4, 19 * mode.height / 32, 
                                    fill = mode.Color, outline = None)
            canvas.create_text(mode.width / 2, 35 * mode.height / 64, 
                                text = "New Design", fill = "white",
                                font = ("ComicSansMS", 50))
            # Continue last design
            canvas.create_rectangle(mode.width / 4, 5 * mode.height / 8, 
                                    3 * mode.width / 4, 23 * mode.height / 32, 
                                    fill = mode.Color, outline = None)
            canvas.create_text(mode.width / 2, 43 * mode.height / 64, 
                                text = "Continue", fill = "white",
                                font = ("ComicSansMS", 50))
            # play
            canvas.create_rectangle(mode.width / 4, 3 * mode.height / 4, 
                                    3 * mode.width / 4, 27 * mode.height / 32, 
                                    fill = mode.Color, outline = None)
            canvas.create_text(mode.width / 2, 51 * mode.height / 64, 
                                text = "Play", fill = "white",
                                font = ("ComicSansMS", 50))
            # quit game
            canvas.create_rectangle(mode.width / 4, 7 * mode.height / 8, 
                                    3 * mode.width / 4, 31 * mode.height / 32, 
                                    fill = mode.Color, outline = None)
            canvas.create_text(mode.width / 2, 59 * mode.height / 64, 
                                text = "Quit", fill = "white",
                                font = ("ComicSansMS", 50))
            canvas.create_text(mode.width / 2, 63 * mode.height / 64, 
                                fill = "white", text = "Press h to get Help", 
                                font = ("ComicSansMS", 15))
                        
class DesignerMode(Mode):
    def appStarted(mode):
        mode.NumOfRoom = 0
        mode.app.RoomList = []
        mode.startColor = "gray"
        mode.backColor = "gray"
        mode.app.initialRoom = None
        mode.movingRoomIndex = 2
        mode.relativeRoom = None
        mode.relativeColor = "red"
        mode.RoomNum = mode.getUserInput("How many rooms would you like to make? Remember to set a final (exit) room. \n (preferably within 10)")
        if mode.RoomNum != None and mode.RoomNum.isdigit():
            if int(mode.RoomNum) <= 10:
                mode.NumOfRoom = int(mode.RoomNum)
                for i in range (mode.NumOfRoom):
                    size = 100
                    margin = ((mode.width - mode.NumOfRoom * size
                                                    ) / (mode.NumOfRoom + 1))
                    if i == 0:
                        room = Rooms(1, mode.width / 4, mode.height / 2, 
                                    mode.width / 4 + 100, mode.height / 2 + 100)
                    else:
                        room = Rooms(i + 1, margin * (i + 1) + size * i, mode.height - size, 
                                    margin * (i + 1) + size * (i + 1), mode.height)
                    mode.app.RoomList.append(room)
            else:
                mode.app.showMessage("Oops, I did not receive a valid number! Please retry!")
                mode.app.setActiveMode(mode.app.SplashScreenMode)
        else:
            mode.app.showMessage("Oops, I did not receive a valid number! Please retry!")
            mode.app.setActiveMode(mode.app.SplashScreenMode)
    
    # not in MVP
    def keyPressed(mode, event):
        if (event.key.isdigit() and mode.relativeRoom == None and 
                                mode.movingRoomIndex <= len(mode.app.RoomList)):
            if 0 < int(event.key) < mode.movingRoomIndex:
                mode.relativeRoom = mode.app.RoomList[int(event.key) - 1]
                mode.app.showMessage(f"You are moving rooms relative to {mode.relativeRoom}")
            else:
                mode.app.showMessage("Type in a valid number, please.")
        if (event.key.isdigit() and mode.relativeRoom == None and 
                                mode.movingRoomIndex > len(mode.app.RoomList)):
            mode.app.showMessage("You have positioned all the rooms! Let's start to design rooms!")
        elif mode.relativeRoom != None:
            if mode.movingRoomIndex <= len(mode.app.RoomList):
                mode.movingRoom = mode.app.RoomList[mode.movingRoomIndex - 1]
                oldX0 = mode.movingRoom.x0
                oldY0 = mode.movingRoom.y0
                oldX1 = mode.movingRoom.x1
                oldY1 = mode.movingRoom.y1
                if event.key == "Left":
                    relX0 = mode.relativeRoom.x0
                    relY0 = mode.relativeRoom.y0
                    mode.movingRoom.x1 = relX0
                    mode.movingRoom.x0 = relX0 - 100
                    mode.movingRoom.y0 = relY0
                    mode.movingRoom.y1 = relY0 + 100
                    if mode.checkRoomsCollide(mode.movingRoom)[0]:
                        mode.app.showMessage("Collision Detected!")
                        mode.movingRoom.x0 = oldX0
                        mode.movingRoom.x1 = oldX1
                        mode.movingRoom.y0 = oldY0
                        mode.movingRoom.y1 = oldY1
                elif event.key == "Right":
                    relX0 = mode.relativeRoom.x1
                    relY0 = mode.relativeRoom.y0
                    mode.movingRoom.x0 = relX0
                    mode.movingRoom.y0 = relY0
                    mode.movingRoom.x1 = relX0 + 100
                    mode.movingRoom.y1 = relY0 + 100
                    if mode.checkRoomsCollide(mode.movingRoom)[0]:
                        mode.app.showMessage("Collision Detected!")
                        mode.movingRoom.x0 = oldX0
                        mode.movingRoom.x1 = oldX1
                        mode.movingRoom.y0 = oldY0
                        mode.movingRoom.y1 = oldY1
                elif event.key == "Up":
                    relY0 = mode.relativeRoom.y0
                    relX1 = mode.relativeRoom.x1
                    mode.movingRoom.x1 = relX1
                    mode.movingRoom.y1 = relY0
                    mode.movingRoom.x0 = relX1 - 100
                    mode.movingRoom.y0 = relY0 - 100
                    if mode.checkRoomsCollide(mode.movingRoom)[0]:
                        mode.app.showMessage("Collision Detected!")
                        mode.movingRoom.x0 = oldX0
                        mode.movingRoom.x1 = oldX1
                        mode.movingRoom.y0 = oldY0
                        mode.movingRoom.y1 = oldY1
                elif event.key == "Down":
                    relX0 = mode.relativeRoom.x0
                    relY0 = mode.relativeRoom.y1
                    mode.movingRoom.x0 = relX0
                    mode.movingRoom.y0 = relY0
                    mode.movingRoom.x1 = relX0 + 100
                    mode.movingRoom.y1 = relY0 + 100
                    if mode.checkRoomsCollide(mode.movingRoom)[0]:
                        mode.app.showMessage("Collision Detected!")
                        mode.movingRoom.x0 = oldX0
                        mode.movingRoom.x1 = oldX1
                        mode.movingRoom.y0 = oldY0
                        mode.movingRoom.y1 = oldY1
                elif event.key == "Enter":
                    if mode.connection(mode.relativeRoom, mode.movingRoom):
                        mode.relativeRoom = None
                        mode.movingRoomIndex += 1
                    else:
                        mode.relativeRoom = None
                        mode.app.showMessage("You quit moving! Choose another relative room before proceeding!")
            else:
                mode.app.showMessage("You have positioned all rooms! Let's Start to design rooms!")

    # not in MVP
    @staticmethod
    def connection(room1, room2):
        Ax0, Ay0, Ax1, Ay1 = room1.getDimension()
        Bx0, By0, Bx1, By1 = room2.getDimension()
        if Ax0 == Bx1 and Ay0 == By0:
            return True
        elif Ax0 == Bx0 and Ay0 == By1:
            return True
        elif Ax1 == Bx0 and Ay0 == By0:
            return True
        elif Ax0 == Bx0 and Ay1 == By0:
            return True
        return False
    
    # not in MVP
    def checkRoomsCollide(mode, room):
        roomIndex = int(repr(room)[5]) - 1
        for i in range (roomIndex):
            prevRoom = mode.app.RoomList[i]
            if room != prevRoom:
                if room.x0 == prevRoom.x0 and room.y0 == prevRoom.y0:
                    return (True, prevRoom)
        return (False, None)
    
    def allConnected(mode):
        for i in range (len(mode.app.RoomList)):
            count = 0
            room1 = mode.app.RoomList[i]
            for j in range (len(mode.app.RoomList)):
                room2 = mode.app.RoomList[j]
                if room1 != room2 and mode.connection(room1, room2):
                    count += 1
            if count == 0:
                return False
        return True

    def mousePressed(mode, event):
        DesignRoom = False
        for rooms in mode.app.RoomList:
            try:
                assert(rooms.initialRoom == False)
            except AssertionError:
                DesignRoom = True
        if DesignRoom == False and mode.allConnected():
            for rooms in mode.app.RoomList:
                if ((rooms.x0 <= event.x <= rooms.x1) and 
                    (rooms.y0 <= event.y <= rooms.y1)):
                    respond = mode.app.getUserInput(f"Set {rooms} into initial room? \n Yes or No")
                    if respond != None:
                        if respond.lower() in ["y", "yes"]:
                            rooms.initialRoom = True
                            mode.app.initialRoom = rooms
                            break
                        elif respond.lower() in ["n", "no"]:
                            mode.canDrag = True
                            rooms.initialRoom = False
                            break
                    else:
                        mode.app.showMessage("You did not type in a correct form of response! Try again!")
        x0 = mode.width / 2 - 100
        y0 = mode.height / 10 + 10
        x1 = mode.width / 2 + 100
        y1 = mode.height / 10 + 70
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            if DesignRoom == True and mode.allConnected():
                mode.app.background = mode.app.getUserInput("Choose a color for the background!")
                mode.app.setActiveMode(mode.app.DesignRoomMode)
            else:
                mode.app.showMessage("You cannot use this function yet! Come back later.")
        x0Back = mode.width / 2 + 130
        y0Back = mode.height / 10 + 10
        x1Back = mode.width / 2 + 330
        y1Back = mode.height / 10 + 70
        if x0Back <= event.x <= x1Back and y0Back <= event.y <= y1Back:
            mode.app.setActiveMode(mode.app.SplashScreenMode)

    def mouseMoved(mode, event):
        x0Start = mode.width / 2 - 100
        y0Start = mode.height / 10 + 10
        x1Start = mode.width / 2 + 100
        y1Start = mode.height / 10 + 70
        if x0Start <= event.x <= x1Start and y0Start <= event.y <= y1Start:
            mode.startColor = "black"
        else:
            mode.startColor = "grey"
        x0Back = mode.width / 2 + 130
        y0Back = mode.height / 10 + 10
        x1Back = mode.width / 2 + 330
        y1Back = mode.height / 10 + 70
        if x0Back <= event.x <= x1Back and y0Back <= event.y <= y1Back:
            mode.backColor = "black"
        else:
            mode.backColor = "grey"

    def drawStartButton(mode, canvas):
        canvas.create_rectangle(mode.width / 2 - 100, mode.height / 10 + 10, 
        mode.width / 2 + 100, mode.height / 10 + 70, fill = "red")
        canvas.create_rectangle(mode.width / 2 - 80, mode.height / 10 + 30, 
        mode.width / 2 + 80, mode.height / 10 + 50, fill = mode.startColor)
        canvas.create_line(mode.width / 2 - 100, mode.height / 10 + 10, 
        mode.width / 2 - 80, mode.height / 10 + 30)
        canvas.create_line(mode.width / 2 + 100, mode.height / 10 + 70, 
        mode.width / 2 + 80, mode.height / 10 + 50)
        canvas.create_line(mode.width / 2 + 80, mode.height / 10 + 30, 
        mode.width / 2 + 100, mode.height / 10 + 10)
        canvas.create_line(mode.width / 2 - 80, mode.height / 10 + 50, 
        mode.width / 2 - 100, mode.height / 10 + 70)
        canvas.create_text(mode.width / 2, mode.height / 10 + 40, 
        text = "Start Designing Rooms", fill = "white")

    def goBackButton(mode, canvas):
        canvas.create_rectangle(mode.width / 2 + 130, mode.height / 10 + 10, 
        mode.width / 2 + 330, mode.height / 10 + 70, fill = "red")
        canvas.create_rectangle(mode.width / 2 + 150, mode.height / 10 + 30, 
        mode.width / 2 + 310, mode.height / 10 + 50, fill = mode.backColor)
        canvas.create_line(mode.width / 2 + 130, mode.height / 10 + 10, 
        mode.width / 2 + 150, mode.height / 10 + 30)
        canvas.create_line(mode.width / 2 + 330, mode.height / 10 + 70, 
        mode.width / 2 + 310, mode.height / 10 + 50)
        canvas.create_line(mode.width / 2 + 310, mode.height / 10 + 30, 
        mode.width / 2 + 330, mode.height / 10 + 10)
        canvas.create_line(mode.width / 2 + 150, mode.height / 10 + 50, 
        mode.width / 2 + 130, mode.height / 10 + 70)
        canvas.create_text(mode.width / 2 + 230, mode.height / 10 + 40, 
        text = "Go back to Menu", fill = "white")

    def redrawAll(mode, canvas):
        state = ""
        for rooms in mode.app.RoomList:
            if rooms == mode.relativeRoom: outline = mode.relativeColor
            else: outline = "black"
            canvas.create_rectangle(rooms.x0, rooms.y0, rooms.x1, rooms.y1, 
                                                            outline = outline)
            cx = (rooms.x0 + rooms.x1) / 2
            cy = (rooms.y0 + rooms.y1) / 2
            if rooms.initialRoom == True: state = "initial"
            elif rooms.initialRoom == False: state = ""
            canvas.create_text(cx, cy, text = f'{rooms} \n {state}')
        mode.drawStartButton(canvas)
        mode.goBackButton(canvas)
        canvas.create_text(mode.width / 2, mode.height / 4, 
        text = 
        """Press a number key to set the room you would like your next room to connect to. Press direction keys to position it. Press 'Enter' to stop.
                                                            (we will start at north of the initial room)""")
        canvas.create_polygon(mode.width / 8, mode.height / 4, mode.width / 7, 
        mode.height / 4, 15 * mode.width / 112, 3 * mode.height / 16)
        canvas.create_text(15 * mode.width / 112, 3 * mode.height / 16 - 10, 
        text = "North")

class DesignRoomMode(Mode):
    def appStarted(mode):
        if mode.app.IsNew == True:
            mode.initialRoom = mode.app.initialRoom
            mode.RoomList = mode.app.RoomList
            mode.setExitForRooms()
            mode.facing = "North"
            mode.RoomWeAreIn = mode.initialRoom
            mode.moving = None
            mode.items = []
            mode.itemsCoordinate = dict()
            mode.itemDragged = None
            mode.background = mode.app.background
            mode.selectedContainer = None
            mode.counter = -1
            # this image is downloaded from the Google Image and 
            # is originally from the website
            # https://www.kissclipart.com/transparent-background-black-door-png-clipart-door-rq1eg8/.
            imageDoor = mode.loadImage('Pictures&Songs/door.png')
            mode.scaledDoor = mode.scaleImage(imageDoor, 17/64)
            # this image is downloaded from the Google Image and 
            # is originally from the website
            # http://pluspng.com/png-120660.html.
            imageContainer = mode.loadImage('Pictures&Songs/Container.png')
            mode.scaledContainer = mode.scaleImage(imageContainer, 61/96)
            # this image is downloaded from the google Image and 
            # is originally from the website
            # https://drawception.com/game/ORZ2NBNZKp/the-most-famous-drawing/
            imageImage = mode.loadImage('Pictures&Songs/image.png')
            mode.scaledImage = mode.scaleImage(imageImage, 3/8)
            # this image is downloaded from the google Image and 
            # is originally from the website
            # https://www.shinola.com/journals.html
            imageJournal = mode.loadImage('Pictures&Songs/journal.png')
            mode.scaledJournal = mode.scaleImage(imageJournal, 3/8)
            # this image is downloaded from the google Image and 
            # is originally from the website
            # https://www.pngguru.com/free-transparent-background-png-clipart-bbene
            imagePaper = mode.loadImage('Pictures&Songs/paper.jpg')
            mode.scaledPaper = mode.scaleImage(imagePaper, 1/8)

        elif mode.app.IsNew == False:
            if findFile() == False:
                mode.app.showMessage("You have not saved anything yet! Come back later!")
                mode.app.setActiveMode(mode.app.SplashScreenMode)
            else:
                try:
                    loading = mode.load()
                    if loading["ready"] == False:
                        mode.initialRoom = loading["initialRoom"]
                        mode.RoomList = loading["RoomList"]
                        mode.facing = loading["facing"]
                        mode.RoomWeAreIn = loading["RoomWeAreIn"]
                        mode.moving = None
                        mode.items = loading["items"]
                        mode.itemsCoordinate = loading["itemsCoordinate"]
                        mode.itemDragged = None
                        mode.background = loading["background"]
                        mode.selectedContainer = None
                        mode.counter = -1
                        # this image is downloaded from the Google Image and
                        # is originally from the website
                        # https://www.kissclipart.com/transparent-background-black-door-png-clipart-door-rq1eg8/.
                        imageDoor = mode.loadImage('Pictures&Songs/door.png')
                        mode.scaledDoor = mode.scaleImage(imageDoor, 17/64)
                        # this image is downloaded from the Google Image and 
                        # is originally from the website
                        # http://pluspng.com/png-120660.html.
                        imageContainer = mode.loadImage('Pictures&Songs/Container.png')
                        mode.scaledContainer = mode.scaleImage(imageContainer, 61/96)
                        # this image is downloaded from the google Image and 
                        # is originally from the website
                        # https://drawception.com/game/ORZ2NBNZKp/the-most-famous-drawing/
                        imageImage = mode.loadImage('Pictures&Songs/image.png')
                        mode.scaledImage = mode.scaleImage(imageImage, 3/8)
                        # this image is downloaded from the google Image and 
                        # is originally from the website
                        # https://www.shinola.com/journals.html
                        imageJournal = mode.loadImage('Pictures&Songs/journal.png')
                        mode.scaledJournal = mode.scaleImage(imageJournal, 3/8)
                        # this image is downloaded from the google Image and 
                        # is originally from the website
                        # https://www.pngguru.com/free-transparent-background-png-clipart-bbene
                        imagePaper = mode.loadImage('Pictures&Songs/paper.jpg')
                        mode.scaledPaper = mode.scaleImage(imagePaper, 1/8)
                    else:
                        mode.app.showMessage("You are already done with this escape room! Play it or create another one!")
                        mode.app.setActiveMode(mode.app.SplashScreenMode)
                except:
                    mode.app.showMessage("You did not select any file!")
                    mode.app.setActiveMode(mode.app.SplashScreenMode)

    # Learnt how to use Pickle Module on the website: 
    # https://pythonprogramming.net/python-pickle-module-save-objects-serialization/#:~:targetText=First%2C%20import%20pickle%20to%20use,into%20opened%20file%2C%20then%20close.&targetText=Use%20pickle.,-load()%20to
    def save(mode, saving):
        filename = mode.app.getUserInput("Name the file before saving!")
        if filename != None:
            filename += ".dat"
            with open (filename, 'wb') as f:
                pickle.dump(saving, f)
        else:
            mode.app.showMessage("You did not save anything.")
    
    # Learnt how to use Pickle Module on the website: 
    # https://pythonprogramming.net/python-pickle-module-save-objects-serialization/#:~:targetText=First%2C%20import%20pickle%20to%20use,into%20opened%20file%2C%20then%20close.&targetText=Use%20pickle.,-load()%20to
    def load(mode):
        filename = askFileName()
        with open (filename, 'rb') as f:
            loading = pickle.load(f)
            return loading
    
    def setExitForRooms(mode):
        for i in range (len(mode.RoomList)):
            for j in range (len(mode.RoomList)):
                currentRoom = mode.RoomList[i]
                nextRoom = mode.RoomList[j]
                if currentRoom != nextRoom:
                    if (currentRoom.x0 == nextRoom.x0 and currentRoom.y0 == nextRoom.y1) and (
                        currentRoom.x1 == nextRoom.x1 and currentRoom.y0 == nextRoom.y1):
                        currentRoom.setExit("North", nextRoom)
                    elif (currentRoom.x0 == nextRoom.x0 and currentRoom.y1 == nextRoom.y0) and (
                        currentRoom.x1 == nextRoom.x1 and currentRoom.y1 == nextRoom.y0):
                        currentRoom.setExit("South", nextRoom)
                    elif (currentRoom.x0 == nextRoom.x1 and currentRoom.y0 == nextRoom.y0) and (
                        currentRoom.x0 == nextRoom.x1 and currentRoom.y1 == nextRoom.y1):
                        currentRoom.setExit("West", nextRoom)
                    elif (currentRoom.x1 == nextRoom.x0 and currentRoom.y1 == nextRoom.y1) and (
                        currentRoom.x1 == nextRoom.x0 and currentRoom.y0 == nextRoom.y0):
                        currentRoom.setExit("East", nextRoom)
    
    def keyPressed(mode, event):
        dirNames = ["North", "East", "South", "West"]
        currentDirIndex = dirNames.index(mode.facing)
        nextRoom = mode.RoomWeAreIn.getExit(mode.facing)
        if (event.key == "Right" and mode.moving == None and 
                                                mode.selectedContainer == None):
            mode.facing = dirNames[(currentDirIndex + 1) % len(dirNames)]
        elif (event.key == "Left" and mode.moving == None and 
                                                mode.selectedContainer == None):
            mode.facing = dirNames[(currentDirIndex - 1)]
        elif event.key == "Up":
            if mode.moving != None:
                mode.app.showMessage("Please finish moving item first!")
            elif nextRoom == None:
                mode.app.showMessage("No room exists behind this wall!")
            else:
                mode.RoomWeAreIn = nextRoom
        elif event.key == "Left" and mode.moving != None:
            mode.moving.x0 -= 10
            mode.moving.x1 -= 10
            if not mode.isLegal(mode.moving.x0, mode.moving.y0, 
                                                mode.moving.x1, mode.moving.y1):
                mode.moving.x0 += 10
                mode.moving.x1 += 10
            if isinstance(mode.moving, Door):
                if isinstance(mode.moving.key, KeyPads):
                    mode.moving.key.x0 -= 10
                    mode.moving.key.x1 -= 10
                    if not mode.isLegal(mode.moving.key.x0, mode.moving.key.y0, 
                        mode.moving.key.x1, mode.moving.key.y1):
                        mode.moving.key.x0 += 10
                        mode.moving.key.x1 += 10
                newDirection = dirNames[dirNames.index(mode.facing) - 2]
                for items in nextRoom.items:
                    if (isinstance(items, Door) and 
                                            items.direction == newDirection):
                        items.x0 += 10
                        items.x1 += 10
                        if isinstance(items.key, KeyPads):
                            items.key.x0 += 10
                            items.key.x1 += 10
                            if (not mode.isLegal(items.key.x0, items.key.y0, 
                                items.key.x1, items.key.y1) or 
                                items.key.x0 > items.x0):
                                items.key.x0 -= 10
                                items.key.x1 -= 10
                        if not mode.isLegal(items.x0, items.y0, 
                                                            items.x1, items.y1):
                            items.x0 -= 10
                            items.x1 -= 10
                        break
        elif event.key == "Right" and mode.moving != None:
            mode.moving.x0 += 10
            mode.moving.x1 += 10
            if not mode.isLegal(mode.moving.x0, mode.moving.y0, 
                                                mode.moving.x1, mode.moving.y1):
                mode.moving.x0 -= 10
                mode.moving.x1 -= 10
            if isinstance(mode.moving, Door):
                if isinstance(mode.moving.key, KeyPads):
                    mode.moving.key.x0 += 10
                    mode.moving.key.x1 += 10
                    if (not mode.isLegal(mode.moving.key.x0, mode.moving.key.y0, 
                        mode.moving.key.x1, mode.moving.key.y1) or 
                        mode.moving.key.x0 > mode.moving.x0):
                        mode.moving.key.x0 -= 10
                        mode.moving.key.x1 -= 10
                newDirection = dirNames[dirNames.index(mode.facing) - 2]
                for items in nextRoom.items:
                    if (isinstance(items, Door) and 
                                            items.direction == newDirection):
                        items.x0 -= 10
                        items.x1 -= 10
                        if isinstance(items.key, KeyPads):
                            items.key.x0 -= 10
                            items.key.x1 -= 10
                            if (not mode.isLegal(items.key.x0, items.key.y0, 
                                items.key.x1, items.key.y1) or 
                                items.key.x0 < items.x0):
                                items.key.x0 += 10
                                items.key.x1 += 10
                        if not mode.isLegal(items.x0, items.y0, 
                                                            items.x1, items.y1):
                            items.x0 += 10
                            items.x1 += 10
                        break
        elif event.key == "n" and mode.itemDragged != None:
            mode.counter += 1
            listOfContainer = []
            for items in mode.RoomWeAreIn.items:
                if (isinstance(items, Containers) and 
                                                items.direction == mode.facing):
                    listOfContainer.append(items)
            try:
                mode.selectedContainer = listOfContainer[mode.counter % len(listOfContainer)]
            except:
                mode.app.showMessage("No Container Found!")
        elif event.key == "Enter":
            if mode.moving != None:
                itemsInOneDirection = mode.everythingInOneDirection()
                for items in itemsInOneDirection:
                    if len(itemsInOneDirection) == 1: 
                        mode.moving = None
                        break
                    elif items == mode.moving: continue
                    else:
                        itemx0, itemy0, itemx1, itemy1 = items.getDimension()
                        movingx0, movingy0, movingx1, movingy1 = mode.moving.getDimension()
                        if (movingx0 > itemx1 or movingx1 < itemx0 or 
                            movingy0 > itemy1 or movingy1 < itemy0):
                            mode.moving = None
                            break
                        else: mode.app.showMessage("There is overlap! Please solve that first")
            elif mode.itemDragged != None and mode.selectedContainer != None:
                mode.items.remove(mode.itemDragged)
                del mode.itemsCoordinate[mode.itemDragged]
                mode.makeCoordinates()
                mode.selectedContainer.items.add(mode.itemDragged)
                mode.selectedContainer = None
                mode.itemDragged = None
            elif mode.itemDragged != None and mode.selectedContainer == None:
                mode.itemDragged = None
        elif event.key == "Delete" and mode.moving != None and mode.itemDragged == None:
            mode.RoomWeAreIn.items.remove(mode.moving)
            if isinstance(mode.moving, Door):
                nextRoom = mode.RoomWeAreIn.getExit(mode.facing)
                nextFacing = dirNames[dirNames.index(mode.facing) - 2]
                for items in nextRoom.items:
                    if isinstance(items, Door) and items.direction == nextFacing:
                        nextRoom.items.remove(items)
                        break
                for items in mode.items:
                    if (isinstance(items, Keys) and items == mode.moving.key):
                        mode.items.remove(items)
                        del mode.itemsCoordinate[items]
                        break
            elif isinstance(mode.moving, Containers):
                for items in mode.moving.items:
                    mode.items.append(items)
            mode.moving = None
        elif event.key == "Delete" and mode.itemDragged != None and mode.moving == None:
            mode.items.remove(mode.itemDragged)
            del mode.itemsCoordinate[mode.itemDragged]
            if isinstance(mode.itemDragged, Keys):
                for rooms in mode.RoomList:
                    for items in rooms.items:
                        if isinstance(items, Door) and items.key == mode.itemDragged:
                            items.key = None
                            break
            mode.itemDragged = None
        mode.makeCoordinates()
    
    def everythingInOneDirection(mode):
        result = []
        for items in mode.RoomWeAreIn.items:
            if items.direction == mode.facing:
                result.append(items)
        return result

    def mousePressed(mode, event):
        if (7 * mode.width / 8 <= event.x <= 39 * mode.width / 40):
            if (3 * mode.height / 50 <= event.y <= 7 * mode.height / 30) and (
                mode.RoomWeAreIn.getExit(mode.facing) != None):
                x0 = 17 * mode.width / 72
                y0 = 3 * mode.height / 25
                x1 = 17 * mode.width / 36
                y1 = 7 * mode.height / 10
                count = 0
                notMaking = False
                goingLeft = True
                while not mode.checkCollision(x0, y0, x1, y1):
                    if goingLeft == True:
                        x0 += 10
                        x1 += 10
                    elif goingLeft == False:
                        x0 -= 10
                        x1 -= 10
                    if not mode.isLegal(x0, y0, x1, y1):
                        count += 1
                        goingLeft = False
                    if count == 2: 
                        notMaking = True
                        mode.app.showMessage("Collision Detected!")
                        break
                if (not notMaking and Door(mode.RoomWeAreIn, mode.facing, 
                    x0, y0, x1, y1) not in mode.RoomWeAreIn.items):
                    mode.RoomWeAreIn.items.add(Door(mode.RoomWeAreIn, 
                    mode.facing, x0, y0, x1, y1))
                    nextRoom = mode.RoomWeAreIn.getExit(mode.facing)
                    dirList = ["North", "East", "South", "West"]
                    newFacing = dirList[dirList.index(mode.facing) - 2]
                    roomX0 = 17 * mode.width / 240
                    roomX1 = 187 * mode.width / 240
                    lastDoorX0 = x0
                    lastDoorX1 = x1
                    doorSize = 17 * mode.width / 72
                    doorX1 = roomX1 - lastDoorX0 + roomX0
                    doorX0 = doorX1 -  doorSize
                    nextRoom.items.add(Door(nextRoom, newFacing, doorX0, 
                            3 * mode.height / 25, doorX1, 7 * mode.height / 10))
                elif (Door(mode.RoomWeAreIn, mode.facing, x0, y0, x1, y1) in 
                        mode.RoomWeAreIn.items):
                    mode.app.showMessage("There is already a door here!")
            elif (3 * mode.height / 50 <= event.y <= 7 * mode.height / 30) and (
                mode.RoomWeAreIn.getExit(mode.facing) == None):
                mode.app.showMessage("No Room is behind that wall!")
            elif 71 * mode.height / 100 <= event.y <= 53 * mode.height / 60:
                for items in mode.RoomWeAreIn.items:
                    if (isinstance(items, Door) and 
                        items.direction == mode.facing and items.key == None):
                        nextRoom = items.room.getExit(mode.facing)
                        dirName = ["North", "East", "South", "West"]
                        dirIndex = dirName.index(mode.facing)
                        for stuff in nextRoom.items:
                            if (isinstance(stuff, Door) and 
                                stuff.direction == dirName[dirIndex - 2] and 
                                stuff.key == None):
                                # Not in MVP for KeyPads
                                form = mode.app.getUserInput("In what form would you like to lock the door? \n Press 1 or type 'key' to use keys and press 2 or type 'keypad' to use keyPads")
                                if form != None and form.lower() in ['1', 'key', 'keys']:
                                    x0 = 0
                                    y0 = 0
                                    x1 = 2 * mode.width / 25
                                    y1 = mode.height / 10
                                    mode.items.append(Keys(None, x0, y0, x1, y1,
                                                items.room, items.direction))
                                    items.key = Keys(None, x0, y0, x1, y1, 
                                                items.room, items.direction)
                                    stuff.key = Keys(None, x0, y0, x1, y1,
                                                items.room, items.direction)
                                    items.locked = True
                                    stuff.locked = True
                                elif form != None and form.lower() in ['2', 'keypad', 'keypads']:
                                    password = mode.app.getUserInput("Please type in password you would like to use \n(letters and numbers only, please.).")
                                    if (password == None or 
                                        not password.isalnum()):
                                        mode.app.showMessage("You did not type in a valid password! Try again!")
                                    else:
                                        cy = (items.y1 + items.y0) / 2
                                        x0 = items.x0
                                        y0 = cy - mode.height / 30
                                        x1 = items.x0 + mode.width / 48
                                        y1 = cy + mode.height / 30
                                        keypadFacing = KeyPads(x0, y0, x1, y1, 
                                        items.room, items.direction, password)
                                        otherY0 = y0
                                        otherY1 = y1
                                        otherX0 = stuff.x0
                                        otherX1 = stuff.x0 + mode.width / 48
                                        keypadOther = KeyPads(otherX0, otherY0, 
                                                otherX1, otherY1, stuff.room, 
                                                stuff.direction, password)
                                        items.key = keypadFacing
                                        stuff.key = keypadOther
                                        items.locked = True
                                        stuff.locked = True
                                else:
                                    mode.app.showMessage("Please type in a valid form of lock.")
                    elif (isinstance(items, Door) and 
                        items.direction == mode.facing and items.key != None):
                        mode.app.showMessage("There is no unpaired door!")
            elif 83 * mode.height / 300 <= event.y <= 9 * mode.height / 20:
                    x0 = 17 * mode.width / 60
                    y0 = mode.height / 5
                    x1 = 17 * mode.width / 30
                    y1 = 4 * mode.height / 5
                    count = 0
                    notMaking = False
                    goingLeft = True
                    while not mode.checkCollision(x0, y0, x1, y1):
                        if goingLeft == True:
                            x0 += 10
                            x1 += 10
                        elif goingLeft == False:
                            x0 -= 10
                            x1 -= 10
                        if not mode.isLegal(x0, y0, x1, y1):
                            count += 1
                            goingLeft = False
                        if count == 2: 
                            notMaking = True
                            mode.app.showMessage("Collision Detected!")
                            break
                    if not notMaking:
                        mode.RoomWeAreIn.items.add(Containers(mode.RoomWeAreIn,
                            mode.facing, x0, y0, x1, y1))
            elif 37 * mode.height / 75 <= event.y <= 2 * mode.height / 3:
                types = mode.app.getUserInput("You can choose to present the hint as a journal, an image, or a paper. Please type in your choice!")
                if types != None and types.lower() in ["journal", "image", "paper"]:
                    x0 = 0
                    y0 = 0
                    x1 = 2 * mode.width / 25
                    y1 = mode.height / 10
                    reasoning = mode.app.getUserInput("Please indicate how it relates to the escaping(None if merely for storyline).")
                    mode.items.append(Hints(None, types, reasoning, 
                                                        None, x0, y0, x1, y1))
                elif types == None or types.lower() not in ["journal", "image", "paper"]:
                    mode.app.showMessage("Please type in a valid type for your hints!")
        elif (3 * mode.width / 5 <= event.x <= 7 * mode.width / 10 and 
                mode.height / 30 <= event.y <= mode.height / 15):
                response = mode.app.getUserInput("""Do you want to set this room as your final room and finish editing this program?
                (Yes if you want to start the game and No if you just want to save it).""")
                if response != None:
                    # not in MVP
                    if response.lower() in ['y', 'yes']:
                        saving = {"initialRoom": mode.initialRoom, 
                                    "RoomList": mode.RoomList, 
                                    "facing": mode.facing, 
                                    "RoomWeAreIn": mode.RoomWeAreIn, 
                                    "items": mode.items, 
                                    "itemsCoordinate": mode.itemsCoordinate,
                                    "background": mode.background, 
                                    "ready": True}
                        mode.save(saving)
                        removeDat()
                        mode.app.setActiveMode(mode.app.SplashScreenMode)
                        # not in MVP
                    elif response.lower() in ['no', 'n']:
                        saving = {"initialRoom": mode.initialRoom, 
                                    "RoomList": mode.RoomList, 
                                    "facing": mode.facing, 
                                    "RoomWeAreIn": mode.RoomWeAreIn, 
                                    "items": mode.items, 
                                    "itemsCoordinate": mode.itemsCoordinate,
                                    "background": mode.background, 
                                    "ready": False}
                        mode.save(saving)
                        removeDat()
                        mode.app.setActiveMode(mode.app.SplashScreenMode)
                    else:
                        mode.app.showMessage("You did not type in a correct command.")
                else:
                    mode.app.showMessage("Let's continue!")
        else:
            for items in mode.RoomWeAreIn.items:
                if (items.x0 <= event.x <= items.x1 and 
                    items.y0 <= event.y <= items.y1 and 
                    mode.moving == None and 
                    mode.itemDragged == None and 
                    items.direction == mode.facing):
                    mode.moving = items
                    mode.app.showMessage(f"You are moving {items}! Press 'Enter' to exit moving!")
                    break
            if not isinstance(mode.moving, Containers):
                for items in mode.itemsCoordinate:
                    x0, y0, x1, y1 = mode.itemsCoordinate[items]
                    if x0 <= event.x <= x1 and y0 <= event.y <= y1:
                        if mode.moving == None and mode.itemDragged == None:
                            mode.itemDragged = items
                            mode.app.showMessage(f"You are moving {items}! Press 'Enter' to confirm moving!")
                            break
                        else: 
                            if mode.moving != None: currentMoving = mode.moving
                            else: currentMoving = mode.itemDragged
                            mode.app.showMessage(f"You are moving {currentMoving} right now! Exit first!")
                            break
            elif isinstance(mode.moving, Containers):
                itemsInContainers = mode.makeCoordinatesForItemsInContainers(mode.moving)
                for items in itemsInContainers:
                    (x0, y0, x1, y1) = itemsInContainers[items]
                    if x0 <= event.x <= x1 and y0 <= event.y <= y1:
                        mode.moving.items.remove(items)
                        mode.items.append(items)
                        mode.app.showMessage("This item is in your item bag now! Exit to view!")
        mode.makeCoordinates()

    def checkCollision(mode, x0, y0, x1, y1):
        for items in mode.RoomWeAreIn.items:
            if items.direction == mode.facing:
                (itemx0, itemy0, itemx1, itemy1) = items.getDimension()
                try:
                    assert(y1 < itemy0 or y0 > itemy1 or x1 < itemx0 or x0 > itemx1)
                except AssertionError:
                    return False
        return True
    
    def isLegal(mode, x0, y0, x1, y1):
        if x0 < 17 * mode.width / 240 or x1 > 187 * mode.width / 240:
            return False
        return True

    def drawCreationBoard(mode, canvas):
        canvas.create_text(37 * mode.width / 40, 3 * mode.height / 100, 
                            text = "Creation Board", font = ("ComicSansMS", 20))
        # Doors
        canvas.create_rectangle(7 * mode.width / 8, 3 * mode.height / 50, 
                            39 * mode.width / 40, 7 * mode.height / 30)
        canvas.create_text(37 * mode.width / 40, 11 * mode.height / 75, 
                            text = "Doors")
        # Container
        canvas.create_rectangle(7 * mode.width / 8, 83 * mode.height / 300, 
                            39 * mode.width / 40, 9 * mode.height / 20)
        canvas.create_text(37 * mode.width / 40, 109 * mode.height / 300, 
                            text = "Containers")
        # Hints
        canvas.create_rectangle(7 * mode.width / 8, 37 * mode.height / 75, 
                            39 * mode.width / 40, 2 * mode.height / 3)
        canvas.create_text(37 * mode.width / 40, 29 * mode.height / 50, 
                            text = "Hints")
        # Keys
        canvas.create_rectangle(7 * mode.width / 8, 71 * mode.height / 100, 
                            39 * mode.width / 40, 53 * mode.height / 60)
        canvas.create_text(37 * mode.width / 40, 239 * mode.height / 300, 
                            text = "Keys")

    def makeCoordinates(mode):
        count = -1
        for items in mode.items:
            count += 1
            width = 2 * mode.width / 25
            height = mode.height / 10
            margin = mode.width / 50
            x0 = mode.width / 20 + items.x0 + (width + margin) * count
            x1 = mode.width / 20 + items.x1 + (width + margin) * count
            y0 = items.y0 + 17 * mode.height / 20
            y1 = items.y1 + 17 * mode.height / 20
            mode.itemsCoordinate[items] = [x0, y0, x1, y1]
    
    def makeCoordinatesForItemsInContainers(mode, container):
        count = -1
        containerItemsCoordinates = dict()
        for items in container.items:
            count += 1
            width = 2 * mode.width / 25
            height = mode.height / 10
            margin = mode.width / 50
            x0 = mode.width / 20 + items.x0 + (width + margin) * count
            x1 = mode.width / 20 + items.x1 + (width + margin) * count
            y0 = items.y0 + 17 * mode.height / 20
            y1 = items.y1 + 17 * mode.height / 20
            containerItemsCoordinates[items] = [x0, y0, x1, y1]
        return containerItemsCoordinates
    
    def drawKey(mode, canvas, x0, y0, x1, y1):
        width = x1 - x0
        height = y1 - y0
        canvas.create_rectangle(x0 + 15 * width / 32, y0 + 2 * height / 16, 
                                    x0 + 17 * width / 32, y0 + 15 * height / 16)
        canvas.create_oval(x0 + 3 * width / 8, y0 + height / 16, 
                                    x0 + 5 * width / 8, y0 + 3 * height / 8, 
                                    fill = "white")
        canvas.create_oval(x0 + 7 * width / 16, y0 + height / 8, 
                                    x0 + 9 * width / 16, y0 + 5 * height / 16, 
                                    fill = "white")
        canvas.create_rectangle(x0 + 12 * width / 32, y0 + 10 * height / 16, 
                                    x0 + 15 * width / 32, y0 + 11 * height / 16)
        canvas.create_rectangle(x0 + 12 * width / 32, y0 + 12 * height / 16, 
                                    x0 + 15 * width / 32, y0 + 13 * height / 16)

    def drawBagBoard(mode, canvas):
        canvas.create_text(3 * mode.width / 100, 9 * mode.height / 10, 
                            text = "I\nT\nE\nM\nS", font = ("ComicSansMS", 20))
        for items in mode.itemsCoordinate:
            (x0, y0, x1, y1) = mode.itemsCoordinate[items]
            if isinstance(items, Keys):
                text = items.name
                mode.drawKey(canvas, x0, y0, x1, y1)
                canvas.create_text(x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2, 
                text = text)
            elif isinstance(items, Hints):
                text = items.types
                if text.lower() == "image":
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledImage))
                elif text.lower() == "journal":
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledJournal))
                else:
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledPaper))
                canvas.create_text(x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2, 
                text = text)

    def drawContainerItems(mode, canvas):
        canvas.create_text(3 * mode.width / 100, 9 * mode.height / 10, 
                            text = "I\nN\nS\nI\nD\nE", font = ("ComicSansMS", 20))
        coordinate = mode.makeCoordinatesForItemsInContainers(mode.moving)
        for items in coordinate:
            (x0, y0, x1, y1) = coordinate[items]
            if isinstance(items, Keys):
                text = items.name
                mode.drawKey(canvas, x0, y0, x1, y1)
                canvas.create_text(x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2, 
                text = text)
            elif isinstance(items, Hints):
                text = items.types
                if text.lower() == "image":
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledImage))
                elif text.lower() == "journal":
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledJournal))
                else:
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledPaper))
                canvas.create_text(x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2, 
                text = text)

    def drawRoom(mode, canvas):
        try:
            canvas.create_rectangle(0, 0, 17 * mode.width / 20, 
                        4 * mode.height / 5, width = 1, fill = mode.background)
        except:
            canvas.create_rectangle(0, 0, 17 * mode.width / 20, 
                        4 * mode.height / 5, width = 1, fill = "white")
        canvas.create_line(17 * mode.width / 240, mode.height / 10, 0, 0)
        canvas.create_line(17 * mode.width / 240, 7 * mode.height / 10, 0, 
                            4 * mode.height / 5)
        canvas.create_line(187 * mode.width / 240, mode.height / 10, 
                            17 * mode.width / 20, 0)
        canvas.create_line(187 * mode.width / 240, 7 * mode.height / 10, 
                            17 * mode.width / 20, 4 * mode.height / 5)
        canvas.create_rectangle(17 * mode.width / 240, mode.height / 10, 
                                187 * mode.width / 240, 7 * mode.height / 10)
        # not in MVP
        if mode.RoomWeAreIn.getExit(mode.facing) != None:
            canvas.create_text(1 * mode.width / 4, mode.height / 20, 
                text = f'{mode.facing} in {mode.RoomWeAreIn}\n(There is a room behind the wall).', 
                font = "Times 20")
        else:
            canvas.create_text(1 * mode.width / 4, mode.height / 20, 
                text = f'{mode.facing} in {mode.RoomWeAreIn}', font = "Times 30")

    # not in MVP
    def drawKeyPad(mode, canvas, x0, y0, x1, y1):
        canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
        margin = 2
        canvas.create_rectangle(x0 + margin, y0 + margin, x1 - margin, 
                                                y0 + 7 * margin, fill = "cyan")
        for row in range (4):
            for col in range (3):
                d = (x1 - x0 - 2 * margin) / 3
                padX0 = x0 + margin + d * col
                padY0 = y0 + 8 * margin + row * d
                padX1 = padX0 + d
                padY1 = padY0 + d
                canvas.create_oval(padX0, padY0, padX1, padY1, fill = "gray")

    def drawItems(mode, canvas):
        for items in mode.RoomWeAreIn.items:
            if mode.selectedContainer != None and items == mode.selectedContainer:
                x0 = items.x0
                y0 = items.y0
                x1 = items.x1
                y1 = items.y1
                canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                image=ImageTk.PhotoImage(mode.scaledContainer))
                canvas.create_rectangle(x0, y0, x1, y1, outline = "red")
            elif items.direction.lower() == mode.facing.lower():
                x0 = items.x0
                y0 = items.y0
                x1 = items.x1
                y1 = items.y1
                if isinstance(items, Door):
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                image=ImageTk.PhotoImage(mode.scaledDoor))
                    if isinstance(items.key, KeyPads):
                        x0, y0, x1, y1 = items.key.getDimension()
                        mode.drawKeyPad(canvas, x0, y0, x1, y1)
                elif isinstance(items, Containers):
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                image=ImageTk.PhotoImage(mode.scaledContainer))
    
    def drawSaveAndBackButton(mode, canvas):
        canvas.create_rectangle(3 * mode.width / 5, mode.height / 30,
         7 * mode.width / 10, mode.height / 15, fill = "gray")
        canvas.create_text(13 * mode.width / 20, mode.height / 20, 
        text = "Save and Exit", fill = "white")
    
    def redrawAll(mode, canvas):
        mode.drawRoom(canvas)
        mode.drawCreationBoard(canvas)
        mode.drawItems(canvas)
        if isinstance(mode.moving, Containers):
            mode.drawContainerItems(canvas)
        else:
            mode.drawBagBoard(canvas)
        mode.drawSaveAndBackButton(canvas)
        if mode.itemDragged != None:
            canvas.create_text(17 * mode.width / 40, 7 * mode.height / 80, 
            text = "Press n to select a container to put this item in.",
            fill = "red")

class PlayerMode(Mode):
    def appStarted(mode):
        # not in MVP
        if findFile() == False:
            mode.app.showMessage("No game is made yet! Go create your own!")
            mode.app.setActiveMode(mode.app.SplashScreenMode)
        else:
            # not in MVP
            try:
                savings = mode.load()
                if savings["ready"] == False:
                    mode.app.showMessage("This game is not ready for playing yet!")
                    mode.app.setActiveMode(mode.app.SplashScreenMode)
                else:
                    mode.initialRoom = savings["initialRoom"]
                    mode.RoomList = savings["RoomList"]
                    mode.facing = "North"
                    mode.RoomWeAreIn = mode.initialRoom
                    mode.items = []
                    mode.itemsCoordinate = {}
                    mode.background = savings["background"]
                    mode.checking = None
                    mode.itemHolding = None
                    mode.finalRoom = savings["RoomWeAreIn"]
                    mode.gameOver = False
                    # this image is downloaded from the Google Image and 
                    # is originally from the website
                    # https://www.kissclipart.com/transparent-background-black-door-png-clipart-door-rq1eg8/.
                    imageDoor = mode.loadImage('Pictures&Songs/door.png')
                    mode.scaledDoor = mode.scaleImage(imageDoor, 17/64)
                    # this image is downloaded from the Google Image and 
                    # is originally from the website
                    # http://pluspng.com/png-120660.html.
                    imageContainer = mode.loadImage('Pictures&Songs/Container.png')
                    mode.scaledContainer = mode.scaleImage(imageContainer, 61/96)
                    # this image is downloaded from the google Image and 
                    # is originally from the website
                    # https://drawception.com/game/ORZ2NBNZKp/the-most-famous-drawing/
                    imageImage = mode.loadImage('Pictures&Songs/image.png')
                    mode.scaledImage = mode.scaleImage(imageImage, 3/8)
                    # this image is downloaded from the google Image and 
                    # is originally from the website
                    # https://www.shinola.com/journals.html
                    imageJournal = mode.loadImage('Pictures&Songs/journal.png')
                    mode.scaledJournal = mode.scaleImage(imageJournal, 3/8)
                    # this image is downloaded from the google Image and 
                    # is originally from the website
                    # https://www.pngguru.com/free-transparent-background-png-clipart-bbene
                    imagePaper = mode.loadImage('Pictures&Songs/paper.jpg')
                    mode.scaledPaper = mode.scaleImage(imagePaper, 1/8)
            except:
                mode.app.showMessage("You did not select any file!")
                mode.app.setActiveMode(mode.app.SplashScreenMode)
    
    # Learnt how to use Pickle Module on the website: 
    # https://pythonprogramming.net/python-pickle-module-save-objects-serialization/#:~:targetText=First%2C%20import%20pickle%20to%20use,into%20opened%20file%2C%20then%20close.&targetText=Use%20pickle.,-load()%20to
    # not in MVP
    def load(mode):
        filename = askFileName()
        with open (filename, 'rb') as f:
            loading = pickle.load(f)
            return loading

    def keyPressed(mode, event):
        if mode.gameOver == False:
            dirNames = ['North', 'East', 'South', 'West']
            dirIndex = dirNames.index(mode.facing)
            if event.key == "Left": 
                if mode.checking == None:
                    mode.facing = dirNames[dirIndex - 1]
                else:
                    mode.app.showMessage("Please finish checking container first!")
            elif event.key == "Right":
                if mode.checking == None:
                    mode.facing = dirNames[(dirIndex + 1) % len(dirNames)]
                else:
                    mode.app.showMessage("Please finish checking container first!")
            elif event.key == "Up":
                if mode.checking == None:
                    if mode.RoomWeAreIn.getExit(mode.facing) == None:
                        mode.app.showMessage("There is no room behind this wall!")
                    else:
                        nextRoom = mode.RoomWeAreIn.getExit(mode.facing)
                        for items in mode.RoomWeAreIn.items:
                            if (isinstance(items, Door) and 
                                mode.facing.lower() == items.direction.lower()):
                                door = items
                                if door.locked and isinstance(door.key, Keys):
                                    mode.app.showMessage("This door is locked. Try to find the key!")
                                elif (door.locked and 
                                                isinstance(door.key, KeyPads)):
                                    mode.app.showMessage("This door is locked. Try to find the password!")
                                else:
                                    mode.RoomWeAreIn = nextRoom
                                    if mode.RoomWeAreIn == mode.finalRoom:
                                        mode.gameOver = True
                                        mode.app.showMessage("Congrats! You just escaped! Press 'r' to go back to menu!")
                else:
                    mode.app.showMessage("Please finish checking container first!")
            elif event.key == "Enter":
                if mode.itemHolding == None and mode.checking != None:
                    mode.checking = None
                    mode.app.showMessage("You quit checking.")
                elif mode.itemHolding != None and mode.checking == None:
                    mode.itemHolding = None
                    mode.app.showMessage("You quit holding item.")
        elif mode.gameOver == True:
            if event.key == "r":
                mode.app.setActiveMode(mode.app.SplashScreenMode)
    
    def mousePressed(mode, event):
        for items in mode.RoomWeAreIn.items:
            x0, y0, x1, y1 = items.getDimension()
            if mode.itemHolding == None:
                if (items.direction == mode.facing and 
                    x0 <= event.x <= x1 and 
                    y0 <= event.y <= y1):
                    if isinstance(items, Containers):
                        mode.checking = items
                    elif isinstance(items, Door):
                        if items.locked:
                            if isinstance(items.key, Keys):
                                mode.app.showMessage("This door is locked.")
                            elif isinstance(items.key, KeyPads):
                                userPsw = mode.app.getUserInput("Please type in password.")
                                if userPsw == items.key.password:
                                    mode.app.showMessage("You opened the door...")
                                    items.locked = False
                                    nextRoom = mode.RoomWeAreIn.getExit(mode.facing)
                                    dirnames =  ['North', 'West', 'South', "East"]
                                    dirindex = dirnames.index(mode.facing)
                                    for stuff in nextRoom.items:
                                        if (isinstance(stuff, Door) and 
                                            stuff.direction.lower() == dirnames[dirindex - 2].lower()):
                                            stuff.locked = False
                                            break
                                else:
                                    mode.app.showMessage("You typed in the wrong password!")
                                break
                        else:
                            mode.app.showMessage("This door is unlocked.")
                    break
            else:
                if isinstance(mode.itemHolding, Keys):
                    if (items.direction.lower() == mode.facing.lower()
                     and x0 <= event.x <= x1 and y0 <= event.y <= y1 
                     and isinstance(items, Door)):
                        if (items.key == mode.itemHolding and 
                            items.locked == True):
                            mode.app.showMessage("You opened this door...")
                            items.locked = False
                            nextRoom = mode.RoomWeAreIn.getExit(mode.facing)
                            dirnames =  ['North', 'West', 'South', "East"]
                            dirindex = dirnames.index(mode.facing)
                            for stuff in nextRoom.items:
                                if (isinstance(stuff, Door) and 
                                    stuff.direction.lower() == dirnames[dirindex - 2].lower()):
                                    stuff.locked = False
                                    break
                            mode.itemHolding = None
                            break
                        elif (items.key == mode.itemHolding and 
                                                        items.locked == False):
                            mode.app.showMessage("You have already opened this door. \nGo explore what is in there.")
        if mode.checking == None:
            for items in mode.itemsCoordinate:
                x0, y0, x1, y1 = mode.itemsCoordinate[items]
                if x0 <= event.x <= x1 and y0 <= event.y <= y1:
                    if isinstance(items, Keys):
                        mode.itemHolding = items
                        mode.app.showMessage("You are holding a key right now!")
                    elif isinstance(items, Hints):
                        mode.app.showMessage(items.reasoning)
                    break
        if mode.checking != None and isinstance(mode.checking, Containers):
            itemsCoor = mode.makeCoordinatesForItemsInContainers(mode.checking)
            for items in itemsCoor:
                x0, y0, x1, y1 = itemsCoor[items]
                if x0 <= event.x <= x1 and y0 <= event.y <= y1:
                    mode.checking.items.remove(items)

                    mode.items.append(items)
                    mode.makeCoordinates()

    def makeCoordinates(mode):
        count = -1
        for items in mode.items:
            count += 1
            width = 2 * mode.width / 25
            height = mode.height / 10
            margin = mode.width / 50
            x0 = mode.width / 20 + items.x0 + (width + margin) * count
            x1 = mode.width / 20 + items.x1 + (width + margin) * count
            y0 = items.y0 + 17 * mode.height / 20
            y1 = items.y1 + 17 * mode.height / 20
            mode.itemsCoordinate[items] = [x0, y0, x1, y1]
    
    def makeCoordinatesForItemsInContainers(mode, container):
        count = -1
        containerItemsCoordinates = dict()
        for items in container.items:
            count += 1
            width = 2 * mode.width / 25
            height = mode.height / 10
            margin = mode.width / 50
            x0 = mode.width / 20 + items.x0 + (width + margin) * count
            x1 = mode.width / 20 + items.x1 + (width + margin) * count
            y0 = items.y0 + 17 * mode.height / 20
            y1 = items.y1 + 17 * mode.height / 20
            containerItemsCoordinates[items] = [x0, y0, x1, y1]
        return containerItemsCoordinates
    
    def drawKey(mode, canvas, x0, y0, x1, y1):
        width = x1 - x0
        height = y1 - y0
        canvas.create_rectangle(x0 + 15 * width / 32, y0 + 2 * height / 16, 
                                    x0 + 17 * width / 32, y0 + 15 * height / 16)
        canvas.create_oval(x0 + 3 * width / 8, y0 + height / 16, 
                                    x0 + 5 * width / 8, y0 + 3 * height / 8, 
                                    fill = "white")
        canvas.create_oval(x0 + 7 * width / 16, y0 + height / 8, 
                                    x0 + 9 * width / 16, y0 + 5 * height / 16, 
                                    fill = "white")
        canvas.create_rectangle(x0 + 12 * width / 32, y0 + 10 * height / 16, 
                                    x0 + 15 * width / 32, y0 + 11 * height / 16)
        canvas.create_rectangle(x0 +12 * width / 32, y0 + 12 * height / 16, 
                                    x0 + 15 * width / 32, y0 + 13 * height / 16)

    def drawRoom(mode, canvas):
        try:
            canvas.create_rectangle(0, 0, 17 * mode.width / 20, 
                        4 * mode.height / 5, width = 1, fill = mode.background)
        except:
            canvas.create_rectangle(0, 0, 17 * mode.width / 20, 
                        4 * mode.height / 5, width = 1, fill = "white")
        canvas.create_line(17 * mode.width / 240, mode.height / 10, 0, 0)
        canvas.create_line(17 * mode.width / 240, 7 * mode.height / 10, 0, 
                            4 * mode.height / 5)
        canvas.create_line(187 * mode.width / 240, mode.height / 10, 
                            17 * mode.width / 20, 0)
        canvas.create_line(187 * mode.width / 240, 7 * mode.height / 10, 
                            17 * mode.width / 20, 4 * mode.height / 5)
        canvas.create_rectangle(17 * mode.width / 240, mode.height / 10, 
                                187 * mode.width / 240, 7 * mode.height / 10)
        canvas.create_text(1 * mode.width / 4, mode.height / 20, 
                            text = mode.facing, font = "Times 30")

    # not in MVP
    def drawKeyPad(mode, canvas, x0, y0, x1, y1, color):
        canvas.create_rectangle(x0, y0, x1, y1, fill = "black")
        margin = 2
        canvas.create_rectangle(x0 + margin, y0 + margin, 
                                    x1 - margin, y0 + 7 * margin, fill = color)
        for row in range (4):
            for col in range (3):
                d = (x1 - x0 - 2 * margin) / 3
                padX0 = x0 + margin + d * col
                padY0 = y0 + 8 * margin + row * d
                padX1 = padX0 + d
                padY1 = padY0 + d
                canvas.create_oval(padX0, padY0, padX1, padY1, fill = "gray")
    
    def drawItems(mode, canvas):
        for items in mode.RoomWeAreIn.items:
            if items.direction.lower() == mode.facing.lower():
                x0 = items.x0
                y0 = items.y0
                x1 = items.x1
                y1 = items.y1
                if isinstance(items, Door):
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledDoor))
                    if isinstance(items.key, KeyPads):
                        x0, y0, x1, y1 = items.key.getDimension()
                        if items.locked == True:
                            mode.drawKeyPad(canvas, x0, y0, x1, y1, "red")
                        else:
                            mode.drawKeyPad(canvas, x0, y0, x1, y1, "cyan")
                elif isinstance(items, Containers):
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledContainer))

    def drawBagBoard(mode, canvas):
        canvas.create_text(3 * mode.width / 100, 9 * mode.height / 10, 
                            text = "I\nT\nE\nM\nS", font = ("ComicSansMS", 20))
        for items in mode.itemsCoordinate:
            (x0, y0, x1, y1) = mode.itemsCoordinate[items]
            if isinstance(items, Keys):
                text = items.name
                mode.drawKey(canvas, x0, y0, x1, y1)
                canvas.create_text(x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2, 
                text = text)
            elif isinstance(items, Hints):
                text = items.types
                if text.lower() == "image":
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledImage))
                elif text.lower() == "journal":
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledJournal))
                else:
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledPaper))
                canvas.create_text(x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2, 
                text = text)

    def drawContainerItems(mode, canvas):
        canvas.create_text(3 * mode.width / 100, 9 * mode.height / 10, 
                            text = "I\nN\nS\nI\nD\nE", font = ("ComicSansMS", 20))
        coordinate = mode.makeCoordinatesForItemsInContainers(mode.checking)
        for items in coordinate:
            (x0, y0, x1, y1) = coordinate[items]
            if isinstance(items, Keys):
                text = items.name
                mode.drawKey(canvas, x0, y0, x1, y1)
                canvas.create_text(x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2, 
                text = text)
            elif isinstance(items, Hints):
                text = items.types
                if text.lower() == "image":
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledImage))
                elif text.lower() == "journal":
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledJournal))
                else:
                    canvas.create_image((x0 + x1) / 2, (y0 + y1) / 2, 
                                    image=ImageTk.PhotoImage(mode.scaledPaper))
                canvas.create_text(x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2, 
                text = text)

    def redrawAll(mode, canvas):
        mode.drawRoom(canvas)
        mode.drawItems(canvas)
        if isinstance(mode.checking, Containers):
            mode.drawContainerItems(canvas)
        else:
            mode.drawBagBoard(canvas)

class HelpMode(Mode):
    def appStarted(mode):
        # This image is downloaded from Google Image and is originally uploaded
        # by https://www.powermazda.com/escape-rooms-portland/
        imageBG = mode.loadImage('background.jpg')
        mode.scaledBG = mode.scaleImage(imageBG, 1.5)

    def keyPressed(mode, event):
        if event.key == "h":
            mode.app.setActiveMode(mode.app.SplashScreenMode)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, 
                                        image=ImageTk.PhotoImage(mode.scaledBG))
        canvas.create_text(mode.width / 2, mode.height / 2, text = """
        This game allows users to create and play an escape room game. To start, click on 'New Design' and you can start to design how to combine rooms. \n
        Remember to follow the instructions. Then set the initial room by clicking on it. Click 'Start' and you can start to design what is in a room! \n
        Click blocks at right of the screen to create items. Click on them if you want to move them. If you made a keyPad, remember that keypads cannot be modified, \n
        for it is locked inside of the door. If it is locked by a key, however, you can delete the key in the bag area. Below the room is your bag items. \n
        You can click on them to move them. If you want to put them into a container, click 'n' after clicking on it and choose the container you would like to put in. \n
        If you click on a container, the bag area will become items in containers, and you can click on them to put them in your bag! \n
        After you are done, click 'Save and Exit' and you can click on 'play' to start the game you did! \n
        Everything works the same except you cannot move around items except moving hints in containers out to your bag!\n 
        To open a door, simply click on the key and then click on the door. If you would like to read informations on hints,\n
        click on them and you will see! Have fun with this game!\n
        Press 'h' to go back!""",
        font = ("Times", 22), fill = "red")

class MyModalApp(ModalApp):
    def appStarted(app):
        # Learnt how to use pygame.mixer.music on 
        # https://www.pygame.org/docs/ref/music.html
        pygame.init()
        # This music is downloaded from https://www.purple-planet.com/creepy
        pygame.mixer.music.load('Pictures&Songs/Theme Song.mp3')
        pygame.mixer.music.play(-1)
        app.SplashScreenMode = SplashScreenMode()
        app.DesignerMode = DesignerMode()
        app.DesignRoomMode = DesignRoomMode()
        app.PlayerMode = PlayerMode()
        app.HelpMode = HelpMode()
        app.setActiveMode(app.SplashScreenMode)

app = MyModalApp(width = 1440, height = 805)

