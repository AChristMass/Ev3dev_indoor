class Area:
    def __init__(self, canvas):
        self.boxes = list()
        self.id = None
        self.points = set()
        self.segment = set()
        self.canvas = canvas

    def clear_area(self):
        for i in self.boxes:
            i.area = None
        self.boxes = list()

    def add_box(self, box):
        self.boxes.append(box)
        local_seg = set()

        local_seg.add(((box.x1, box.y1), (box.x2, box.y1)))
        local_seg.add(((box.x2, box.y1), (box.x2, box.y2)))
        local_seg.add(((box.x2, box.y2), (box.x1, box.y2)))
        local_seg.add(((box.x1, box.y2), (box.x1, box.y1)))

        for seg in local_seg:
            if seg in self.segment:
                self.segment.remove(seg)
            elif (seg[1], seg[0]) in self.segment:
                self.segment.remove((seg[1], seg[0]))
            else:
                self.segment.add(seg)

    def draw_area(self, zoom, originx, originy):
        for seg in self.segment:
            self.canvas.create_line(seg[0][0] * zoom - originx, seg[0][1] * zoom - originy,
                                    seg[1][0] * zoom - originx, seg[1][1] * zoom - originy, fill="red2")

    def remove_box(self, box):
        self.boxes.remove(box)

        local_seg = set()

        local_seg.add(((box.x1, box.y1), (box.x2, box.y1)))
        local_seg.add(((box.x2, box.y1), (box.x2, box.y2)))
        local_seg.add(((box.x2, box.y2), (box.x1, box.y2)))
        local_seg.add(((box.x1, box.y2), (box.x1, box.y1)))

        for seg in local_seg:
            if seg in self.segment:
                self.segment.remove(seg)
            elif (seg[1], seg[0]) in self.segment:
                self.segment.remove((seg[1], seg[0]))
            else:
                self.segment.add(seg)

    def draw_boxes(self, zoom, originx, originy):
        for i in self.boxes:
            i.draw_box_area(zoom, originx, originy)
        self.draw_area(zoom, originx, originy)

    def undraw_boxes(self, zoom, originx, originy):
        for i in self.boxes:
            i.draw_box(zoom, originx, originy)

    def valAbs(self, x):
        return -x if x < 0 else x
