import random
import time

from bin.mud_object import Mud_Object
from lib.room.log import LOG_EXP, ROOM_EXP_LIMIT, LOG_FLAGS


INTERVAL_BETWEEN_HEALING = 10
WEAPON_CLASS_OF_HANDS = 3
ARMOUR_CLASS_OF_BARE = 0
KILL_NEUTRAL_ALIGNMENT = 10
def ADJ_ALIGNMENT(al): ((-al - KILL_NEUTRAL_ALIGNMENT)/4)
NAME_OF_GHOST ="some mist"

class Living(Mud_Object):
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

    # Include this file in objects that "lives".
    # The following variables are defined here:

    time_to_heal = 0   # Count down variable. #
    money = 0           # Amount of money on player. #
    name = None         # Name of object. #
    msgin = None 
    msgout = None # Messages when entering or leaving a room. #
    is_npc = 0 
    brief = 0  # Flags. #
    level = 0     # Level of monster. #
    armour_class = 0 # What armour class of monster. #
    hit_point = 0     # Number of hit points of monster. #
    max_hp = 0 
    max_sp = 0 
    experience = 0     # Experience points of monster. #
    mmsgout = None     # Message when leaving magically. #
    mmsgin = None     # Message when arriving magically. #
    attacker_ob = None# Name of player attacking us. #
    alt_attacker_ob = None# Name of other player also attacking us. #
    weapon_class = 0 # How good weapon. Used to calculate damage. #
    name_of_weapon = None# To see if we are wielding a weapon. #
    head_armour = None# What armour we have. #
    ghost = 0     # Used for monsters that can leave a ghost. #
    local_weight = 0 # weight of items #
    hunted = None
    hunter = None# used in the hunt mode #
    hunting_time = 0 # How long we will stay in hunting mode. #
    cap_name = None # Capital version of "name". #
    spell_points = 0 # Current spell points. #
    spell_name = None 
    spell_cost = 0 
    spell_dam = 0 
    age = 0     # Number of heart beats of this character. #
    is_invis = 0     # True when player is invisible #
    frog = 0     # If the player is a frog #
    whimpy = 0     # Automatically run when low on HP #
    auto_load = None # Special automatically loaded objects. #
    dead = 0     # Are we alive or dead? #
    flags = None     # Bit field of flags #
    
    # All characters have an aligment, depending on how good or chaotic
    # they are.
    # This value is updated when killing other players.
    alignment = 0 
    gender = 0 # 0 means neuter ("it"), 1 male ("he"),  2 female ("she") #
    

    # Character stat variables.
    Str = 0 
    Int = 0 
    Con = 0 
    Dex = 0 
    

    # The following routines are defined for usage:
    # stop_fight        Stop a fight. Good for scroll of taming etc.
    # hit_player        Called when fighting.
    # transfer_all_to:    Transfer all objects to dest.
    # move_player:        Called by the object that moves the monster.
    # query_name:        Gives the name to external objects.
    # attacked_by        Tells us who are attacking us.
    # show_stats        Dump local status.
    # stop_wielding    Called when we drop a weapon.
    # stop_wearing        Called when we drop an armour.
    # query_level        Give our level to external objects.
    # query_value        Always return 0. Can't sell this object.
    # query_npc        Return 1 if npc otherwise 0.
    # get            Always return 0. Can't take this object.
    # attack        Should be called from heart_beat. Will maintain attack.
    # query_attack
    # drop_all_money    Used when the object dies.
    # wield        Called by weapons.
    # wear            Called by armour.
    # add_weight        Used when picking up things.
    # heal_self        Enable wizards to heal this object.
    # can_put_and_get    Can look at inventory, but not take things from it.
    # attack_object    Called when starting to attack an object.
    # test_if_any_here    For monsters. Call this one if you suspect no enemy
    #            is here any more.
    #            Return 1 if anyone there, 0 if none.
    # force_us        Force us to do a command.
    # query_spell_points    Return how much spell points the character has.
    # reduce_hit_point    Reduce hit points, but not below 0.
    

    # This routine is called from objects that moves the player.
    # Special: direction "X" means teleport.
    # The argument is "how#where".
    # The second optional argument is an object to move the player to.
    # If the second argument exists, then the first argument is taken
    # as the movement message only.

    def move_player(self, dir_dest, optional_dest_ob):
        raise NotImplementedError
