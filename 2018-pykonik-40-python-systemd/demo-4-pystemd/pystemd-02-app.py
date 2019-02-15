#!/usr/bin/python3

from time import sleep
import pystemd.daemon


class App(object):
    def __init__(self):
        self.count = 1

    def start(self):
        # do something specific to app startup
        sleep(2)

        # tell systemd we're ready
        pystemd.daemon.notify(False, ready=1,
                              status="starting processor service")
        while True:
            self.process_something()

        # if you'd like to stop properly
        self.stop()

    def process_something(self):
        print("watchdog...")
        pystemd.daemon.notify(False, ready=1,
                              status="STATUS=Count is {}".format(self.count))
        pystemd.daemon.notify(False, watchdog=1)
        # processing....
        self.count += 1
        sleep(1)

    def stop(self):
        # tell systemd we're stopping service
        pystemd.daemon.notify(False, 'STOPPING=1')


app = App()
app.start()
