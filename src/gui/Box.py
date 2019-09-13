class Box:
    '''Box represent a box on the map'''
    def __init__(self, x1, y1, x2, y2, canvas, chess):
        self.area = None
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        self.chess = chess
        self.canvas = canvas

    def draw_box(self, zoom, originx, originy, color):
        '''draw the box on the map via the canvas (@self.canvas)'''
        self.canvas.create_rectangle(self.x1 * zoom - originx,
                                     self.y1 * zoom - originy,
                                     self.x2 * zoom - originx,
                                     self.y2 * zoom - originy,
                                     outline=color, fill="")

    def asign_area(self, area):
        '''assign a new Area to @self.area'''
        self.area = area

    def get_area(self):
        '''return the current area'''
        return self.area