#     {
#         string dir, dest
#         object ob;
#         int is_light, i;
#      
#         if (!optional_dest_ob) {
#         if (sscanf(dir_dest, "%s#%s", dir, dest) != 2) {
#             tell_object(this_object(), "Move to bad dir/dest\n");
#             return;
#         }
#         } else {
#         dir = dir_dest;
#         dest = optional_dest_ob;
#         }
#         hunting_time -= 1;
#         if (hunting_time == 0) {
#         if (hunter)
#             call_other(hunter, "stop_hunter");
#         hunter = 0;
#         hunted = 0;
#         }
#         if (attacker_ob and present(attacker_ob)) {
#         hunting_time = 10;
#         if (!hunter)
#             tell_object(this_object(), "You are now hunted by " +
#                 call_other(attacker_ob, "query_name", 0) + ".\n");
#             hunter = attacker_ob;
#         }
#         is_light = set_light(0);
#         if(is_light < 0)
#         is_light = 0;
#         if(is_light) {
#         if (!msgout)
#             msgout = "leaves";
#         if (ghost)
#             say(NAME_OF_GHOST + " " + msgout + " " + dir + ".\n");
#         else if (dir == "X" and !is_invis)
#             say(cap_name + " " + mmsgout + ".\n");
#         else if (!is_invis)
#             say(cap_name + " " + msgout + " " + dir + ".\n");
#         }
#         move_object(this_object(), dest);
#         is_light = set_light(0);
#         if(is_light < 0)
#         is_light = 0;
#         if (level >= 20) {
#         if (!optional_dest_ob)
#             tell_object(this_object(), "/" + dest + "\n");
#         }
#         if(is_light) {
#         if (!msgin)
#             msgin = "arrives";
#         if (ghost)
#             say(NAME_OF_GHOST + " " + msgin + ".\n");
#         else if (dir == "X" and !is_invis)
#             say(cap_name + " " + mmsgin + ".\n");
#         else if (!is_invis)
#             say(cap_name + " " + msgin + ".\n");
#         }
#         if (hunted and present(hunted))
#             attack_object(hunted);
#         if (hunter and present(hunter))
#             call_other(hunter, "attack_object", this_object());
#         if (is_npc)
#         return;
#         if (!is_light) {
#         self.write("A dark room.\n");
#         return;
#         }
#         ob = environment(this_object());
#         if (brief)
#         self.write(call_other(ob, "short", 0) + ".\n");
#         else
#         call_other(ob, "long", 0);
#         for (i=0, ob=first_inventory(ob); ob; ob = next_inventory(ob)) {
#         if (ob != this_object()) {
#             string short_str;
#             short_str = call_other(ob, "short");
#             if (short_str)
#             self.write(short_str + ".\n");
#         }
#         if (i++ > 40) {
#             self.write("*** TRUNCATED\n");
#             break;
#         }
#         }
#     }
     
 
    # This function is called from other players when they want to make
    # damage to us. We return how much damage we received, which will
    # change the attackers score. This routine is probably called from
    # heart_beat() from another player.
    # Compare this function to reduce_hit_point(dam).
    def hit_player(self, dam):
        raise NotImplementedError
