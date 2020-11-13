import select
import socket
import sys
from telnetlib import IAC, WONT

from bin import config, interpret, comm, mud_object
from bin import simulate, main, backend, access_check, interactive


TELOPT_ECHO = bytes([1])
MAX_TEXT = 2048
MESSAGE_FLUSH = None

# #define MAX_SOCKET_PACKET_SIZE    1024    # Wild guess. #
# #define DESIRED_SOCKET_PACKET_SIZE 800

all_players = []
player_for_flush = []
s = None  # Server s #
num_player = 0


def prepare_ipc():
    global s
    # set up server s #
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)

    # bind to port #
    try:
        s.bind(("localhost", main.port_number))
    except OSError:
        print("Socket already bound on port",
              main.port_number,
              file=sys.stderr)
        exit(1)

    # keep 5 channels open to listen #
    s.listen(5)


def ipc_remove():
    """
    This one is called when shutting down the MUD.
    """
    print("Shutting down ipc...")
    s.close()


def add_message(msg):
    """
    Send a message to a player. If that player is shadowed, special
    care hs tobe taken.
    """
    raise NotImplementedError
# void add_message(fmt, a1, a2, a3, a4, a5, a6, a7, a8, a9)
#     char *fmt;
#     int a1, a2, a3, a4, a5, a6, a7, a8, a9;
# {
#     char buff[10000];        # Kludgy! Hope this is enough ! #
#     char buff2[MAX_SOCKET_PACKET_SIZE+1];
#     struct interactive *ip;
#     int n, chunk, length;
#     int from, to;
#     int min_length;
#     int old_message_length;
#
#     if (command_giver == 0 || (command_giver.flags & O_DESTRUCTED) ||
#     command_giver.interactive == 0 ||
#     command_giver.interactive.do_close) {
#     putchar(']');
#     if ( fmt != MESSAGE_FLUSH )
#         printf(fmt, a1, a2, a3, a4, a5, a6, a7, a8, a9);
#     fflush(stdout);
#     return;
#     }
#     ip = command_giver.interactive;
#     old_message_length = ip.message_length;
#     if ( fmt == MESSAGE_FLUSH ) {
#     min_length = 1;
#     strncpy ( buff, ip.message_buf, length=old_message_length );
#         buff[length] = '\0';
#     } else {
# #ifdef COMM_STAT
#     add_message_calls++; /* We want to know how many packets the old
#                 version would have sent             */
# #endif
#     min_length = DESIRED_SOCKET_PACKET_SIZE;
#     (void)sprintf(buff+old_message_length,fmt,a1,a2,a3,a4,a5,a6,a7,a8,a9);
#     length = old_message_length + strlen(buff+old_message_length);
#     /*
#      * Always check that your arrays are big enough ! :-)
#      */
#     if (length > sizeof buff)
#         fatal("To long message!\n");
#     if (shadow_catch_message(command_giver, buff+old_message_length))
#         return;
#     if (ip.snoop_by) {
#         struct object *save = command_giver;
#         command_giver = ip.snoop_by.ob;
#         add_message("%%%s", buff+old_message_length);
#         command_giver = save;
#     }
#     if ( length >= min_length ) {
#         strncpy ( buff, ip.message_buf, old_message_length );
#     } else {
#         strcpy( ip.message_buf+old_message_length,
#         buff+old_message_length );
#     }
#     }
#     if (d_flag > 1)
#     debug_message("[%s(%d)]: %s", command_giver.name, length, buff);
#     /*
#      * Insert CR after all NL.
#      */
#     to = 0;

#     for (from = 0; length-from >= min_length; to = 0 ) {
#     for ( ; to < (sizeof buff2)-1 and buff[from] != '\0';) {
#         if (buff[from] == '\n')
#         buff2[to++] = '\r';

#         buff2[to++] = buff[from++];

