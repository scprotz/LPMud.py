
import sys
import time

from bin import config, comm, simulate, call_out, wiz_list, interpret, \
    mud_object


current_time = 0  # The 'current_time' is updated at every heart beat.
current_heart_beat = None
time_to_call_heart_beat = 0
heart_beat_list = []
_next_time = 0

comm_time_to_call_heart_beat = 0  # this is set by interrupt, #


def clear_state():
    """
    There are global variables that must be zeroed before any execution.
    In case of errors, there will be a longjmp(), and the variables will
    have to be cleared explicitely. They are normally maintained by the
    code that use them.

    This routine must only be called from top level, not from inside
    stack machine execution (as stack will be cleared).
    """
    simulate.current_object = None
    simulate.command_giver = None
    simulate.current_interactive = None
    simulate.previous_ob = None


def logon(ob):
    save = simulate.current_object

    # current_object must be set here, so that the static "logon" in
    # player.c can be called.

    simulate.current_object = ob
    ret = interpret.apply("logon", ob, 0)
    if ret is None:
        comm.add_message("prog %s:\n" % ob.name)
        raise Exception("Could not find logon on the player %s\n" % ob.name)

    simulate.current_object = save


def parse_command(arg, ob):
    """
    Take a player command and parse it.
    The command can also come from a NPC.
    Beware that 'str' can be modified and extended !
    """
    save = simulate.command_giver

    simulate.command_giver = ob
    res = simulate.player_parser(arg)
    simulate.command_giver = save
    return res


def backend():
    """
    This is the backend. We will stay here for ever (almost).
    """

    buff = []

    print("Setting up ipc.")
    sys.stdout.flush()
    comm.prepare_ipc()

    ''' maybe add for unix/linux/osx later '''
    # (void)signal(SIGHUP, startshutdowngame);

    call_heart_beat()

    while True:

        # The call of clear_state() should not really have to be done
        # once every loop. However, there seem to be holes where the
        # state is not consistent. If these holes are removed,
        # then the call of clear_state() can be moved to just before the
        # while() - statement. *sigh* /Lars

        clear_state()
        remove_destructed_objects()  # marion - before ref checks! #
        if simulate.game_is_being_shut_down:
            simulate.shutdowngame()

        buff.clear()
        if comm.get_message(buff):
            # Now we have a string from the player. This string can go to
            # one of several places. If it is prepended with a '!', then
            # it is an escape from the 'ed' editor, so we send it
            # as a command to the parser.
            # If any object function is waiting for an input string, then
            # send it there.
            # Otherwise, send the string to the parser.
            # The player_parser() will find that current_object is 0, and
            # then set current_object to point to the object that defines
            # the command. This will enable such functions to be static.

            simulate.current_object = None
            simulate.current_interactive = simulate.command_giver

            if buff[0] == '!' and simulate.command_giver.parent:
                parse_command(buff+1, simulate.command_giver)
            elif comm.call_function_interactive(
                    simulate.command_giver.interactive, buff):
                pass    # Do nothing ! #
            else:
                parse_command(buff, simulate.command_giver)

            # Print a prompt if player is still here.
            if simulate.command_giver.interactive:
                comm.print_prompt()

        if time_to_call_heart_beat:
            call_heart_beat()
        simulate.command_giver = None


def look_for_objects_to_swap():
    global _next_time
    """
    Despite the name, this routine takes care of several things.
    It will loop through all objects once every 10 minutes.

    If an object is found in a state of not having done reset, and the
    delay to next reset has passed, then reset() will be done.

    If the object has a existed more than the time limit given for swapping,
    then 'clean_up' will first be called in the object, after which it will
    be swapped out if it still exists.

    There are some problems if the object self-destructs in clean_up, so
    special care has to be taken of how the linked list is used.
    """

    if backend.current_time < _next_time:
        return  # Not time to look yet #
    _next_time = current_time + 15 * 60  # Next time is in 15 minutes #

    # Objects object can be destructed, which means that
    # next object to investigate is saved in next_ob. If very unlucky,
    # that object can be destructed too. In that case, the loop is simply
    # restarted.

    for ob in simulate.obj_list:

        if ob.O_DESTRUCTED:
            continue

        # Should this object have reset(1) called ?

        if ob.next_reset < backend.current_time and not ob.O_RESET_STATE:
            mud_object.reset_object(ob, 1)