#     {
#         if (!attacker_ob)
#         set_heart_beat(1);
#         if (!attacker_ob and this_player() != this_object())
#         attacker_ob = this_player();
#         else if (!alt_attacker_ob and attacker_ob != this_player() and
#              this_player() != this_object())
#         alt_attacker_ob = this_player();
#         # Don't damage wizards too much ! #
#         if (level >= 20 and !is_npc and dam >= hit_point) {
#         tell_object(this_object(),
#                 "Your wizardhood protects you from death.\n");
#         return 0;
#         }
#         if(dead)
#         return 0;    # Or someone who is dead #
#         dam -= random(armour_class + 1);
#         if (dam <= 0)
#         return 0;
#         if (dam > hit_point+1)
#         dam = hit_point+1;
#         hit_point = hit_point - dam;
#         if (hit_point<0) {
#         object corpse;
#         # We died ! #
#          
#         if (!is_npc and !query_ip_number(this_object())) {
#             # This player is linkdead. #
#             self.write(cap_name + " is not here. You cannot kill a player who is not logged in.\n");
#             hit_point = 20;
#             stop_fight();
#             if (this_player())
#                 this_player().stop_fight();
#                 return 0;
#         }
#      
#         dead = 1;
#         if (hunter)
#             call_other(hunter, "stop_hunter");
#         hunter = 0;
#         hunted = 0;
#         say(cap_name + " died.\n");
#         experience = 2 * experience / 3;    # Nice, isn't it ? #
#         hit_point = 10;
#         # The player killing us will update his alignment ! #
#         # If he exist #
#         if(attacker_ob) {
#             call_other(attacker_ob, "add_alignment",
#                ADJ_ALIGNMENT(alignment));
#             call_other(attacker_ob, "add_exp", experience / 35);
#         }
#         corpse = clone_object("obj/corpse");
#         call_other(corpse, "set_name", name);
#         transfer_all_to(corpse);
#         move_object(corpse, environment(this_object()));
#         if (!call_other(this_object(), "second_life", 0))
#             destruct(this_object());
#         if (!is_npc)
#             save_object("players/" + name);
#         }
#         return dam;
#     }
     
    def transfer_all_to(self, dest):    
     
        for ob in self.this_object().inventory():
            # Beware that drop() might destruct the object. #
            if self.call_other(ob, "drop", 1) and ob:
                self.move_object(ob, dest)
        
        self.local_weight = 0
        if self.money == 0:
            return
        ob = self.clone_object("obj/money")
        self.call_other(ob, "set_money", self.money)
        self.move_object(ob, dest)
        self.money = 0
    
     
    def query_name(self):
        if self.ghost:
            return NAME_OF_GHOST
        return self.cap_name
    
     
    def query_alignment(self):
        return self.alignment
         
    def query_npc(self):
        return self.is_npc
     
    # This routine is called when we are attacked by a player.
    def attacked_by(self, ob):    
        if not self.attacker_ob:
            self.attacker_ob = ob
            self.set_heart_beat(1)
            return
        
        if not self.alt_attacker_ob:
            self.alt_attacker_ob = ob
            return
     
    def show_stats(self):    
        self.write(self.short() + "\nlevel:\t" + self.level +  
        "\ncoins:\t" + self.money +
          "\nhp:\t" + self.hit_point +
          "\nmax:\t" + self.max_hp +
          "\nspell\t" + self.spell_points +
          "\nmax:\t" + self.max_sp)
        self.write("\nep:\t") 
        self.write(self.experience)
        self.write("\nac:\t") 
        self.write(self.armour_class)
        if self.head_armour:
            self.write("\narmour: " + self.call_other(self.head_armour, "rec_short", 0))
        self.write("\nwc:\t") 
        self.write(self.weapon_class)
        if self.name_of_weapon:
            self.write("\nweapon: " + self.call_other(self.name_of_weapon, "query_name", 0))
        self.write("\ncarry:\t" + self.local_weight)
        if self.attacker_ob:
            self.write("\nattack: " + self.call_other(self.attacker_ob, "query_name"))
        if self.alt_attacker_ob:
            self.write("\nalt attack: " + self.call_other(self.alt_attacker_ob, "query_name"))
        self.write("\nalign:\t" + self.alignment + "\n")
        self.write("gender:\t" + self.query_gender_string() + "\n")
        i = self.call_other(self.this_object(), "query_quests", 0)
        if i:
            self.write("Quests:\t" + i + "\n")
        self.write(self.query_stats())
        self.show_age()
    
     
    def stop_wielding(self):    
        if not self.name_of_weapon:
            # This should not happen ! #
            self.log_file("wield_bug", "Weapon not wielded !\n")
            self.write("Bug ! The weapon was marked as wielded ! (fixed)\n")
            return
        
        self.call_other(self.name_of_weapon, "un_wield", self.dead)
        self.name_of_weapon = None
        self.weapon_class = 0
    
     
    def stop_wearing(self, name):
        if not self.head_armour:
            # This should not happen ! #
            self.log_file("wearing_bug", "armour not worn!\n")
            self.write("This is a bug, no head_armour\n")
            return
        
        self.head_armour = self.call_other(self.head_armour, "remove_link", name)
        if self.head_armour and self.objectp(self.head_armour):
            self.armour_class = self.call_other(self.head_armour, "tot_ac")
        else:
            self.armour_class = 0
            self.head_armour = None
        
        if not self.is_npc:
            if not self.dead:
                self.say(self.cap_name + " removes " + self.name + ".\n")
        self.write("Ok.\n")
    
     
    def query_level(self):
        return self.level
    
     
    # This object is not worth anything in the shop ! #
    def query_value(self):
        return 0
     
    # It is never possible to pick up a player ! #
    def get(self):
        return 0
     
    # Return true if there still is a fight.
    def attack(self):
        raise NotImplementedError
