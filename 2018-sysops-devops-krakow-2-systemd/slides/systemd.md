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

## Trochę więcej na temat systemd

### SysOps / DevOps Kraków MeetUp #2

2018-01-17<br>
Maciej Lasyk

---
template: left

# agenda

- bonus: Amazon Linux 2
- systemd-bin
- services & unit files
- journal / logging
- nspawn containers
- integrating apps w/sd-notify

---
template: default

# Amazon Linux 2

.left[
- [Release notes](https://aws.amazon.com/amazon-linux-2/release-notes/)
- This is a LTS candidate (5 years support when GA)
- Kernel 4.9.75-25.55.amzn1.x86_64 (very similar to previous)
- diff pstree
- new gcc, glibc, binutils (taken from Fedora 25 & 26)
- systemd v.219 (Same as RedHat/Centos 7) - 2015-02-16 (current v.236)
  - /bin, /sbin/, /lib, /lib64 moved to /usr (mainly thanks to systemd)
  - control groups aka cgroups
  - have built-in Linux containers
- same package manager (yum)
- amazon-linux-extras & topics (carefully w/this!)
]

---
template: default

# Amazon Linux 2: 
### interesting facts

.left[
- there is now a CFQ I/O scheduler available for default EBS root device (still 
  NOOP is default).
- old runlevel vs current target 
] 

---
template: default

# Amazon Linux 2: 
### Kernel loaded modules comparison

---
template: default

# Amazon Linux 2: 
### sysctl changes 

.left[
```bash
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
```
]
"The solution is to not allow the creation of hardlinks to files that a given user would be unable to write to originally."

---
template: default

# Amazon Linux 2: 
### sysctl changes 

.left[
```bash
kernel.hotplug = /sbin/hotplug
```
]

"The kernel will execute a user-specified program during run time"

--

.left[
```bash
-bash: /sbin/hotplug: No such file or directory
```
]

# xD

---
template: default

# Amazon Linux 2: 
### sysctl changes 

.left[
```bash
kernel.panic = 30 => 0
```
]

(so now will reboot immediately)

---
template: default

# Amazon Linux 2: 
### sysctl changes 

.left[
```bash
net.ipv4.conf.all.promote_secondaries 0->1
```
]

failover when using more than one IP within same CIDR

---
template: default

# Amazon Linux 2: 
### sysctl changes 

.left[
```bash
net.ipv4.conf.all.rp_filter 0->1
```
]

Reverse Path Forwarding is used to prevent packets that arrived via one interface from leaving via a different interface

Been in RHEL6.

---
template: default

# Amazon Linux 2: 
### sysctl changes 

.left[
```bash
net.ipv4.conf.lo.accept_source_route 0->1
```
]

Less security, more performance on loopback device

---
template: default

# Amazon Linux 2: 
### sysctl changes 

.left[
```bash
user.max_cgroup_namespaces = 3903
user.max_ipc_namespaces = 3903
user.max_mnt_namespaces = 3903
user.max_net_namespaces = 3903
user.max_pid_namespaces = 3903
user.max_user_namespaces = 3903
user.max_uts_namespaces = 3903
```

```bash
user.max_cgroup_namespaces = 3868
user.max_ipc_namespaces = 3868
user.max_mnt_namespaces = 3868
user.max_net_namespaces = 3868
user.max_pid_namespaces = 3868
user.max_user_namespaces = 3868
user.max_uts_namespaces = 3868
```
]

--

#### dunno :)

---
template: default

# Amazon Linux 2: 
### sysctl changes 

nfs and xfs default entries - see urself


---
template: default

# systemd - what is that?

--

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
```bash`
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
# coredumps

--

With systemd we may browse and analyse any historical coredumps dumped by Kernel:

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
systemd-cgls /system.slice/docker.service
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
loginctl lock-session
loginctl terminate-session
loginctl kill-user

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
```]

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

systemctl kill

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
# journal & Python

--

demo

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
dnf --releasever=25 --installroot=/var/lib/machines/f25-systemd-demo
   install systemd passwd dnf fedora-release 
systemd-nspawn -D /var/lib/machines/f25-systemd-demo
passwd
cp /usr/lib/systemd/system/systemd-nspawn\@.service
   /etc/systemd/system/systemd-nspawn@f25-systemd-demo.service
systemctl daemon-reload
systemctl enable --now systemd-nspawn@f25-systemd-demo.service
machinectl
machinectl login f25-systemd-demo
```]

--

### machinectl

---
template: default

# nspawn: mkosi

A fancy wrapper around dnf --installroot, debootstrap, pacstrap and zypper that may generate disk images with a number of bells and whistles.

Fedora, Debian, Ubuntu, Arch Linux, openSUSE, Mageia, CentOS

[https://github.com/systemd/mkosi](https://github.com/systemd/mkosi)

---
template: default

# sd-notify

--

even more demos...

---
template: default

# sd-notify & JAVA

.left[
- proper method: read ENV variable NOTIFY_SOCKET, connect to this AF_UNIX socket, send notification
- but Java is not platform specific, so no Unix socket there
- JNI / JNA / JNR
- JNI implementation: [https://github.com/faljse/SDNotify](https://github.com/faljse/SDNotify)
- More reliable but no (ProcessBuilder): [https://gist.github.com/yrro/18dc22513f1001d0ec8d](https://gist.github.com/yrro/18dc22513f1001d0ec8d)
- Java Native Runtime (!): [https://github.com/jnr/jnr-unixsocket](https://github.com/jnr/jnr-unixsocket)
- Some ideas: [https://stackoverflow.com/questions/170600/unix-socket-implementation-for-java](https://stackoverflow.com/questions/170600/unix-socket-implementation-for-java)

]


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
[https://maciej.lasyk.info/slides/sysops-devops-systemd/](https://maciej.lasyk.info/slides/sysops-devops-systemd/)

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
