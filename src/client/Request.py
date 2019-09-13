from enum import *


class Request:
    """This class is used to interpret packet received, it store in
    a map functions whih can be accessed with an opcode as a key."""
    State = Enum("State", "DONE REFILL ERROR")

    def __init__(self):
        self.map = dict()
        self.opcode = -1

    def register(self, opcode, func):
        """Register a new function with an opcode as key in @self.map"""
        self.map[opcode] = func

    def remove(self, opcode):
        """Remove a function given by the key 'opcode' in @self.map"""
        if opcode in self.map:
            del self.map[opcode]

    def run(self, request):
        """Call the matching function according to the current opcode"""
        self.map[self.opcode](request)

    def process(self, request):
        """Split @request to get the opcode and call the matching function"""
        try:
            self.opcode = int(request[0])
            self.run(request)
            return self.State.DONE
        except KeyError:
            return self.State.ERROR
