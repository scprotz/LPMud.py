from bin.mud_object import Mud_Object


# This file defines a general purpose armour. See below for configuration
# functions: set_xx.
# If you are going to copy this file, in the purpose of changing
# it a little to your own need, beware:
#
# First try one of the following:
#
# 1. Do clone_object(), and then configure it. This object is specially
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
class Armour(Mud_Object):

    name = None
    alias = None
    short_desc = None
    long_desc = None
    value = 0
    weight = 0
    typ = None
    worn = False
    ac = 0
    worn_by = None
    next = None
    info = None
    
    def reset(self, arg):
        if(arg):
            return;
        self.typ = "armour";
   
    def link(self, ob):
        self.next = ob;
    
    def remove_link(self, arg):
        ob = None    
        if arg == self.name:
            ob = self.next;
            self.next = None
            return ob        
        if self.next:
            self.next = self.call_other(self.next, "remove_link", arg);
        return self.this_object();
    
    def init(self):
        self.add_action("wear", "wear");
        self.add_action("remove", "remove");
        
    def rec_short(self):
        if self.next:
            return self.name + ", " + self.call_other(self.next, "rec_short");
        return self.name
    
    def short(self):
        if not self.short_desc:
            return None
        if self.worn:
            return self.short_desc + " (worn)";
        return self.short_desc;
    
    
    def long(self,arg):
        self.write(self.long_desc);
    
    def id(self, arg):
        return arg == self.name or arg == self.alias or arg == self.typ;
    
    def test_type(self, arg):
        if arg == self.typ:
            return self.this_object();
        if self.next:
            return self.call_other(self.next, "test_type", arg);
        return None
    
    def tot_ac(self):
        if self.next:
            return self.ac + self.call_other(self.next, "tot_ac");
        return self.ac
    
    def query_type(self): 
        return self.typ
    
    def query_value(self): 
        return self.value
    
    def query_worn(self): 
        return self.worn
    
    def query_name(self): 
        return self.name
    
    def armour_class(self): 
        return self.ac
    
    def wear(self, arg):
    
        if not self.id(arg):
            return False
        if self.environment() != self.this_player():
            self.write("You must get it first!\n");
            return True
        
        if self.worn:
            self.write("You already wear it!\n");
            return True
        
        self.next = None
        ob = self.call_other(self.this_player(), "wear", self.this_object());
        if not ob:
            self.worn_by = self.this_player();
            self.worn = True
            return True
        
        self.write("You already have an armour of class " + self.typ + ".\n");
        self.write("Worn armour " + self.call_other(ob,"short") + ".\n");
        return True
    
    def get(self): 
        return True
    
    def drop(self,silently):
        if self.worn:
            self.call_other(self.worn_by, "stop_wearing", self.name);
            self.worn = False
            self.worn_by = None
            if not self.silently:
                self.tell_object(self.environment(self.this_object()),"You drop your worn armour.\n")        
        return False
        
    def remove(self,arg):
        if not self.id(arg):
            return False
        if not self.worn:
            return False        
        self.call_other(self.worn_by, "stop_wearing",self.name)
        self.worn_by = None
        self.worn = False
        return False    
    
    def query_weight(self): 
        return self.weight
    
    def set_id(self,n): 
        self.name = n
        
    def set_name(self,n): 
        self.name = n
        
    def set_short(self,s): 
        self.short_desc = s; 
        self.long_desc = s + ".\n"
        
    def set_value(self,v): 
        self.value = v
        
    def set_weight(self,w): 
        self.weight = w
        
    def set_ac(self,a): 
        self.ac = a
        
    def set_alias(self,a): 
        self.alias = a
        
    def set_long(self,l): 
        self.long_desc = l
        
    def set_type(self,t):
        self.typ = t;
    
    def set_arm_light(self,l): 
        self.set_light(l)
        
    def set_info(self,i):
        self.info = i;    
    
    def query_info(self):
        return self.info;
    
