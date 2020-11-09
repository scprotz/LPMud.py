'''
--- quicktyper.py --- 
A quicktyping utility that stores a list of command aliases and
keeps a history of the last command given by the player
and let you put several commands on a single line.
 
do get more information do "help quicktyper"
 
Tech's quicktyper.py
 
this file requires the debug.h file
 
and it also requires LPC version 2.3
 
This utility was developed in Genesis (the original LP-Mud)
by Tech the toolmaker also known as Anders Ripa (ripa@cd.chalmers.se)
and bug reports etc should be sent to me 
'''

from bin.mud_object import Mud_Object
from lib.obj.debug import Debug


class Quicktyper(Mud_Object, Debug):
    
 
    VERSION = "2.06"
    VERSION_DATE = "901020"
    FILE_NAME = "obj/quicktyper" # used by query_autoload #
         
    owner = None
    list_ab = []
    list_cmd = []
    list_history = None
     
    MAX_HISTORY = 20
    history_pos = 0
    history_offset = 0
    no_history_add = False
     
    refreshing = False
    needs_refresh = False
    
    ob = None # used to hold this_player() #     
    wrapped = False
    last_cmd_added = None
    last_str_added = None
    counter = 0
    COUNT_UNTIL_REFRESH = 40
    
    org_cmds = None
    more_cmds = None
    first_call = False
    paused = False


    def __init__(self):
        super().__init__()

 
    # return som info for the interested
    def query_info(self):
        return "A magic quick typing utility made by Tech."

 
    # make it possible to retrieve information from the quicktyper
    def query_quicktyper(self, arg):

        if arg == 0:
            return self.list_ab
        
        if arg == 1:
            return self.list_cmd;
        
        if arg == 2:
            return self.list_history;
        
        if arg == 3:
            return self.history_pos;
        
        if arg == 4:
            return self.history_offset
        
        return 0;

 
    def id(self, arg):
        if arg and (arg == "quicktyper" or arg == self.owner + "'s quicktyper" or arg == "tech_quicktyper"):
            return True        
        return False

 
    def query_name(self):
        return self.owner + "'s quicktyper";
     
    def reset(self, arg):   
     
        if self.is_debug:
            self.write("reset(" + arg + ")\n");
            self.write(self.VERSION + "\n");             
            self.write("this_object()="); 
            self.write(self.this_object()); 
            self.write("\n");
            self.write("environment(this_object())="); 
            self.write(self.environment(self.this_object())); 
            self.write("\n");
            self.write("this_player()="); 
            self.write(self.this_player()); 
            self.write("\n");
            self.write("environment(this_player())="); 
            self.write(self.environment(self.this_player())); 
            self.write("\n");        
         
        if not self.refreshing and self.this_player():
            self.owner = self.call_other(self.this_player(), "query_name")        
         
        if not self.list_history:
            self.list_history = []
    

    def init_alias_list(self):
                 
        if not self.list_ab:
            self.list_ab = []
        
        if not self.list_cmd:
            self.list_cmd = []
         
    def init(self, arg):
        raise NotImplementedError
#         int    i;
#         object    obj;
#          
#         if(is_debug) {
#         write("init(" + arg + ")\n");
#         write("this_object()="); write(this_object()); write("\n");
#         write("environment(this_object())="); write(environment(this_object())); write("\n");
#         write("this_player()="); write(this_player()); write("\n");
#         write("environment(this_player())="); write(environment(this_player())); write("\n");
#         }
#          
#         if(this_player()) {
#         owner = call_other(this_player(), "query_name");
#         }
#         init_alias_list();
#          
#         if(environment(this_object()) == this_player()) {
#         add_action("alias", "alias");
#         add_action("do_cmd", "do");
#         add_action("history", "history");
#         add_action("resume", "resume");
#         add_action("do_refresh", "refresh");
#         add_action("help", "help");
#         /*
#           add_action("drop_object", "drop");
#          */
#         /* let wizards have some additional information commands */
#         if(call_other(this_player(), "query_level") >= 20) {
#             add_action("version", "ver");
#             add_action("debug_toggle", "debug");     /* declared in debug.h */
#         }
#          
#         i = 0;
#         while(i < sizeof(list_ab)) {
#             if(list_ab[i] and list_ab[i] != "" and list_cmd[i] and list_cmd[i] != "") {
#             add_action("do_it", list_ab[i]);
#             }
#             i += 1;
#         }
#          
#         add_action("history_add", "", 1);
#          
#         if(!refreshing) {
#             write("Quicktyper....\n");
#         } else {
#             if(is_debug) {
#             write("quick refresh -init \n");
#             }
#         }
#         if(!needs_refresh and !refreshing) {
#             if(is_debug) {
#             write("registred an refresh in 30 sec\n");
#             needs_refresh = 1;
#             }
#             call_out("refresh", 30, this_player());
#         }
#          
#         }

 
    def do_refresh(self):
        self.write("Refreshing Quicktyper ..");
        self.refresh(self.this_player());
        self.write("Done.\n");
        return True

 
    def refresh(self, obj):   
        raise NotImplementedError  
