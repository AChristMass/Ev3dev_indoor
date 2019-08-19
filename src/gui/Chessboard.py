from gui.Area import Area
from gui.Box import Box


class Chessboard:
    def __init__(self, width, height, canvas, zoom, originx, originy):
        self.width = width
        self.height = height
        self.boxes = list()
        self.areas_list = list()
        self.canvas = canvas
        self.areas = 100
        self.zoom = zoom
        self.selected_box = None
        self.selected_area = None
        self.originx = originx
        self.originy = originy
        xpas = width / self.areas
        ypas = height / self.areas
        for i in range(0, self.areas):
            for j in range(0, self.areas):
                self.boxes.append(Box(xpas * i, ypas * j, xpas * i + xpas, ypas * j + ypas, canvas))

    def draw_boxes(self):
        for i in self.boxes:
            i.draw_box(self.zoom, self.originx, self.originy)

    def get_box(self, x, y):
        box_height = (self.height / self.areas) * self.zoom
        box_width = (self.width / self.areas) * self.zoom

        cols = int(y / box_height)
        rows = int(x / box_width)

        box_number = rows * self.areas + cols

        return self.boxes[box_number]

    def select_box(self, x, y):
        print(self.originx)
        print (self.originy)
        print ("________")
        if self.selected_box:
            self.selected_box.draw_box(self.zoom, self.originx, self.originy)
        if self.selected_area is not None:
            self.areas_list[self.selected_area].undraw_boxes(self.zoom)

        box_height = (self.height / self.areas) * self.zoom
        box_width = (self.width / self.areas) * self.zoom

        cols = int(y / box_height)
        rows = int(x / box_width)

        box_number = rows * self.areas + cols

        box = self.boxes[box_number]
        self.selected_box = box
        box.draw_box_red(self.zoom, self.originx, self.originy)

        area = box.get_area()

        if area is not None:
            self.areas_list[area].draw_boxes(self.zoom)
            self.selected_area = box.get_area()

    def create_area(self):
        area = Area()

        box = self.selected_box
        if box.get_area() is not None:
            return

        area.add_box(box)
        area.id = len(self.areas_list)
        box.asign_area(area.id)

        self.areas_list.append(area)

        area.draw_boxes(self.zoom)
        self.selected_area = area.id

    def select_area(self, x, y):
        box = self.selected_box(x, y)
        return box.get_area()

    def add_box_to_area(self):
        box = self.selected_box

        if box.get_area() is not None:
            return
        box.asign_area(self.selected_area)
        self.areas_list[self.selected_area].add_box(box)
        self.areas_list[self.selected_area].draw_boxes(self.zoom)
