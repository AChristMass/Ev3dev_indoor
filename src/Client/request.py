from enum import *

class Request :
    State = Enum("State", "DONE REFILL ERROR")
    def __init__(self) :
        self.map = dict()
        self.opcode = -1

    def register(self, opcode, func):
        self.map[opcode] = func

    def remove(self, opcode) :
        if opcode in self.map:
            del self.map[opcode]

    #Call the matching function according to the current opcode
    def run(self, request) :
        self.map[self.opcode](request)

    def process(self, request) :
        try :
            self.opcode = int(request[0])
            self.run(request)
            return self.State.DONE
        except KeyError :
            return self.State.ERROR
        
            
            
    