def call_heart_beat():
    """
    Call all heart_beat() functions in all objects.  Also call the next reset,
    and the call out.
    We do heart beats by moving each object done to the end of the heart beat
    list before we call its function, and always using the item at the head
    of the list as our function to call.  We keep calling heart beats until
    a timeout or we have done num_heart_objs calls.  It is done this way so
    that objects can delete heart beating objects from the list from within
    their heart beat without truncating the current round of heart beats.

    Set command_giver to current_object if it is a living object. If the object
    is shadowed, check the shadowed object if living. There is no need to save
    the value of the command_giver, as the caller resets it to 0 anyway.
    """

    hide_current = simulate.current_object

    time_to_call_heart_beat = 0  # interrupt loop if we take too long #
    comm_time_to_call_heart_beat = 0

    alarm(2)  # set or push the alarm to 2 seconds in the future #

    backend.current_time = time.time()
    simulate.current_interactive = None

    if comm.num_player > 0 and len(heart_beat_list) > 0:

        for ob in heart_beat_list:
            if comm_time_to_call_heart_beat:
                break

            if not ob.O_HEART_BEAT:
                raise Exception("Heart beat not set " +
                                "in object on heart beat list!")

            simulate.current_object = ob
            backend.current_heart_beat = ob
            simulate.command_giver = ob
            while simulate.command_giver.shadowing:
                simulate.command_giver = simulate.command_giver.shadowing
            if not simulate.command_giver.O_ENABLE_COMMANDS:
                simulate.command_giver = None
            if ob.user:
                ob.user.heart_beats += 1
            ob.heart_beat()

    simulate.current_object = hide_current
    backend.current_heart_beat = None
    look_for_objects_to_swap()
    call_out.call_out()  # some things depend on this, even without players!
    comm.flush_all_player_mess()
    wiz_list.wiz_decay()


# # 
#  * Take the first object off the heart beat list, place it at the end
#  # 
# static void cycle_hb_list()
# {
#     struct object * ob;
#     if (!hb_list)
#     fatal("Cycle heart beat list with empty list!");
#     if (hb_list == hb_tail)
#     return; #  1 object on list # 
#     ob = hb_list;
#     hb_list = hb_list . next_heart_beat;
#     hb_tail . next_heart_beat = ob;
#     hb_tail = ob;
#     ob.next_heart_beat = 0;
# }
# 
# # 
#  * add or remove an object from the heart beat list; does the major check...
#  * If an object removes something from the list from within a heart beat,
#  * various pointers in call_heart_beat could be stuffed, so we must
#  * check current_heart_beat and adjust pointers.
#  # 
# 
# int set_heart_beat(ob, to)
#     struct object * ob;
#     int to;
# {
#     struct object * o = hb_list;
#     struct object * oprev = 0;
# 
#     if (ob.flags & O_DESTRUCTED)
#     return 0;
#     if (to)
#     to = 1;
# 
#     while (o and o != ob) {
#     if (!(o.flags & O_HEART_BEAT))
#         fatal("Found disabled object in the active heart beat list!\n");
#     oprev = o;
#     o = o.next_heart_beat;
#     }
# 
#     if (!o and (ob.flags & O_HEART_BEAT))
#     fatal("Couldn't find enabled object in heart beat list!");
#     
#     if (to == ((ob.flags & O_HEART_BEAT) != 0))
#     return(0);
# 
#     if (to) {
#     ob.flags |= O_HEART_BEAT;
#     if (ob.next_heart_beat)
#         fatal("Dangling pointer to next_heart_beat in object!");
#     ob.next_heart_beat = hb_list;
#     hb_list = ob;
#     if (!hb_tail) hb_tail = ob;
#     num_hb_objs++;
#     cycle_hb_list();     #  Added by Linus. 911104 # 
#     }
#     else { #  remove all refs # 
#     ob.flags &= ~O_HEART_BEAT;
#     if (hb_list == ob)
#         hb_list = ob.next_heart_beat;
#     if (hb_tail == ob)
#         hb_tail = oprev;
#     if (oprev)
#         oprev.next_heart_beat = ob.next_heart_beat;
#     ob.next_heart_beat = 0;
#     num_hb_objs--;
#     }
# 
#     return(1);
# }
# # 
#  * sigh.  Another status function.
#  # 
# int heart_beat_status(verbose)
#     int verbose;
# {
#     char buf[20];
# 
#     if (verbose) {
#     add_message("\nHeart beat information:\n");
#     add_message("-----------------------\n");
#     add_message("Number of objects with heart beat: %d, starts: %d\n",
#             num_hb_objs, num_hb_calls);
#     sprintf(buf, "%.2f", perc_hb_probes);
#     add_message("Percentage of HB calls completed last time: %s\n", buf);
#     }
#     return 0;
# }
 

# There is a file with a list of objects to be initialized at
# start up.

