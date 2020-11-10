'''
# A general purpose monster. Clone this object,
# and call local functions to configure it.

# If you are going to copy this file, in the purpose of changing
# it a little to your own need, beware:
#
# First try one of the following:
#
# 1. Do clone_object(), and then configure it. This object is specially
#    prepared for configuration.
#
# 2. If you still is not pleased with that, create a new empty
#    object, and make an inheritance of this object on the first line.
#    This will automatically copy all variables and functions from the
#    original object. Then, add the functions you want to change. The
#    original function can still be accessed with '::' prepended on the name.

# The maintainer of this LPmud might become sad with you if you fail
# to do any of the above. Ask other wizards if you are doubtful.
#
# The reason of this, is that the above saves a lot of memory.
'''
import random

from lib.obj.living import Living, INTERVAL_BETWEEN_HEALING


class Monster(Living):
    # The heart beat is always started in living.h when we are attacked.
    
    short_desc = None
    long_desc = None
    alias = None
    alt_name = None
    race = None
    move_at_reset = False
    aggressive = False
    kill_ob = None
    healing = False        # True if this monster is healing itself. #
    
    chat_head = None    # Vector with all chat Strings. #
    chat_chance = 0
    
    a_chat_head = None    # Vector with all a_chat Strings. #
    a_chat_chance = 0
    
    talk_ob = None
    talk_func = None    # Vector of functions. #
    talk_match = None    # Vector of Strings. #
    talk_type = None    # Vector of types. #
    the_text = None
    have_text = False
    
    
    dead_ob = None
    init_ob = None
    
    random_pick = 0
    
    spell_chance = 0
    spell_dam = 0
    spell_mess1 = None
    spell_mess2 = None
    me = None
    create_room = None
    
    busy_catch_tell = False

    
    
    def reset(self,arg):    
        if arg:
            if self.move_at_reset:
                self.random_move();
            return
        
        self.is_npc = 1;
        self.enable_commands();
        self.me = self.this_object();
        self.create_room = self.environment(self.me);
    
    
    def random_move(self):   
     
        n = random.randrange(4);
        if (n == 0):
            self.command("west");
        elif (n == 1):
            self.command("east");
        elif (n == 2):
            self.command("south");
        elif (n == 3):
            self.command("north");
    
    
    def short(self):
        return self.short_desc;    
    
    def long(self):
        self.write(self.long_desc)
        
    def id(self,arg):
        return arg == self.name or arg == self.alias or arg == self.race or arg == self.alt_name
    
    def heart_beat(self):
        raise NotImplementedError
