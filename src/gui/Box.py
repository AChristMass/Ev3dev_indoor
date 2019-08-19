class Box:
    def __init__(self, x1, y1, x2, y2, canvas):
        self.area = None
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

        self.canvas = canvas

    def draw_box(self, zoom):
        self.canvas.create_rectangle(self.x1 * zoom,
                                     self.y1 * zoom,
                                     self.x2 * zoom,
                                     self.y2 * zoom,
                                     outline="blue", fill="")

    def draw_box_red(self, zoom):
        self.canvas.create_rectangle(self.x1 * zoom,
                                     self.y1 * zoom,
                                     self.x2 * zoom,
                                     self.y2 * zoom,
                                     outline="red", fill="")

    def draw_box_area(self, zoom):
        self.canvas.create_rectangle(self.x1 * zoom,
                                     self.y1 * zoom,
                                     self.x2 * zoom,
                                     self.y2 * zoom,
                                     outline="green", fill="")

    def asign_area(self, area):
        self.area = area

    def get_area(self):
        return self.area
