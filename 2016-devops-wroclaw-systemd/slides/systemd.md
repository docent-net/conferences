name: default
layout: true

class: center, middle
count: false
---
name: left
layout: true

class: left, middle
count: false
---
template: default

![Default-aligned image](pid1.png)

# systemd primer

## devops Wrocław Meetup #5

2016-11-29<br>
Maciej Lasyk

---
template: left

# agenda

- systemd-bin (30min)
- 5-min break?
- services & unit files (15min)
- journal / logging (25min)
- 5-min break?
- nspawn containers (5min)
- integrating apps w/sd-notify (15min)

---
template: default

# systemd - what is that?
---
template: default

# systemd - learning

--

```bash
man systemd.index
```

--

See what's more:
```bash
man systemd[TAB][TAB]
```

---
template: default

# systemd-bin
---
template: default

#### systemd-bin
# systemctl

--
For dealing with unit files, services, targets etc we use **systemctl**

---
template: default

#### systemd-bin
# systemctl

.left[
```bash`
- man systemctl
- What's happening on my system? `systemctl status`
- Show me loaded services: `systemctl -t service`
- Show me all unit files: `systemctl list-unit-files`
- Set vendors default (enable / disable): `systemctl preset docker`
- What's my system's current state? `systemctl is-system-running`
- Which units are in failed state? `systemctl --failed`
- Plz show me dependencies of httpd: `systemctl list-dependencies httpd`
- `systemctl enable --now httpd`
- `sytemctl disable --now mariadb`
- `systemctl show httpd`
```]
---
template: default

#### systemd-bin
# analyzing boot process

--

With systemd analyzing boot process looks quite interesting<br>
(demo, pictures!):

--

.left[
```bash`
systemd-analyze time
systemd-analyze blame
systemd-analyze plot 
systemd-analyze dump
systemd-analyze verify system.slice
systemd-analyze dot 'docker.*' | dot -Tsvg > docker.svg
systemd-analyze dot --to-pattern='*.target' --from-pattern='*.target' | \`
dot -Tsvg > targets.svg
```]
---
template: default

#### systemd-bin
# coredumps

--

With systemd we may generate and browse and view any historical coredumps:

--

.left[
```bash`
coredumpctl dump
coredumpctl dump docker
coredumpctl dump _PID=666
    (journalctl general predicates; man systemd.directives)
coredumpctl dump /usr/sbin/httpd
coredumpctl gdb _PID=666
```]

---
template: default

#### systemd-bin
# cgroups
.left[
```bash`
systemd-cgtop
systemd-cgtop -d 5 -n 3
systemd-cgls /system.slice/auditd.service
```]

---
template: default

#### systemd-bin
# killing processes
--

Actually units may have policy about how to be killed in a proper way
by setting **KillMode=** in unit file:
.left[
```bash`
systemctl kill docker.service
man systemd.kill
```]

---
template: default

#### systemd-bin
# FHS!
--

systemd actually takes care about FHS
<br>You may easily see what's purpose of
specific directories

--

.left[
```bash`
systemd-path
man file-hierarchy
systemd-path temporary
systemd-path system-state-logs
```]

don't confuse with systemd.path (path activation)

---
template: default

#### systemd-bin
# detecting virtualization

--

Systemd will tell you if you're on bare, VM, container of chroot:

--

.left[
```bash
systemd-detect-virt
man systemd-detect-virt
```]

---
template: default

#### systemd-bin
# DNS resolving

--

systemd provides resolver service (systemd-resolved). You may query it against
DNS entries:

--
.left[
```bash
systemd-resolve www.google.com
systemd-resolve -t mx google.com
```]

---
template: default

#### systemd-bin
# finger

--
.left[
```bash
loginctl list-users
loginctl list-sessions
loginctl user-status
loginctl session-status
man loginctl
```]
---
template: default

#### systemd-bin
# system time management

--

.left[
```bash
timedatectl
timedatectl list-timezones
timedatectl set-time 2016-11-30 11:12:13
systemctl status systemd-timesyncd.service
timedatectl set-ntp true
```]

---
template: default

#### systemd-bin
# inhibit

--

systemd provides a way to make sure that your hardware doesn't sleep / 
hibernate / poweroff during execution of given command:

--
.left[
```bash
systemd-inhibit something
man systemd-inhibit
```]