#         int c;
#     
#         age += 1;
#         if(!test_if_any_here()) {
#         if(have_text and talk_ob) {
#             have_text = 0;
#             test_match(the_text);
#         } else {
#             set_heart_beat(0);
#             if (!healing)
#             heal_slowly();
#             return;
#         }
#         }
#         if (kill_ob and present(kill_ob, environment(this_object()))) {
#         if (random(2) == 1)
#             return;        # Delay attack some #
#         attack_object(kill_ob);
#         kill_ob = 0;
#         return;
#         }
#         if (attacker_ob and present(attacker_ob, environment(this_object())) and
#           spell_chance > random(100)) {
#         say(spell_mess1 + "\n", attacker_ob);
#         tell_object(attacker_ob, spell_mess2 + "\n");
#         call_other(attacker_ob, "hit_player", random(spell_dam));
#         }
#         attack();
#         if (attacker_ob and whimpy and hit_point < max_hp/5)
#         run_away();
#         if(chat_chance or a_chat_chance){
#         c = random(100);
#         if(attacker_ob and a_chat_head) {
#             if(c < a_chat_chance){
#             c = random(sizeof(a_chat_head));
#             tell_room(environment(), a_chat_head[c]);
#             }
#         } else {
#             if(c < chat_chance and chat_chance){
#             c = random(sizeof(chat_head));
#             tell_room(environment(), chat_head[c]);
#             }
#         }
#         }
#         if(random_pick) {
#         c = random(100);
#         if(c < random_pick)
#             pick_any_obj();
#         }
#         if(have_text and talk_ob) {
#         have_text = 0;
#         test_match(the_text);
#         }
#     
    
    def can_put_and_get(self, arg):    
        if not arg:
            return False
        return True
    
    def catch_tell(self,arg):
        if self.busy_catch_tell:
            return;
        self.busy_catch_tell = True
        if self.talk_ob:
            if self.have_text:
                self.test_match(self.the_text);
                self.the_text = arg;
            else:
                self.the_text = arg;
                self.have_text = True
        self.busy_catch_tell = False
    
    
    
    # Call the following functions to setup the monster.
    # Call them in the order they appear.
    
    def set_name(self,n):
        self.name = n;
        self.set_living_name(n);
        self.alignment = 0;        # Neutral monster #
        self.cap_name = self.capitalize(n);
        self.short_desc = self.cap_name;
        self.long_desc = "You see nothing special.\n";
    
    
    def set_level(self, l):
        self.level = l;
        self.Str = l; 
        self.Int = l; 
        self.Con = l; 
        self.Dex = l;
        self.weapon_class = self.level/2 + 3;
        self.armour_class = self.level/4;
        self.hit_point = 50 + (self.level - 1) * 8;    # Same as a player #
        self.max_hp = self.hit_point;
        self.spell_points = self.max_hp;
        self.experience = self.call_other("room/adv_guild", "query_cost", l-1);
        # This is for level 1 monsters. #
        if self.experience == 0:
            self.experience = random.randrange(500);
    
    
    # Optional #
    def set_alias(self, a):
        self.alias = a
        
    # Optional #
    def set_alt_name(self, a):
        self.alt_name = a
        
    # Optional #
    def set_race(self,r):
        self.race = r
        
    # optional #
    def set_hp(self,hp):
        self.max_hp = hp
        self.hit_point = hp
    
    # optional. Can only be lowered #
    def set_ep(self,ep):
        if ep < self.experience:
            self.experience = ep
    
    # optional #
    def set_al(self,al):
        self.alignment = al
    
    # optional #
    def set_short(self,sh):
        self.short_desc = sh
        self.long_desc = self.short_desc + "\n"
    
    # optional #
    def set_long(self, lo):
        self.long_desc = lo
    
    # optional #
    def set_wc(self, wc):
        if wc > self.weapon_class:
            self.weapon_class = wc
    
    # optional #
    def set_ac(self, ac):
        if ac > self.armour_class:
            self.armour_class = ac
    
    # optional #
    def set_move_at_reset(self):
        self.move_at_reset = True
    
    # optional
    # 0: Peaceful.
    # 1: Attack on sight.
    def set_aggressive(self, a):
        self.aggressive = a
    
    
    # Now some functions for setting up spells !
    
    # The percent chance of casting a spell.
    def set_chance(self, c):
        self.spell_chance = c
    
    # Message to the victim. #
    def set_spell_mess1(self, m):
        self.spell_mess1 = m;    
    
    def set_spell_mess2(self, m):
        self.spell_mess2 = m;
        
    def set_spell_dam(self, d):
        self.spell_dam = d
        
    # Set the frog curse. #
    def set_frog(self):
        self.frog = True
        
    # Set the whimpy mode #
    def set_whimpy(self):
        self.whimpy = True
    
    # Force the monster to do a command. The force_us() function isn't
    # always good, because it checks the level of the caller, and this function
    # can be called by a room.
    def init_command(self, cmd):
        self.command(cmd)    
    
    def load_chat(self, chance, args):
        if isinstance(args, list):  # Just ensure that it is an array. #
            self.chat_head = args;
            self.chat_chance = chance;
        
    # Load attack chat #    
    def load_a_chat(self, chance, args):
        if isinstance(args, list):  # Just ensure that it is an array. #
            self.a_chat_head = args;
            self.a_chat_chance = chance;
        
    # Catch the talk #    
    def set_match(self, ob, func, typ, match):

        if (len(func) != len(type) or len(match) != len(typ)):
            return;
        self.talk_ob = ob;
        self.talk_func = func;
        self.talk_type = typ;
        self.talk_match = match;
        self.say("talk match length " + len(func) + "\n");
        
    def set_dead_ob(self,ob):
        self.dead_ob = ob;
    
    def second_life(self):
        if self.dead_ob:
            return self.call_other(self.dead_ob,"monster_died",self.this_object())
    
    def set_random_pick(self, r):
        self.random_pick = r
        
    def pick_any_obj(self):
        for ob in self.environment(self.this_object()).inventory():
            if (self.call_other(ob, "get", 0) and self.call_other(ob, "short")): 
                weight = self.call_other(ob, "query_weight", 0);
                if not self.add_weight(weight): 
                    self.say(self.cap_name + " tries to take " + self.call_other(ob, "short", 0) + " but fails.\n");
                    return;
                self.move_object(ob, self.this_object())
                self.say(self.cap_name + " takes " + self.call_other(ob, "short", 0) + ".\n");
                if self.call_other(ob, "weapon_class", 0):
                    self.call_other(ob, "wield", self.call_other(ob,"query_name"));
                elif self.call_other(ob, "armour_class", 0):
                    self.call_other(ob, "wear", self.call_other(ob,"query_name"));
                return;            
    
    def set_init_ob(self, ob):
        self.init_ob = ob;    
    
    def init(self):
    
        self.create_room = self.environment(self.me);
        if self.this_player() == self.me:
            return;
        if self.init_ob:
            if self.call_other(self.init_ob,"monster_init",self.this_object()):
                return;
        if self.attacker_ob:
            self.set_heart_beat(1); # Turn on heart beat #
        
        if self.this_player() and not self.call_other(self.this_player(),"query_npc"):
            self.set_heart_beat(1);
        if self.aggressive:
            self.kill_ob = self.this_player();
    
    def query_create_room(self):
        return self.create_room;
    
    def query_race(self):
        return self.race;
    
    def test_match(self, arg): 
       
        i = 0
        typ = None
        
        while i < len(self.talk_match):
            if self.talk_type[i]:
                typ = self.talk_type[i];
            match = self.talk_match[i]
            if match == 0:
                match = "";
            if self.talk_func[i]:
                func = self.talk_func[i]
                
            who = None
            arg1 = None
            
            if arg.find(typ+match):
                who = arg[:arg.find(" ")]
                arg1 = arg[arg.find(typ+match) + len(typ+match) +1 :-1]
                return self.call_other(self.talk_ob, func, arg);
            elif arg.find(typ + " " + match):
                who = arg[:arg.find(" ")]
                arg1 = arg[arg.find(typ+" "+match) + len(typ+" "+match) +1 :-1]
                return self.call_other(self.talk_ob, func, arg);
                
#             if (sscanf(arg,"%s " + typ + match + " %s\n",who,arg1) == 2 or
#                sscanf(arg,"%s " + typ + match + "\n",who) == 1 or
#                sscanf(arg,"%s " + typ + match + "%s\n",who,arg1) == 2 or
#                sscanf(arg,"%s " + typ + " " + match + "\n",who) == 1 or
#                sscanf(arg,"%s " + typ + " " + match + " %s\n",who,arg1) == 2):            
                return self.call_other(self.talk_ob, func, arg);
            
            i += 1
        
    
    # The monster will heal itself slowly.
    def heal_slowly(self):
    
        self.hit_point += 120 // (INTERVAL_BETWEEN_HEALING * 2);
        if self.hit_point > self.max_hp:
            self.hit_point = self.max_hp
        self.spell_points += 120 // (INTERVAL_BETWEEN_HEALING * 2)
        if self.spell_points > self.max_hp:
            self.spell_points = self.max_hp
        self.healing = True
        if self.hit_point < self.max_hp or self.spell_points < self.max_hp:
            self.call_out("heal_slowly", 120)
        else:
            self.healing = True
    
