from tkinter import *
from GUI.RobotWindow import RobotWindow
from Server.server import Server
from GUI.Map import Map
import platform


class Interface:
    def __init__(self):
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
        self.screen.bind("<Left>", lambda e: self.move_left())
        self.screen.bind("<Up>", lambda e: self.move_up())
        self.screen.bind("<Right>", lambda e:  self.move_right())
        self.screen.bind("<Down>", lambda e: self.move_down())
        self.screen.bind("<p>", lambda e: self.zoom_up())
        self.screen.bind("<m>", lambda e: self.zoom_down())
        self.screen.bind("<1>", lambda e: self.on_click())

        self.origin_x = 0
        self.origin_y = 0

        self.robot_point = None
        self.position_flag = False
        self.zoom = 1

        self.mapMat = self.load_map()

        self.button_list = []
        self.currentRobot = None
        self.robotList = Server.logged

    def set_up_lines(self):
        self.maps.pack(expand=False, fill="both", padx=0, pady=0)
        self.menu.pack(expand=True, fill="both", padx=0, pady=0)
        self.left_box.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.right_box.pack(side="right", expand=True, fill="both", padx=5, pady=5)
        self.maps.propagate(0)
        self.left_box.propagate(0)

    def set_up_buttons(self):
        Button(self.right_box, text='Add Robot', command=self.screen.destroy, height=2, width=100).pack(padx=1, pady=1)
        Button(self.right_box, text='Select Robot', command=self.set_robot, height=2, width=100).pack(padx=1, pady=1)
        self.button_list = [
            Button(self.left_box, text='FingerPrint List', command=self.screen.destroy, height=10, width=25,
                   state=DISABLED),
            Button(self.left_box, text='Add FingerPrint', command=self.scanDemand, height=10, width=25,
                   state=DISABLED),
            Button(self.left_box, text='Set Position', command=self.set_position, height=10, width=25,
                   state=DISABLED),
            Button(self.left_box, text='Move', command=self.screen.destroy, height=10, width=25, state=DISABLED),
        ]
        for b in self.button_list:
            b.pack(padx=1, pady=1, side='left')
    
    def scanDemand(self) :
        if self.currentRobot is None :
            return
        else :
            self.currentRobot.askScan()

    def move_right(self):
        self.canvas.move("all", -20, 0)
        self.origin_x -= (-20)

    def move_left(self):
        self.canvas.move("all", 20, 0)
        self.origin_x -= 20

    def move_up(self):
        self.canvas.move("all", 0, 20)
        self.origin_y -= 20

    def move_down(self):
        self.canvas.move("all", 0, -20)
        self.origin_y -= (-20)

    def zoom_up(self):
        if self.zoom != 8:
            self.zoom += 1
        self.draw_map()

    def zoom_down(self):
        if self.zoom != 1:
            self.zoom -= 1
        self.draw_map()

    def on_click(self):
        if self.position_flag:
            x, y = self.screen.winfo_pointerxy()
            if y > self.height * 10/12:
                return
            x = int((x + self.origin_x)/self.zoom)
            y = int((y + self.origin_y)/self.zoom)
            if y >= self.mapMat.y or x >= self.mapMat.x:
                return
            if self.mapMat.map[y][x-1] == 'X':
                return
            self.position_flag = False
            self.currentRobot.x = x
            self.currentRobot.y = y
            self.button_list[2]["borderwidth"] = 1
            self.draw_map()

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
        self.canvas.pack(fill=BOTH, expand=True)


if __name__ == '__main__':
    inter = Interface()
    inter.create_interface()
