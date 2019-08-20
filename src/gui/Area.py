class Area:
    def __init__(self):
        self.boxes = list()
        self.id = None
        self.points = set()

    def clear_area(self):
        for i in self.boxes:
            i.area = None
        self.boxes = list()

    def add_box(self, box):
        self.boxes.append(box)
        points = list()

        points.append((box.x1, box.y1))
        points.append((box.x2, box.y1))
        points.append((box.x1, box.y2))
        points.append((box.x2, box.y2))

        pts = None
        for i in points:
            if i not in self.points:
                pts = i
                break
        #print("Point : ", pts)
        #print("Closest to point :", self.find_closest(pts))

    def find_closest(self, anchor):
        distance = 0
        closest = None
        for pts in self.points:
            if pts != anchor:
                closest = pts
                distance = valAbs(pts[0] - anchor[0]) + valAbs(pts[1] - anchor[1])
                print("distance 1", distance)
                break

        for pts in self.points:
            dist = valAbs(pts[0] - anchor[0]) + valAbs(pts[1] - anchor[1])
            if dist < distance:
                distance = dist
                print("distance 2", distance)
                closest = pts

        return closest

    def remove_box(self, box):
        self.boxes.remove(box)
        
    def draw_boxes(self, zoom, originx, originy):
        for i in self.boxes:
            i.draw_box_area(zoom, originx, originy)

    def undraw_boxes(self, zoom, originx, originy):
        for i in self.boxes:
            i.draw_box(zoom, originx, originy)

    # def find_contour(self, begin):

    def valAbs(self, x):
        return -x if x < 0 else x