#         int    may_need_warning;
#          
#         may_need_warning = 0;
#          
#         if(is_debug) {
#         tell_object(obj, "Refreshing Quicktyper,");
#         }
#         if(first_inventory(obj) != this_object()) {
#         may_need_warning = 1;
#         }
#         refreshing = 1;
#          
#         move_object(this_object(), "room/storage");
#          
#         if(is_debug) {
#         tell_object(obj, "moved to storage,");
#         }
#          
#         move_object(this_object(), obj);
#          
#         if(is_debug) {
#         tell_object(obj, "back again\n");
#         }
#          
#         if(may_need_warning and obj->query_level() > 19)  {
#         tell_object(obj, "Quicktyper: Your inventory has been rearranged.\n");
#         }
#         refreshing = 0;
#         needs_refresh = 0;
#          
#         return 1;

 
    def do_old(self, verb, arg):
        raise NotImplementedError 
#     {        
#         int    pos;
#         arging    temp;
#          
#         if(is_debug) {
#         write("verb=" + verb + "\n");
#         write("arg=" + arg + "\n");
#         }
#          
#         if(strlen(verb) <= 1 or verb[0] != '%') {
#         write("do_old: return 0\n");
#         return 0;
#         }
#          
#         if(verb == "%%") {    
#         if(is_debug) {
#             write("last command\n");
#         }
#         if(history_pos == 0) {
#             if(!wrapped) {
#             write("No history!\n");
#             return 1;
#             }
#             pos = MAX_HISTORY -1;
#         } else {
#             pos = history_pos -1;
#         }
#          
#         if(is_debug) {
#             write("history_pos=" + history_pos + "\n");
#             write("pos=" + pos + "\n");
#             write("will do: " + list_history[pos] + "\n");
#         }
#          
#         if(arg and arg != "") {
#             write(list_history[pos] + " " + arg + "\n");
#             command(list_history[pos] + " " + arg, this_player());
#         } else {
#             write(list_history[pos] + "\n");
#             command(list_history[pos], this_player());
#         }
#         return 1;
#         }
#         if(sscanf(verb, "%%d%s", pos, temp) >= 1) {
#         if(is_debug) {
#             write("old command\n");
#         }
#         if(temp == 0) {
#             temp = "";
#         }
#         if(pos < 1 or pos <= history_offset) {
#             write("History position " + pos + " is not available!\n");
#             return 1;
#         }
#         if(!wrapped and (pos-1) >= history_pos) {
#             write("History position " + pos + " is not available!\n");
#             return 1;
#         }
#         if(pos > MAX_HISTORY + history_offset - 1) {
#             write("History position " + pos + " is not available!\n");
#             return 1;
#         }
#         if(!wrapped) {
#             if(is_debug) {
#             write("Not wrapped.\n");
#             }
#             if(arg and arg != "") {
#             write(list_history[pos-1] + temp + " " + arg + "\n");
#             command(list_history[pos-1] + temp + " " + arg, this_player());
#             } else {
#             write(list_history[pos-1] + temp + "\n");
#             command(list_history[pos-1] + temp, this_player());
#             }
#             return 1;
#         } else {
#             if(is_debug) {
#             write("pos=" + pos + "\n");
#             write("history_offset=" + history_offset + "\n");
#             write("history_pos=" + history_pos + "\n");
#             }
#              
#             pos -= history_offset;
#              
#             if(is_debug) {
#             write("pos-history_offset=" + pos + "\n");
#             }
#              
#             pos += history_pos;
#              
#             if(is_debug) {
#             write("pos-history_offset+history_pos=" + pos + "\n");
#             }
#              
#             if(pos >= MAX_HISTORY) {
#             pos -= MAX_HISTORY;
#             }
#              
#             if(is_debug) {
#             write("pos-history_offset+history_pos=" + pos + "\n");
#             write("would do: " + list_history[pos] + "\n");
#             }
#             if(arg and arg != "") {
#             write(list_history[pos] + " " + arg + "\n");
#             command(list_history[pos] + " " + arg, this_player());
#             } else {
#             write(list_history[pos] + "\n");
#             command(list_history[pos], this_player());
#             }
#             return 1;
#         }
#         }
#         write("do_old: return 0\n");
#         return 0;
#     }
 
    def history(self):
        raise NotImplementedError 
