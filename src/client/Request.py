from enum import *

"""This class is used to interpret packet received, it store in 
a map functions whih can be accessed with an opcode as a key."""


class Request:
    State = Enum("State", "DONE REFILL ERROR")

    def __init__(self):
        self.map = dict()
        self.opcode = -1

    """Register a new function with an opcode as key in @self.map"""

    def register(self, opcode, func):
        self.map[opcode] = func

    """Remove a function given by the key 'opcode' in @self.map"""

    def remove(self, opcode):
        if opcode in self.map:
            del self.map[opcode]

    """Call the matching function according to the current opcode"""

    def run(self, request):
        self.map[self.opcode](request)

    """Split @request to get the opcode and call the matching function"""

    def process(self, request):
        try:
            self.opcode = int(request[0])
            self.run(request)
            return self.State.DONE
        except KeyError:
            return self.State.ERROR
