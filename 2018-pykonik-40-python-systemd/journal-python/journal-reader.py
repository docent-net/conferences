#!/usr/bin/python3
# See https://www.freedesktop.org/software/systemd/python-systemd/journal.html

from systemd import journal
j = journal.Reader()
j.this_boot()
# j.log_level(journal.LOG_DEBUG)
# j.add_match(_SYSTEMD_UNIT="sd-notify-app-service.service")
# j.add_match("MESSAGE_ID=7729991e-244c-49cd-91c4-35299ea40026")
j.add_match("SYSLOG_IDENTIFIER=myapp")
for entry in j:
    # print(entry)
    print(entry['MESSAGE'])