#     {
#         int    i;
#         int    number;
#          
#         owner = call_other(this_player(), "query_name");
#          
#         if(wrapped) {
#         number = history_offset + 1;
#         i = history_pos + 1;
#         while(i < MAX_HISTORY) {
#             if(is_debug) {
#             write(i + " ");
#             }
#             write("%" + number + "\t" + list_history[i] + "\n");
#             i += 1;
#             number += 1;
#         }
#         } else {
#         number = 1;
#         }
#         i=0;
#         while(i < history_pos) {
#         if(is_debug) {
#             write(i + " ");
#         }
#         write("%" + number + "\t" + list_history[i] + "\n");
#         i += 1;
#         number += 1;
#         }
#         return 1;
#     }
 

 
    def history_add(self, arg):
        raise NotImplementedError 
#     {
#          
#         string    verb;
#         int    i;
#          
#         if(is_debug) { 
#         write("history_add\n");
#         }
#          
#         verb = query_verb();
#          
#         if(!needs_refresh) {
#         counter += 1;
#         }
#          
#         if(counter >= COUNT_UNTIL_REFRESH or verb == "get" or verb == "take") {
#         counter = 0;
#         if(!needs_refresh) {
#             needs_refresh = 1;
#             if(is_debug) { 
#             write("registered an refresh in 20 sec\n");
#             }
#             call_out("refresh", 20, this_player());
#         }
#         }
#          
#         if(is_debug) { 
#         write("verb=" + verb + "\n");
#         write("str=" + arg + "\n");
#         }
#          
#         if(verb == 0 or  verb =="") {
#         return 0;
#         }
#          
#         if(strlen(verb) > 1 and verb[0] == '%') {
#         if(is_debug) {
#             write("calling do_old\n");
#         }
#         return do_old(verb, arg);
#         }
#          
#         if(verb == last_cmd_added) {
#         if(!arg) {
#             return 0;
#         }
#         if(arg == last_str_added) {
#             return 0;
#         }
#         }
#          
#         if(no_history_add) {
#         no_history_add = 0;
#         return 0;
#         }
#          
#         last_cmd_added = verb;
#         last_str_added = arg;
#          
#         i = 0;
#         while(i < sizeof(list_ab)) {
#         if(list_ab[i] == verb) {
#             return 0;    /* dont add aliases to the list */
#         }
#         i += 1;
#         }
#          
#         if(arg and arg != "") {
#         list_history[history_pos] = verb + " " + arg;
#         } else {
#         list_history[history_pos] = verb;
#         }
#         history_pos += 1;
#         if(history_pos >= MAX_HISTORY) {
#         history_pos = 0;
#         wrapped = 1;
#         }
#         if(wrapped) {
#         history_offset += 1;
#         }
#         return 0;
#     }
 
    def short(self):    
        return self.owner + "'s quicktyper";
    
 
    def long(self):    
        self.write("This is a typing aid to allow long commands to be replaced with short aliases.\n");
        self.write("It also contains a history of your commands\n");
        self.write("Do \"help quicktyper\" to get more information about how to use this tool.\n");
         
 
    def version(self, arg):
        if not arg or not id(arg):
            return 0;
        
        self.write("Tech's quicktyper version " + self.VERSION + " created " + self.VERSION_DATE + "\n")
        return True
    
 
    def alias(self, arg):
        raise NotImplementedError 
