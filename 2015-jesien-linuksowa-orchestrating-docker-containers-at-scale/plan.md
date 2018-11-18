
- Intro (Fedora, Infrastruktura, Dockerfiles)
- Agenda
- Quick survey
- Problemy
    - Ryzyko procesu CI: "It works on my machine"
    - Deploy and build time
    - Infrastructure size - automation!
    - Dependency hell
    - Configuration spaghetti
    - Cost control (Elastic (on-demand) scaling of smaller
    services leads to better cost control)
- Wstęp - krótka historia skalowania platform
    - skrypty, ansible, puppety (scp, conf.d etc)
    - problem warstwy (Bare, IaaS, PaaS)
    - klasyczny proces CI
    - Kiedy Docker ma sens?
- Docker
    - co to jest
        - open-source 
        - automates the deployment of any
        application as a lightweight, portable,
        self-sufficient container that will run
        virtually anywhere
        - VMs and containers
            - obrazek vms_vs_containers http://www.linuxjournal.com/
        - Java’s promise: Write Once. Run Anywhere.
    - jak działa?
        - lxc / libcontainer Go 0.9) - obrazek docker execa
            http://www.infoq.com/news/2014/03/docker_0_9
            Execution drivers via pluggable API
        - control groups & kernel namespaces
            - ogólnie cgroups + namespaces + image = docker container
        - layered filesystem, copy-on-write
            - btrfs
            - device mapper thin provisioning + loopback mounts
            - disk capacity and memory savings
        - Concepts
            - images
                - read only
                - act as templates
            - Dockerfile
                - like a makefile
                - extends the base image
                - results in a new image
                - dockerfile + base image = docker container
            - Containers - instances running apps
        - docker registry https://github.com/docker/docker-registry
            - git repo semantics
            - pull, push, commit
            - hierarchy
        - hierarchy of images: base image -> child image -> grandchild imag
            Git’s promise: Tiny footprint with lightning fast performance.
        - container lifecycle
            - conception / BUILD
            - initialization: RUN (create + start)
            - process: COMMIT (persistance), RUN
            - sleep & wake (KILL, START)
            - remove (RM) and obliterate (RMI)
        - is it secure? selinux / apparmor
    - use cases
        - complete CI stack - obrazek docekr_workflow z
          http://sattia.blogspot.com/2014/05/docker-lightweight-linux-containers-for.html
            - local dev
            - deployment
                http://blog.scoutapp.com/articles/2013/08/28/docker-git-for-deployment
            - testing
                - unit testing of any commit on dedicated env
                - don't worry about cleaning up after testing
                - parrarelized tests across any machines
        - version control system for apps
        - whn you want to have same env everywhere
        - Microservices
            - Services can be deployed independently and
            faster
            - Changing a monolith could have more impact
            and risk so deployments are slower

    - historia
        - dotCloud pracował nad PAASem
        - oryginalnie python, teraz go
        - historia
            - początek 2013 internal project dotcloud
            - 2013 marzec: public
            - 2013 august: 0.6
            - 2014 February: stable 1.0
        - 2 obrazki z google trends

- Orchestration at scale problem
    - one host (cli, fig)
    - to isolate or not?
    - many hosts (slajdy being)
        - Configuration management system
        - Maestro-ng: https://github.com/signalfuse/maestro-ng
    - really many hosts (hundreds): Helios
    - zounddss: Kubernetes
    - want more? docekr ecosystem obraz (docekr_ecosystem)
      http://www.cloudssky.com/en/blog/Docker-Is-Not-Enough/
- To PAAS or not to PAAS?
    - beijing slajdy
    - which one?
        - dokku
            - Open source PaaS
            - Less than 100 lines of Bash
            - Git push deployment
            - https://github.com/progrium/dokku
        - flynn.io
            - Open source PaaS (Go)
            - Uses Docker to manage containers
            - https://flynn.io
        - deis.io
            - Open source PaaS (Python)
            - Git push deployments
            - https://deis.io
- docker cli
    - budowanie bezpośrednio z kontenera + commit (django slajdy, koniec)
    - quick code demo na fedorze (może być z slajdów moich)
    - delikatny opis możliwości z dokumentacji
    - Dockerfile
        https://docs.docker.com/userguide/level1/ - game ;)
- fig
    - one host (beijing slajdy)
- ansible docker
    - ansible docker module
    - ansible build in Dockerfile
- coreos / fleet
- kubernetes
    - overview
    - 
- smartstack
- Armada?
- podsumowanie
