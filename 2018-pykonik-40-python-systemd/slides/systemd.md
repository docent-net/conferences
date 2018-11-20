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

![Default-aligned image](logo.png)

## Python, systemd i journald: lecimy XD

### Pykonik #40

2018-11-22<br>
Maciej Lasyk

---
template: default

# agenda

.left[
- intro to systemd
- services & unit files
- journal / logging
- nspawn containers
- portable services
- socket activation
- dbus
- sd-notify
- maybe some python? :)
]

---
template: default

# systemd - what is that?

---
template: default

#### Linux startup:
.left[
- BIOS etc (hardware related stuff)
- boot loader (BIOS w/MBR, UEFI no need for boot loader: Kernel loader direct exec)
   - LILO (remember?), GRUB 1 & 2, SYS/ISOLINUX etc
- Kernel loading
   - loading stage: load compressed Kernel into mem and decompress
   - startup stage: detect hardware, load init system and setup user - space and go idle
- init system goes in (systemd here)
]

---
template: default

# systemd - learning

```bash
man systemd.index

[...]
This index contains 691 entries, referring to 245 individual manual pages.
```

--

See what's more:
```bash
man systemd[TAB][TAB]
```
--

.left[
- [systemd for developers I](http://0pointer.de/blog/projects/socket-activation.html)
- [systemd for developers II](http://0pointer.de/blog/projects/socket-activation2.html)
- [systemd for developers III](http://0pointer.de/blog/projects/journal-submit.html)
]

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
- Plz show me dependencies of httpd: `systemctl list-dependencies docker`
- `systemctl enable --now docker`
- `sytemctl disable --now docker`
- `systemctl show docker`
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
```bash
systemd-analyze time
systemd-analyze blame
systemd-analyze plot > boot.svg 
systemd-analyze dump
systemd-analyze verify system.slice
systemd-analyze dot 'docker.*' | dot -Tsvg > docker.svg
systemd-analyze dot --to-pattern='*.target' --from-pattern='*.target' | \`
dot -Tsvg > targets.svg
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
- `systemd-run --unit=test_run env`
- `systemd-run -p BlockIOWeight=10 updatedb`
- Timers:
    - `date; systemd-run --on-active=20 --timer-property=AccuracySec=100ms \
       /bin/touch /tmp/foo`
    - `journalctl -b -u run-71.timer`
    
    `--on-active=, --on-boot=, --on-startup=` 
    `--on-unit-active=, --on-unit-inactive=`
```]

---
template: default

#### systemd-bin
# and many more

.left[
- systemd-cgtop
- systemctl kill
- man systemd.kill
- systemd-path
- man file-hierarchy
- systemd-detect-virt
- timedatectl
]

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

systemctl kill

KillMode, KillSignal, SendSIGHUP, SendSIGKILL

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

# nspawn containers

--

### containers built into the systemd

--

### no daemon behind

--

### no need to do anything with storage or network

--

however quite low - level w/higher entry barrier than Docker

---
template: default

#### nspawn containers

.left[
```bash
dnf --releasever=25 --installroot=/var/lib/machines/f25-systemd-demo
   install systemd passwd dnf fedora-release 
systemd-nspawn -D /var/lib/machines/f25-systemd-demo
passwd
cp /usr/lib/systemd/system/systemd-nspawn\@.service
   /etc/systemd/system/systemd-nspawn@f25-systemd-demo.service
systemctl daemon-reload
systemctl enable --now systemd-nspawn@f25-systemd-demo.service
machinectl
machinectl login/shell f25-systemd-demo
```]

--

### machinectl

---
template: default

# portable services

big fat TODO

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

---
template: default

#### Python & systemd

.left[
- python-systemd: https://github.com/systemd/python-systemd - **obsolete**
- cysystemd: https://github.com/mosquito/cysystemd
- sdnotify: https://github.com/bb4242/sdnotify - **obsolete**
- pystemd: https://github.com/facebookincubator/pystemd
]

---
template: default

#### demo 1: working with journal/logging

cysystemd: https://github.com/mosquito/cysystemd

---
template: default

#### demo 2: self - healing w/sd-notify

cysystemd: https://github.com/mosquito/cysystemd

---
template: default

#### demo 3: manaigng services w/pystemd

pystemd: https://github.com/facebookincubator/pystemd

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

![Default-aligned image](logo.png)

# Thanks, Q&A?

### Maciej Lasyk

@docent-net<br>
[https://maciej.lasyk.info/slides/2018-pykonik-40-python-systemd/](https://maciej.lasyk.info/slides/2018-pykonik-40-python-systemd/)