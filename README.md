# Venom2

## Introduction
V3n0M is a free and open source scanner, that automates the process of finding possibly SQL injection vulnerable URLs. It harnesses the power of async, and proxy support to scour the interwebs.

##Installation
Preferably, you can download sqlmap by cloning the Git repository:

    git clone https://github.com/The-da-vinci/Venom2.git
    cd venom2
    python3 -m pip install -r requirements.txt
    python3 venom2.py

Venom2 works out of the box with [Python](http://www.python.org/download/) version **3.6.x** and **3.7.x** on any platform.

##Usage
----

To get a list of basic options and switches use:

    python3 venom2.py -h

    usage: venom2.py [-h] [-p [PROXY]] [-t TARGET] [-d DORKS] [-P PAGES]

    optional arguments:
    -h, --help            show this help message and exit
    -p [PROXY], --proxy [PROXY]
                        Enable proxy, default is TOR proxy
                        socks5://127.0.0.1:9050
    -t TARGET, --target TARGET
                        Targeted Top Level Domain
    -d DORKS, --dorks DORKS
                        amount of dorks
    -P PAGES, --pages PAGES
                        Number of pages to go through
