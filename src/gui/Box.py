class Box:
  
    def __init__(self, x1, y1, x2, y2, canvas, chess):

        self.area = None
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

        self.chess = chess

        self.canvas = canvas

    def draw_box(self, zoom, originx, originy):
        restex = originx % (zoom * self.chess.xpas)
        restey = originy % (zoom * self.chess.ypas)
        self.canvas.create_rectangle(self.x1 * zoom - restex,
                                     self.y1 * zoom - restey,
                                     self.x2 * zoom - restex,
                                     self.y2 * zoom - restey,
                                     outline="blue", fill="")

    def draw_box_red(self, zoom, originx, originy):
        restex = originx % (zoom * self.chess.xpas)
        restey = originy % (zoom * self.chess.ypas)
        self.canvas.create_rectangle(self.x1 * zoom - restex,
                                     self.y1 * zoom - restey,
                                     self.x2 * zoom - restex,
                                     self.y2 * zoom - restey,
                                     outline="red", fill="")

    def draw_box_area(self, zoom, originx, originy):
        restex = originx % (zoom * self.chess.xpas)
        restey = originy % (zoom * self.chess.ypas)
        self.canvas.create_rectangle(self.x1 * zoom - restex,
                                     self.y1 * zoom - restey,
                                     self.x2 * zoom - restex,
                                     self.y2 * zoom - restey,
                                     outline="green", fill="")

    def asign_area(self, area):
        self.area = area

    def get_area(self):
        return self.area