#     }
#     if ( to == sizeof(buff2) ) {
#         to -= 2;
#         from--;
#     }
#     chunk = to;
#     /*
#      * We split up the message into something smaller than the max size.
#      */
#     if ((n = write(ip.socket, buff2, chunk)) == -1) {
#         if (errno == EMSGSIZE) {
#         fprintf(stderr, "comm1: write EMSGSIZE.\n");
#         return;
#         }
#         if (errno == EINVAL) {
#         fprintf(stderr, "comm1: write EINVAL.\n");
#             if (old_message_length) remove_flush_entry(ip);
#         ip.do_close = 1;
#         return;
#         }
#         if (errno == ENETUNREACH) {
#         fprintf(stderr, "comm1: write ENETUNREACH.\n");
#             if (old_message_length) remove_flush_entry(ip);
#         ip.do_close = 1;
#         return;
#         }
#         if (errno == EHOSTUNREACH) {
#         fprintf(stderr, "comm1: write EHOSTUNREACH.\n");
#             if (old_message_length) remove_flush_entry(ip);
#         ip.do_close = 1;
#         return;
#         }
#         if (errno == EPIPE) {
#         fprintf(stderr, "comm1: write EPIPE detected\n");
#             if (old_message_length) remove_flush_entry(ip);
#         ip.do_close = 1;
#         return;
#         }
#         if (errno == EWOULDBLOCK) {
#         fprintf(stderr, "comm1: write EWOULDBLOCK. Message discarded.\n");
#             if (old_message_length) remove_flush_entry(ip);
# #        ip.do_close = 1;  -- LA #
#         return;
#         }
#         fprintf(stderr, "write: unknown errno %d\n", errno);
#         perror("write");
#         if (old_message_length) remove_flush_entry(ip);
#         ip.do_close = 1;
#         return;
#     }
# #ifdef COMM_STAT
#     inet_packets++;
#     inet_volume += n;
# #endif
#     if (n != chunk)
#         fprintf(stderr, "write socket: wrote %d, should be %d.\n",
#             n, chunk);
#     continue;
#     }
#     length -= from;
#     ip.message_length=length;
#     if (from)
#         strncpy( ip.message_buf, buff+from, length );
#     if ( length and !old_message_length ) { # buffer became 'dirty' #
#     if ( (ip.next_player_for_flush = first_player_for_flush) ) {
#         first_player_for_flush.interactive.previous_player_for_flush =
#         command_giver;
#     }
#     ip.previous_player_for_flush = 0;
#     first_player_for_flush = command_giver;
#     }
#     if ( !length and old_message_length ) { # buffer has become empty #
#     remove_flush_entry(ip);
#     }
# }
# 
# void remove_flush_entry(ip)
#     struct interactive *ip;
# {
# 
#     ip.message_length=0;
#     if ( ip.previous_player_for_flush ) {
#     ip.previous_player_for_flush.interactive.next_player_for_flush
#     = ip.next_player_for_flush;
#     } else {
#     first_player_for_flush = ip.next_player_for_flush;
#     }
#     if ( ip.next_player_for_flush ) {
#     ip.next_player_for_flush.interactive.previous_player_for_flush
#     = ip.previous_player_for_flush;
#     }
# }


def flush_all_player_mess():
    save = simulate.command_giver
    for p in player_for_flush:
        simulate.command_giver = p
        add_message(MESSAGE_FLUSH)
    simulate.command_giver = save


