#!/usr/bin/python3

#
# Gesture daemon for ubports. Listen on DBus for gestures and do stuff.
# 
# Copyright 2019 Willem-Jan de Hoog
#
# based on dbus-python example
# mpris stuff thanks to https://github.com/mel00010/OmniPause/blob/master/OmniPause.py

import os
import sys
import traceback

#import gobject
from gi.repository import GObject as gobject

import dbus
import dbus.mainloop.glib

# does not work due to permissions 
def config_gestures():
    try:
        fp = open("/proc/touchpanel/music_enable", "r+")
        fp.write("1")
        fp = open("/proc/touchpanel/double_tap_enable", "r+")
        fp.write("1")
        fp = open("/proc/touchpnanel/flashlight_enable", "r+")
        fp.write("1")
    except Exception as exc:
         print("Exception in config_gestures:", exc)

def toggle_flash():
    try:
        fp = open("/sys/class/leds/torch-light/brightness", "r+")
        cur_state = fp.read(1)
        fp.seek(0)
        if cur_state == '0':
           fp.write("1")
        else:
           fp.write("0")
    except Exception as exc:
         print("Exception in toggle_flash:", exc)

sessionBus = dbus.SessionBus()

def mprisCommand(command):
    mprisPlayers = []
    for i in sessionBus.list_names():
        if i.startswith("org.mpris.MediaPlayer2."):
            print("found: ", i)
            player = sessionBus.get_object(i, '/org/mpris/MediaPlayer2')
            if command == 'previous-song':
                player.Previous(dbus_interface='org.mpris.MediaPlayer2.Player')
            elif command == 'next-song':
                player.Next(dbus_interface='org.mpris.MediaPlayer2.Player')
            elif command == 'play-pause':
                player.PlayPause(dbus_interface='org.mpris.MediaPlayer2.Player')

def catchall_gesture_signals_handler(gesture_string):
    print( "received: " + gesture_string )
    try:
        if gesture_string == 'toggle-flash':
            toggle_flash()
        else:
            mprisCommand(gesture_string)
    except Exception as exc:
         print("Exception in catchall_gesture_signals_handler:", exc)

def catchall_signal_handler(*args, **kwargs):
    print( ("Caught signal (in catchall handler) "
            + kwargs['dbus_interface'] + "." + kwargs['member']) )
    for arg in args:
        print( "        " + str(arg) )

def catchall_gesture_interface_handler(gesture_string, dbus_message):
    print( "com.ubports.Unity.Gestures interface says " + gesture_string + " when it sent signal " + dbus_message.get_member())


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    #bus = dbus.SessionBus()
    bus = dbus.SystemBus()
    try:
        object  = bus.get_object("com.ubports.Unity.Gestures", "/com/ubports/Unity/Gestures")

    except dbus.DBusException:
        traceback.print_exc()
        print( usage )
        sys.exit(1)

    #bus.add_signal_receiver(catchall_signal_handler, interface_keyword='dbus_interface', member_keyword='member')

    bus.add_signal_receiver(catchall_gesture_signals_handler, dbus_interface = "com.ubports.Unity.Gestures", signal_name = "Gesture")

    #bus.add_signal_receiver(catchall_gesture_interface_handler, dbus_interface = "com.ubports.Unity.Gestures", message_keyword='dbus_message')

    #config_gestures()

    loop = gobject.MainLoop()
    loop.run()