# {
#         int    i;
#         string    ab, cmd;
#          
#         owner = call_other(this_player(), "query_name");
#          
#         if(!arg or arg == "") {
#         write("The aliases in your quicktyper are:\n");
#         i = 0;
#         while(i < sizeof(list_ab)) {
#             if(list_ab[i]) {
#             write(extract(list_ab[i] + "         ", 0, 9) + list_cmd[i] + "\n");
#             }
#             i += 1;
#         }
#         return 1;
#         }
#         if(sscanf(arg, "%s %s", ab, cmd) == 2) {
#         /* adding a new alias */
#         i = 0;
#         while(i < sizeof(list_ab)) {
#             if(list_ab[i] == ab) {
#             /* replace old definition */
#             list_cmd[i] = cmd;
#             write("Ok.\n");
#             return 1;
#             }
#             i += 1;
#         }
#         i = 0;
#         while(i < sizeof(list_ab)) {
#             if(!list_ab[i]) {
#             list_ab[i] = ab;
#             list_cmd[i] = cmd;
#             add_action("do_it", list_ab[i]);
#             add_action("history_add", "", 1);
#             write("Ok.\n");
#             return 1;
#             }
#             i += 1;
#         }
#         write("Sorry the quicktyper is full!\n");
#         return 1;
#         }
#         if(sscanf(arg, "%s", ab) == 1) {
#         /* removing an alias */
#         i = 0;
#         while(i < sizeof(list_ab)) {
#             if(list_ab[i] and list_ab[i] == ab) {
#             list_ab[i] = 0;
#             list_cmd[i] = 0;
#             write("Removed alias for " + ab + ".\n");
#             return 1;
#             }
#             i += 1;
#         }
#         write(ab + " didn't have an alias!\n");
#         return 1;
#         }
#         write("This can't happen!\n");
#         return 0;
#     }
 
    def help(self, arg):
        if not arg or not id(arg):
            return False
        
        self.write("This Quicktyper alows for command alias, e.g. short commands \nthat is expanded by the Quicktyper\n")
        self.write("The commands available for the quicktyper are:\n")
        self.write("alias            - show the list of current alias\n")
        self.write("alias command what to do\n            - make \"command\" an alias for the \"what to do\"\n")
        self.write("alias command        - remove alias for \"command\"\n")
        self.write("do cmd1,cmd2,cmd3,..    - do a series of commands\n")
        self.write("do            - pauses execution of a series of commands\n")
        self.write("resume            - resume paused commands\n")
        self.write("history            - give a list of previous commands\n")
        self.write("%%            - repeat last command\n")
        self.write("%n            - repeat command number 'n'\n")
        self.write("help quicktyper        - this helptext\n")
         
        if self.call_other(self.this_player(), "query_level") >= 20:
            self.write("ver quicktyper        - shows version information\n")
            self.write("debug quicktyper    - toggle internal debug status\n")
        
        self.write("examples:    'alias l look at watch'\n        enables you to write l to look at your watch.\n")
        self.write("        'do smile,look,laugh'\n    will first make you smile then look and laugh.\n")
        self.write("        doing '%%' will then repeat this three commands again\n\n")
        self.write("Another product from the kingdom of Zalor.\n(send bugreports etc. to Tech)\n")
        self.write("(Error: messages that tell you that something is not found,\nis due to the LP-Mud security system and can not be avoided.)\n")
        self.owner = self.call_other(self.this_player(), "query_name")
        return True
    
 
    def get(self):
        if self.contains("tech_quicktyper", self.this_player()):
            return False        
        return True
 
    def drop(self):
        return True # cant drop ! #
 
    def query_value(self):
        return 0    # no value #
 
    def query_auto_load(self):
        raise NotImplementedError
#     {
#         string    temp;
#         int    i, count;
#          
#         i = 0;
#         count = 0;
#         while(i < sizeof(list_ab)) {
#         if(list_ab[i] and list_cmd[i]) {
#             count += 1;
#         }
#         i += 1;
#         }
#         temp = FILE_NAME + ":"  + count + ";";
#         i = 0;
#         while(i < sizeof(list_ab)) {
#         if(list_ab[i] and list_cmd[i]) {
#             temp += list_ab[i] + " " + list_cmd[i] + ";.X.Z;";
#         }
#         i += 1;
#         }
#          
#         return temp;    
#     }
 
    def do_it(self,arg):
        raise NotImplementedError