def get_message(buff):
    """
    Get a message from any player.  For all players without a completed
    cmd in their input buffer, read their socket.  Then, return the first
    cmd of the next player in sequence that has a complete cmd in their buffer.
    CmdsGiven is used to allow people in ED to send more cmds (if they have
    them queued up) than normal players.  If we get a heartbeat, still read
    all sockets; if the next cmd giver is -1, we have already cycled and
    can go back to do the heart beat.
    """

    # Stay in this loop until we have a message from a player. #

    while True:
        readable, _, _ = select.select([s], [], [])
        for sock in readable:
            if sock is s:
                # First, try to get a new player... #
                new_socket, address = s.accept()
                if new_socket:
                    new_player(new_socket, address)
            else:
                print("else")
                for ip in all_players:
                    if ip.do_close:
                        ip.do_close = False
                        remove_interactive(ip.ob)
                        continue

                for ip in all_players:
                    # Don't overfill their buffer.
                    # Use a very conservative estimate on how much we can
                    # read.

                    try:
                        buffer = s.recv(MAX_TEXT)

                        if ip.closing:
                            print("Tried to read from closing socket.n")
                            remove_interactive(ip.ob)
                            return False
                        if buffer is None:
                            remove_interactive(ip.ob)
                            continue

                        for c in buffer[:]:
                            ip.text.append(c)

                    except Exception as e:
                        print(e)
                        remove_interactive(ip.ob)
                        continue

                # we have read the sockets; now find and return a command
                p = None
                ip = None
                iterp = list(all_players)
                for i in iterp:
                    ip = i
                    if backend.comm_time_to_call_heart_beat:
                        backend.time_to_call_heart_beat = True
                        return False

                    p = first_cmd_in_buf(ip)
                    if p is not None:  # wont respond to partials #
                        break

                if not ip or not p:
                    # no cmds found; loop and select (on timeout) again #
                    if backend.comm_time_to_call_heart_beat:
                        # may as well do it now, # no cmds, do heart beat #
                        backend.time_to_call_heart_beat = True
                        return False
                    continue  # else await another cmd #

                # we have a player cmd - return it.  If he is in ed, count his
                # cmds, else only allow 1 cmd.  If he has only one partially
                # completed cmd left after * this, move it to the start of his
                # buffer; new stuff will be appended.

                simulate.command_giver = ip.ob
                next_cmd_in_buf(ip)  # move on buffer pointers #

                # manage snooping - should the snooper see type ahead? #
                # Well, he doesn't here #
                if ip.snoop_by and not ip.noecho:
                    simulate.command_giver = ip.snoop_by.ob
                    add_message("%% %s\n", buff)

                simulate.command_giver = ip.ob
                if ip.noecho:
                    # Must not enable echo before the user input is received. #
                    add_message("%c%c%c" % IAC, WONT, TELOPT_ECHO)

                ip.noecho = False
                ip.last_time = backend.current_time
                return True


def first_cmd_in_buf(ip):
    """
    find the first character of the next complete cmd in a buffer, 0 if no
    completed cmd.  There is a completed cmd if there is a null between
    text_start and text_end.  Zero length commands are discarded (as occur
    between <cr> and <lf>).  Update text_start if we have to skip leading
    nulls.
    """

    buff = None

    while ip.text.find('\n') != -1:
        ip.text[ip.text.find('\n')] = '\0'

    if ip.text.find('\0') != -1:
        buff = ip.text[:ip.text.find('\0').strip()]

    if buff is not None and len(buff) > 0:
        buff = telnet_neg(buff)

    if buff is not None and len(buff) == 0:
        next_cmd_in_buf(ip)
        return None

    return buff


def next_cmd_in_buf(ip):
    """
    move pointers to next cmd, or clear buf.
    """
    if ip.text.find('\0') != -1:
        ip.text = ip.text[: ip.text.find('\0') + 1]


def remove_interactive(ob):
    """
    Remove an interactive player immediately.
    """
    raise NotImplementedError
#     struct object *ob;
# {
#     struct object *save = command_giver;
#     int i;
# 
#     for (i=0; i<MAX_PLAYERS; i++) {
#     if (all_players[i] != ob.interactive)
#         continue;
#     if (ob.interactive.closing)
#         fatal("Double call to remove_interactive()\n");
#     ob.interactive.closing = 1;
#     if (ob.interactive.snoop_by) {
#         ob.interactive.snoop_by.snoop_on = 0;
#         ob.interactive.snoop_by = 0;
#     }
#     if (ob.interactive.snoop_on) {
#         ob.interactive.snoop_on.snoop_by = 0;
#         ob.interactive.snoop_on = 0;
#     }
#     command_giver = ob;
#     add_message("Closing down.\n");
#     if (ob.interactive.ed_buffer) {
#         extern void save_ed_buffer();
# 
#         save_ed_buffer();
#     }
#     add_message(MESSAGE_FLUSH);
#     (void)shutdown(ob.interactive.socket, 2);
#     close(ob.interactive.socket);
# #ifdef ACCESS_RESTRICTED
#         release_host_access (ob.interactive.access_class);
# #endif
#     num_player--;
#     if (ob.interactive.input_to) {
#         free_object(ob.interactive.input_to.ob, "remove_interactive");
#         free_sentence(ob.interactive.input_to);
#         ob.interactive.input_to = 0;
#     }
#     free((char *)ob.interactive);
#     ob.interactive = 0;
#     all_players[i] = 0;
#     free_object(ob, "remove_interactive");
#     command_giver = save;
#     return;
#     }
#     (void)fprintf(stderr, "Could not find and remove player %s\n", ob.name);
#     abort();
# }


