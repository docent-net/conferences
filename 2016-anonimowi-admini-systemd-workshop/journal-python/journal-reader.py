#!/usr/bin/python3
# See https://www.freedesktop.org/software/systemd/python-systemd/journal.html

from systemd import journal
j = journal.Reader()
j.this_boot()
j.log_level(journal.LOG_DEBUG)
# j.add_match(_SYSTEMD_UNIT="sd-notify-app-service.service")
j.add_match("MESSAGE_ID=ad3774a3e11348d8bf0457d8ca04899b")
j.add_match("LOGGER=app_logger")
for entry in j:
    print(entry)
    # print(entry['MESSAGE'])
