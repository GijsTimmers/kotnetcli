kotnetcli
=========

An easy automated way to log in on Kotnet.

Installation
-----

You can either install the dependencies and run the python file,
[or just download the binary]
(https://github.com/GijsTimmers/kotnetcli/releases/download/1.0.0/kotnetcli).
Currently, we only support 64-bit Linux. If you decide to download the
binary, skip steps 1 and 2.

1. Install the dependencies:
  - Ubuntu:
  
            sudo apt-get install python-mechanize python-keyring
        
  - Arch:
  
            sudo pacman -S python2-mechanize python2-keyring
        
  - Pip:
  
            sudo pip install mechanize keyring
        
2. Clone this repository:

        git clone https://github.com/GijsTimmers/kotnetcli.git
        
3. Mark kotnetcli.py as executable:

        chmod +x kotnetcli*
        
4. Run kotnetcli.py:

        ./kotnetcli*      

When run for the first time, kotnetcli will ask you for your username
and password. Both will be stored safely in the keyring of your desktop
environment.

You can add kotnetcli to your autostart programs to log in to Kotnet
at boot-time.