# 
# #ifndef MSDOS
# #ifndef ACCESS_RESTRICTED
# 
# int
# allow_host_access(new_socket)
#     int new_socket;
# {
#     struct sockaddr_in apa;
#     int len = sizeof apa;
#     char * ipname, *calloc(), *xalloc(), *index();
#     static int read_access_list = 0;
#     static struct access_list {
#     int addr_len;
#     char * addr, *name, *comment;
#     struct access_list * next;
#     } * access_list;
#     register struct access_list * ap;
# 
#     if(!read_access_list) {
#     FILE * f = fopen("ACCESS.DENY", "r");
#     char buf[1024], ipn[50], hname[100], comment[1024], *p1, *p2;
#     struct access_list * na;
#     struct hostent * hent;
# 
#     read_access_list = 1;
#     if(f) {
#         while(fgets(buf, sizeof buf - 1, f)) {
#         if(*buf != '#') {
#             ipn[0] = hname[0] = comment[0] = 0;
#             if(p1 = index(buf, ':')) *p1 = 0;
#             if(buf[0] and buf[0] != '\n')
#             strncpy(ipn, buf, sizeof ipn - 1);
#             if((p2 = p1) and *++p2) {
#             if(p1 = index(p2, ':')) *p1 = 0;
#             if(p2[0] and p2[0] != '\n')
#                 strcpy(hname, p2);
#             if(p1 and p1[1] and p1[1] != '\n')
#                 strcpy(comment, p1+1);
#             }
#             
#             if(!(na = (struct access_list *)xalloc(sizeof na[0]))) {
#             fatal("Out of mem.\n");
#             }
#             na.addr = na.name = na.comment = 0;
#             na.next = 0;
#             if(*ipn and (!(na.addr = xalloc(strlen(ipn) + 1)) ||
#                 !strcpy(na.addr, ipn)))
#             fatal("Out of mem.\n");
#             if(*hname and (!(na.name = xalloc(strlen(hname) + 1)) ||
#                   !strcpy(na.name, hname)))
#             fatal("Out of mem.\n");
#             if(*comment and (!(na.comment=xalloc(strlen(comment)+1))||
#                     !strcpy(na.comment, comment)))
#             fatal("Out of mem.\n");
# 
#             if((!(int)*ipn)
#             and
#             ((!*hname)
#               || (!(hent = gethostbyname(hname))) ||
#                  (!(na.addr =
#                    xalloc(hent.h_length+1)))||
#                  !strcpy(na.addr,
#                     inet_ntoa(*(struct in_addr *)hent.h_addr)))) {
#             if(na.name) free(na.name);
#             if(na.comment) free(na.comment);
#             free((char *)na);
#             continue;
#             }
#             if(!(na.addr_len = strlen(na.addr)))
#             continue;
# 
#             /* printf("disabling: %s:%s:%s\n", na.addr,
#                na.name?na.name:"no name",
#                na.comment?na.comment:"no comment");  */
# 
#             na.next = access_list;
#             access_list = na;
#         }
#         }
#         fclose(f);
#     }
#     }
#     
#     if (!access_list)
#     return 0;
#     
#     if(getpeername(new_socket, (struct sockaddr *)&apa, &len) == -1) {
#     close(new_socket);
#     perror("getpeername");
#     return -1;
#     }
# 
#     ipname = inet_ntoa(apa.sin_addr);
#     
#     for(ap = access_list; ap; ap = ap.next)
#     if(!strncmp(ipname, ap.addr, ap.addr_len)){
#         if(ap.comment) (void) write(new_socket, ap.comment,
#                      strlen(ap.comment));
#         printf("Stopping: %s:%s\n", ap.addr, ap.name?ap.name:"no name");
#         close(new_socket);
#         return -1;
#     }
#     return 0;
# }
# #endif # not ACCESS_RESTRICTED #
# #endif
# 
# /*
#  * get the I'th player object from the interactive list, i starts at 0
#  * and can go to num_player - 1.  For users(), etc.
#  */
# struct object * get_interactive_object(i)
# int i;
# {
#     int n;
# 
#     if (i >= num_player) # love them ASSERTS() :-) #
#     fatal("Get interactive (%d) with only %d players!", i, num_player);
# 
#     for (n = 0; n < MAX_PLAYERS; n++)
#     if (all_players[n])
#         if (!(i--))
#         return(all_players[n].ob);
# 
#     fatal("Get interactive: player %d not found! (num_players = %d)",
#         i, num_player);
#     return 0;    # Just to satisfy some compiler warnings #
# }

