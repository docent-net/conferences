## LAB 1: systemd-bin ##

### The beginning ###

During this part of workshops we'll learn some basics. Let's start with
documentation. It's the true pillar of systemd:

- Enter the main page: `man systemd.index`
- See what's more: `man systemd[TAB]`
- Take a quick look at: `man systemd.unit`

### Runlevels and targets ###

Before systemd we had runlevels (remember? chkconfig && 2,3,5?). Now we have
units of type **target**. Think of targets as **unit aggregators / groups**

- A bit of documentation: `man systemd.target`
- Display possible targets: `systemctl list-units --type=target`
- Which is default (current runlevel)? `systemctl get-default`
- Wanna change default target (runlevel)? `systemctl isolate [target]` / AllowIsolate=
- `# systemctl isolate multi-user.target (or) systemctl isolate runlevel3.target`
- `# systemctl isolate graphical.target (or) systemctl isolate runlevel5.target`

### systemctl aka system control ###

For dealing with unit files, services, targets etc we use **systemctl**:

- `man systemctl`
- What's happening on my system? `systemctl status`
- Show me loaded services: `systemctl -t service`
- Show me all unit files: `systemctl list-unit-files`
- Set vendors default (enable / disable): `systemctl preset docker`
- What's my system's current state? `systemctl is-system-running`
- Whic units are in failed state? `systemctl --failed`
- Plz show me dependencies of httpd: `systemctl list-dependencies httpd`
- `systemctl enable --now httpd`
- `sytemctl disable --now mariadb`
- `systemctl show httpd`

### analyzing boot process ###

With systemd analyzing boot process looks quite interesting:

- `systemd-analyze time`
- `systemd-analyze blame` (watch out for dependencies - info time may lie)
- `systemd-analyze plot` prints an SVG graphic detailing which system services have been started at what time, highlighting the time they spent on initialization.
- `systemd-analyze dump`
- `systemd-analyze verify system.slice`
- `systemd-analyze dot 'docker.*' | dot -Tsvg > docker.svg`
- `systemd-analyze dot --to-pattern='*.target' --from-pattern='*.target' | dot -Tsvg > targets.svg`

### Managing coredumps ###

With systemd we may generate and browse and view any historical coredumps:

- `coredumpctl dump`
- `coredumpctl dump docker`
- `coredumpctl dump _PID=666` (journalctl's general predicates; man systemd.directives)
- `coredumpctl dump /usr/sbin/httpd`
- `coredumpctl gdb _PID=666`

### cgroups top ###

Like atop/htop but for cgroups :)

- `systemd-cgtop`
- `systemd-cgtop -d 5 -n 3`
- `systemd-cgls /system.slice/auditd.service`

### What about killing processes? ###

Actually units may have policy about how to be killed in a proper way.

- `systemctl kill docker.service`
- `man systemd.kill` (see KillMode=)

### FHS ftw! ###

systemd actually takes care about FHS. You may easily see what's purpose of
specific directories:

- `systemd-path`
- don't confuse with systemd.path (path activation)
- `man file-hierarchy`
- `systemd-path temporary`
- `systemd-path system-state-logs`

### Am I a robot? ###

Systemd will tell you if you're on bare, VM, container of chroot:

- `systemd-detect-virt`
- `man systemd-detect-virt`

### DNS ###

systemd provides resolver service (systemd-resolved). You may query it against
DNS entries:

- `systemd-resolve www.google.com`
- `systemd-resolve -t mx google.com`

### finger ###

finger / w in the oldtimes, and now:

- `loginctl list-users`
- `loginctl list-sessions`
- `loginctl user-status`
- `loginctl session-status`
- `man loginctl`

### Time management ###

- `timedatectl`
- `timedatectl list-timezones`
- `timedatectl set-time 2016-11-30 11:12:13`
- `systemctl status systemd-timesyncd.service`
- `timedatectl set-ntp true`

### Don't sleep! ###

systemd provides a way to make sure that your hardware doesn't sleep / 
hibernate / poweroff during execution of given command:

- `systemd-inhibit something`
- `man systemd-inhibit`

### Setting hostname ###

Actually a basic functionality; it's part of systemd-firstboot:

-` hostnamectl set-hostname aa.workshops`

### Getting network details ###

- `networkctl status eno1`

### IPC communication / D-Bus ###

So systemd uses D-Bus for IPC (inter - process communication).

- see current state of procs registered in bus: `busctl`
- more info: https://freedesktop.org/wiki/Software/dbus/
- check [dbus](dbus/) directory for a quick task:
    - `python server.py`
    - `python client.py`
    - jak on tam się dostał?
    - Could you extend this a bit? Create another endpoint providing current
      time and add a client method asking about this time?
- `sudo busctl capture > test.pcap` + wireshark
- `busctl tree`

### Confining processes ###

You may run any process inder systemd / cgroups confinement:

- `systemd-run env`
- `systemd-run -p BlockIOWeight=10 updatedb`
- Timers:
    - `date; systemd-run --on-active=30 --timer-property=AccuracySec=100ms /bin/touch /tmp/foo`
    - `journalctl -b -u run-71.timer`
- `systemd-run --scope -p BlockIOWeight=10 --user tmux`
    - `tmux ls`
	
### Do it @home ###

see yourself:
- systemd-firstboot
- systemd-ask-password
- systemd-sysusers
- systemd-tmpfiles
- bootctl
- systemd-escape  
- systemd-machine-id-setup
- systemd-network
- systemd-notify	