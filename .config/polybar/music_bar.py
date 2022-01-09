#! /bin/env python3

from os import getppid, system, getpid
from subprocess import getoutput
import dbus
from time import sleep

with open("/tmp/polybar-music.pid", "w") as f:
    f.write(str(getpid()).strip())

session_bus = dbus.SessionBus()

while True:
    player_names = [service  for service in session_bus.list_names() if service.startswith('org.mpris.MediaPlayer2.')]
    players = [session_bus.get_object(service, '/org/mpris/MediaPlayer2') for service in player_names]
    print(players, player_names)
    process_id = getoutput("xprop -name 'polybar-middle' _NET_WM_PID").split()[-1]
    process_id = "" if process_id == "exists!" else process_id
    if (len(players) == 0):
        # kill polybar if already running
        #print("no player")
        if process_id != "":
            # print("killing polybar!")
            system("kill {0}".format(process_id))
    else:
        # start polybar
        # print("player exists")
        if process_id == "":
            # print("creating polybar!")
            system("polybar middle &")
            
    sleep(2)
