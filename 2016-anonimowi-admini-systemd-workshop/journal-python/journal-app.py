#!/usr/bin/python3
# See https://www.freedesktop.org/software/systemd/python-systemd/journal.html

from systemd import journal

journal.send('Hello world')
journal.send('Hello, again, world', FIELD2='Greetings!')

stream = journal.stream('myapp', priority=3)
res = stream.write('message...\n')