from bin.mud_object import Mud_Object


class STD(Mud_Object):

    DEST = None
    DIR1 = None
    DIR2 = None
    DIR3 = None
    DIR4 = None
    SH = None
    LO = None
    LIGHT = None

    def EXTRA_INIT(self, *args):
        pass

    def EXTRA_RESET(self, *args):
        pass

    def EXTRA_LONG(self, *args):
        pass

    def EXTRA_MOVE1(self, *args):
        pass

    def EXTRA_MOVE2(self, *args):
        pass

    def EXTRA_MOVE3(self, *args):
        pass

    def EXTRA_MOVE4(self, *args):
        pass

    def __init__(self, DEST=None, DIR1=None, DIR2=None,
                 DIR3=None, DIR4=None, SH=None, LO=None, LIGHT=0):
        super().__init__()
        self.DEST = DEST
        self.DIR1 = DIR1
        self.DIR2 = DIR2
        self.DIR3 = DIR3
        self.DIR4 = DIR4
        self.SH = SH
        self.LO = LO
        self.LIGHT = LIGHT

    def reset(self, arg):
        self.EXTRA_RESET()
        if arg:
            return
        self.set_light(self.LIGHT)

    def short(self):
        if self.set_light(0):
            return self.SH
        return "dark room"

    def init(self):
        if self.DIR1:
            self.add_action("move1", self.DIR1)
        if self.DIR2:
            self.add_action("move2", self.DIR2)
        if self.DIR3:
            self.add_action("move2", self.DIR3)
        if self.DIR4:
            self.add_action("move2", self.DIR4)
        self.EXTRA_INIT()

    def move1(self):
        self.EXTRA_MOVE1()
        self.call_other(self.this_player(), "move_player", self.DIR1 + "#" +
                        self.DEST)
        return True

    def move2(self):
        self.EXTRA_MOVE2()
        self.call_other(self.this_player(), "move_player", self.DIR2 + "#" +
                        self.DEST)
        return True

    def move3(self):
        self.EXTRA_MOVE3()
        self.call_other(self.this_player(), "move_player", self.DIR3 + "#" +
                        self.DEST)
        return True

    def move4(self):
        self.EXTRA_MOVE4()
        self.call_other(self.this_player(), "move_player", self.DIR4 + "#" +
                        self.DEST)
        return True

    def long(self, name):
        if self.set_light(0) == 0:
            self.write("It is dark.\n")
            return
        self.EXTRA_LONG()
        self.write(self.LO)
        if not self.DIR1 and not self.DIR2 and not self.DIR3 and not self.DIR4:
            self.write("    There are no obvious exits.\n")
        elif not self.DIR2 and not self.DIR3 and not self.DIR4:
            self.write("    The only obvious exit is " + self.DIR + ".\n")
        elif not self.DIR3 and not self.DIR4:
            self.write("There are three obvious exits, " + self.DIR1 + ", " +
                       self.DIR2 + " and " + self.DIR3 + ".\n")
        else:
            self.write("There are four obvious exits, " + self.DIR1 + ", " +
                       self.DIR2 + ", " + self.DIR3 + " and " +
                       self.DIR4 + ".\n")
