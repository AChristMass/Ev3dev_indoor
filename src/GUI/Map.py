class Map:
    def __init__(self, name):
        self.file = open("../map/"+name, "r")
        self.map = self.load_map(self.file)
        self.y = len(self.map)
        self.x = len(self.map[0])

    @staticmethod
    def load_map(file):
        t = file.readlines()
        maps = []
        for line in t:
            lst = []
            for letter in line:
                lst.append(letter)
            maps.append(lst)
        return maps
