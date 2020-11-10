from lib.room.std import STD
from lib.room.tune import Tune

class Adv_guild(STD, Tune):

    next_level = 0
    next_exp = 0
    level = 0
    exp = 0
    title = None # now with arrays. :) #
    player_ob = None
    banished_by = None
    male_title_str = None
    fem_title_str = None
    neut_title_str = None     
    exp_str = 0
 
    def EXTRA_RESET(self, arg):
        if arg:
            return
        self.move_object("obj/book", self.this_object())
        self.move_object(self.clone_object("obj/bull_board"), self.this_object())
        ob = self.clone_object("obj/quest_obj")
        self.call_other(ob, "set_name", "orc_slayer")
        self.call_other(ob, "set_hint", "Retrieve the Orc slayer from the evil orc shaman, and give it to Leo.\n")
        self.move_object(ob, "room/quest_room")

 
    def EXTRA_INIT(self):
        self.add_action("cost_for_level", "cost")
        self.add_action("advance", "advance")
        self.add_action("south", "south")
        self.add_action("banish", "banish")
        self.add_action("list_quests", "list")
 
 
    def __init__(self):
        super().__init__(DEST="room/vill_road2", 
                         DIR1="north",
                         SH="Commands: cost, advance [level, str, dex, int, con], list (number).\n" + "The adventurers guild",
                         LO="There is an opening to the south, and some shimmering\n" +
                         "You can also buy points for a new level.\n" +
                         "You have to come here when you want to advance your level.\n" +
                         "blue light in the doorway.\n", 
                         LIGHT=1)
 

     
    # some minor changes by Iggy. #
    # get level asks get_next_exp() and  get_next_title() #
     
    def get_level(self, name):    
        self.level = name
       
        self.next_exp   = self.get_next_exp(self.level)
        self.next_level = self.level + 1    
        self.title      = self.get_new_title(self.level)
        
     
    # return title #
    def get_new_title(self, arg):
    
        if not self.male_title_str:
            male_title_str = []
            for _ in range(20):
                self.male_title.str.append(" ") 
            male_title_str[19]    ="the apprentice Wizard"
            male_title_str[18]    ="the grand master sorcerer"
            male_title_str[17]    ="the master sorcerer"
            male_title_str[16]    ="the apprentice sorcerer"
            male_title_str[15]    ="the warlock"
            male_title_str[14]    ="the enchanter"
            male_title_str[13]    ="the magician"
            male_title_str[12]    ="the apprentice magician"
            male_title_str[11]    ="the conjurer"
            male_title_str[10]    ="the champion"
            male_title_str[9]    ="the warrior"
            male_title_str[8]    ="the great adventurer"
            male_title_str[7]    ="the experienced adventurer"
            male_title_str[6]    ="the small adventurer"
            male_title_str[5]    ="the experienced fighter"
            male_title_str[4]    ="the small fighter"
            male_title_str[3]    ="the master ranger"
            male_title_str[2]    ="the lowrank ranger"
            male_title_str[1]    ="the simple wanderer"
            male_title_str[0]    ="the utter novice"
            self.male_title_str = male_title_str
     
        if not self.fem_title_str:
            fem_title_str = []
            for _ in range(20):
                fem_title_str.append(" ")            
         
            fem_title_str[19]    ="the apprentice Wizard"
            fem_title_str[18]    ="the grand master sorceress"
            fem_title_str[17]    ="the master sorceress"
            fem_title_str[16]    ="the apprentice sorceress"
            fem_title_str[15]    ="the witch"
            fem_title_str[14]    ="the enchantress"
            fem_title_str[13]    ="the magicienne"
            fem_title_str[12]    ="the apprentice magicienne"
            fem_title_str[11]    ="the conjuress"
            fem_title_str[10]    ="the deadly amazon"
            fem_title_str[9]    ="the amazon"
            fem_title_str[8]    ="the great adventuress"
            fem_title_str[7]    ="the experienced adventuress"
            fem_title_str[6]    ="the small adventuress"
            fem_title_str[5]    ="the charming siren"
            fem_title_str[4]    ="the siren"
            fem_title_str[3]    ="the master ranger"
            fem_title_str[2]    ="the lowrank ranger"
            fem_title_str[1]    ="the simple wanderer"
            fem_title_str[0]    ="the utter novice"
            self.fem_title_str = fem_title_str
     
        if not self.neut_title_str:
            neut_title_str = []
            for _ in range(20):
                neut_title_str.append(" ")
                
            neut_title_str[19]    ="the apprentice Wizard"
            neut_title_str[18]    ="the ferocious tyrannosaur"
            neut_title_str[17]    ="the small tyrannosaur"
            neut_title_str[16]    ="the vicious dragon"
            neut_title_str[15]    ="the devious dragon"
            neut_title_str[14]    ="the small dragon"
            neut_title_str[13]    ="the powerful demon"
            neut_title_str[12]    ="the small demon"
            neut_title_str[11]    ="the beholder"
            neut_title_str[10]    ="the great monster"
            neut_title_str[9]    ="the experienced monster"
            neut_title_str[8]    ="the medium monster"
            neut_title_str[7]    ="the small monster"
            neut_title_str[6]    ="the threatening shadow"
            neut_title_str[5]    ="the shadow"
            neut_title_str[4]    ="the wraith"
            neut_title_str[3]    ="the bugbear"
            neut_title_str[2]    ="the furry creature"
            neut_title_str[1]    ="the simple creature"
            neut_title_str[0]    ="the utter creature"
            self.neut_title_str = neut_title_str
            
        if not self.player_ob or not self.player_ob.query_gender():
            return self.neut_title_str[str]
        elif self.player_ob.query_gender() == 1:
            return self.male_title_str[str]
        else:
            return self.fem_title_str[str]
         
    # returns the next_exp. #
    def get_next_exp(self, arg):
        if not self.exp_str:
            exp_str = []
            for _ in range(20):
                exp_str.append(0)
         
            exp_str[19]    = 1000000
            exp_str[18]    =  666666 
            exp_str[17]    =  444444
            exp_str[16]    =  296296
            exp_str[15]    =  197530
            exp_str[14]    =  131687
            exp_str[13]    =   97791
            exp_str[12]    =   77791
            exp_str[11]    =   58527
            exp_str[10]    =   39018
            exp_str[9]    =   26012
            exp_str[8]    =   17341
            exp_str[7]    =   11561
            exp_str[6]    =    7707
            exp_str[5]    =    5138
            exp_str[4]    =    3425
            exp_str[3]    =    2283
            exp_str[2]    =    1522
            exp_str[1]    =    1014
            exp_str[0]    =     676
            self.exp_str = exp_str
            
        return self.exp_str[arg]
    
     
    # This routine is called by monster, to calculate how much they are worth.
    # This value should not depend on the tuning.    
    def query_cost(self, l):
        self.player_ob = self.this_player()
        self.level = self.l
        if self.level >= 20:
            return 1000000
        self.get_level(self.level)
        return self.next_exp
         

    # Special function for other guilds to call. Arguments are current level
    # and experience points.

    def query_cost_for_level(self, l, e):
        self.level = l
        self.exp = e
        self.get_level()
        if self.next_exp <= self.exp:
            return 0
        return (self.next_exp - self.exp) * 1000 / self.EXP_COST
    
     
    def cost_for_level(self):
    
    
        self.player_ob = self.this_player()
        self.level = self.call_other(self.player_ob, "query_level", 0)
     
        cost = self.raise_cost(self.player_ob.query_str())
        if (cost):
            self.write("Str: " + cost + " experience points.\n")
        else:
            self.write("Str: Not possible.\n")
     
        cost = self.raise_cost(self.player_ob.query_con())
        if (cost):
            self.write("Con: " + cost + " experience points.\n")
        else:
            self.write("Con: Not possible.\n")
     
        cost = self.raise_cost(self.player_ob.query_dex())
        if (cost):
            self.write("Dex: " + cost + " experience points.\n")
        else:
            self.write("Dex: Not possible.\n")
     
        cost = self.raise_cost(self.player_ob.query_int())
        if (cost):
            self.write("Int: " + cost + " experience points.\n")
        else:
            self.write("Int: Not possible.\n")
     
        if (self.level >= 20):
            self.write("You will have to seek other ways.\n")
            return True
        
        self.exp = self.call_other(self.player_ob, "query_exp", 0)
        self.get_level(self.level)
        if (self.next_exp <= self.exp):
            self.write("It will cost you nothing to be promoted.\n")
            return True
        
        self.write("It will cost you ") 
        self.write((self.next_exp - self.exp) * 1000 / self.EXP_COST)
        self.write(" gold coins to advance to level ") 
        self.write(self.next_level)
        self.write(".\n")
        return True
    
     
    def advance(self, arg):
     
        if (arg == "con"):
            self.raise_con()
            return True
             
        if (arg == "dex"):        
            self.raise_dex()
            return True        
     
        if (arg == "int"):
            self.raise_int()
            return True
             
        if (arg == "str"):
            self.raise_str()
            return True
             
        if (arg and arg != "level"):
            return False
     
        self.player_ob = self.this_player()
        name_of_player = self.call_other(self.player_ob, "query_name", 0)
        self.level = self.call_other(self.player_ob, "query_level", 0)
        if self.level == -1:
            level = 0
        self.exp = self.call_other(self.player_ob, "query_exp", 0)
        self.title = self.call_other(self.player_ob, "query_title", 0)
        if self.level >= 20:
            self.write("You are still ") 
            self.write(self.title) 
            self.write("\n")
            return True
        
        self.get_level(level)
        if self.next_level == 20 and self.call_other("room/quest_room", "count", 0):
            return True
        if level == 0:
            self.next_exp = self.exp
        cost = (self.next_exp - self.exp) * 1000 / self.EXP_COST
        if self.next_exp > self.exp:
            if self.call_other(self.player_ob, "query_money", 0) < cost:
                self.write("You don't have enough gold coins.\n")
                return True
        
            self.call_other(self.player_ob, "add_money", - cost)
        
        self.say(self.call_other(self.player_ob, "query_name", 0) + " is now level " +
                 self.next_level + ".\n")
        self.call_other(self.player_ob, "set_level", self.next_level)
        self.call_other(self.player_ob, "set_title", self.title)
        if self.exp < self.next_exp:
            self.call_other(self.player_ob, "add_exp", self.next_exp - self.exp)
        if self.next_level < 7:
            self.write("You are now " + name_of_player + " " + self.title +
                       " (level " + self.next_level + ").\n")
            return True
        
        if self.next_level < 14:
            self.write("Well done, " + name_of_player + " " + self.title +
              " (level " + self.next_level + ").\n")
            return True
        
        if self.next_level < 20:
            self.write("Welcome to your new class, mighty one.\n" +
              "You are now " + self.title + " (level " + self.next_level + ").\n")
        
        if self.next_level == 20:
            self.write("A new Wizard has been born.\n")
            self.shout("A new Wizard has been born.\n")
            return True
        
        return True    
     
    def raise_con(self):    
     
        if self.too_high_average():
            return
        lvl = self.this_player().query_con()
        if lvl >= 20:
            self.alas("tough and endurable")
            return
        
        if self.raise_cost(lvl, 1):        
            self.this_player().set_con(lvl + 1)
            self.write("Ok.\n")        
        else:
            self.write("You don't have enough experience.\n")    
     
    def raise_dex(self):
        if self.too_high_average():
            return
        lvl = self.this_player().query_dex()
        if lvl >= 20:
            self.alas("skilled and vigorous")
            return
        if self.raise_cost(lvl, 1):
            self.this_player().set_dex(lvl + 1)
            self.write("Ok.\n")
        else:
            self.write("You don't have enough experience.\n")
     
    def raise_int(self):
        if self.too_high_average():
            return
        lvl = self.this_player().query_int()
        if lvl >= 20:
            self.alas("knowledgeable and wise")
            return
        if self.raise_cost(lvl, 1):
            self.this_player().set_int(lvl + 1)
            self.write("Ok.\n")
        else:
            self.write("You don't have enough experience.\n")
     
    def raise_str(self):
        if self.too_high_average():
            return
        lvl = self.this_player().query_str()
        if lvl >= 20:
            self.alas("strong and powerful")
            return
        if self.raise_cost(lvl, 1):
            self.this_player().set_str(lvl + 1)
            self.write("Ok.\n")
        else:
            self.write("You don't have enough experience.\n")
 
    # Compute cost for raising a stat one level. 'base' is the level that
    # you have now, but never less than 1.

    def raise_cost(self, base, action):
        if base >= 20:
            return 0
        cost = (self.get_next_exp(base) - self.get_next_exp(base - 1)) / self.STAT_COST;
        saldo = self.this_player().query_exp() - self.get_next_exp(self.this_player().query_level()- 1);
        if action == 0:
            return cost;
        if saldo < cost:
            return 0;
        self.this_player().add_exp(-cost);
        return cost

    # Banish a monster name from being used.

    def banish(self, who):
        self.level = self.call_other(self.this_player(), "query_level");
        if self.level < 21:
            return False
        if not who:
            self.write("Who ?\n");
            return True        
        if not self.call_other(self.this_player(), "valid_name", who):
            return True
        if self.restore_object("players/" + who):
            self.write("That name is already used.\n");
            return True
        if self.restore_object("banish/" + who):
            self.write("That name is already banished.\n");
            return True        
        self.banished_by = self.call_other(self.this_player(), "query_name");
        self.title = self.call_other(self.this_player(), "query_title");
        if self.banished_by == "Someone":
            self.write("You must not be invisible!\n");
            return True        
        self.save_object("banish/" + who);
        return True
    
     
    def south(self):
        if self.call_other(self.this_player(), "query_level", 0) < 20:
            self.write("A strong magic force stops you.\n");
            self.say(self.call_other(self.this_player(), "query_name", 0) +
                     " tries to go through the field, but fails.\n");
            return True
        
        self.write("You wriggle through the force field...\n");
        self.call_other(self.this_player(), "move_player", "south#room/adv_inner");
        return True
        
    def list_quests(self, num):
                
        qnumbers = [int(s) for s in num.split() if s.isdigit()]
        if len(qnumbers) == 1 and num:
            self.call_other("room/quest_room", "list", qnumbers[0]);
        else:
            self.call_other("room/quest_room", "count", 0);
        return True
    
     
    def query_drop_castle(self):
        return True
         
    def alas(self, what):
        self.write("Sorry " + self.gnd_prn() + ", but you are already as " + what +
          "\nas any");
        if self.this_player().query_gender() == 0:
            self.write("thing could possibly hope to get.\n");
        else:
            self.write("one could possibly hope to get.\n");
       

    # Check that the player does not have too high average of the stats.

    def too_high_average(self):
        if ((self.this_player().query_con() + self.this_player().query_str() +
                self.this_player().query_int() + self.this_player().query_dex()) // 4) >= self.this_player().query_level() + 3:
            self.write("Sorry " + self.gnd_prn() + ", but you are not of high enough level.\n");
            return True        
        return False
    
     
    def gnd_prn(self):
        gnd = self.this_player().query_gender();
        if gnd == 1: 
            return "sir";
        elif gnd == 2:
            return "madam";
        else: 
            return "best creature";