def new_player(new_socket, address):

    _class = access_check.allow_host_access(new_socket, address, new_socket)
    if not _class:
        return

    if len(all_players) < config.MAX_PLAYERS + 1:

        interpret.assert_master_ob_loaded()
        simulate.command_giver = simulate.master_ob
        simulate.master_ob.interactive = interactive.Interactive()
        simulate.master_ob.interactive.default_err_message = None
        simulate.master_ob.O_ONCE_INTERACTIVE - True
        # This initialization is not pretty. #
        simulate.master_ob.interactive.ob = simulate.master_ob
        simulate.master_ob.interactive.text = []
        simulate.master_ob.interactive.input_to = None
        simulate.master_ob.interactive.closing = False
        simulate.master_ob.interactive.snoop_on = None
        simulate.master_ob.interactive.snoop_by = None
        simulate.master_ob.interactive.do_close = False
        simulate.master_ob.interactive.noecho = False
        simulate.master_ob.interactive.last_time = backend.current_time

        all_players.append(simulate.master_ob.interactive)
        simulate.master_ob.interactive.socket = new_socket

        set_prompt("> ")

        simulate.master_ob.interactive.access_class = _class

        # The player object has one extra reference.
        # It is asserted that the master_ob is loaded.
        #
        ret = interpret.apply_master_ob("connect", 0)
        if ret is None or not isinstance(mud_object.Mud_Object):
            comm.remove_interactive(simulate.master_ob)
            return

        # There was an object returned from connect(). Use this as the
        # player object.

        ret.interactive = simulate.master_ob.interactive
        ret.interactive.ob = ret
        ret.O_ONCE_INTERACTIVE = True
        simulate.master_ob.O_ONCE_INTERACTIVE = False
        comm.add_message(MESSAGE_FLUSH)
        simulate.master_ob.interactive = None
        mud_object.free_object(simulate.master_ob, "reconnect");

        simulate.command_giver = ret

        backend.logon(ret)
        comm.flush_all_player_mess()
        return

    new_socket.send(b'Lpmud is full. Come back later.\r\n')
    new_socket.shutdown()
    new_socket.close()


def call_function_interactive(i, str):
    raise NotImplementedError
#     struct interactive *i;
#     char *str;
# {
#     char *function;
#     struct object *ob;
# 
#     if (!i.input_to)
#     return 0;
#     /*
#      * Special feature: input_to() has been called to setup
#      * a call to a function.
#      */
#     if (i.input_to.ob.flags & O_DESTRUCTED) {
#     # Sorry, the object has selfdestructed ! #
#     free_object(i.input_to.ob, "call_function_interactive");
#     free_sentence(i.input_to);
#     i.input_to = 0;
#     return 0;
#     }
#     free_object(i.input_to.ob, "call_function_interactive");
#     function = string_copy(command_giver.interactive.input_to.function);
#     ob = i.input_to.ob;
#     free_sentence(i.input_to);
#     /*
#      * We must clear this reference before the call to apply(), because
#      * someone might want to set up a new input_to().
#      */
#     i.input_to = 0;
#     /*
#      * Now we set current_object to this object, so that input_to will
#      * work for static functions.
#      */
#     push_constant_string(str);
#     current_object = ob;
#     (void)apply(function, ob, 1);
#     free(function);
#     flush_all_player_mess();
#     return 1;
# }
# 
# int set_call(ob, sent, noecho)
#     struct object *ob;
#     struct sentence *sent;
#     int noecho;
# {
#     struct object *save = command_giver;
#     if (ob == 0 || sent == 0)
#     return 0;
#     if (ob.interactive == 0 || ob.interactive.input_to)
#     return 0;
#     ob.interactive.input_to = sent;
#     ob.interactive.noecho = noecho;
#     command_giver = ob;
#     if (noecho)
#     add_message("%c%c%c", IAC, WILL, TELOPT_ECHO);
#     command_giver = save;
#     return 1;
# }
# 
# void show_info_about(str, room, i)
#     char *str, *room;
#     struct interactive *i;
# {
#     struct hostent *hp = 0;
# 
# #if 0
#     hp = gethostbyaddr(&i.addr.sin_addr.s_addr, 4, AF_INET);
# #endif
#     add_message("%-15s %-15s %s\n",
#         hp ? hp.h_name : inet_ntoa(i.addr.sin_addr), str, room);
# }


