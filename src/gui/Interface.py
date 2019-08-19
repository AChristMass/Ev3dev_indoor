import platform
from tkinter import *

from gui.Chessboard import Chessboard
from gui.Area import Area
from gui.Map import Map
from gui.RobotWindow import RobotWindow
from server.Server import Server


class Interface:
    step = 20

    def __init__(self, database):

        self.database = database

        self.screen = Tk()
        self.width = self.screen.winfo_screenwidth()
        self.height = self.screen.winfo_screenheight()

        if platform.system() == 'Darwin':
            self.screen.tk.call("::tk::unsupported::MacWindowStyle", "style", self.screen._w, "plain", "none")
        self.screen.attributes('-fullscreen', True)
        self.screen.title("RobotManager")

        self.maps = Frame(self.screen, width=self.width, height=self.height * 10 / 12, borderwidth=0, relief="solid")
        self.menu = Frame(self.screen, height=self.height * (2 / 12), borderwidth=2, relief="solid")

        self.left_box = Frame(self.menu, width=self.width * 2 / 3, borderwidth=1, relief="solid")
        self.right_box = Frame(self.menu, borderwidth=1, relief="solid")
        self.label_msg = Label(self.left_box, text="Select a Robot")
        self.label_msg.pack()
        self.canvas = Canvas(self.maps)

        self.screen.bind('<Escape>', lambda e: self.screen.destroy())
        self.screen.bind("<Left>", lambda e: self.__move_left())
        self.screen.bind("<Up>", lambda e: self.__move_up())
        self.screen.bind("<Right>", lambda e: self.__move_right())
        self.screen.bind("<Down>", lambda e: self.__move_down())
        self.screen.bind("<space>", lambda e: self.show_finger_print())
        self.screen.bind("<p>", lambda e: self.__zoom_up())
        self.screen.bind("<m>", lambda e: self.__zoom_down())
        self.screen.bind("<1>", lambda e: self.__on_click())
        self.screen.bind("<4>", lambda e: self.__move_up())
        self.screen.bind("<5>", lambda e: self.__move_down())
        self.screen.bind("<t>", lambda e: self.currentRobot.askScanForPosition())
        self.screen.bind("<y>", lambda e: self.currentRobot.showScans())
        self.screen.bind("<d>", lambda e: self.currentRobot.askDistance())
        self.screen.bind("<a>", lambda e: self.chessboard.create_area())
        self.screen.bind("<z>", lambda e: self.add_box_to_area())


        self.origin_x = 0
        self.origin_y = 0

        self.robot_point = None
        self.position_flag = False
        self.selected_box = None
        self.zoom = 1
        self.chessboard = Chessboard(self.width, self.height, self.canvas, self.zoom, self.origin_x, self.origin_y)


        self.currentRobot = None
        self.mapMat = self.load_map()

        self.button_list = []
        self.robotList = Server.logged

        self.fingerPrintList = self.database.get_fp_list()
        self.is_finger_print_visible = False

        self.fp_draw_list = []

    def set_up_lines(self):
        self.maps.pack(expand=False, fill="both", padx=0, pady=0)
        self.menu.pack(expand=True, fill="both", padx=0, pady=0)

        self.left_box.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.right_box.pack(side="right", expand=True, fill="both", padx=5, pady=5)
        self.maps.propagate(0)
        self.left_box.propagate(0)

    def set_up_buttons(self):
        Button(self.right_box, text='Add Robot', command=self.add_robot, height=2, width=100).pack(padx=1, pady=1)
        Button(self.right_box, text='Select Robot', command=self.set_robot, height=2, width=100).pack(padx=1, pady=1)
        self.button_list = [
            Button(self.left_box, text='FingerPrint List', command=self.show_finger_print, height=10, width=25,
                   state=ACTIVE),
            Button(self.left_box, text='Add FingerPrint', command=self.scan_request, height=10, width=25,
                   state=DISABLED),
            Button(self.left_box, text='Set Position', command=self.set_position, height=10, width=25,
                   state=DISABLED),
            Button(self.left_box, text='Move', command=self.screen.destroy, height=10, width=25, state=DISABLED),
        ]
        for b in self.button_list:
            b.pack(padx=1, pady=1, side='left')

    def add_robot(self):
        return self

    def scan_request(self):
        if self.currentRobot is None:
            return
        self.fingerPrintList.append((self.currentRobot.x, self.currentRobot.y))
        self.currentRobot.askScan()

    def show_finger_print(self):
        if self.is_finger_print_visible:
            self.is_finger_print_visible = False
            self.button_list[0]["borderwidth"] = 1
            for i in self.fp_draw_list:
                self.canvas.delete(i)
        else:
            self.is_finger_print_visible = True
            for i in self.fp_draw_list:
                self.canvas.delete(i)
            self.fp_draw_list = []
            for pos in self.fingerPrintList:
                self.fp_draw_list.append(
                    self.canvas.create_rectangle((-self.origin_x / self.zoom + pos[0]) * self.zoom,
                                                 (-self.origin_y / self.zoom + pos[1]) * self.zoom,
                                                 (-self.origin_x / self.zoom + pos[0] + 1)
                                                 * self.zoom, (-self.origin_y / self.zoom + pos[1] + 1) * self.zoom,
                                                 outline="blue",
                                                 fill="blue"))
            self.button_list[0]["borderwidth"] = 5

    def __move_right(self):
        self.canvas.move("all", -Interface.step, 0)
        self.origin_x -= -Interface.step
        self.chessboard.originx = self.origin_x

    def __move_left(self):
        self.canvas.move("all", Interface.step, 0)
        self.origin_x -= Interface.step
        self.chessboard.originx = self.origin_x

    def __move_up(self):
        self.canvas.move("all", 0, Interface.step)
        self.origin_y -= Interface.step

    def __move_down(self):
        self.canvas.move("all", 0, -Interface.step)
        self.origin_y -= -Interface.step

    def __zoom_up(self):
        if self.zoom != 8:
            self.zoom += 1
            self.chessboard.zoom += 1
        self.draw_map()

    def __zoom_down(self):
        if self.zoom != 1:
            self.zoom -= 1
            self.chessboard.zoom -= 1
        self.draw_map()

    def __on_click(self):


        if self.position_flag:
            x, y = self.screen.winfo_pointerxy()
            if y > self.height * 10 / 12:
                return
            x = int((x + self.origin_x) / self.zoom)
            y = int((y + self.origin_y) / self.zoom)
            if y >= self.mapMat.y or x >= self.mapMat.x:
                return
            if self.mapMat.map[y][x - 1] == 'X':
                return
            self.position_flag = False
            self.currentRobot.x = x
            self.currentRobot.y = y
            self.button_list[2]["borderwidth"] = 1
            self.draw_map()
            return
        x, y = self.screen.winfo_pointerxy()
        x = int(x + self.origin_x)
        y = int(y + self.origin_y)

        #Those 2 next calls have to be made in that order
        #cause the field selected_box of chessboard
        #is updated in the function "select_box"
        self.chessboard.select_box(x, y)
        self.selected_box = self.chessboard.selected_box


    def add_box_to_area(self):
        self.chessboard.add_box_to_area()


    def create_interface(self):
        self.set_up_lines()
        self.set_up_buttons()
        self.draw_map()
        self.screen.mainloop()

    def set_robot(self):
        RobotWindow(self, self.screen)

    @staticmethod
    def load_map():
        m = Map("file.txt")
        return m

    def set_position(self):
        if self.position_flag:
            self.position_flag = False
            self.button_list[2]["borderwidth"] = 1
        else:
            self.position_flag = True
            self.button_list[2]["borderwidth"] = 5

    def draw_map(self):
        self.origin_y = 0
        self.origin_x = 0
        self.canvas.delete("all")

        largeur = self.width
        hauteur = int(self.height * (10 / 12))
        self.canvas.create_rectangle(0, 0, self.mapMat.x * self.zoom,
                                     self.mapMat.y * self.zoom, outline="white", fill="white")
        for i in range(self.mapMat.y):
            numb = 0
            last = self.mapMat.map[i][0]
            for j in range(self.mapMat.x):
                if last == self.mapMat.map[i][j]:
                    numb += 1
                else:
                    if last == "X":
                        self.canvas.create_rectangle((j - (numb - 1)) * self.zoom, i * self.zoom, (j + 1) * self.zoom,
                                                     i * self.zoom + self.zoom, outline="black", fill="black")
                        last = "."
                    else:
                        last = "X"
                    numb = 1
        if self.currentRobot is not None:
            self.robot_point = self.canvas.create_rectangle(self.currentRobot.x * self.zoom,
                                                            self.currentRobot.y * self.zoom,
                                                            (self.currentRobot.x + 1) * self.zoom,
                                                            (self.currentRobot.y + 1) * self.zoom,
                                                            outline="red", fill="red")
            self.canvas.move("all", -self.currentRobot.x * self.zoom + largeur / 2,
                             -self.currentRobot.y * self.zoom + hauteur / 2)
            self.origin_x -= -self.currentRobot.x * self.zoom + largeur / 2
            self.origin_y -= -self.currentRobot.y * self.zoom + hauteur / 2
        if self.fp_draw_list:
            for pos in self.fingerPrintList:
                self.fp_draw_list.append(
                    self.canvas.create_rectangle(pos[0] * self.zoom, pos[1] * self.zoom, (pos[0] + 1)
                                                 * self.zoom, (pos[1] + 1) * self.zoom, outline="blue", fill="blue"))
        self.chessboard.draw_boxes()
        self.canvas.pack(fill=BOTH, expand=True)
