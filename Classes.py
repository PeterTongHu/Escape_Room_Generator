# this file contains all necessary classes created for the project.

class Door(object):
    def __init__(self, room, direction, x0, y0, x1, y1, locked = False, key = None):
        self.room = room
        self.direction = direction
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.locked = locked
        self.key = key

    def __repr__(self):
        return f"Door at the {self.direction} of {self.room}"

    def __eq__(self, other):
        return (isinstance(other, Door) and self.room == other.room and 
            self.direction == other.direction)

    def __hash__(self):
        return hash((self.direction,))

    def getDimension(self):
        return (self.x0, self.y0, self.x1, self.y1)

class Containers(object):
    def __init__(self, room, direction, x0, y0, x1, y1):
        self.room = room
        self.direction = direction
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.items = set()
    
    def __repr__(self):
        return f"Container at the {self.direction} of {self.room}"

    def __eq__(self, other):
        return (isinstance(other, Containers) and self.room == other.room and 
                self.direction == other.direction and self.x0 == other.x0 and 
                self.y0 == other.y0 and self.x1 == other.x1 and self.y1 == other.y1)
    
    def __hash__(self):
        return hash((self.direction, ))
    
    def getDimension(self):
        return (self.x0, self.y0, self.x1, self.y1)

class Keys(object):
    def __init__(self, container, x0, y0, x1, y1, doorRoom, doorDir):
        self.container = container
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.doorRoom = doorRoom
        self.doorDir = doorDir
        self.name = "Keys"
    
    def __repr__(self):
        return f"Key"

    def __eq__(self, other):
        dirName = ["North", "East", "South", "West"]
        doorDirIndex = dirName.index(self.doorDir)
        if self.doorRoom == other.doorRoom and self.doorDir == other.doorDir:
            return (isinstance(other, Keys) and self.container == other.container)
        elif self.doorRoom.getExit(self.doorDir) == other.doorRoom and dirName[doorDirIndex - 2] == other.doorDir:
            return (isinstance(other, Keys) and self.container == other.container)
    
    def __hash__(self):
        return hash((self.container, ))

    def getDimension(self):
        return (self.x0, self.y0, self.x1, self.y1)

class Hints(object):
    def __init__(self, container, types, reasoning, direction, x0, y0, x1, y1):
        self.container = container
        self.types = types
        # type refers to notes, journals, images, etc
        self.reasoning = reasoning
        self.direction = direction
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def __repr__(self):
        return f"a {self.types}"
    
    def __eq__(self, other):
        return False
    
    def __hash__(self):
        return hash((self.container, self.types, self.x0, self.y0))
    
    def getDimension(self):
        return (self.x0, self.y0, self.x1, self.y1)


class Rooms(object):
    def __init__(self, n, x0, y0, x1, y1, initialRoom = False):
        self.n = n
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.initialRoom = initialRoom
        self.exits = dict()
        self.items = set()

    def __repr__(self):
        return f"Room {self.n}"

    def __eq__(self, other):
        return (isinstance(other, Rooms)) and (self.n == other.n) and (self.x0 == other.x0
        ) and (self.y0 == other.y0) and (self.initialRoom == other.initialRoom)

    def __hash__(self):
        return hash((self.n, self.initialRoom))

    def getDimension(self):
        return (self.x0, self.y0, self.x1, self.y1)

    # setExit, getExit and getAvailableDirNames are inspired by the text adventure
    # game in homework 4.
    def setExit(self, dirName, room):
        dirName = dirName.lower()
        self.exits[dirName] = room
    
    def getExit(self, dirName):
        if (dirName == None):
            return None
        else:
            dirName = dirName.lower()
            return self.exits.get(dirName, None)
    
    def getAvailableDirNamesAndRooms(self):
        availableDirections = [ ]
        for dirName in ['North', 'South', 'East', 'West', 'Up', 'Down']:
            if (self.getExit(dirName) != None):
                dirName = dirName.lower()
                availableDirections.append((dirName, self.getExit(dirName)))
        return availableDirections

# Not For MVP
class KeyPads(object):
    def __init__(self, x0, y0, x1, y1, doorRoom, doorDir, password):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.doorRoom = doorRoom
        self.doorDir = doorDir
        self.password = password
    
    def __repr__(self):
        return "A Keypad"
    
    def __hash__(self):
        return hash((self.doorDir, self.password))
    
    def __eq__(self, other):
        return (isinstance(other, KeyPads) and self.x0 == other.x0 and
                self.y0 == other.y0 and self.x1 == other.x1 and 
                self.y1 == other.y1 and self.doorRoom == other.doorRoom and 
                self.doorDir == other.doorDir and self.password == other.password)
    
    def getDimension(self):
        return (self.x0, self.y0, self.x1, self.y1)