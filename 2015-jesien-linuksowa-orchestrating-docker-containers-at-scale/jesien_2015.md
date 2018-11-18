name: title
class: middle, center
background-image: url(img/ship.jpg)

# Orchestrating Docker containers at scale #

Maciej Lasyk

maciej@lasyk.info

---
name: current_state
class: left, top

# Current state of delivery pipeline #
--

1. Static ENVs architecture (XAT, PROD, DEV)
--

1. No automation on rolling up new ENVs (bare / VM layer)
--

1. Zero DevOPS culture on Dev - Ops line
--

1. No reliable secure connection with ENVs (faulty VPN)
--

1. Monitoring (app, functional) is not a part of app; DEVs not contributing
--

1. Very complicated and fuzzy infrastructure (network, hardware, OS)
--

1. No roadmap defined (or not published) for infrastructure
--

1. Deploys, monitoring, infrastructure, processes defined in cost - uneffective way
--

1. App scalability issues: sticky sessions, global schema, shared cache
--

# Consequences #
--

- Heavy and risky app deployment model
--

- Very expensive delivery pipeline
--

- Impossible EAP
--

- Almost impossible to achieve isolation on customer / slice level

???

- Why so many mentioned issues (infra related?)
- Devops as glue

---
name: objectives
class: left, top

# Objectives #
--

1. General DevOPS/CI objectives
--

    - Reduce risks
--
    - Reduce repetitive processes
--
    - Generate deployable software
--
    - Establish product confidence
--
    - Build software at every change
--
    - Continous database integration
--
    - Continous testing, inspection, feedback
--

1. An iterative delivery in configurable model
--

    - CI->(DEV->TEST->PrePROD->PROD)
--
    - CI->(EXT / Pre-SALES)
--

1. Cost effectiveness
--

    1. Fully automated delivery pipeline
--
    1. Ephemeral environments (hosting anywhere)

---
name: accomplishment
class: left, top

# Accomplishment / Roadmap proposal  #
--

1. We can't afford revolution; let's go evolution way
--

1. Let's start with something small
--

    - Current CI needs couple of improvements
--
1. Then we can move to major improvements
--

    1. Achieving homogeneous environments - by providing automation
--
        - Unified envs (any number of envs!)
--
        - Can be done with Linux Containers (LXC and Docker) + Vagrant
--
        - Ensures DevOPS culture as needs collaboration of Dev/OPS/QC
--
    1. Work together with developers / platform providing resolution for major
       architectural challenges
        - sticky sessions
        - global schema
        - shared cache
--
    1. Work together with Service Delivery providing new ideas and solutions
       for IaaS
        - New DCs (think hybrid clouds)
--
        - Possible hypervizor replacement
--
        - Possibility to work on PaaS

---
name: sources
class: left, top

# Details?

1. Read http://goo.gl/wHRJyg for details
1. IAAS considerations: https://gist.github.com/docent-net/f87cea10a7e37c16f207

---
name: finish
class: center, middle

# DevOPS @Lumesse #

Maciej Lasyk

maciej.lasyk@lumesse.com
