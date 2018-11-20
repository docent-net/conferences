import dbus

bus = dbus.SessionBus()
server = bus.get_object('org.documentroot.AAuname', '/AAuname')
print(server.aa_uname(dbus_interface='org.documentroot.AAuname'))
