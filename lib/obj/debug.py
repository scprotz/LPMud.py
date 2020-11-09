'''
--------- debug.py ---------------------
 created by Tech the toolmaker also known
 as Anders Ripa (ripa@cd.chalmers.se)
 
 updated for Python by scprotz also known
 as Dave Mobley (dave.mobley@uky.edu)
--------------------------------------------
'''
from bin.efun import Efun

class Debug(Efun):
    is_debug = False

    '''
    generic debug support for any object
    
    typical uses are:
    
        if(is_debug) {
            write("in routine...\n");
        }
    or
        if(is_debug) {
            tell_object(ob, "in routine...\n");
        }
    '''

    def debug_toggle(self, arg): 
    
        if not arg or not id(arg):
            return False
    
        self.is_debug = not self.is_debug
        
        if self.is_debug:            
            self.write("Debug is enabled for " + self.short() + "\n");
        else:
            self.write("Debug is disabled for " + self.short() + "\n");        
        return True
    

    def query_debug(self):
        return self.is_debug

    def set_debug(self, arg):
        self.is_debug = arg
