import threading
from tkinter import *
from database.Database import Database
from gui.Interface import Interface
from server.Server import Server


class Core:

    def __init__(self, host, port):
        self.database = Database()

        self.server = Server(host, port, self.database)
        t = threading.Thread(target=self.server.launch)
        t.daemon = True
        print("Launching server...")
        t.start()
        print("Launching GUI...")
        self.currentRobot = None
        self.interface = Interface(self.database, self.currentRobot)
        self.screen = self.interface.screen
        self.binding()
        self.button_map = self.set_up_buttons()
        self.interface.set_button_map(self.button_map)
        self.screen.mainloop()

    def binding(self):
        self.screen.bind('<Escape>', lambda e: self.screen.destroy())
        self.screen.bind("<Left>", lambda e: self.interface.move_left())
        self.screen.bind("<Up>", lambda e: self.interface.move_up())
        self.screen.bind("<Right>", lambda e: self.interface.move_right())
        self.screen.bind("<Down>", lambda e: self.interface.move_down())
        self.screen.bind("<space>", lambda e: self.interface.show_finger_print())
        self.screen.bind("<p>", lambda e: self.interface.zoom_up())
        self.screen.bind("<m>", lambda e: self.interface.zoom_down())
        self.screen.bind("<1>", lambda e: self.interface.on_click())
        self.screen.bind("<4>", lambda e: self.interface.move_up())
        self.screen.bind("<5>", lambda e: self.interface.move_down())
        self.screen.bind("<t>", lambda e: self.currentRobot.askScanForPosition())
        self.screen.bind("<y>", lambda e: self.currentRobot.showScans())
        self.screen.bind("<d>", lambda e: self.currentRobot.askDistance())
        self.screen.bind("<a>", lambda e: self.interface.chessboard.create_area())
        self.screen.bind("<z>", lambda e: self.interface.chessboard.add_box_to_area())
        self.screen.bind("<e>", lambda e: self.interface.chessboard.remove_box_from_area())
        self.screen.bind("<h>", lambda e: self.interface.hide_show_chessboard())
        self.screen.bind("<r>", lambda e: self.interface.chessboard.clear_areas())
        self.screen.bind("<q>", lambda e: self.interface.chessboard.show_hide_area())

    def set_up_buttons(self):
        maps = {
            "add_robot": Button(self.interface.frame_map["first_box"], image=self.interface.image_map["add"],
                                command=self.interface.add_robot),
            "remove_robot": Button(self.interface.frame_map["first_box"], image=self.interface.image_map["remove"],
                                   command=self.screen.destroy),
            "select_robot": Button(self.interface.frame_map["first_box"], image=self.interface.image_map["robot"],
                                   command=self.interface.set_robot),

            "set_position": Button(self.interface.frame_map["second_box"], image=self.interface.image_map["location"],
                                   command=self.interface.set_position, state=DISABLED),
            "get_position": Button(self.interface.frame_map["second_box"], image=self.interface.image_map["radar"],
                                   command=self.interface.get_robot_position, state=DISABLED),
            "move": Button(self.interface.frame_map["second_box"], image=self.interface.image_map["move"],
                           command=self.nothing,
                           state=DISABLED),

            "add_fp": Button(self.interface.frame_map["third_box"], image=self.interface.image_map["add"],
                             command=self.interface.scan_request),
            "remove_fp": Button(self.interface.frame_map["third_box"], image=self.interface.image_map["remove"],
                                command=self.nothing),
            "show_fp": Button(self.interface.frame_map["third_box"], image=self.interface.image_map["eye"],
                              command=self.interface.show_finger_print),
            "list_fp": Button(self.interface.frame_map["third_box"], image=self.interface.image_map["list"],
                              command=self.nothing),

            "add_area": Button(self.interface.frame_map["fourth_box"], image=self.interface.image_map["add"],
                               command=self.nothing),
            "remove_area": Button(self.interface.frame_map["fourth_box"], image=self.interface.image_map["remove"],
                                  command=self.nothing),
            "show_chessboard": Button(self.interface.frame_map["fourth_box"], image=self.interface.image_map["grid"],
                                      command=self.interface.hide_show_chessboard),
            "show_area": Button(self.interface.frame_map["fourth_box"], image=self.interface.image_map["eye"],
                                command=self.interface.chessboard.show_hide_area),

            "zoom_up": Button(self.interface.frame_map["fifth_box"], image=self.interface.image_map["zoomup"],
                              command=self.interface.zoom_up),
            "zoom_down": Button(self.interface.frame_map["fifth_box"], image=self.interface.image_map["zoomdown"],
                                command=self.interface.zoom_down),
        }

        for b in maps.values():
            b.pack(side="left", padx=1, pady=1)

        Label(self.interface.frame_map["fifth_box"], text="   Step ").pack(side='left')
        b = Button(self.interface.frame_map["fifth_box"], text="Ok", command=self.interface.change_step)
        b.pack(side='left')
        maps["step"] = b
        return maps

    def nothing(self):
        return
