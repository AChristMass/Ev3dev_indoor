from gui.Area import Area
from gui.Box import Box


class Chessboard:
    area_id = 0

    def __init__(self, canvas, zoom, width, height, database, interface):
        self.width = width
        self.height = height
        self.canvas = canvas
        self.zoom = zoom
        self.database = database
        self.xpas = 10
        self.ypas = 5
        self.areas_list = self.load_area_list()
        self.boxes = []
        self.load_id_on_connect()
        self.selected_box = None
        self.selected_area = None
        self.area_flag = False
        self.interface = interface

        self.originx = 0
        self.originy = 0
        for i in range(0, int(self.width / self.xpas)):
            for j in range(0, int(self.height / self.ypas)):
                self.boxes.append(
                    Box(self.xpas * i, self.ypas * j, self.xpas * i + self.xpas, self.ypas * j + self.ypas, canvas,
                        self))
        self.load_cases_list()

    def draw_specified_area(self, id):
        temp = None
        for area in self.areas_list:
            if area.id == id:
                temp = area
        temp.draw_specific_area(self.zoom, self.originx, self.originy)

    def draw_boxes(self):
        for i in self.boxes:
            i.draw_box(self.zoom, self.originx, self.originy)

    def show_hide_area(self):
        if self.area_flag is False:
            self.area_flag = True
            for area in self.areas_list:
                self.areas_list[area].draw_area(self.zoom, self.originx, self.originy)
                self.areas_list[area].draw_boxes(self.zoom, self.originx, self.originy)

        else:
            self.area_flag = False
            if not self.interface.chessboard_flag:
                self.interface.draw_map()
                return
            for area in self.areas_list:
                self.areas_list[area].undraw_boxes(self.zoom, self.originx, self.originy)

    def clear_areas(self):
        for area in self.areas_list:
            self.areas_list[area].clear_area()
            self.areas_list[area].undraw_boxes(self.zoom, self.originx, self.originy)
        self.selected_area = None
        self.areas_list = {}

    def draw_all_area(self):
        for area in self.areas_list:
            self.areas_list[area].draw_area(self.zoom, self.originx, self.originy)

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
        if box is None:
            return

        if box.get_area() is not None:
            return

        area.add_box(box)
        box.asign_area(Chessboard.area_id)
        self.areas_list[Chessboard.area_id] = area
        area.draw_boxes(self.zoom, self.originx, self.originy)

        coord_x, coord_y = self.get_box_coord()
        self.database.add_new_box(coord_x, coord_y, Chessboard.area_id)
        self.selected_area = Chessboard.area_id
        Chessboard.area_id += 1

    def select_area(self, x, y):
        box = self.selected_box(x, y)
        return box.get_area()

    def add_box_to_area(self):
        box = self.selected_box
        if self.selected_area is None:
            return

        if box.get_area() is not None:
            return
        box.asign_area(self.selected_area)
        self.areas_list[self.selected_area].add_box(box)

        self.areas_list[self.selected_area].draw_boxes(self.zoom, self.originx, self.originy)

        coord_x, coord_y = self.get_box_coord()
        self.database.add_new_box(coord_x, coord_y, self.selected_area)

    def remove_box_from_area(self):
        box = self.selected_box

        if box.get_area() is None:
            return
        box.asign_area(None)

        self.areas_list[self.selected_area].remove_box(box)
        box.draw_box(self.zoom, self.originx, self.originy)
        self.areas_list[self.selected_area].draw_boxes(self.zoom, self.originx, self.originy)
        coord_x, coord_y = self.get_box_coord()
        self.database.delete_area_from_case(coord_x, coord_y)

    def get_box_coord(self):
        rows = int(self.selected_box.x1/self.xpas)
        cols = int(self.selected_box.y1/self.ypas)
        return rows, cols

    def get_box_coord_with_coord(self,x,y):
        rows = int(x/self.xpas)
        cols = int(y/self.ypas)
        return rows, cols

    def load_id_on_connect(self):
        Chessboard.area_id = self.database.load_id_area()
        if Chessboard.area_id is None:
            Chessboard.area_id = 0
        else:
            Chessboard.area_id = Chessboard.area_id + 1

    def load_cases_list(self):
        cmd = self.database.load_cases()
        for i in cmd:
            nb_cols = int(self.height / self.ypas)
            box = self.boxes[i[0] * nb_cols + i[1]]
            if i[2] != -1:
                box.asign_area(i[2])
                self.areas_list[i[2]].add_box(box)

    def load_area_list(self):
        lst = self.database.load_areas()
        dico = {}
        for l in lst:
            a = Area(self.canvas)
            dico[int(l)] = a
        return dico



