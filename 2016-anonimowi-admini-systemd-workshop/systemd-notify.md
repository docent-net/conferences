## LAB 5: systemd-notify ##

How systemd knows about application state? We have a **sd_notify** syscall
that we might use. There're 2 libraries that implements via cython this syscall:

- [sd_notify](https://github.com/bb4242/sdnotify)
- [systemd.notify](https://pypi.python.org/pypi/systemd/)

So now let's have some fun with it. Enter [sd-notify-python](sd-notify-python)
directory and follow those steps:

1. **sd-notify**:
    1. view **sd-notify-app-service.service** file
    1. copy service file to **/etc/systemd/system/** and enable/run it
    1. view **journalctl -f -u sd-notify-app-service**
1. **systemd-notify** + **socket activation**
    1. view **systemd-notify-app.service** and **systemd-notify-app.socket**
    1. copy service and socket file to **/etc/systemd/system/**
    1. start **systemd-notify-app.socket** service
    1. **curl localhost:1025** && **journalctl -f**
    
Remember about reading socket activation posts:

- [http://0pointer.de/blog/projects/socket-activation.html](http://0pointer.de/blog/projects/socket-activation.html)
- [http://0pointer.de/blog/projects/socket-activation2.html](http://0pointer.de/blog/projects/socket-activation2.html)
- [http://0pointer.de/blog/projects/socket-activated-containers.html](http://0pointer.de/blog/projects/socket-activated-containers.html)