#!/usr/bin/env python
import os
import pyinotify

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        if '.py' in event.pathname:
            print("Compiling {}".format(event.pathname))
            os.system("python {}".format(event.pathname))
            print("Compiling rackprinter")
            os.system("python {}".format('rackprinter.py'))
            print("Ok")

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('.', mask, rec=True)

notifier.loop()
