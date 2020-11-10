from bin.mud_object import Mud_Object

# start_mark.c#
# Mrpr 901122#


class Death_mark(Mud_Object):

    # Function name: init
    # Description:   Init this object
    def init(self):
        self.start_death()

    # Function name: get
    # Description:   Don't give it away.
    def get(self):
        return True

    # Function name: id
    # Description:   Identify the object
    def id(self, arg):
        return arg == "death_mark"

    # Function name: start_death
    # Description:   Start the death sequence.
    def start_death(self):
        my_host = self.environment(self.this_object())

        if my_host:
            if self.living(my_host):
                if not my_host.query_ghost():
                    self.destruct(self.this_object())
                    return
            else:
                return
        else:
            return

        self.say("You see a dark shape gathering some mist..." +
                 "or maybe you're just imagining that.\n")
        self.write("You can see a dark hooded man standing beside " +
                   "your corpse.\nHe is wiping the bloody blade " +
                   "of a wicked looking scythe with slow measured\n" +
                   "motions. Suddenly he stops and seems to look " +
                   "straight at you with his empty...\n" +
                   "no, not empty but.... orbs....\n\n")

        self.write("Death says: COME WITH ME, MORTAL ONE!\n\n")

        self.write("He reaches for you and suddenly you find " +
                   "yourself in another place.\n\n")
        self.move_object(my_host, "/room/death/death_room")

    # Function name: query_auto_load
    # Description:   Automatic load of this object
    def query_auto_load(self):
        return "room/death/death_mark:"

    # Function name: drop
    # Description:   No dropping.
    def drop(self):
        return True
