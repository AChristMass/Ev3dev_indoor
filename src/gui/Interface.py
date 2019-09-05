import platform
from tkinter import *

from PIL import Image
from PIL import ImageTk

from gui.Chessboard import Chessboard
from gui.Map import Map
from gui.RobotWindow import RobotWindow


class Interface:
    step = 100

    def __init__(self, database, currentRobot):
        self.database = database
        self.screen = Tk()
        self.width = self.screen.winfo_screenwidth()
        self.height = self.screen.winfo_screenheight()
        if platform.system() == 'Darwin':
            self.screen.tk.call("::tk::unsupported::MacWindowStyle", "style", self.screen._w, "plain", "none")
        self.screen.attributes('-fullscreen', True)
        self.screen.title("RobotManager")

        self.currentRobot = currentRobot
        self.button_map = {}
        self.frame_map = self.load_frame_map()
        self.label_msg = Label(self.frame_map["second_box"], text="Select a Robot").pack()
        self.canvas = Canvas(self.frame_map["maps"])
        self.canvas.pack(fill=BOTH, expand=True)
        self.entry_box = Entry(self.frame_map["fifth_box"], width=5)
        self.image_map = self.load_image()

        self.origin_x = 0
        self.origin_y = 0

        self.robot_point = None
        self.position_flag = False
        self.chessboard_flag = False
        self.selected_box = None
        self.zoom = 1

        self.mapMat = self.load_map()
        self.chessboard = Chessboard(self.canvas, self.zoom, self.mapMat.x, self.mapMat.y, self.database, self)

        self.fingerPrintList = self.database.get_fp_list()
        self.is_finger_print_visible = False

        self.fp_draw_list = []
        self.create_interface()

    def set_button_map(self, button_map):
        self.button_map = button_map

    def load_frame_map(self):
        frame_map = {
            "maps": Frame(self.screen, width=self.width, height=self.height * 11 / 12, borderwidth=0, relief="solid"),
            "menu": Frame(self.screen, height=self.height * (1 / 12), borderwidth=2, relief="solid")
        }
        frame_map["first_box"] = Frame(frame_map["menu"], width=self.width * 1 / 5, borderwidth=1, relief="solid")
        frame_map["second_box"] = Frame(frame_map["menu"], width=self.width * 1 / 5, borderwidth=1, relief="solid")
        frame_map["third_box"] = Frame(frame_map["menu"], width=self.width * 1 / 5, borderwidth=1, relief="solid")
        frame_map["fourth_box"] = Frame(frame_map["menu"], width=self.width * 1 / 5, borderwidth=1, relief="solid")
        frame_map["fifth_box"] = Frame(frame_map["menu"], width=self.width * 1 / 5, borderwidth=1, relief="solid")
        return frame_map

    @staticmethod
    def load_image():
        return {"add": ImageTk.PhotoImage(Image.open('../asset/add.png')),
                     "remove": ImageTk.PhotoImage(Image.open('../asset/remove.png')),
                     "robot": ImageTk.PhotoImage(Image.open('../asset/robot.png')),
                     "eye": ImageTk.PhotoImage(Image.open('../asset/eye.png')),
                     "list": ImageTk.PhotoImage(Image.open('../asset/list.png')),
                     "grid": ImageTk.PhotoImage(Image.open('../asset/grid.png')),
                     "location": ImageTk.PhotoImage(Image.open('../asset/location.png')),
                     "move": ImageTk.PhotoImage(Image.open('../asset/move.png')),
                     "zoomup": ImageTk.PhotoImage(Image.open('../asset/zoomup.png')),
                     "zoomdown": ImageTk.PhotoImage(Image.open('../asset/zoomdown.png')),
                     "radar": ImageTk.PhotoImage(Image.open('../asset/radar.png'))
                     }

    def hide_show_chessboard(self):
        if self.chessboard_flag is False:
            self.chessboard_flag = True
            self.chessboard.draw_boxes()
        else:
            self.chessboard_flag = False
            self.draw_map()

    def set_up_frame(self):
        self.frame_map["maps"].pack(expand=False, fill="both", padx=0, pady=0)
        self.frame_map["menu"].pack(expand=True, fill="both", padx=0, pady=0)

        self.frame_map["first_box"].pack(side="left", expand=True, fill="both")
        self.frame_map["second_box"].pack(side="left", expand=True, fill="both")
        self.frame_map["third_box"].pack(side="left", expand=True, fill="both")
        self.frame_map["fourth_box"].pack(side="left", expand=True, fill="both")
        self.frame_map["fifth_box"].pack(side="left", expand=True, fill="both")

        self.frame_map["maps"].propagate(0)
        self.frame_map["first_box"].propagate(0)
        self.frame_map["second_box"].propagate(0)
        self.frame_map["third_box"].propagate(0)
        self.frame_map["fourth_box"].propagate(0)
        self.frame_map["fifth_box"].propagate(0)

    def get_robot_position(self):
        if self.currentRobot is None:
            return
        self.currentRobot.askScanForPosition()

    def change_step(self):
        n = int(self.entry_box.get())
        self.screen.focus_force()
        if 0 < n < 200:
            Interface.step = n
        else:
            self.entry_box.delete(0, END)
            self.entry_box.insert(0, str(Interface.step))

    def add_robot(self):
        return

    def scan_request(self):
        if self.currentRobot is None:
            return
        self.fingerPrintList.append((self.currentRobot.x, self.currentRobot.y))
        self.currentRobot.askScan()

    def show_finger_print(self):
        if self.is_finger_print_visible:
            self.is_finger_print_visible = False
            self.button_map["show_fp"]["borderwidth"] = 1
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
            self.button_map["show_fp"]["borderwidth"] = 2

    def move_right(self):
        self.canvas.move("all", -Interface.step, 0)
        self.origin_x -= -Interface.step
        self.chessboard.originx = self.origin_x

    def move_left(self):
        self.canvas.move("all", Interface.step, 0)
        self.origin_x -= Interface.step
        self.chessboard.originx = self.origin_x

    def move_up(self):
        self.canvas.move("all", 0, Interface.step)
        self.origin_y -= Interface.step
        self.chessboard.originy = self.origin_y

    def move_down(self):
        self.canvas.move("all", 0, -Interface.step)
        self.origin_y -= -Interface.step
        self.chessboard.originy = self.origin_y

    def zoom_up(self):
        self.origin_x, self.origin_y = 0, 0
        self.chessboard.originx, self.chessboard.originy = 0, 0
        if self.zoom != 8:
            self.zoom += 1
            self.chessboard.zoom += 1
        self.draw_map()

    def zoom_down(self):
        self.origin_x, self.origin_y = 0, 0
        self.chessboard.originx, self.chessboard.originy = 0, 0
        if self.zoom != 1:
            self.zoom -= 1
            self.chessboard.zoom -= 1
        self.draw_map()

    def on_click(self):
        if self.position_flag:
            x, y = self.screen.winfo_pointerxy()
            if y > self.height * 11 / 12:
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
            self.currentRobot.area = self.chessboard.get_box(x,y).area
            self.button_map["set_position"]["borderwidth"] = 1
            self.draw_map()
            return
        if self.chessboard_flag is not False:
            x, y = self.screen.winfo_pointerxy()
            self.chessboard.select_box(x, y)
            self.selected_box = self.chessboard.selected_box

    def create_interface(self):
        Label(self.frame_map["first_box"], text="Robots").pack()
        Label(self.frame_map["third_box"], text="Fingerprint").pack()
        Label(self.frame_map["fourth_box"], text="Chessboard").pack()
        Label(self.frame_map["fifth_box"], text="Tools").pack()
        self.entry_box.pack(side='left')
        self.entry_box.delete(0, END)
        self.entry_box.insert(0, str(Interface.step))
        self.set_up_frame()
        self.draw_map()

    def set_robot(self):
        RobotWindow(self, self.screen)

    @staticmethod
    def load_map():
        m = Map("file.txt")
        return m

    def set_position(self):
        if self.position_flag:
            self.position_flag = False
            self.button_map["set_position"]["borderwidth"] = 1
        else:
            self.position_flag = True
            self.button_map["set_position"]["borderwidth"] = 2

    def draw_map(self):
        self.canvas.delete("all")
        print("origin : ", self.origin_x, self.origin_y)
        largeur = self.width
        hauteur = int(self.height * (11 / 12))
        self.canvas.create_rectangle(0 - self.origin_x, 0 - self.origin_y, self.mapMat.x * self.zoom - self.origin_x,
                                     self.mapMat.y * self.zoom - self.origin_y, outline="white", fill="white")
        for i in range(self.mapMat.y):
            numb = 0
            last = self.mapMat.map[i][0]
            for j in range(self.mapMat.x):
                if last == self.mapMat.map[i][j]:
                    numb += 1
                else:
                    if last == "X":
                        self.canvas.create_rectangle((j - (numb - 1)) * self.zoom - self.origin_x, i * self.zoom - self.origin_y, (j + 1) * self.zoom - self.origin_x,
                                                     i * self.zoom + self.zoom - self.origin_y, outline="black", fill="black")
                        last = "."
                    else:
                        last = "X"
                    numb = 1
        if self.currentRobot is not None:
            self.robot_point = self.canvas.create_rectangle(self.currentRobot.x * self.zoom - self.origin_x,
                                                            self.currentRobot.y * self.zoom - self.origin_y,
                                                            (self.currentRobot.x + 1) * self.zoom - self.origin_x,
                                                            (self.currentRobot.y + 1) * self.zoom - self.origin_y,
                                                            outline="red", fill="red")
            self.canvas.move("all", -self.currentRobot.x * self.zoom + largeur / 2,
                             -self.currentRobot.y * self.zoom + hauteur / 2)
            self.origin_x -= -self.currentRobot.x * self.zoom + largeur / 2
            self.origin_y -= -self.currentRobot.y * self.zoom + hauteur / 2
        if self.fp_draw_list:
            for pos in self.fingerPrintList:
                self.fp_draw_list.append(
                    self.canvas.create_rectangle(pos[0] * self.zoom + self.origin_x, pos[1] * self.zoom + self.origin_y, (pos[0] + 1)
                                                 * self.zoom + self.origin_x, (pos[1] + 1) * self.zoom + self.origin_y, outline="blue", fill="blue"))
        if self.chessboard_flag:
            self.chessboard.draw_boxes()
        if self.is_finger_print_visible:
            for pos in self.fingerPrintList:
                self.fp_draw_list.append(
                    self.canvas.create_rectangle((-self.origin_x / self.zoom + pos[0]) * self.zoom,
                                                 (-self.origin_y / self.zoom + pos[1]) * self.zoom,
                                                 (-self.origin_x / self.zoom + pos[0] + 1)
                                                 * self.zoom, (-self.origin_y / self.zoom + pos[1] + 1) * self.zoom,
                                                 outline="blue",
                                                 fill="blue"))


