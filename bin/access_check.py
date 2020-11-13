"""
check a given internet address against patterns given in an ACCESS.ALLOW
file.
Written by Markus Wild for Loch Ness in 1991.
Spread by gec with permission of Markus Wild.
Source is in the public domain. No charges allowed.

notice the time stamp when we last scanned the file, and rescan if it
changed since that (this enables us to edit the file without having to
reboot lpmud to read it)
NOTICE: when changing the access file, the old tables ARE DISCARDED. This
        means, that users logged in will not count for the per-class
        maximum. This will normalize, as soon as users log out, as the
        "currently" counter will not go below 0.
"""
# this file should better be defined in config.h ;-) #


from datetime import datetime
import os
import socket


ACCESS_FILE = "ACCESS.ALLOW"

# log-file to show valid and rejected connections #
ACCESS_LOG = True  # simply NOT define this for NO logs#

# maximal string length to be output #
MAX_MESSAGE = 255

addr_tab = None
class_tab = None
last_read = 0


class Access_Class():
    class_num = 0  # the class number #
    currently = 0  # currently <= this number of logged in users #
    maximum = -1  # 0: disallowed, -1: no maximum #
    message = []  # message to be printed in case a login can't be permitted #


class Access_Address():
    addr = []        # [0..255]: number, -1: all #
    hstart = 0
    hend = 0    # start/end hour #
    ac = None


def check_read_file(name):
    global addr_tab, class_tab, last_read
    """
    check the file, and if it was changed, (re)read it into memory
    """

    if os.path.isfile(name):
        st_mtime = os.path.getmtime(name)
        if st_mtime > last_read:

            addr_tab = []
            class_tab = {}
            # throw away the old information #

            try:
                f = open(name, "r")

                for buffer in f:

                    aa = Access_Address()
                    ac = Access_Class()

                    # a comment, skip #
                    if buffer[0] == '#':
                        continue

                    # if there is no ':' in there, #
                    # this is probably an empty line #
                    if buffer.find(':') == -1:
                        continue

                    # more or less no error-checking ;-)) #
                    strs = buffer.split(":")
                    addr = strs[0].split(".")

                    ac.class_num = int(strs[1])
                    ac.currently = 0
                    ac.maximum = int(strs[2])
                    aa.hstart = int(strs[3])
                    aa.hend = int(strs[4])
                    ac.message = strs[5]
                    aa.addr = []

                    # check whether this class is already defined #
                    i = 0
                    while i < len(class_tab.keys()):
                        if class_tab[i].class_num == ac.class_num:
                                # in this case just set a pointer #
                                # to the defined class #
                                aa.ac = class_tab[i]
                                break
                        i += 1

                    # if not, define it #
                    if i == len(class_tab.keys()):
                        class_tab[i] = ac
                    aa.ac = class_tab[i]

                    # now set up the address, #
                    # maps into -1, anything else is vanilla #
                    aa.addr.append(int(addr[0]) if addr[0] is not "*" else -1)
                    aa.addr.append(int(addr[1]) if addr[1] is not "*" else -1)
                    aa.addr.append(int(addr[2]) if addr[2] is not "*" else -1)
                    aa.addr.append(int(addr[3]) if addr[3] is not "*" else -1)

                    # and add it to our address table #
                    addr_tab.append(aa)

                # over total input #
                f.close()
                last_read = st_mtime
                return
            except Exception as e:
                print(e)
    else:
        raise Exception("No file " + ACCESS_FILE)


def allow_host_access(sock, address, out_file):
    """
    the main function, validate an address (peer of given socket).
    return 0, if access is not permitted, else return a pointer to the
    corresponding class. Pass that pointer on logout to "release_host_access".
    """
    check_read_file(ACCESS_FILE)

    # getting the IP address using socket.gethostbyname() method
    ipname = address[0]

    addr = [int(num) for num in ipname.split(".")]

    for ap in addr_tab:
        pos = 0
        # check for address. match if either equal or wildcard #
        while pos < 4:
            if ap.addr[pos] != addr[pos] and ap.addr[pos] != -1:
                break
            pos += 1

        if pos == 4:  # a match #
            # if hstart and hend are not == 0, #
            # check whether ap is in the interval #
            if ap.hstart or ap.hend:
                now = datetime.now()
                if ap.hstart < ap.hend:
                    if now.hour < ap.hstart or now.hour > ap.hend:
                        continue
                else:
                    if now.hour > ap.hend and now.hour < ap.hstart:
                        continue

            # no maxmium? #
            if ap.ac.maximum == -1:
                log_access(ipname, 1)
                return ap.ac

            # else there is a maximum, in the worst case 0 #
            if ap.ac.currently >= ap.ac.maximum:
                out_file.send(bytes(ap.ac.message, "utf-8"))
                out_file.send(b'\n', 1)
                out_file.shutdown(2)
                out_file.close()
                log_access(ipname, 0)
                return None

            # bump up the counter #
            ap.ac.currently += 1
            log_access(ipname, 1)
            return ap.ac

    # default is: don't allow access #
    out_file.send(b'Sorry, you\'re not allowed to use LPMUD.\n')
    out_file.shutdown(2)
    out_file.close()
    log_access(ipname, 0)
    return None


# This is called, when a user logs out. #

# void
# release_host_access (class)
#      struct access_class *class;
# {
#   if (class.maximum != -1 and class.currently > 0)
#     -- class.currently;
# }
#


def log_access(addr, ok):
    if ACCESS_LOG:
        try:
            log = open(ACCESS_LOG, "a")

            if log:
                log.write("%s: %s\n" % addr,  "granted" if ok else "denied")
            log.close()
        except Exception as e:
            print(e)
