

class Interactive():
    socket = None
    ob = None           # Points to the associated object #
    input_to = None     # To be called with next input line ! #

    prompt = None
    closing = False     # True when closing this socket. #
    do_close = False    # This is to be closed down. #
    text = []
    snoop_on = None
    snoop_by = None
    noecho = False      # Don't echo lines #
    last_time = 0       # Time of last command executed #
    default_err_message = None  # This or What ? is printed when error #
    access_class = None  # represents a "cluster" where this player is from #

    message_buf = []
