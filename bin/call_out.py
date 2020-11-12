
"""
This file implements delayed calls of functions.
Static functions can not be called this way.
"""
from bin import backend, simulate, interpret, mud_object


# #define CHUNK_SIZE    20
call_list = []
call_list_free = []
num_call = 0
last_time = 0


class Call():
    delta = 0
    function = None
    ob = None
    command_giver = None
    v = None


def free_call(call):
    """
    Free a call out structure.
    """

    call.v = None
    call.function = None
    mud_object.free_object(call.ob, "free_call")
    if (call.command_giver):
        mud_object.free_object(call.command_giver, "free_call")
    call.ob = None
    call_list_free.append(call)


#  #
# void new_call_out(ob, fun, delay, arg)
#     struct object *ob;
#     char *fun;
#     int delay;
#     struct svalue *arg;
# {
#     struct call *cop, **copp;
# 
#     if (delay < 1)
#     delay = 1;
#     if (!call_list_free) {
#     int i;
#     call_list_free =
#         (struct call *)xalloc(CHUNK_SIZE * sizeof (struct call));
#     for (i=0; i<CHUNK_SIZE - 1; i++)
#         call_list_free[i].next  = &call_list_free[i+1];
#     call_list_free[CHUNK_SIZE-1].next = 0;
#     num_call += CHUNK_SIZE;
#     }
#     cop = call_list_free;
#     call_list_free = call_list_free.next;
#     cop.function = string_copy(fun);
#     cop.command_giver = command_giver; # save current player context #
#     if (command_giver)
#     add_ref(command_giver, "new_call_out");        # Bump its ref #
#     cop.ob = ob;
#     add_ref(ob, "call_out");
#     cop.v.type = T_NUMBER;
#     cop.v.u.number = 0;
#     if (arg)
#     assign_svalue(&cop.v, arg);
#     for (copp = &call_list; *copp; copp = &(*copp).next) {
#     if ((*copp).delta >= delay) {
#         (*copp).delta -= delay;
#         cop.delta = delay;
#         cop.next = *copp;
#         *copp = cop;
#         return;
#     }
#     delay -= (*copp).delta;
#     }
#     *copp = cop;
#     cop.delta = delay;
#     cop.next = 0;
# }


def call_out():
    global last_time
    """
    See if there are any call outs to be called. Set the 'command_giver'
    if it is a living object. Check for shadowing objects, which may also
    be living objects.
    """
    if len(call_list) == 0:
        last_time = backend.current_time
        return

    if last_time == 0:
        last_time = backend.current_time
    save_command_giver = simulate.command_giver
    simulate.current_interactive = None
    call_list.delta -= backend.current_time - last_time
    last_time = backend.current_time

    while call_list and call_list[0] and call_list[0].delta <= 0:

        # Move the first call_out out of the chain.
        call = call_list.pop(0)

        # A special case:
        # If a lot of time has passed, so that current call out was missed,
        # then it will have a negative delta. This negative delta implies
        # that the next call out in the list has to be adjusted.

        if call_list[0] and call.delta < 0:
            call_list[0].delta += call.delta
        if not call.ob.O_DESTRUCTED:
            try:
                ob = call.ob
                while ob.shadowing:
                    ob = ob.shadowing
                simulate.command_giver = None
                if call.command_giver and not call.command_giver.O_DESTRUCTED:
                    simulate.command_giver = call.command_giver
                elif ob.O_ENABLE_COMMANDS:
                    simulate.command_giver = ob

                interpret.apply(call.function, call.ob, call.v)

            except Exception as e:
                backend.clear_state()
                print("Error in call out.")
                print(e)

        free_call(call)

    simulate.command_giver = save_command_giver


# #
# # Throw away a call out. First call to this function is discarded.
# # The time left until execution is returned.
# # -1 is returned if no call out pending.
#  #
# int remove_call_out(ob, fun)
#     struct object *ob;
#     char *fun;
# {
#     struct call **copp, *cop;
#     int delay = 0;
# 
#     for (copp = &call_list; *copp; copp = &(*copp).next) {
#     delay += (*copp).delta;
#     if ((*copp).ob == ob and strcmp((*copp).function, fun) == 0) {
#         cop = *copp;
#         if (cop.next)
#         cop.next.delta += cop.delta;
#         *copp = cop.next;
#         free_call(cop);
#         return delay;
#     }
#     }
#     return -1;
# }
# 
# int find_call_out(ob, fun)
#     struct object *ob;
#     char *fun;
# {
#     struct call **copp;
#     int delay = 0;
#     for (copp = &call_list; *copp; copp = &(*copp).next) {
#     delay += (*copp).delta;
#     if ((*copp).ob == ob and strcmp((*copp).function, fun) == 0) {
#         return delay;
#     }
#     }
#     return -1;
# }
# 
# int print_call_out_usage(verbose)
#     int verbose;
# {
#     int i;
#     struct call *cop;
# 
#     for (i=0, cop = call_list; cop; cop = cop.next)
#     i++;
#     if (verbose) {
#     add_message("\nCall out information:\n");
#     add_message("---------------------\n");
#     add_message("Number of allocated call outs: %8d, %8d bytes\n",
#             num_call, num_call * sizeof (struct call));
#     add_message("Current length: %d\n", i);
#     } else {
#     add_message("call out:\t\t\t%8d %8d (current length %d)\n", num_call,
#             num_call * sizeof (struct call), i);
#     }
#     return num_call * sizeof (struct call);
# }
# 
# #ifdef DEBUG
# void count_ref_from_call_outs()
# {
#     struct call *cop;
# 
#     for (cop = call_list; cop; cop = cop.next) {
#     switch(cop.v.type)
#     {
#         case T_POINTER:
#         cop.v.u.vec.extra_ref++;
#         break;
#         case T_OBJECT:
#         cop.v.u.ob.extra_ref++;
#         break;
#     }
#     cop.ob.extra_ref++;
#     }
# }
# #endif
# 
# #
# # Construct an array of all pending call_outs. Every item in the array
# # consists of 4 items (but only if the object not is destructed):
# # 0:    The object.
# # 1:    The function (string).
# # 2:    The delay.
# # 3:    The argument.
#  #
# struct vector *get_all_call_outs() {
#     int i, next_time;
#     struct call *cop;
#     struct vector *v;
# 
#     for (i=0, cop = call_list; cop; i++, cop = cop.next)
#     ;
#     v = allocate_array(i);
#     next_time = 0;
#     #
#     # Take for granted that all items in an array are initialized to
#     # number 0.
#      #
#     for (i=0, cop = call_list; cop; i++, cop = cop.next) {
#     struct vector *vv;
# 
#     next_time += cop.delta;
#     if (cop.ob.flags & O_DESTRUCTED)
#         continue;
#     vv = allocate_array(4);
#     vv.item[0].type = T_OBJECT;
#     vv.item[0].u.ob = cop.ob;
#     add_ref(cop.ob, "get_all_call_outs");
#     vv.item[1].type = T_STRING;
#     vv.item[1].string_type = STRING_SHARED;
#     vv.item[1].u.string = make_shared_string(cop.function);
#     vv.item[2].u.number = next_time;
#     assign_svalue_no_free(&vv.item[3], &cop.v);
# 
#     v.item[i].type = T_POINTER;
#     v.item[i].u.vec = vv;        # Ref count is already 1 #
#     }
#     return v;
# }
