## LAB 3: systemd journal ##

**journald** is awesome e.g. for security concerns. Classical syslog based logs 
might be spoofed easily by applications introducing as different applications. 
In **systemd/journald** it's impossible - there is an actual authentication in 
systemd-units

No more Disk /dev/sda1 is **out of space** due to overgrowing logs. journald 
knows if there's enough disk space where it could write logs. If there's very 
low number of free space it will start to rotate old logs 
(**man journald.conf**)

If any application is spamming journald the **rate - limiting** will block it 
by dropping this application's messages. So the journald will not be lagged
(man journald.conf)

**Messages filtering** is done durring accepting messages (so during READ) not 
during write.

Message logtime is a time of when it was received.

Let's do something with journald:

1. What happened recently? `journalctl -e`
1. Show me last 40 entries: `journalctl -n 40`
1. In reverse order: `journalctl -r`
1. Kernel related (like dmesg, but not 1:1): `journalctl -k`
1. Since last boot: `journalctl -b`
1. Only errors or worse please (severity): `journalctl -p err`
    - emerg(0), alert(1), crit(2), err(3), warning(4), notice(5), info(6), debug(7)
1. From info to errors: `journalctl -p info..err`
1. Actually show everything (so like systemctl): `journalctl -p debug`
1. By default journalctl uses 'less' paging; let's disable it: `journalctl --no-pager`
1. Live version like tail -f please: `journalctl -f`
1. Different output format?
    1. `journalctl -o json`
    1. `journalctl -o json-pretty`
    1. short, verbose, export, json, cat    
1. What about time filtering?
    1. `man systemd.time` (don't confuse with systemd.timer)
    1. `journalctl --since="2016-08-01"`
    1. `journalctl --until="2016-09-01"`
    1. Timezone? default local, but you may add definition, e.g. UTC
        - `journalctl --since="2016-11-26 07:00:00 UTC"`
    1. today, yesterday, tomorrow, -1week, -1month, -20day - see docs
1. Managing logs capacity / disk space?
    1. Journald should already have persistent storage (since F19?) Simply
       `mkdir /var/log/journal` if not exists and edit /etc/systemd/journal.conf`
    1. Show current disk usage: `journalctl --disk-usage`
    1. Truncate logs to given size: `journalctl --vacuum-size=2.8GG`
	1. Set logs retention: `journalctl --vacuum-time=1years`
	1. or simply define it in configuration: 
        1. `man journald.conf`
	    1. `/etc/systemd/journald.conf`
1. Specify unit: `journalctl -u httpd`
1. Show entries related to specific device: `journalctl /dev/sda`
    - but actually might be safer with UUID instead of device; UUID doesn't 
      change between reboots!
1. Old school grepping still works, but takes a lot of time for huge logs 
   (no indexation involved). Use smart - with journald filters
1. Show entries related to binary? `journalctl /usr/bin/bash`
1. Show detailed metadata: `journalctl -o verbose`
    1. `journalctl -F [TAB]`
    1. `man systemd.directives`
    1. Specific PID: `journalctl _PID=1`
    1. Could provide more than one: `journalctl _PID=1 _PID=123`
    1. `journalctl -F _SYSTEMD_UNIT`
    1. `journalctl _SE[TAB]`
    1. Could you filter by specific source code and code line?
    1. Could you filter by specific source code and specific code function?
    1. Like `-u` but differently? `journalctl _SYSTEMD_UNIT=crond.daemon.service`
    1. Filter by hostname: `journalctl _HOSTNAME=somehost`
    1. `journalctl _UID=x GID=y`
    1. Add more contextual info: `journalctl -x` - this might not show 
       anything; depending if application provides this kind of information
1. Cursors: thanks to that journald knows where it stopped pulling data from 
   specified journal and where to continue you can see the cursor state 
   in `-o verbose` on top: [s=...some-very-long-string]
1. Pipelining program output to journal with **systemd-cat**:
    1. `systemd-cat cat /proc/loadavg`
    1. cat /proc/loadavg | systemd-cat
    1. The first one will capture stderr and stdout and latter only stdout
1. Let's setup simple HTTP logs viewer:
	1. `dnf install systemd-journal-remote`
	1. `systemctl enable --now systemd-journal-gatewayd`
	1. http://localhost:19531/browse
	1. http://localhost:19531/machine
	1. man systemd-journal-gatewayd
1. Testing journal? use logger: `logger test`
    - Might even specify loglevel: `logger -p error some test errmessage`
1. Sealing the journal
    1. FSS stands for Forward Secure Sealing. It is used by journald to ensure
       the integrity of the journal and to seal the logs cryptographically. For
       details on FSS see [https://eprint.iacr.org/2013/397.pdf]
    1. Now you may check integrity of your journal with `journalctl --verify`
    1. Generate your keys: `journactl --setup-keys`
    1. Verify your journal integrity with FSS keys: `journalctl --verify-key [path-to-key] --verify`
1. journal & Python
    - check [journal-python](journal-python/) directory for a quick task:
        - run **journal-app.py** and see code how it works
        - run **journal-app-handler** and check how to integrate w/system 
          logger
        - register **journal-app-service.service** (enable / start)
        - see `journalctl -u journal-app-service -o verbose`
        - run **journal-reader** while **journal-app-service** is running. What
          do you see? :)

### Do it @home ###

Learn about pushing logs to a central server. Read following manuals to see
how to do it:

- man systemd-journal-upload
- man systemd-journal-gatewayd.service
- man systemd-journal-gatewayd.service
- man systemd-journal-remote