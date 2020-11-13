from bin.mud_object import Mud_Object


# This is a generic valuable object. Clone a copy, and
# setup local values.
# If you are going to copy this file, in the purpose of changing
# it a little to your own need, beware:
#
# First try one of the following:
#
# 1. Do clone_object(), and then configur it. This object is specially
#    prepared for configuration.
#
# 2. If you still is not pleased with that, create a new empty
#    object, and make an inheritance of this objet on the first line.
#    This will automatically copy all variables and functions from the
#    original object. Then, add the functions you want to change. The
#    original function can still be accessed with '::' prepended on the name.
#
# The maintainer of this LPmud might become sad with you if you fail
# to do any of the above. Ask other wizards if you are doubtful.
#
# The reason of this, is that the above saves a lot of memory.


class Treasure(Mud_Object):
    
    short_desc = None
    long_desc = None
    value = 0
    local_weight = 0
    name = None
    alias_name = None
    read_msg = None
    info = None
    
    def id(self, arg):
        return arg == self.name or arg == self.alias_name
    
    def short(self):
        return self.short_desc
        
    def long(self):
        self.write(self.long_desc)
        
    def query_value(self): 
        return self.value
    
    def set_id(self, arg):
        self.local_weight = 1
        self.name = arg    

    def set_alias(self, arg):
        self.alias_name = arg
    
    def set_short(self, arg):
        self.short_desc = arg
        self.long_desc = "You see nothing special.\n"
        
    def set_long(self, arg):
        self.long_desc = arg
        
    def set_value(self, v):
        self.value = v
        
    def set_weight(self, w):
        self.local_weight = w
    
    def set_read(self, arg):
        self.read_msg = arg    
    
    def set_info(self, i):
        self.info = i
    
    def query_info(self):
        return self.info
    
    def get(self):
        return True
    
    def query_weight(self):
        return self.local_weight
    
    
    def init(self):
        if not self.read_msg:
            return
        self. add_action("read", "read")    
    
    def read(self, arg):
        if arg != self.name and arg != self.alias_name:
            return False
        self.write(self.read_msg)
        return True
