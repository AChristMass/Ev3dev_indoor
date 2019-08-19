class Area:
    def __init__(self):
        self.boxes = list()
        self.id = None

    def add_box(self, box):
        self.boxes.append(box)

    def remove_box(self, box):
        self.boxes.remove(box)

    def draw_boxes(self, zoom):
        for i in self.boxes:
            i.draw_box_area(zoom)

    def undraw_boxes(self, zoom):
        for i in self.boxes:
            i.draw_box(zoom)
