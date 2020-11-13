from bin import mud_object


class Weapon(mud_object.Mud_Object):
    """
    This file defines a general purpose weapon. See below for configuration
    functions: set_xx.
    If you are going to copy this file, in the purpose of changing
    it a little to your own need, beware:

    First try one of the following:

    1. Do clone_object(), and then configure it. This object is specially
       prepared for configuration.

    2. If you still is not pleased with that, create a new empty
       object, and make an inheritance of this objet on the first line.
       This will automatically copy all variables and functions from the
       original object. Then, add the functions you want to change. The
       original function can still be accessed with '::' prepended on the name.

    The maintainer of this LPmud might become sad with you if you fail
    to do any of the above. Ask other wizards if you are doubtful.

    The reason of this, is that the above saves a lot of memory.
    """
    wielded = False
    wielded_by = None
    name_of_weapon = None
    cap_name = None
    alt_name = None
    alias_name = None
    short_desc = None
    long_desc = None
    read_msg = None
    class_of_weapon = 0
    value = 0
    local_weight = 0
    hit_func = None
    wield_func = None
    info = None

    def query_name(self):
        return self.name_of_weapon


    def long(self):
        self.write(self.long_desc)


    def reset(self, arg):
        if arg:
            return
        self.wielded = 0 
        self.value = 0


    def init(self):
        if self.read_msg:
            self.add_action("read", "read")
        self.add_action("wield", "wield")


    def wield(self, arg):
        if not id(arg):
            return False
        if self.environment() != self.this_player():
            # write("You must get it first!\n") #
            return False

        if self.wielded:
            self.write("You already wield it!\n")
            return True

        if self.wield_func:
            if not self.call_other(self.wield_func, "wield", self.this_object()):
                return True
        self.wielded_by = self.this_player()
        self.call_other(self.this_player(), "wield", self.this_object())
        self.wielded = True
        return True


    def short(self):
        if self.wielded:
            if self.short_desc:
                return self.short_desc + " (wielded)"
        return self.short_desc
        
    def weapon_class(self):
        return self.class_of_weapon


    def id(self, arg):
        return arg == self.name_of_weapon or arg == self.alt_name or arg == self.alias_name
    
    def drop(self, silently):
        if self.wielded:
            self.call_other(self.wielded_by, "stop_wielding")
            self.wielded = False
            if not silently:
                self.write("You drop your wielded weapon.\n")        
        return False


    def un_wield(self):
        if self.wielded:
            self.wielded = False


    def hit(self, attacker):
        if self.hit_func:
            return self.call_other(self.hit_func, "weapon_hit", attacker)
        return 0


    def set_id(self, n):
        self.name_of_weapon = n
        self.cap_name = self.capitalize(n)
        self.short_desc = self.cap_name
        self.long_desc = "You see nothing special.\n"


    def set_name(self, n):
        self.name_of_weapon = n
        self.cap_name = self.capitalize(n)
        self.short_desc = self.cap_name
        self.long_desc = "You see nothing special.\n"


    def read(self, arg):
        if not self.id(arg):
            return False
        self.write(self.read_msg)
        return True


    def query_value(self):
        return self.value


    def get(self): 
        return True


    def query_weight(self): 
        return self.local_weight


    def set_class(self, c): 
        self.class_of_weapon = c


    def set_weight(self, w): 
        self.local_weight = w


    def set_value(self, v): 
        self.value = v


    def set_alt_name(self, n): 
        self.alt_name = n


    def set_hit_func(self, ob): 
        self.hit_func = ob


    def set_wield_func(self, ob): 
        self.wield_func = ob


    def set_alias(self, n): 
        self.alias_name = n


    def set_short(self, sh): 
        self.short_desc = sh 
        self.long_desc = self.short_desc + "\n"


    def set_long(self, long): 
        self.long_desc = long


    def set_read(self, arg): 
        self.read_msg = arg


    def set_info(self, i):
        self.info = i


    def query_info(self):
        return self.info