def load_first_objects():
 
    print("Loading init file %s" % config.INIT_FILE)
    try:
        f = open(config.INIT_FILE, "r")

        tms1 = time.time()

        for buff in f:

            # comment line #
            if buff[0] == '#':
                continue;

            # clean up extra whitespace #
            buff = buff.strip()

            # empty line #
            if len(buff) == 0:
                continue

            print("Preloading: %s" % buff, end="")
            sys.stdout.flush()
            simulate.find_object(buff)

            tms2 = time.time()

            print(" %.2f" % ((tms2 - tms1) / 60.0))
            tms1 = tms2

            sys.stdout.flush()

        f.close()
    except FileNotFoundError:
        comm.add_message("Anomaly in the fabric of world space.\n")
        print("Error loading file %s" % config.INIT_FILE)

# # 
#  * New version used when not in -o mode. The epilog() in master.c is
#  * supposed to return an array of files (castles in 2.4.5) to load. The array
#  * returned by apply() will be freed at next call of apply(), which means that
#  * the ref count has to be incremented to protect against deallocation.
#  *
#  * The master object is asked to do the actual loading.
#  # 
# void preload_objects(eflag)
#     int eflag;
# {
#     struct vector *prefiles;
#     struct svalue *ret;
#     int ix;
# 
#     push_number(eflag);
#     ret = apply_master_ob("epilog", 1);
# 
#     if ((ret == 0) or (ret.type != T_POINTER))
#     return;
#     else
#     prefiles = ret.u.vec;
# 
#     if ((prefiles == 0) or (prefiles.size < 1))
#     return;
# 
#     prefiles.ref++;
# 
#     ix = -1;
#     if (setjmp(error_recovery_context)) {
#     clear_state();
#     add_message("Anomaly in the fabric of world space.\n");
#     }
#     error_recovery_context_exists = 1;
# 
#     while (++ix < prefiles.size) {
#     if (prefiles.item[ix].type != T_STRING)
#         continue;
# 
#     eval_cost = 0;
#     push_string(prefiles.item[ix].u.string, STRING_MALLOC);
#     (void)apply_master_ob("preload", 1);
# 
# #ifdef MALLOC_malloc
#     resort_free_list();
# #endif
#     }
#     free_vector(prefiles);
#     error_recovery_context_exists = 0;
# }
 
 
def catch_alarm():
    """
    catch alarm, set flag for comms code and heart_beat to catch.
    comms code sets time_to_call_heart_beat for the backend when
    it has completed the current round of player commands.
    """
    comm_time_to_call_heart_beat = True


def remove_destructed_objects():
    """
    All destructed objects are moved int a sperate linked list,
    and deallocated after program execution.
    """
    for ob in simulate.obj_list_destruct:
        simulate.destruct2(ob)
        simulate.obj_list_destruct.remove(ob)


