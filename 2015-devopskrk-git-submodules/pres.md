name: default

class: center, middle
---
template: default

![Default-aligned image](git.png)

# Git submodules

# Devops Meetup Krk

2015-06-17<br>
Maciej Lasyk

---
template: default

# GIT submodules - WTF?

---
template: default

## PL: moduły zależne

---
template: default

```bash
 git submodule add <URL> <dirname>

 git status

 git diff --cached --submodule
```
---
template: default

.gitmodules
```bash
[submodule "ansible-piwik"]
        path = ansible-piwik
        url = git@github.com:docent-net/ansible-piwik.git
```
---
template: default

## Cloning repos w/submodules?

```bash
git clone <URL> # just standard content without submodules data
```
---
template: default

## Cloning repos w/submodules?

```bash
git submodule init
git sumobule update
```
---
template: default

## Cloning repos w/submodules?

```bash
git clone --recursive <URL>
```
---
template: default

## Update submodule code to the latest revision?

```bash
# run in submodule dir
git fetch
git merge <origin/master>
```

```bash
# updates all submodules data
# run from maindir
git submodule update --remote
```
---
template: default

## Change submodule branch?

- .gitmodules
- ~/.git/config
---
template: default

### by default: detach HEAD state

```bash
git checkout <branch>
git submodule update --remote merge
```
---
template: default

### Pushing changes?

```bash
git push --recurse-submodules
```
---
template: default

### Removing submodule?

```bash
# edit .gitmodules
git rm --cached <submodule-dir>
# commit change
```
---
template: default

### foreach

```bash
git submodule foreach 'git diff'
git submodule foreach 'git pull'
```
---
template: default

![Default-aligned image](git.png)

# Thanks :)

### Maciej Lasyk

@docent-net<br>
http://maciej.lasyk.info
