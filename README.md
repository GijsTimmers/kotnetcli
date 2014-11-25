# kotnetcli

*KotNet Command Line Interface* -- An easy automated way to log in to [KotNet](https://admin.kuleuven.be/icts/english/kotnet).

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
| [Python 2](https://www.python.org) | The `kotnetcli` application is entirely written in python.  Since python is an interpreted language, running the `kotnetcli.py` script implies having a python interpreter installed. Running the compiled [binary](https://github.com/GijsTimmers/kotnetcli/releases/latest) however doesn't require having python installed. The newer `python3` isn't backwards compatible with `python2`. | Python2 is pre-installed on many UNIX systems. If not most of them provide `python2` in the standard package manager.|
| [curses lib](https://docs.python.org/2/library/curses.html) | `kotnetcli` uses the `curses` library to display dynamic colorized progress-output  | Most UNIX versions are shipped with a version of the `ncurses` library. If not, most of them provide `ncurses` in the standard package manager. |
| [mechanize lib](https://pypi.python.org/pypi/mechanize/) | A library emulating a browser in python. This is used by `kotnetcli` to access the netlogin.kuleuven.be page | The following section lists platform specific info to resolve this dependency.|
| [keyring lib](https://pypi.python.org/pypi/keyring) | `kotnetcli` uses the keyring library to securely save your kotnet credentials to your operating system specific keyring back-end. | The following section lists platform specific info to resolve this dependency.|

## Platform dependent instructions
This section lists the platform specific instructions to resolve the above dependencies:

  - Ubuntu:
  
            $ sudo apt-get install python-mechanize python-keyring
        
  - Arch:
  
            $ sudo pacman -S python2-mechanize python2-keyring
        
  - Pip:
  
            $ sudo pip install mechanize keyring