# # 
#  * Append string to file. Return 0 for failure, otherwise 1.
#  # 
# int write_file(file, str)
#     char *file;
#     char *str;
# {
#     FILE *f;
# 
# #ifdef COMPAT_MODE
#     file = check_file_name(file, 1);
# #else
#     file = check_valid_path(file, current_object.eff_user, "write_file", 1);
# #endif
#     if (!file)
#     return 0;
#     f = fopen(file, "a");
#     if (f == 0)
#     error("Wrong permissions for opening file %s for append.\n", file);
#     fwrite(str, strlen(str), 1, f);
#     fclose(f);
#     return 1;
# }
# 
# char *read_file(file,start,len)
#     char *file;
#     int start,len;
# {
#     struct stat st;
#     FILE *f;
#     char *str,*p,*p2,*end,c;
#     int size;
# 
#     if (len < 0) return 0;
# #ifdef COMPAT_MODE
#     file = check_file_name(file, 0);
# #else    
#     file = check_valid_path(file, current_object.eff_user, "read_file", 0);
# #endif    
# 
#     if (!file)
#     return 0;
#     f = fopen(file, "r");
#     if (f == 0)
#     return 0;
#     if (fstat(fileno(f), &st) == -1)
#     fatal("Could not stat an open file.\n");
#     size = st.st_size;
#     if (size > READ_FILE_MAX_SIZE) {
#     if ( start or len ) size = READ_FILE_MAX_SIZE;
#     else {
#         fclose(f);
#         return 0;
#     }
#     }
#     if (!start) start = 1;
#     if (!len) len = READ_FILE_MAX_SIZE;
#     str = xalloc(size + 1);
#     str[size] = '\0';
#     do {
#     if (size > st.st_size)
#         size = st.st_size;
#         if (fread(str, size, 1, f) != 1) {
#             fclose(f);
#         free(str);
#             return 0;
#         }
#     st.st_size -= size;
#     end = str+size;
#         for (p=str; ( p2=memchr(p,'\n',end-p) ) and --start; ) p=p2+1;
#     } while ( start > 1 );
#     for (p2=str; p != end; ) {
#         c = *p++;
#     if ( !isprint(c) and !isspace(c) ) c=' ';
#     *p2++=c;
#     if ( c == '\n' )
#         if (!--len) break;
#     }
#     if ( len and st.st_size ) {
#     size -= ( p2-str) ; 
#     if (size > st.st_size)
#         size = st.st_size;
#         if (fread(p2, size, 1, f) != 1) {
#             fclose(f);
#         free(str);
#             return 0;
#         }
#     st.st_size -= size;
#     end = p2+size;
#         for (; p2 != end; ) {
#         c = *p2;
#         if ( !isprint(c) and !isspace(c) ) *p2=' ';
#         p2++;
#         if ( c == '\n' )
#             if (!--len) break;
#     }
#     if ( st.st_size and len ) {
#         #  tried to read more than READ_MAX_FILE_SIZE # 
#         fclose(f);
#         free(str);
#         return 0;
#     }
#     }
#     *p2='\0';
#     fclose(f);
# #if 0 #  caller immediately frees the string again,
#        * so there's no use to make it smaller now
#        # 
#     if ( st.st_size > (p2-str) ) {
# #  can't allocate shared string when string type isn't passed to the caller # 
#     p2=strdup(str);
#     free(str);
#     return p2;
#     }
# #endif
#     return str;
# }
# 
# 
# char *read_bytes(file,start,len)
#     char *file;
#     int start,len;
# {
#     struct stat st;
# 
#     char *str,*p;
#     int size, f;
#     int lseek();
# 
#     if (len < 0)
#     return 0;
#     if(len > MAX_BYTE_TRANSFER)
#     return 0;
# #ifdef COMPAT_MODE
#     file = check_file_name(file, 0);
# #else    
#     file = check_valid_path(file, current_object.eff_user, 
#                 "read_bytes", 0);
# #endif    
# 
#     if (!file)
#     return 0;
#     f = open(file, O_RDONLY);
#     if (f < 0)
#     return 0;
# 
#     if (fstat(f, &st) == -1)
#     fatal("Could not stat an open file.\n");
#     size = st.st_size;
#     if(start < 0) 
#     start = size + start;
# 
#     if (start >= size) {
#     close(f);
#     return 0;
#     }
#     if ((start+len) > size) 
#     len = (size - start);
# 
#     if ((size = lseek(f,start, 0)) < 0)
#     return 0;
# 
#     str = xalloc(len + 1);
# 
#     size = read(f, str, len);
# 
#     close(f);
# 
#     if (size <= 0) {
#     free(str);
#     return 0;
#     }
# 
#     #  We want to allow all characters to pass untouched!
#     for (il=0;il<size;il++) 
#     if (!isprint(str[il]) and !isspace(str[il]))
#         str[il] = ' ';
# 
#     str[il] = 0;
#     # 
#     # 
#      * The string has to end to '\0'!!!
#      # 
#     str[size] = '\0';
# 
#     p = string_copy(str);
#     free(str);
# 
#     return p;
# }
# 
# int write_bytes(file,start,str)
#     char *file, *str;
#     int start;
# {
#     struct stat st;
# 
#     int size, f;
#     int lseek();
# 
# #ifdef COMPAT_MODE    
#     file = check_file_name(file, 1);
# #else    
#     file = check_valid_path(file, current_object.eff_user, 
#                 "write_bytes", 1);
# #endif    
# 
#     if (!file)
#     return 0;
#     if(strlen(str) > MAX_BYTE_TRANSFER)
#     return 0;
#     f = open(file, O_WRONLY);
#     if (f < 0)
#     return 0;
# 
#     if (fstat(f, &st) == -1)
#     fatal("Could not stat an open file.\n");
#     size = st.st_size;
#     if(start < 0) 
#     start = size + start;
# 
#     if (start >= size) {
#     close(f);
#     return 0;
#     }
#     if ((start+strlen(str)) > size) 
#     return 0;
# 
#     if ((size = lseek(f,start, 0)) < 0)
#     return 0;
# 
#     size = write(f, str, strlen(str));
# 
#     close(f);
# 
#     if (size <= 0) {
#     return 0;
#     }
# 
#     return 1;
# }
# 
# 
# int file_size(file)
#     char *file;
# {
#     struct stat st;
# 
# #ifdef COMPAT_MODE
#     file = check_file_name(file, 0);
# #else
#     file = check_valid_path(file, current_object.eff_user, "file_size", 0);
# #endif
#     if (!file)
#     return -1;
#     if (stat(file, &st) == -1)
#     return -1;
#     if (S_IFDIR & st.st_mode)
#     return -2;
#     return st.st_size;
# }


alarm_time = 0

def sigalrm_run():
    while(True):
        
        t = time.time() # get the current time #        
        if alarm_time < t: # test if the alarm_time is older #
            catch_alarm() # call catch_alarm #
        time.sleep(0.01) # spin #
        

def alarm(t):
    """
    Set a new alarm time for t seconds in the future
    """
    
    alarm_time = time.time() + t
