# kotnetcli

An easy automated way to log in on Kotnet.

## Installation

You can either install the dependencies and run the python file, or just download [the binary](https://github.com/GijsTimmers/kotnetcli/releases/latest). The general steps to get the latest `kotnetcli.py` are listed below. Currently, we only support 64-bit Linux. If you decide to download the
binary, skip steps 1 and 2.

1. Resolve the dependencies: see the next section for an overview and platform-specific instructions
        
2. Clone this repository and change the directory:

        $ git clone https://github.com/GijsTimmers/kotnetcli.git
        $ cd kotnetcli
        
3. Mark kotnetcli.py as executable:

        $ chmod +x kotnetcli.py
        
4. Run kotnetcli.py:

        $ ./kotnetcli.py

When run for the first time, kotnetcli will ask you for your username
and password. Both will be stored safely in the keyring of your desktop
environment.

You can add kotnetcli to your autostart programs to log in to Kotnet
at boot-time.

## Dependencies overview

| Dependency | Rationale | Where to get it|
|------------|-----------|--------------|
| [Python 2](jo) | jo | jo |
| [curses lib](https://docs.python.org/2/library/curses.html) | jo | jo |

## Platform dependent instructions
This section lists the platform specific instructions to resolve the above dependencies:

  - Ubuntu:
  
            $ sudo apt-get install python-mechanize python-keyring
        
  - Arch:
  
            $ sudo pacman -S python2-mechanize python2-keyring
        
  - Pip:
  
            $ sudo pip install mechanize keyring
