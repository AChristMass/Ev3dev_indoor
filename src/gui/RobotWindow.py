from tkinter import *


class RobotWindow(Toplevel):
    def __init__(self, mother, root):
        Toplevel.__init__(self, root)
        self.geometry("600x400")
        self.mother = mother
        self.frame = Frame(self)
        self.box = Listbox(self)
        self.box.pack(fill="both", expand=YES)
        b = Button(self, text="Ok", command=self.print_robot, width=20)
        u = Button(self, text="Unselect", command=self.unselect, width=20)
        self.bind('<Escape>', lambda e: self.destroy())

        for i in range(len(self.mother.robotList)):
            self.box.insert(i, self.mother.robotList[i])

        self.box.pack()
        u.pack(padx=1, pady=1, side='left')
        b.pack(padx=1, pady=1, side='right')
        if not self.mother.robotList:
            b.configure(state=DISABLED)
            u.configure(state=DISABLED)
        self.frame.pack()

    def unselect(self):
        self.mother.label_msg.config(text="Select a Robot")
        self.mother.currentRobot = None
        self.mother.canvas.delete("all")
        self.mother.draw_map()
        for b in self.mother.button_current_robot:
            b.configure(state=DISABLED)
        self.destroy()

    def print_robot(self):
        ind = self.box.curselection()[0]
        self.mother.currentRobot = self.mother.robotList[ind]
        self.mother.currentRobot.xc, self.mother.currentRobot.yc = self.mother.chessboard.get_box_coord_with_coord(self.mother.currentRobot.x,
                                                                                            self.mother.currentRobot.y)
        self.mother.label_msg.config(text=self.mother.currentRobot.name)
        for b in self.mother.button_current_robot:
            b.configure(state=ACTIVE)
        self.mother.canvas.delete("all")
        self.mother.draw_map()
        self.destroy()
