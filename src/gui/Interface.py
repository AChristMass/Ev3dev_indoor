import platform
from tkinter import *

from PIL import Image
from PIL import ImageTk

from gui.Chessboard import Chessboard
from gui.Map import Map
from gui.RobotWindow import RobotWindow
from server.Server import Server


class Interface:
    step = 100

    def __init__(self, database):

        self.database = database
        self.screen = Tk()
        self.width = self.screen.winfo_screenwidth()
        self.height = self.screen.winfo_screenheight()

        if platform.system() == 'Darwin':
            self.screen.tk.call("::tk::unsupported::MacWindowStyle", "style", self.screen._w, "plain", "none")
        self.screen.attributes('-fullscreen', True)
        self.screen.title("RobotManager")

        self.maps = Frame(self.screen, width=self.width, height=self.height * 11 / 12, borderwidth=0, relief="solid")
        self.menu = Frame(self.screen, height=self.height * (1 / 12), borderwidth=2, relief="solid")

        self.first_box = Frame(self.menu, width=self.width * 1 / 5, borderwidth=1, relief="solid")
        self.second_box = Frame(self.menu, width=self.width * 1 / 5, borderwidth=1, relief="solid")
        self.third_box = Frame(self.menu, width=self.width * 1 / 5, borderwidth=1, relief="solid")
        self.fourth_box = Frame(self.menu, width=self.width * 1 / 5, borderwidth=1, relief="solid")
        self.fifth_box = Frame(self.menu, width=self.width * 1 / 5, borderwidth=1, relief="solid")
        self.label_msg = Label(self.second_box, text="Select a Robot").pack()
        self.canvas = Canvas(self.maps)
        self.entry_box = Entry(self.fifth_box, width=5)
        if not platform.system() == 'Darwin':
            self.add = PhotoImage(file='../asset/add.png')
            self.remove = PhotoImage(file='../asset/remove.png')
            self.robot = PhotoImage(file='../asset/robot.png')
            self.eye = PhotoImage(file='../asset/eye.png')
            self.list = PhotoImage(file='../asset/list.png')
            self.grid = PhotoImage(file='../asset/grid.png')
            self.location = PhotoImage(file='../asset/location.png')
            self.move = PhotoImage(file='../asset/move.png')
            self.zoomup = PhotoImage(file='../asset/zoomup.png')
            self.zoomdown = PhotoImage(file='../asset/zoomdown.png')
            self.radar = PhotoImage(file='../asset/radar.png')
        else:
            self.add = ImageTk.PhotoImage(Image.open('../asset/add.png'))
            self.remove = ImageTk.PhotoImage(Image.open('../asset/remove.png'))
            self.robot = ImageTk.PhotoImage(Image.open('../asset/robot.png'))
            self.eye = ImageTk.PhotoImage(Image.open('../asset/eye.png'))
            self.list = ImageTk.PhotoImage(Image.open('../asset/list.png'))
            self.grid = ImageTk.PhotoImage(Image.open('../asset/grid.png'))
            self.location = ImageTk.PhotoImage(Image.open('../asset/location.png'))
            self.move = ImageTk.PhotoImage(Image.open('../asset/move.png'))
            self.zoomup = ImageTk.PhotoImage(Image.open('../asset/zoomup.png'))
            self.zoomdown = ImageTk.PhotoImage(Image.open('../asset/zoomdown.png'))
            self.radar = ImageTk.PhotoImage(Image.open('../asset/radar.png'))

        self.binding()

        self.origin_x = 0
        self.origin_y = 0

        self.robot_point = None
        self.position_flag = False
        self.chessboard_flag = False
        self.selected_box = None
        self.zoom = 1

        self.currentRobot = None
        self.mapMat = self.load_map()
        self.chessboard = Chessboard(self.canvas, self.zoom, self.mapMat.x, self.mapMat.y, self.database, self)

        self.button_current_robot = []
        self.button_robots = []
        self.button_fingerprint = []
        self.button_chessboard = []
        self.button_tools = []
        self.robotList = Server.logged

        self.fingerPrintList = self.database.get_fp_list()
        self.is_finger_print_visible = False

        self.fp_draw_list = []
        self.create_interface()
        self.screen.mainloop()

    def binding(self):
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
        self.screen.bind("<z>", lambda e: self.chessboard.add_box_to_area())
        self.screen.bind("<e>", lambda e: self.chessboard.remove_box_from_area())
        self.screen.bind("<h>", lambda e: self.hide_show_chassboard())
        self.screen.bind("<r>", lambda e: self.chessboard.clear_areas())
        self.screen.bind("<q>", lambda e: self.chessboard.show_hide_area())

    def nothing(self):
        return

    def hide_show_chassboard(self):
        self.database.show_cases()
        if self.chessboard_flag is False:
            self.chessboard_flag = True
            self.chessboard.draw_boxes()
        else:
            self.chessboard_flag = False
            self.draw_map()

    def set_up_lines(self):
        self.maps.pack(expand=False, fill="both", padx=0, pady=0)
        self.menu.pack(expand=True, fill="both", padx=0, pady=0)

        self.first_box.pack(side="left", expand=True, fill="both")
        self.second_box.pack(side="left", expand=True, fill="both")
        self.third_box.pack(side="left", expand=True, fill="both")
        self.fourth_box.pack(side="left", expand=True, fill="both")
        self.fifth_box.pack(side="left", expand=True, fill="both")

        self.maps.propagate(0)
        self.first_box.propagate(0)
        self.second_box.propagate(0)
        self.third_box.propagate(0)
        self.fourth_box.propagate(0)
        self.fifth_box.propagate(0)

    def set_up_buttons(self):
        Label(self.first_box, text="Robots").pack()
        Label(self.third_box, text="Fingerprint").pack()
        Label(self.fourth_box, text="Chessboard").pack()
        Label(self.fifth_box, text="Tools").pack()

        self.button_robots = [
            Button(self.first_box, image=self.add, command=self.add_robot),
            Button(self.first_box, image=self.remove, command=self.screen.destroy),
            Button(self.first_box, image=self.robot, command=self.set_robot)
        ]
        for b in self.button_robots:
            b.pack(side="left", padx=1, pady=1)

        self.button_current_robot = [
            Button(self.second_box, image=self.location, command=self.set_position, state=DISABLED),
            Button(self.second_box, image=self.radar, command=self.get_robot_position, state=DISABLED),
            Button(self.second_box, image=self.move, command=self.nothing, state=DISABLED),
        ]
        for b in self.button_current_robot:
            b.pack(padx=1, pady=1, side='left')

        self.button_fingerprint = [
            Button(self.third_box, image=self.add, command=self.scan_request),
            Button(self.third_box, image=self.remove, command=self.nothing),
            Button(self.third_box, image=self.eye, command=self.show_finger_print),
            Button(self.third_box, image=self.list, command=self.nothing)
        ]
        for b in self.button_fingerprint:
            b.pack(side="left", padx=1, pady=1)

        self.button_chessboard = [
            Button(self.fourth_box, image=self.add, command=self.nothing),
            Button(self.fourth_box, image=self.remove, command=self.nothing),
            Button(self.fourth_box, image=self.grid, command=self.hide_show_chassboard),
            Button(self.fourth_box, image=self.eye, command=self.chessboard.show_hide_area)
        ]
        for b in self.button_chessboard:
            b.pack(side="left", padx=1, pady=1)

        self.button_tools = [
            Button(self.fifth_box, image=self.zoomup, command=self.__zoom_up),
            Button(self.fifth_box, image=self.zoomdown, command=self.__zoom_down),
        ]
        for b in self.button_tools:
            b.pack(side="left", padx=1, pady=1)

        Label(self.fifth_box, text="   Step ").pack(side='left')
        self.entry_box.pack(side='left')
        self.entry_box.delete(0, END)
        self.entry_box.insert(0, str(Interface.step))
        b = Button(self.fifth_box, text="Ok", command=self.change_step)
        b.pack(side='left')
        self.button_tools.append(b)

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
            self.button_fingerprint[2]["borderwidth"] = 1
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
            self.button_fingerprint[2]["borderwidth"] = 5

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
        self.chessboard.originy = self.origin_y

    def __move_down(self):
        self.canvas.move("all", 0, -Interface.step)
        self.origin_y -= -Interface.step
        self.chessboard.originy = self.origin_y

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
            self.button_list[2]["borderwidth"] = 1
            self.draw_map()
            return
        if self.chessboard_flag is not False:
            x, y = self.screen.winfo_pointerxy()
            self.chessboard.select_box(x, y)
            self.selected_box = self.chessboard.selected_box

    def create_interface(self):
        self.set_up_buttons()
        self.set_up_lines()
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
            self.button_list[2]["borderwidth"] = 1
        else:
            self.position_flag = True
            self.button_list[2]["borderwidth"] = 5

    def draw_map(self):
        self.origin_y = 0
        self.origin_x = 0
        self.chessboard.originx = 0
        self.chessboard.originy = 0
        self.canvas.delete("all")

        largeur = self.width
        hauteur = int(self.height * (11 / 12))
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
        if self.chessboard_flag is not False:
            self.chessboard.draw_boxes()
        self.canvas.pack(fill=BOTH, expand=True)
