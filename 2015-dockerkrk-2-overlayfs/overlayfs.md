name: default

class: center, middle

---
template: default

#OverlayFS

![Default-aligned image](docker_logo.png)

# KrkDocker Meetup #2

2015-04-29<br>
Maciej Lasyk

---
template: default

# OverlayFS - what is that?

---
template: default

##simply: overlaying one filesystem (or dir) over another

---
template: default

## used mainly for LiveCDs, OpenWRT, R-PI2 / OpenELEC and lately CoreOS

---
template: default

## and us w/LXC ;)

---
template: default

# CoreOS PR #372
## disk_layout: switch to ext4 as the default root filesystem. #372 

--

![Default-aligned image](coreos.gif)

https://github.com/coreos/scripts/pull/372
---
template: default

# OverlayFS: "upper" and "lower"
--

### -> content collision (hiding, merging)

--

### -> lower may be almost any FS, dir, another overlayFS

---
template: default

## In future (maybe 3.19)..

http://lkml.iu.edu/hypermail/linux/kernel/1412.1/00943.html

## This adds support for multiple read-only layers to overlayfs. It also makes the writable upper layer optional.

---
template: default

# This is the only unions FS in mainstream right now (since 3.18)

---
template: default

# Miklos Szeredi (lead developer) tried to put this into mainstream since... 3.10? (and Linus liked it)

---
template: default

# So what about Docker & OvelayFS?

--

# (note: It's not only about Docker)

---
template: default

## Docker FS requirements?

--

### -> The Need for speed

--

### -> copy-on-write

---
template: default

### -> AUFS was not in the mainstream

--

### -> RHEL went w/devmapper w/loopback mount

--

### -> both performance sucked

--

### -> and btrfs is still unstable	

---
template: default
```bash
 // Slice of drivers that should be used in an order
 priority = []string{
 "aufs",
 "btrfs",
 "devicemapper",
 "vfs",
 "overlayfs",
```
---
template: default

# it's about performance

--

## -> page cache sharing

--

## see yourself

http://developerblog.redhat.com/2014/09/30/overview-storage-scalability-docker/

---
template: default
background-image: url(img1.png)
---
template: default
background-image: url(img2.png)
---
template: default
background-image: url(img3.png)
---
template: default

![Default-aligned image](docker_logo.png)

# Thanks :)

### Maciej Lasyk

@docent-net<br>
http://maciej.lasyk.info
