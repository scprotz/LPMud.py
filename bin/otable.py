import hashlib


'''
 * Object name hash table.  Object names are unique, so no special
 * problems - like stralloc.c.  For non-unique hashed names, we need
 * a better package (if we want to be able to get at them all) - we
 * cant move them to the head of the hash chain, for example.
 *
 * Note: if you change an object name, you must remove it and reenter it.
'''


obj_table = {}
 
 
# static void init_otable()
# {
#     int x;
#     obj_table = (struct object **)
#             xalloc(sizeof(struct object *) * OTABLE_SIZE);
# 
#     for (x=0; x<OTABLE_SIZE; x++)
#         obj_table[x] = 0;
# }
 
# Object hash function, ripped off from stralloc.c.
def ObjHash(s):
    return hashlib.md5(s.encode('utf-8'))
 
# /*
#  * Looks for obj in table, moves it to head.
#  */
# 
# static int obj_searches = 0, obj_probes = 0, objs_found = 0;
# 
def find_obj_n(s):

    h = None
    try:
        h = obj_table[ObjHash(s)]
    except:
        pass
    return h

# Add an object to the table - can't have duplicate names.
def enter_object_hash(ob):
    
    h = ObjHash(ob.name)
    
    s = find_obj_n(ob.name)
    
    if (s):
        if (s != ob):
            raise Exception("Duplicate object \"%s\" in object hash table" % ob.name)
        else:
            raise Exception("Entering object \"%s\" twice in object table" % ob.name)
        
    obj_table[h] = ob
 
# /*
#  * Remove an object from the table - generally called when it
#  * is removed from the next_all list - i.e. in destruct.
#  */
# 
# void remove_object_hash(ob)
# struct object *ob;
# {
#     struct object * s;
#     int h = ObjHash(ob.name);
# 
#     s = find_obj_n(ob.name);
# 
#     if (s != ob)
#         fatal("Remove object \"%s\": found a different object!",
#             ob.name);
#     
#     obj_table[h] = ob.next_hash;
#     ob.next_hash = 0;
#     objs_in_table--;
#     return;
# }
# 
# /*
#  * Lookup an object in the hash table; if it isn't there, return null.
#  * This is only different to find_object_n in that it collects different
#  * stats; more finds are actually done than the user ever asks for.
#  */
# 
# static int user_obj_lookups = 0, user_obj_found = 0;
# 
# struct object * lookup_object_hash(s)
# char * s;
# {
#     struct object * ob = find_obj_n(s);
#     user_obj_lookups++;
#     if (ob) user_obj_found++;
#     return(ob);
# }
# 
# /*
#  * Print stats, returns the total size of the object table.  All objects
#  * are in table, so their size is included as well.
#  */
# 
# static char sbuf[100];
# 
# int show_otable_status(verbose)
#     int verbose;
# {
#     if (verbose) {
#     add_message("\nObject name hash table status:\n");
#     add_message("------------------------------\n");
#     sprintf(sbuf, "%.2f", objs_in_table / (float) OTABLE_SIZE);
#     add_message("Average hash chain length               %s\n", sbuf);
#     sprintf(sbuf, "%.2f", (float)obj_probes / obj_searches);
#     add_message("Searches/average search length       %d (%s)\n",
#             obj_searches, sbuf);
#     add_message("External lookups succeeded (succeed) %d (%d)\n",
#             user_obj_lookups, user_obj_found);
#     }
#     add_message("hash table overhead\t\t\t %8d\n",
#         OTABLE_SIZE * sizeof(struct object *));
#     return (OTABLE_SIZE * sizeof(struct object *) +
#         objs_in_table * sizeof(struct object));
# }