---
template: default

#### systemd-bin
# d-bus

--

So systemd uses D-Bus for IPC (inter - process communication).

--

.left[
```bash
- see current state of procs registered in bus: `busctl`
- more info: https://freedesktop.org/wiki/Software/dbus/
- `sudo busctl capture > test.pcap` + wireshark
- `busctl tree`
```]

--

### demo?
.left[
```bash
busctl --user
```]

---
template: default

#### systemd-bin
# process confinement

--

You may run any process under systemd / cgroups confinement:

--

.left[
```bash
- `systemd-run env`
- `systemd-run -p BlockIOWeight=10 updatedb`
- Timers:
    - `date; systemd-run --on-active=30 --timer-property=AccuracySec=100ms \
       /bin/touch /tmp/foo`
    - `journalctl -b -u run-71.timer`
- `systemd-run --scope -p BlockIOWeight=10 --user tmux`
    - `tmux ls`
```]

---
template: default

5 - min break?
---
template: default

# services & unit files
---
template: default

#### services & unit files
# imperativeness vs declarativeness

--

compare httpd init script vs unit file
---
template: default

#### services & unit files
# types of units

--

service

target

path

timer

socket

...

--

**man systemd.(device|mount|automount|swap|slice|scope)**

---
template: default

#### services & unit files
# runlevels & targets

--

Before systemd we had runlevels (remember? chkconfig && 2,3,5?). Now we have
units of type **target**. Think of targets as **unit aggregators / groups**

--

.left[
```bash
- A bit of documentation: `man systemd.target`
- Display possible targets: `systemctl list-units --type=target`
- Which is default (current runlevel)? `systemctl get-default`
- Wanna change default target (runlevel)? `systemctl isolate [target]` / AllowIsolate=
- `systemctl isolate multi-user.target` (or) `systemctl isolate runlevel3.target`
- `systemctl isolate graphical.target` (or) `systemctl isolate runlevel5.target`
```]

---
template: default

#### services & unit files
# services dependencies

--

   Requires, Requisite, Wants, BindsTo, PartOf, Conflicts, Before,
   After, OnFailure, PropagatesReloadTo, ReloadPropagatedFrom,
   StopWhenUnneeded, DefaultDependencies, WantedBy, RequiredBy, Also
---
template: default

#### services & unit files
# starting after installation

--

**systemctl mask**

--

Debian, Ubuntu & autostart

--

> http://maciej.lasyk.info/2016/Nov/29/systemd-mask/

---
template: default

#### services & unit files
# cronjobs / timers

--

.left[
```bash
[Unit]
Description=Run script every hour

[Timer]
OnBootSec=10min
OnUnitActiveSec=1h
Unit=script.service

[Install]
WantedBy=multi-user.target
```]

---
template: default

#### services & unit files
# socket activation

--

    ListenStream, ListenDatagram, ListenSequentialPacket, ListenFifo,
    ListenSpecial, ListenNetlink, ListenMessageQueue, ListenUSBFunction,
    SocketProtocol, BindToDevice...
    
--

.left[
```bash
[Unit]
Description=Socket activation for simple systemd-notify app

[Socket]
ListenStream=1025

[Install]
WantedBy=sockets.target
```]

---
template: default

#### services & unit files
# cgroups control

--

   CPUShares, CPUAccounting, MemoryAccounting, MemoryLimit,
   BlockIOAccounting, BlockIOWeight, BlockIOReadBandwidth,
   BlockIOWriteBandwidth

---
template: default

#### services & unit files
# defining kill method

--

systemd-kill

KillMode, KillSignal, SendSIGHUP, SendSIGKILL
---
template: default

#### services & unit files
# GUI? 

--

cockpit demo!
---
template: default

#### services & unit files
# sysv import?

--
.left[
1. Systemd maintains 99% backwards compatibility with LSB 
   compatible initscripts and the exceptions are well documented
2. No need to convert
3. http://www.freedesktop.org/wiki/Software/systemd/Incompatibilities/
4. http://0pointer.de/blog/projects/systemd-for-admins-3.html
]

---
template: default

# journal & logging

--

journald resolves security in syslog (authentication)

--

no more "disk is out of space" due to growing logs

--

built-in anti d-dos (rate - limiter)

---
template: default

