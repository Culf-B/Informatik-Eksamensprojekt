class SharedObjectEventHandler:
    '''
    A class for handling events for shared objects
    '''
    def __init__(self, nondefaultEvents = []):
        self.eventDict = {}
        self.defaultEvents = [
            "sharedObjectCreated",
            "sharedObjectLocked",
            "SharedObjectUnlocked"
        ]
        for event in self.defaultEvents:
            self.addEventType(event)
        for event in nondefaultEvents:
            self.addEventType(event)

    def addEventType(self, name):
        if name in self.eventDict.keys():
            print(f'Event with name "{name}" already exists and will not be overwritten.')
        else:
            # Eventdict has name as a key that points to an array containing functions listening for that event
            self.eventDict[name] = []
    
    def addEventListener(self, eventName, listenerFunction):
        if not eventName in self.eventDict.keys():
            print(f'Event with name "{eventName}", does not exist. Creating it anyway.')
            self.addEventType(eventName)

        self.eventDict[eventName].append(listenerFunction)

    def throwEvent(self, eventName, *args, **kwargs):
        if eventName in self.eventDict.keys():
            for listener in self.eventDict[eventName]:
                listener(args, kwargs) # Arguments can vary depending on eventtype, see documentation on thrower
        else:
            print(f'Event with name "{eventName}", does not exist.')

class SharedObject:
    '''
    Baseplate for object meant to be shared between multiple clients and a server over network

    Lock function locks the object so only the client who locked it can change it.
    Unlock function unlocks the object and makes it available to all clients again.

    To reduce chances conflicts, an object should only be edited when locked.
    This should be enforced by the server.

    A conversation between a client and server could look like this:
    Client 1: Lock object
    Server to all clients: Object is locked by client 1
    Client 1: Edits object
    Server to client 1: Okay, updates object
    Client 1: Unlock object
    Server to all clients: Here is updated version of object, now unlocked

    Events and arguments
    __init__ throws a sharedObjectCreated event with args: id = int
    lock throws a sharedObjectLocked event with args: id = int, lockedBy = any (probably gonna be string or an object)
    unlock throws a sharedObjectUnlocked event with args: id = int
    '''
    def __init__(self, objectId, eventHandler):
        self.id = objectId
        self.locked = False
        self.currentlyLockedBy = None
        self.eventHandler = eventHandler

        self.eventHandler.throwEvent("sharedObjectCreated", id = self.id)

    def lock(self, lockedBy):
        self.locked = True
        self.currentlyLockedBy = lockedBy

        self.eventHandler.throwEvent("sharedObjectLocked", id = self.id, lockedBy = self.currentlyLockedBy)

    def unlock(self):
        self.locked = False
        self.currentlyLockedBy = None

        self.eventHandler.throwEvent("SharedObjectUnlocked", id = self.id)

    def isLocked(self):
        return self.locked

    