#     {
#         int tmp
#         int whit
#         string name_of_attacker;
#      
#         if (!attacker_ob) {
#         spell_cost = 0;
#         return 0;
#         }
#         name_of_attacker = call_other(attacker_ob, "query_name", 0);
#         if (!name_of_attacker or name_of_attacker == NAME_OF_GHOST or
#         environment(attacker_ob) != environment(this_object())) {
#         if (!hunter and name_of_attacker and
#             !call_other(attacker_ob, "query_ghost", 0))
#         {
#             tell_object(this_object(), "You are now hunting " +
#                 call_other(attacker_ob, "query_name", 0) + ".\n");
#             hunted = attacker_ob;
#             hunting_time = 10;
#         }
#         attacker_ob = 0;
#         if (!alt_attacker_ob)
#             return 0;
#         attacker_ob = alt_attacker_ob;
#         alt_attacker_ob = 0;
#         if (attack()) {
#             if (attacker_ob)
#             tell_object(this_object(),
#                     "You turn to attack " +
#                     attacker_ob.query_name() + ".\n");
#             return 1;
#         }
#         return 0;
#         }
#         if (spell_cost) {
#         spell_points -= spell_cost;
#         tell_object(attacker_ob, "You are hit by a " + spell_name + ".\n");
#         self.write("You cast a " + spell_name + ".\n");
#         }
#         if(name_of_weapon) {
#         whit = call_other(name_of_weapon,"hit",attacker_ob);
#         if (!attacker_ob) {
#             tell_object(this_object(), "CRACK!\nYour weapon broke!\n");
#             log_file("BAD_SWORD", name_of_weapon.short() + ", " +
#                  creator(name_of_weapon) + " XX !\n");
#             spell_cost = 0;
#             spell_dam = 0;
#             destruct(name_of_weapon);
#             weapon_class = 0;
#             return 1;
#         }
#         }
#         if(whit != "miss") {
#         tmp = ((weapon_class + whit) * 2 + Dex) / 3;
#         if (tmp == 0)
#             tmp = 1;
#         tmp = call_other(attacker_ob, "hit_player", 
#                 random(tmp) + spell_dam);
#         } else
#         tmp = 0;
#         tmp -= spell_dam;
#         if (!is_npc and name_of_weapon and tmp > 20 and
#           random(100) < weapon_class - level * 2 / 3 - 14) {
#         tell_object(this_object(), "CRACK!\nYour weapon broke!\n");
#         tell_object(this_object(),
#                 "You are too inexperienced for such a weapon.\n");
#         log_file("BAD_SWORD", name_of_weapon.short() + ", " +
#              creator(name_of_weapon) + "\n");
#         spell_cost = 0;
#         spell_dam = 0;
#         destruct(name_of_weapon);
#         weapon_class = 0;
#         return 1;
#         }
#         tmp += spell_dam;
#         if (tmp == 0) {
#         tell_object(this_object(), "You missed.\n");
#         say(cap_name + " missed " + name_of_attacker + ".\n");
#         spell_cost = 0;
#         spell_dam = 0;
#         return 1;
#         }
#         experience += tmp;
#         tmp -= spell_dam;
#         spell_cost = 0;
#         spell_dam = 0;
#         # Does the enemy still live ? #
#         if (attacker_ob and
#           call_other(attacker_ob, "query_name", 0) != NAME_OF_GHOST) {
#         string how, what;
#         how = " to small fragments";
#         what = "massacre";
#         if (tmp < 30) {
#             how = " with a bone crushing sound";
#             what = "smash";
#         }
#         if (tmp < 20) {
#             how = " very hard";
#             what = "hit";
#         }
#         if (tmp < 10) {
#             how = " hard";
#             what = "hit";
#         }
#         if (tmp < 5) {
#             how = "";
#             what = "hit";
#         }
#         if (tmp < 3) {
#             how = "";
#             what = "grazed";
#         }
#         if (tmp == 1) {
#             how = " in the stomach";
#             what = "tickled";
#         }
#         tell_object(this_object(), "You " + what + " " + name_of_attacker +
#                 how + ".\n");
#         tell_object(attacker_ob, cap_name + " " + what + " you" + how +
#                 ".\n");
#         say(cap_name + " " + what + " " + name_of_attacker + how +
#                 ".\n", attacker_ob);
#         return 1;
#         }
#         tell_object(this_object(), "You killed " + name_of_attacker + ".\n");
#         attacker_ob = alt_attacker_ob;
#         alt_attacker_ob = 0;
#         if (attacker_ob)
#         return 1;
#     }
     
    def query_attack(self):
        return self.attacker_ob
     
    def drop_all_money(self, verbose):
        
        if self.money == 0:
            return
        mon = self.clone_object("obj/money")
        self.call_other(mon, "set_money", self.money)
        self.move_object(mon, self.environment())
        if verbose:
            self.say(self.cap_name + " drops " + self.money + " gold coins.\n")
            self.tell_object(self.this_object(), "You drop " + self.money + " gold coins.\n")
        
        self.money = 0
    
     
    # Wield a weapon. #
    def wield(self, w):
        if self.name_of_weapon:
            self.stop_wielding()
        self.name_of_weapon = w
        self.weapon_class = self.call_other(w, "weapon_class", 0)
        self.say(self.cap_name + " wields " + self.call_other(w, "query_name", 0) + ".\n")
        self.write("Ok.\n")
         
    # Wear some armour. #
    def wear(self, a):
        old = None
     
        if self.head_armour:
            old = self.call_other(self.head_armour, "test_type", self.call_other(a, "query_type"))
            if old:
                return old
            old = self.head_armour
            self.call_other(a, "link", old)
        
        self.head_armour = a
        # Calculate new ac #
        self.armour_class = self.call_other(self.head_armour, "tot_ac")
        self.say(self.cap_name + " wears " + self.call_other(a, "query_name", 0) + ".\n")
        self.write("Ok.\n")
        return False
    
     
    def add_weight(self, w):
        if ((w + self.local_weight) > (self.Str + 10)) and (self.level < 20):
            return False
        self.local_weight += w
        return True    
     
    def heal_self(self, h):
        if h <= 0:
            return
        self.hit_point += h
        if self.hit_point > self.max_hp:
            self.hit_point = self.max_hp
        self.spell_points += h
        if self.spell_points > self.max_sp:
            self.spell_points = self.max_sp
         
    def restore_spell_points(self, h):
        self.spell_points += h
        if self.spell_points > self.max_sp:
            self.spell_points = self.max_sp
         
    def can_put_and_get(self, arg):
        return arg != 0
     
    def attack_object(self, ob):
        if self.call_other(ob, "query_ghost", 0):
            return
        self.set_heart_beat(1)    # For monsters, start the heart beat #
        if self.attacker_ob == ob:
            self.attack()
            return
       
        if self.alt_attacker_ob == ob:
            self.alt_attacker_ob = self.attacker_ob
            self.attacker_ob = ob
            self.attack()
            return
       
        if not self.alt_attacker_ob:
            self.alt_attacker_ob = self.attacker_ob
        self.attacker_ob = ob
        self.call_other(self.attacker_ob, "attacked_by", self.this_object())
        self.attack()
     
    def query_ghost(self):
        return self.ghost
     
    def zap_object(self, ob):    
        self.call_other(ob, "attacked_by", self.this_object())
        self.say(self.cap_name + " summons a flash from the sky.\n")
        self.write("You summon a flash from the sky.\n")
        self.experience += self.call_other(ob, "hit_player", 100000)
        self.write("There is a big clap of thunder.\n\n")
         
    def missile_object(self, ob):
        if self.spell_points < 10:
            self.write("Too low on power.\n")
            return
        
        self.spell_name = "magic missile"
        self.spell_dam = random.randrange(1,21)
        self.spell_cost = 10
        self.attacker_ob = ob

    def shock_object(self, ob):
        if self.spell_points < 15:
            self.write("Too low on power.\n")
            return
        
        self.spell_name = "shock"
        self.spell_dam = random.randrange(1,31)
        self.spell_cost = 15
        self.attacker_ob = ob
     
    def fire_ball_object(self,ob):    
        if self.spell_points < 20:
            self.write("Too low on power.\n")
            return
        
        self.spell_name = "fire ball"
        self.spell_dam = random.randrange(1,41)
        self.spell_cost = 20
        self.attacker_ob = ob
    
     
    # If no one is here (except ourself), then turn off the heart beat.
    def test_if_any_here(self):
        ob = self.environment()
        if not ob:
            return
        for ob in self.environment():
            if (ob != self.this_object() and self.living(ob) and not self.call_other(ob, "query_npc")):
                return True
        return False
     
    def show_age(self): 
        self.write("age:\t")
        i = self.age
        if i//43200:
            self.write(i//43200 + " days ")
            i = i - (i//43200)*43200        
        if i//1800:
            self.write(i//1800 + " hours ")
            i = i  - (i//1800)*1800        
        if i//30:
            self.write(i//30 + " minutes ")
            i = i - (i//30)*30        
        self.write( (i*2) + " seconds.\n")
     
    def stop_hunter(self):    
        self.hunter = None
        self.tell_object(self.this_object(), "You are no longer hunted.\n")
    
    # This function remains only because of compatibility, as command() now
    # can be called with an object as argument.
    def force_us(self, cmd):
        if not self.this_player() or (self.this_player().query_level() <= self.level) or \
            self.query_ip_number(self.this_player()) == 0:
            self.tell_object(self.this_object(), self.this_player().query_name() +
                             " failed to force you to " + cmd + "\n")
            return        
        self.command(cmd)
    
     
    # This is used by the shop etc. #
    def add_money(self, m):        
        if LOG_EXP:
            if self.this_player() and \
                self.this_player() != self.this_object() and \
                self.query_ip_number(self.this_player()) and \
                self.query_ip_number(self.this_object()) and \
                self.level < 20 and m >= ROOM_EXP_LIMIT:
                self.log_file("EXPERIENCE", time.time() + " " + self.name + "(" + self.level + 
                ") " + m + " money by " + self.this_player().query_real_name() +
                "(" + self.this_player().query_level() + ")\n")
        
        self.money = self.money + m
        if self.level <= 19 and not self.is_npc:
            self.add_worth(m)
    
     
    def query_money(self):
        return self.money
         
    def query_exp(self):
        return self.experience
    
     
    def query_frog(self):
        return self.frog
         
    def frog_curse(self, arg):
        if (arg):
            if (self.frog):
                return True
            self.tell_object(self.this_object(), "You turn into a frog !\n")
            self.frog = True
            return True
        
        self.tell_object(self.this_object(), "You turn HUMAN again.\n")
        self.frog = False
        return False
    
     
    def run_away(self):
        here = self.environment()
        i = 0
        j = random.randrange(6)
        while i<6 and here == self.environment():
            i += 1
            j += 1
            if (j > 6):
                j = 1
            if (j == 1): self.command("east")
            if (j == 2): self.command("west")
            if (j == 3): self.command("north")
            if (j == 4): self.command("south")
            if (j == 5): self.command("up")
            if (j == 6): self.command("down")
        
        if (here == self.environment()):
            self.say(self.cap_name + " tried, but failed to run away.\n", self.this_object())
            self.tell_object(self.this_object(),
            "Your legs tried to run away, but failed.\n")
        else:
            self.tell_object(self.this_object(), "Your legs run away with you!\n")        
    
     
    def query_hp(self):
        return self.hit_point
     
    def query_wimpy(self):
        return self.whimpy
     
    def query_current_room(self):
        return self.file_name(self.environment(self.this_object()))    
     
    def query_spell_points(self):
        return self.spell_points    
     
    def stop_fight(self):
        self.attacker_ob = self.alt_attacker_ob
        self.alt_attacker_ob = None
         
    def query_wc(self):
        return self.weapon_class    
     
    def query_ac(self):
        return self.armour_class
         
    def reduce_hit_point(self, dam):
        o = None
        
        if self.this_player() != self.this_object():
            self.log_file("REDUCE_HP", self.query_name()+" by ")
            if not self.this_player():
                self.log_file("REDUCE_HP","?\n")
            else:
                self.log_file("REDUCE_HP", self.this_player().query_name())
                o=self.previous_object()
                if o:
                    self.log_file("REDUCE_HP", " " + self.file_name(o) + ", " +
                     o.short() + " (" + self.creator(o) + ")\n")
                else:
                    self.log_file("REDUCE_HP", " ??\n")
        
        
        # this will detect illegal use of reduce_hit_point in weapons #
        self.hit_point -= dam
        if self.hit_point <= 0:
            self.hit_point = 1
        return self.hit_point
    
     
    def query_age(self):
        return self.age
         
    #----------- Most of the gender handling here: ------------#
     
    def query_gender(self): 
        return self.gender
     
    def query_neuter(self): 
        return not self.gender
     
    def query_male(self): 
        return self.gender == 1
    
    def query_female(self): 
        return self.gender == 2
     
    def set_gender(self, g):
        if g == 0 or g == 1 or g == 2:
            self.gender = g
    
    def set_neuter(self): 
        self.gender = 0 
        
    def set_male(self): 
        self.gender = 1 
        
    def set_female(self): 
        self.gender = 2 
     
    def query_gender_string(self):
        if not self.gender:
            return "neuter"
        elif self.gender == 1:
            return "male"
        else:
            return "female"    
     
    def query_pronoun(self):
        if not self.gender:
            return "it"
        elif self.gender == 1:
            return "he"
        else:
            return "she"
    
     
    def query_possessive(self):
        if not self.gender:
            return "its"
        elif self.gender == 1:
            return "his"
        else:
            return "her"
         
    def query_objective(self):
        if not self.gender:
            return "it"
        elif self.gender == 1:
            return "him"
        else:
            return "her"
         
    # Flags manipulations. You are not supposed to do this arbitrarily.
    # Every wizard can allocate a few bits from the administrator, which
    # he then may use. If you mainpulate bits that you don't know what they
    # are used for, unexpected things can happen.
    def set_flag(self, n):
        if self.flags == 0:
            self.flags = ""

        if LOG_FLAGS:            
        
            self.log_file("FLAGS", self.name + " bit " + n + " set\n")
            if self.previous_object():
                if self.this_player() and self.this_player() != self.this_object() and  self.query_ip_number(self.this_player()):
                    self.log_file("FLAGS", "Done by " +
                        self.this_player().query_real_name() + " using " +
                        self.file_name(self.previous_object()) + ".\n")
            
        
        self.flags = self.set_bit(self.flags, n)
    
     
    def test_flag(self,n):
        if self.flags == 0:
            self.flags = ""
        return self.test_bit(self.flags, n)
    
     
    def clear_flag(self, n):
        if self.flags == 0:
            self.flags = ""
        if LOG_FLAGS:
            self.log_file("FLAGS", self.name + " bit " + n + " cleared\n")
            if self.previous_object():
                if self.this_player() and self.this_player() != self.this_object() and self.query_ip_number(self.this_player()):
                    self.log_file("FLAGS", "Done by " + \
                         self.this_player().query_real_name() + " using " + \
                         self.file_name(self.previous_object()) + ".\n")            
     
        self.flags = self.clear_bit(self.flags, n)
        return True

     
    def query_stats(self):
        return "str:\t" + self.Str + \
          "\nint:\t" + self.Int + \
          "\ncon:\t" + self.Con + \
          "\ndex:\t" + self.Dex + "\n"
     
    def query_str(self): return self.Str
    def query_int(self): return self.Int
    def query_con(self): return self.Con
    def query_dex(self): return self.Dex
     
    # Note that previous object is 0 if called from ourselves. #
    def set_str(self, i):
        if i<1 or i > 20:
            return
        self.Str = i
         
    def set_int(self, i):
        if i<1 or i > 20:
            return
        self.Int = i
        self.max_sp = 42 + self.Int * 8    
     
    def set_con(self, i):
        if i<1 or i > 20:
            return
        self.Con = i
        self.max_hp = 42 + self.Con * 8
         
    def set_dex(self, i):
        if i<1 or i > 20:
            return
        self.Dex = i
    