#### journal & logging
# basic filtering
.left[
```bash
journalctl:
recently: -e, last 4 entries: -n 40, reverse: -r, kernel related: -k,
since last boot: -b, no-paging: --no-pager, live tailing: -f
```]

--

# severity filtering:
.left[
```bash
logs severity: -p err, range? -p info..err
    - emerg(0), alert(1), crit(2), err(3), warning(4), notice(5), info(6), debug(7)
```]

---
template: default

#### journal & logging
# output formatting
.left[
```bash
journalctl -o json
journalctl -o json-pretty
short, verbose, export, json, cat
```
]

--

# time filtering
.left[
```bash
man systemd.time
journalctl --since="2016-08-01"
journalctl --until="2016-09-01"
Timezone? default local, but you may add definition, e.g. UTC
    journalctl --since="2016-11-26 07:00:00 UTC"
today, yesterday, tomorrow, -1week, -1month, -20day - see docs
```]
---
template: default

#### journal & logging
# grepping

--

Simply remember to filter first!

```bash
journalctl -b -u some.service --no-pager | grep -i 'some_keyword'
```

---
template: default

#### journal & logging
# managing disk space

--

persistent storage? mkdir /var/log/journal

--

.left[
```
Show current disk usage: `journalctl --disk-usage`
Truncate logs to given size: `journalctl --vacuum-size=2.8GG`
Set logs retention: `journalctl --vacuum-time=1years`

Or simply define it in configuration: `man journald.conf`
```]
---
template: default

#### journal & logging
# metadata

--

.left[
```bash
Show detailed metadata: `journalctl -o verbose`
> `journalctl -F [TAB]`
> `man systemd.directives`
Specific PID: `journalctl _PID=1`
Could provide more than one: `journalctl _PID=1 _PID=123`
> `journalctl -F _SYSTEMD_UNIT`
> `journalctl _SE[TAB]`
Filter by hostname: `journalctl _HOSTNAME=somehost`
> `journalctl _UID=x GID=y`
Add more contextual info: `journalctl -x` - (info app - defined)
```]
---
template: default

#### journal & logging
# pipelining stdout/err to journal

--
.left[
```bash
> `systemd-cat cat /proc/loadavg`
> `cat /proc/loadavg | systemd-cat`

The first one will capture stderr and stdout and latter only stdout
```]

---
template: default

#### journal & logging
# HTTPD logs viewer?
.left[
```bash
> `dnf install systemd-journal-remote`
> `systemctl enable --now systemd-journal-gatewayd`
http://localhost:19531/browse
http://localhost:19531/machine
man systemd-journal-gatewayd
```]

---
template: default

#### journal & logging
# sealing journal

--

FSS - Forward Secure Sealing
used by journald to ensure the integrity of the journal and to seal the logs 
cryptographically.
 
> https://eprint.iacr.org/2013/397.pdf

--

.left[
```bash
Now you may check integrity of your journal with `journalctl --verify`
Generate your keys: `journactl --setup-keys`
Verify journal integrity w/FSS keys: `journalctl --verify-key [path-to-key] --verify`
```]

---
template: default

#### journal & logging
# journal & Python

--

another demo

---
template: default

# 5 - min break?
---
template: default

# nspawn containers

--

### very simple containers

--

### no daemon behind

--

### no need to do anything with storage or network

--

just dnf / yum install and go!

---
template: default

#### nspawn containers

.left[
```bash
dnf --releasever=25 --installroot=/var/lib/machines/f25
   install systemd passwd dnf fedora-release 
systemd-nspawn -D /var/lib/container/f25
passwd
cp /usr/lib/systemd/system/systemd-npawn\@.service
   /etc/systemd/system/systemd-nspawn@f25.service
systemctl enable --now systemd-nspawn@f25.service
```]

--

### machinectl

---
template: default

# sd-notify

--

even more demos...

---
template: default

# #learningsystemd

man systemd.index

https://www.freedesktop.org/wiki/Software/systemd/

http://0pointer.de/blog/projects/ (look 4 systemd*)

http://0pointer.de/blog/projects/the-biggest-myths.html

http://maciej.lasyk.info/tag/learning-systemd.html
---
template: default

![Default-aligned image](pid1.png)

# Thanks, Q&A?

### Maciej Lasyk

@docent-net<br>
http://maciej.lasyk.info
