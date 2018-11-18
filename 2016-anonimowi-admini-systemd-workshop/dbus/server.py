# read this: https://dbus.freedesktop.org/doc/dbus-python/api/

from PyQt4.QtCore import *
import dbus
import dbus.service
from dbus.mainloop.qt import DBusQtMainLoop
from os import uname


class AAUname(dbus.service.Object):
    def __init__(self):
        busname = dbus.service.BusName('org.documentroot.AAuname',
                                       bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, busname, '/AAuname')

    @dbus.service.method('org.documentroot.AAuname')
    def aa_uname(self): return uname()[2]


DBusQtMainLoop(set_as_default=True)
app = QCoreApplication([])
aa_uname = AAUname()
app.exec_()
