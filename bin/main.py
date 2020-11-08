import os
import sys
import time

from bin import backend
from bin import config
from bin import simulate
from bin import wiz_list

port_number = config.PORTNO

def main():
    
    # set the game current time
    backend.current_time = time.time()
    
    # change to the mudlib directory as the working directory
    os.chdir(config.MUD_LIB)
    
    # load the master object
    simulate.master_ob = simulate.load_object("obj/master",0)
       
    # test that it loaded correctly
    if simulate.master_ob == None:
        print("The file secure/master must be loadable.", file=sys.stderr)
        exit(1)

    # did the game shutdown while we were loading?
    if simulate.game_is_being_shut_down:
        exit(1)
        
    # load the wiz_list files
    wiz_list.load_wiz_file()
    
    # load the initial objects needed
    backend.load_first_objects()

    # start the game
    backend.backend()

if __name__ == "__main__":
    main()
    

