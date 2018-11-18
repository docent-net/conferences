1. About systemd (init & service manager)
1. systemd-bin (30min)
    1. RTM (wdech, wydech, czytać, zapomnieć o tym co było)
    3. systemctl
    4. analyzing boot process
    5. coredumps
    6. cgroups
    7. FHS!
    8. detecting virtualization
    9. DNS
    10. finger
    11. time management
    12. inhibit :)
    13. bus / d-bus / demo
    14. process confinement
2. services & unit files (15min)
    1. declarativeness
        1. httpd sysv example
        2. unit file example
    2. types of units
    2. runlevels & targets
    3. Dependencies
        1. Requires, Requisite, Wants, BindsTo, PartOf, Conflicts, Before,
           After, OnFailure, PropagatesReloadTo, ReloadPropagatedFrom,
           StopWhenUnneeded, DefaultDependencies, WantedBy, RequiredBy, Also
    4. Starting after installation
    5. Cronjobs / Timers
    6. Socket activation
    7. cgroups control
        1. CPUShares, CPUAccounting, MemoryAccounting, MemoryLimit,
           BlockIOAccounting, BlockIOWeight, BlockIOReadBandwidth,
           BlockIOWriteBandwidth
    8. Defining kill method
    9. Debugabbility
    10. GUI? http://127.0.0.1:9090
    11. sysv import?
        1. Systemd maintains 99% backwards compatibility with LSB 
           compatible initscripts and the exceptions are well documented
        2. No need to convert
        3. http://www.freedesktop.org/wiki/Software/systemd/Incompatibilities/
        4. http://0pointer.de/blog/projects/systemd-for-admins-3.html
3. journal (25min)
    
4. nspawn containers (5min)
    1. very simple containers
    2. no daemon behind
    3. no need to do anything with storage or network
    4. just dnf / yum install and go!
    5. like this (demo?):
        1. dnf --releasever=25 --installroot=/var/lib/machines/f25
           install systemd passwd dnf fedora-release 
        2. systemd-nspawn -D /var/lib/container/f25
        3. passwd
        4. cp /usr/lib/systemd/system/systemd-npawn\@.service
           /etc/systemd/system/systemd-nspawn@f25.service
        5. systemctl enable --now systemd-nspawn@f25.service
    6. machinectl
5. sd-notify (15min)