def remove_all_players():
    raise NotImplementedError 
# void remove_all_players()
# {
#     int i;
# 
#     for (i=0; i<MAX_PLAYERS; i++) {
#     if (all_players[i] == 0)
#         continue;
#     command_giver = all_players[i].ob;
#     (void)apply("quit", all_players[i].ob, 0);
#     }
# }


def set_prompt(pr):
    simulate.command_giver.interactive.prompt = pr


def print_prompt():
    """
    Print the prompt, but only if input_to not is disabled.
    """

    if simulate.command_giver is None:
        raise Exception("command_giver is None.")
    if simulate.command_giver.interactive.input_to == 0:
        add_message(simulate.command_giver.interactive.prompt)
        flush_all_player_mess()


# /*
#  * Let object 'me' snoop object 'you'. If 'you' is 0, then turn off
#  * snooping.
#  */
# void set_snoop(me, you)
#     struct object *me, *you;
# {
#     struct interactive *on = 0, *by = 0, *tmp;
#     int i;
# 
#     if (me.flags & O_DESTRUCTED)
#     return;
#     if (you and (you.flags & O_DESTRUCTED))
#     return;
#     for(i=0; i<MAX_PLAYERS and (on == 0 || by == 0); i++) {
#     if (all_players[i] == 0)
#         continue;
#     if (all_players[i].ob == me)
#         by = all_players[i];
#     else if (all_players[i].ob == you)
#         on = all_players[i];
#     }
#     if (you == 0) {
#     if (by == 0)
#         error("Could not find myself to stop snoop.\n");
#     add_message("Ok.\n");
#     if (by.snoop_on == 0)
#         return;
#     by.snoop_on.snoop_by = 0;
#     by.snoop_on = 0;
#     return;
#     }
#     if (on == 0 || by == 0) {
#     add_message("Failed.\n");
#     return;
#     }
#     if (by.snoop_on) {
#     by.snoop_on.snoop_by = 0;
#     by.snoop_on = 0;
#     }
#     if (on.snoop_by) {
#     add_message("Busy.\n");
#     return;
#     }
#     /*
#      * Protect against snooping loops.
#      */
#     for (tmp = on; tmp; tmp = tmp.snoop_on) {
#     if (tmp == by) {
#         add_message("Busy.\n");
#         return;
#     }
#     }
#     on.snoop_by = by;
#     by.snoop_on = on;
#     add_message("Ok.\n");
#     return;
# }
# 
# /*
#  * Let object 'me' snoop object 'you'. If 'you' is 0, then turn off
#  * snooping.
#  *
#  * This routine is almost identical to the old set_snoop. The main
#  * difference is that the routine writes nothing to player directly,
#  * all such communication is taken care of by the mudlib. It communicates
#  * with master.c in order to find out if the operation is permissble or
#  * not. The old routine let everyone snoop anyone. This routine also returns
#  * 0 or 1 depending on success.
#  */
# int new_set_snoop(me, you)
#     struct object *me, *you;
# {
#     struct interactive *on = 0, *by = 0, *tmp;
#     int i;
#     struct svalue *ret;
# 
#     # Stop if people managed to quit before we got this far #
#     if (me.flags & O_DESTRUCTED)
#     return 0;
#     if (you and (you.flags & O_DESTRUCTED))
#     return 0;
# 
#     # Find the snooper & snopee #
#     for(i = 0 ; i < MAX_PLAYERS and (on == 0 || by == 0); i++) 
#     {
#     if (all_players[i] == 0)
#         continue;
#     if (all_players[i].ob == me)
#         by = all_players[i];
#     else if (all_players[i].ob == you)
#         on = all_players[i];
#     }
# 
#     # Illegal snoop attempt by null object #
#     if (!current_object.eff_user)
#     return 0;
# 
#     # Check for permissions with valid_snoop in master #
#     push_object(me);
#     if (you == 0)
#     push_number(0);
#     else
#     push_object(you);
#     ret = apply_master_ob("valid_snoop", 2);
# 
#     if (!ret || ret.type != T_NUMBER || ret.u.number == 0)
#     return 0;
# 
#     # Stop snoop #
#     if (you == 0) 
#     {
#     if (by == 0)
#         error("Could not find snooper to stop snoop on.\n");
#     if (by.snoop_on == 0)
#         return 1;
#     by.snoop_on.snoop_by = 0;
#     by.snoop_on = 0;
#     return 1;
#     }
# 
#     # Strange event, but possible, so test for it #
#     if (on == 0 || by == 0)
#     return 0;
# 
#     # Protect against snooping loops #
#     for (tmp = on; tmp; tmp = tmp.snoop_on) 
#     {
#     if (tmp == by) 
#         return 0;
#     }
# 
#     # Terminate previous snoop, if any #
#     if (by.snoop_on) 
#     {
#     by.snoop_on.snoop_by = 0;
#     by.snoop_on = 0;
#     }
#     if (on.snoop_by)
#     {
#     on.snoop_by.snoop_on = 0;
#     on.snoop_by = 0;
#     }
# 
#     on.snoop_by = by;
#     by.snoop_on = on;
#     return 1;
#     
# }