#     {
#         int    i;
#         string    verb;
#          
#         if(is_debug) {
#         write("query_verb=" + query_verb() + "\n");
#         write("str=" + arg + "\n");
#         }
#         verb = query_verb();
#         if(verb == 0) return 0;
#          
#         i = 0;
#         while(i < sizeof(list_ab)) {
#         if(list_ab[i] == verb) {
#             if(list_cmd[i] == 0) {
#             list_ab[i] = 0;
#             } else {
#             if(arg and arg != "") {
#                 if(is_debug) {
#                 write(list_cmd[i] + " " + arg + "\n");
#                 }
#                 /*
#                   no_history_add = 1;
#                  */
#                 command(list_cmd[i] + " " + arg, this_player());
#                 no_history_add = 0;
#             } else {
#                 if(is_debug) {
#                 write(list_cmd[i] + "\n");
#                 }
#                 /*
#                   no_history_add = 1;
#                  */
#                 command(list_cmd[i], this_player());
#                 no_history_add = 0;
#             }
#             return 1;
#             }
#         }
#         i += 1;
#         }
#         /* not found */
#         return 0;
#     }
 
    def init_arg(self, arg):
        raise NotImplementedError 
#     {
#         int    temp;
#         int    count, place;
#         string    ab, cmd;
#         string    the_rest;
#          
#         if(is_debug) write("init_arg(" + arg + ")\n");
#          
#         if(arg) {
#         the_rest = "";
#         if(sscanf(arg, "%d;%s", count, the_rest) == 2) {
#             if(is_debug) write("count=" + count + "\n");
#             init_alias_list();
#              
#             while(the_rest and the_rest != "" and place < sizeof(list_ab))
#             {
#             arg = the_rest;
#             if(sscanf(arg, "%s %s;.X.Z;%s", ab, cmd, the_rest) >= 2) {
#                 if(ab and ab != "" and cmd and cmd != "") {
#                 list_ab[place] = ab;
#                 list_cmd[place] = cmd;
#                 place += 1;
#                 }
#             }
#             }
#         }
#         }
#     }
 
 
# do one ore more commands #
 

 
    def do_cmd(self, arg):
        raise NotImplementedError
#     {
#          
#         if(!arg or arg == "")  {
#         if(more_cmds) {
#             set_heart_beat(0);
#             write("Paused. Use \"resume to continue\"\n");
#             paused = 1;
#         } else {
#             write("usage: do cmd1,cmd2, cmd3,...\n");
#         }
#         return 1;
#         }
#          
#         if(more_cmds and !paused) {
#         write("Busy doing your commands:\n" + more_cmds + "\n");
#         return 1;
#         }
#         if(paused) {
#         write("Skipping paused commands:\n" + more_cmds + "\n");
#         paused = 0;
#         }
#         more_cmds = arg;
#         ob = this_player();
#         first_call = 1;
#         heart_beat();
#         first_call = 0;
#         set_heart_beat(1);
#         return 1;
#     }
 
    def resume(self):
        if self.paused and self.ob and self.more_cmds and self.more_cmds != "":
            self.paused = False
            self.first_call = True
            self.heart_beat();
            self.first_call = False
            self.set_heart_beat(1);
            return True
        
        self.write("Nothing to resume.\n");
        return True
    
 
    def heart_beat(self):
        
        if self.ob and self.more_cmds and self.more_cmds != "":
            if len(self.more_cmds.split(',')) == 2:
                cmd = self.more_cmds.split(',')[0]
                the_rest = self.more_cmds.split(',')[1]
                self.tell_object(self.ob, "doing: " + cmd + "\n");
                self.no_history_add = True
                self.command(cmd, self.ob)
                self.no_history_add = False
                self.more_cmds = the_rest;
            else:
                cmd = self.more_cmds
                self.tell_object(self.ob, "doing: " + cmd + "\n")
                self.no_history_add = True
                self.command(cmd, self.ob)
                self.no_history_add = False
                self.more_cmds = None
                if not self.first_call:
                    self.set_heart_beat(False);
                
                self.tell_object(self.ob, "Done.\n");            
         
        else:
            self.ob = None
            self.more_cmds = None
            if(not self.first_call):
                self.set_heart_beat(False)
        
        
    
 
# ------- contains ----------- #
 
# check to see if an object "obj" contains another object "str" #
 
    def contains(self, arg, obj):
         
        if not arg or arg == "":
            return False
         
        for ob in obj.inventory():               
        
            if self.call_other(ob, "id", arg):
                return True # we found it #
         
        
        return False # not found #

 
# --- end of quicktyper.py #

