from gui.Area import Area
from gui.Box import Box


class Chessboard:
    def __init__(self, canvas, zoom, width, height):
        self.width = width
        self.height = height
        self.boxes = list()
        self.areas_list = list()
        self.canvas = canvas
        self.zoom = zoom
        self.selected_box = None
        self.selected_area = None
        self.area_flag = False
        self.xpas = 10
        self.ypas = 5

        self.originx = 0
        self.originy = 0
        for i in range(0, int(self.width / self.xpas)):
            for j in range(0, int(self.height / self.ypas)):
                self.boxes.append(
                    Box(self.xpas * i, self.ypas * j, self.xpas * i + self.xpas, self.ypas * j + self.ypas, canvas,
                        self))

    def draw_boxes(self):
        for i in self.boxes:
            i.draw_box(self.zoom, self.originx, self.originy)

    def show_hide_area(self):
        if self.area_flag is False:
            self.area_flag = True
            for area in self.areas_list:
                area.draw_area(self.zoom, self.originx, self.originy)
        else:
            self.area_flag = False
            for area in self.areas_list:
                area.undraw_boxes(self.zoom, self.originx, self.originy)

    def clear_areas(self):
        print("clear area")
        for i in self.areas_list:
            i.clear_area()
            i.undraw_boxes(self.zoom, self.originx, self.originy)
        self.selected_area = None
        self.areas_list = list()

    def draw_all_area(self):
        for area in self.areas_list:
            area.draw_area(self.zoom, self.originx, self.originy)

    def get_box(self, x, y):
        nb_cols = int(self.height / self.ypas)

        cols = int((y / self.ypas) / self.zoom)
        rows = int((x / self.xpas) / self.zoom)

        box_number = int(rows * nb_cols + cols)

        return self.boxes[box_number]

    def select_box(self, x, y):
        ox = x + self.originx
        oy = y + self.originy

        x += self.originx % (self.zoom * self.xpas)
        y += self.originy % (self.zoom * self.ypas)

        if self.selected_box and self.selected_box.get_area() is None:
            self.selected_box.draw_box(self.zoom, self.originx, self.originy)
        if self.selected_area is not None and self.area_flag is False:
            self.areas_list[self.selected_area].undraw_boxes(self.zoom, self.originx, self.originy)

        nb_cols = int(self.height / self.ypas)

        cols = int((oy / self.ypas) / self.zoom)
        rows = int((ox / self.xpas) / self.zoom)
        box_number = int(rows * nb_cols + cols)

        box = self.boxes[box_number]
        self.selected_box = box
        box.draw_box_red(self.zoom, self.originx, self.originy)

        area = box.get_area()


        if area is not None:
            self.areas_list[area].draw_boxes(self.zoom, self.originx, self.originy)
            self.selected_area = box.get_area()

    def create_area(self):
        area = Area(self.canvas)

        box = self.selected_box
        if box.get_area() is not None:
            return

        area.add_box(box)
        area.id = len(self.areas_list)
        box.asign_area(area.id)

        self.areas_list.append(area)

        area.draw_boxes(self.zoom, self.originx, self.originy)

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

        self.areas_list[self.selected_area].draw_boxes(self.zoom, self.originx, self.originy)

    def remove_box_from_area(self):
        box = self.selected_box

        if box.get_area() is None:
            return
        box.asign_area(None)

        self.areas_list[self.selected_area].remove_box(box)

        box.draw_box(self.zoom, self.originx, self.originy)

        self.areas_list[self.selected_area].draw_boxes(self.zoom, self.originx, self.originy)