TS_DATA = 0
TS_IAC = 1
TS_WILL = 2
TS_WONT = 3
TS_DO = 4
TS_DONT = 5


def telnet_neg(old_str):

    new_str = ""

    for i in range(len(old_str)):
        ch = old_str[i] & 0xff

        if ch == '\b' or ch == 0x7f:  # Backspace or Delete #
            if len(new_str) > 0:
                new_str = new_str[:-1]  # take off the last thing added #
            continue
        else:
            new_str = new_str + ch
    return new_str


# #define IPSIZE 200
# static struct ipentry {
#     long addr;
#     char *name;
# } iptable[IPSIZE];
# static int ipcur;
# 
# char *query_ip_name(ob)
#     struct object *ob;
# {
#     int i;
# 
#     if (ob == 0)
#     ob = command_giver;
#     if (!ob || ob.interactive == 0)
#     return 0;
#     for(i = 0; i < IPSIZE; i++) {
#     if (iptable[i].addr == ob.interactive.addr.sin_addr.s_addr and
#         iptable[i].name)
#         return iptable[i].name;
#     }
#     return inet_ntoa(ob.interactive.addr.sin_addr);
# }
# 
# static void add_ip_entry(addr, name)
# long addr;
# char *name;
# {
#     int i;
# 
#     for(i = 0; i < IPSIZE; i++) {
#     if (iptable[i].addr == addr)
#         return;
#     }
#     iptable[ipcur].addr = addr;
#     if (iptable[ipcur].name)
#     free_string(iptable[ipcur].name);
#     iptable[ipcur].name = make_shared_string(name);
#     ipcur = (ipcur+1) % IPSIZE;
# }
# 
# char *query_ip_number(ob)
#     struct object *ob;
# {
#     if (ob == 0)
#     ob = command_giver;
#     if (!ob || ob.interactive == 0)
#     return 0;
#     return inet_ntoa(ob.interactive.addr.sin_addr);
# }
# 
# #ifndef INET_NTOA_OK
# /*
# Note: if the address string is "a.b.c.d" the address number is
#       a * 256^3 + b * 256^2 + c * 256 + d
# 
# */
# 
# char *inet_ntoa(ad)
#     struct in_addr ad;
# {
#     u_long s_ad;
#     int a, b, c, d;
#     static char addr[20]; # 16 + 1 should be enough #
# 
#     s_ad = ad.s_addr;
#     d = s_ad % 256;
#     s_ad /= 256;
#     c = s_ad % 256;
#     s_ad /= 256;
#     b = s_ad % 256;
#     a = s_ad / 256;
#     sprintf(addr, "%d.%d.%d.%d", a, b, c, d);
#     return addr;
# }
# #endif # INET_NTOA_OK #
# 
# char *query_host_name() {
#     static char name[20];
#     
#     gethostname(name, sizeof name);
#     name[sizeof name - 1] = '\0';    # Just to make sure #
#     return name;
# }
# 
# struct object *query_snoop(ob)
#     struct object *ob;
# {
#     if (ob.interactive.snoop_by == 0)
#     return 0;
#     return ob.interactive.snoop_by.ob;
# }
# 
# int query_idle(ob)
#     struct object *ob;
# {
#     if (!ob.interactive)
#     error("query_idle() of non-interactive object.\n");
#     return current_time - ob.interactive.last_time;
# }
# 
# void notify_no_command() {
#     char *p,*m;
# 
#     if (!command_giver.interactive)
#     return;
#     p = command_giver.interactive.default_err_message;
#     if (p) {
#     m = process_string(p); # We want 'value by function call' /JnA #
#     if (!shadow_catch_message(command_giver, m))
#         add_message(m);
#     if (m != p)
#         free(m);
#     free_string(p);
#     command_giver.interactive.default_err_message = 0;
#     }
#     else {
#     add_message("What ?\n");
#     }
# }
# 
# void clear_notify() {
#     if (!command_giver.interactive)
#     return;
#     if (command_giver.interactive.default_err_message) {
#     free_string(command_giver.interactive.default_err_message);
#     command_giver.interactive.default_err_message = 0;
#     }
# }
# 
# void set_notify_fail_message(str)
#     char *str;
# {
#     if (!command_giver || !command_giver.interactive)
#     return;
#     clear_notify();
#     if (command_giver.interactive.default_err_message)
#     free_string(command_giver.interactive.default_err_message);
#     command_giver.interactive.default_err_message = make_shared_string(str);
# }
# 
# int replace_interactive(ob, obfrom, #IGN#name)
#     struct object *ob;
#     struct object *obfrom;
#     char *name;
# {
#     /* marion
#      * i see no reason why to restrict this, besides - the length
#      * (was) missing to strncmp()
#      * JnA: There is every reason to restrict this.
#      *      Otherwise I can write my own player object without any security
#      *      at all!
#      */
#     struct svalue *v;
# 
#     push_string(name, STRING_CONSTANT);
#     v = apply_master_ob("valid_exec", 1);
#     if (!v || v.type != T_NUMBER || v.u.number == 0)
#     return 0;
# /*
#     if (strcmp(name, "secure/login.c") != 0)
#     return 0;
# */
#     # fprintf(stderr,"DEBUG: %s,%s\n",ob.name,obfrom.name); #
#     if (ob.interactive)
#     error("Bad argument1 to exec()\n");
#     if (!obfrom.interactive)
#     error("Bad argument2 to exec()\n");
#     if (obfrom.interactive.message_length) {
#         struct object *save;
#         save=command_giver;
#         command_giver=obfrom;
#         add_message(MESSAGE_FLUSH);
#     command_giver=save;
#     }
#     ob.interactive = obfrom.interactive;
#     obfrom.interactive = 0;
#     ob.interactive.ob = ob;
#     ob.flags |= O_ONCE_INTERACTIVE;
#     obfrom.flags &= ~O_ONCE_INTERACTIVE;
#     add_ref(ob, "exec");
#     free_object(obfrom, "exec");
#     if (obfrom == command_giver) command_giver = ob;
#     return 1;
# }
# 
# #ifdef DEBUG
# /*
#  * This is used for debugging reference counts.
#  */
# 
# void update_ref_counts_for_players() {
#     int i;
# 
#     for (i=0; i<MAX_PLAYERS; i++) {
#     if (all_players[i] == 0)
#         continue;
#     all_players[i].ob.extra_ref++;
#     if (all_players[i].input_to)
#         all_players[i].input_to.ob.extra_ref++;
#     }
# }
# #endif # DEBUG #
# 
# #ifdef MUDWHO
# 
# char mudwhoid[200];
# 
# sendmudwhoinfo()
# {
#     struct object *ob;
#     int i;
#     static int last_called_time;
# 
#     if (current_time - last_called_time < MUDWHO_REFRESH_TIME)
#     return;
# 
#     last_called_time = get_current_time();
# 
#     rwhocli_pingalive();
# 
#     for (i = 0; i < num_player; i++) {
#     ob = get_interactive_object(i);
#     if (ob.living_name)
#     {
#         sscanf(ob.name,"%*[^#]#%s",mudwhoid);
#         strcat(mudwhoid,"@");
#         strcat(mudwhoid,MUDWHO_NAME);
#         rwhocli_userlogin(mudwhoid,ob.living_name,
#         ob.interactive.login_time);
#     }
#     }
# }
# sendmudwhologout(ob)
# struct object *ob;
# {
#     if (ob.interactive)
#     {
#         sscanf(ob.name,"%*[^#]#%s",mudwhoid);
#         strcat(mudwhoid,"@");
#         strcat(mudwhoid,MUDWHO_NAME);
#         rwhocli_userlogout(mudwhoid);
#     }
# }
# #endif
