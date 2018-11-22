#!/usr/bin/python3

from time import sleep
import logging
from cysystemd import journal

class App(object):
    def __init__(self):
        self.create_logger()

    def create_logger(self):
        self.log = logging.getLogger('pykonik_logger')
        self.log.propagate = False
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(journal.JournaldLogHandler())

    def start(self):
        # do something specific to app startup
        sleep(2)

        count = 1
        while True:
            self.log.info("Running... {}".format(count))
            count += 1
            sleep(2)
            if count == 10:
                break

app = App()
app.start()