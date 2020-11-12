import sys

from bin import backend, wiz_list


class Wizard:
    name = None
    score = 0
    cost = 0
    total_worth = 0
    heart_beats = 0
#     
# struct wiz_list {
#     char *name;
#     int length;
#     struct wiz_list *next;
#     int score;
#     int cost;
#     int heart_beats;
#     int total_worth;
#     int size_array;       #  Total size of this wizards arrays.#
#    # 
#    # The following values are all used to store the last error
#    # message.
#     #
#     char *file_name;
#     char *error_message;
#     int line_number;
# };


all_wiz = []  # Maintain the wizards high score list about most popular castle.
next_time = 0

# 
# Sort the wiz list in ascending order.
#

# static struct wiz_list *insert(w, wl)
#     struct wiz_list *w, *wl;
# {
#     if (wl == 0) {
#     w.next = 0;
#     return w;
#     }
#     if (w.score > wl.score) {
#     wl.next = insert(w, wl.next);
#     return wl;
#     }
#     w.next = wl;
#     return w;
# }

# static void rebuild_list() {
#     struct wiz_list *wl, *w, *new_list = 0;
#
#     for (w = all_wiz; w; w = wl) {
#     wl = w.next;
#     new_list = insert(w, new_list);
#     }
#     all_wiz = new_list;
# }


def find_wiz(name):
    """
    Find the data, if it exists.
    """
    for wiz in all_wiz:
        if wiz.name == name:
            return wiz
    return None


def add_name(name):
    """
    Check that a name exists. Add it, if it doesn't.
    """
    wl = find_wiz(name)
    if wl is not None:
        return wl
    wl = Wizard()
    wl.name = name
    wl.score = 0
    wl.cost = 0
    wl.heart_beats = 0
    wl.total_worth = 0
    all_wiz.append(wl)
    return wl


def add_score(name, score):
    """
    Add score to an existing name.
    """
    wl = find_wiz(name)
    if wl is None:
        print("Add_score: could not find wizard %s" % name, file=sys.stderr)
    wl.score += score


def wiz_decay():
    """
    This one is called at every complete walkaround of reset.
    """
    # Perform this once every hour.#
    if next_time > backend.current_time:
        return
    wiz_list.next_time = backend.current_time + 60 * 60

    for wl in all_wiz:
        wl.score = wl.score * 99 / 100
        wl.total_worth = wl.total_worth * 99 // 100
        wl.cost = wl.cost * 9 / 10
        wl.heart_beats = wl.heart_beats * 9 // 10


def load_wiz_file():
    """
    Load the wizlist file.
    """
    try:
        f = open("WIZLIST", "r")
        for line in f:
            p = line.split()
            if len(p) != 3:
                print("Bad WIZLIST file.", file=sys.stderr)
            break

            name = p[0]
            score = int(p[1])

            if score > 0:
                add_name(name)
                add_score(name, score)
            f.close()
    except FileNotFoundError as fnfe:
        print("WIZLIST file not found", file=sys.stderr)
        print(fnfe)


def save_wiz_file():
    # Save the wizlist file.
    try:
        f = open("WIZLIST", "w")

        for wl in all_wiz:
            print("%s %d %d\n" % wl.name, wl.score, wl.total_worth)
        f.close()
    except FileNotFoundError:
        print("Could not open WIZLIST for write", sys.stderr)


# void wizlist(v)
#     char *v;
# {
#     struct wiz_list *wl, *this_wiz;
#     int total = 0, num = 0, this_pos, total_wizards;
#     extern struct object *command_giver;
#     int all = 0;
#     struct svalue *name;
#
#     if (!command_giver)
#     return;
#     if (v == 0) {
#     name = apply("query_real_name", command_giver, 0);
#     if (!name || name.type != T_STRING)
#         return;
#     v = name.u.string;
#     }
#     if (strcmp(v, "ALL") == 0)
#     all = 1;
#     this_wiz = find_wiz(v);
#     rebuild_list();
#     for (num = 0, wl = all_wiz; wl; wl = wl.next) {
#         total += wl.score;
#     num++;
#     if (wl == this_wiz)
#         this_pos = num;
#     }
#     total_wizards = num;
#     add_message("\nWizard top score list\n\n");
#     this_pos = num - this_pos + 1;
#     if (total == 0)
#     total = 1;
#     for (wl = all_wiz; wl; wl = wl.next) {
#     if (!all && num > 15 && (num < this_pos - 2 || num > this_pos + 2))
#         ;
#     else
#         add_message("%-15s %5d %2d%% (%d)\t[%4dk,%5d] %6d %d\n", wl.name,
#             wl.score, wl.score# 100 / total, num,
#             wl.cost / 1000,
#             wl.heart_beats, wl.total_worth, wl.size_array);
#     num--;
#     }
#     add_message("\nTotal         %7d     (%d)\n\n", total, total_wizards);
# }

# void remove_wiz_list() {
#     struct wiz_list *wl, *w;
#
#     for (w = all_wiz; w; w = wl) {
#     free(w.name);
#     wl = w.next;
#     free((char *)w);
#     }
# }

# void save_error(msg, file, line)
#     char *msg;
#     char *file;
#     int line;
# {
#     struct wiz_list *wl;
#     char name[100];
#     char *p;
#     int len;
#
#     p = get_wiz_name(file);
#     if(!p)
#     return;
#     strcpy(name, p);
#     wl = add_name(name);
#     if (wl.file_name)
#     free(wl.file_name);
#     len = strlen(file);
#     wl.file_name = xalloc(len + 4);#  May add .c plus the null byte, and /#
##ifdef COMPAT_MODE
#     strcpy(wl.file_name, file);
##else
#     strcpy(wl.file_name, "/");
#     strcat(wl.file_name, file);
#     len++;
##endif
#    # 
#    # If it is a cloned object, we have to find out what the file
#    # name is, and add '.c'.
#     #
#     p = strrchr(wl.file_name, '#');
#     if (p) {
#     p[0] = '.';
#     p[1] = 'c';
#     p[2] = '\0';
#     len = p - wl.file_name + 2;
#     }
#     if (wl.file_name[len-1] != 'c' || wl.file_name[len-2] != '.')
#     strcat(wl.file_name, ".c");
#     if (wl.error_message)
#     free(wl.error_message);
#     wl.error_message = string_copy(msg);
#     wl.line_number = line;
# }

# char *get_error_file(name)
#     char *name;
# {
#     struct wiz_list *wl;
#
#     wl = add_name(name);
#
#    # The error_message is used as a flag if there has been any error.
#     #
#     if (wl.error_message == 0) {
#     add_message("No error.\n");
#     return 0;
#     }
#     add_message("%s line %d: %s\n", wl.file_name, wl.line_number,
#         wl.error_message);
#     free(wl.error_message);
#     wl.error_message = 0;
#     return wl.file_name;
# }

#
# Argument is a file name, which we want to get the owner of.
# Ask the master.c object !
#
# char *get_wiz_name(file)
#     char *file;
# {
#     struct svalue *ret;
#     static char buff[50];
#
#     push_string(file, STRING_CONSTANT);
#     ret = apply_master_ob("get_wiz_name", 1);
#     if (ret == 0 || ret.type != T_STRING)
#     return 0;
#     strcpy(buff, ret.u.string);
#     return buff;
# }
