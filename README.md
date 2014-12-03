# kotnetcli

*KotNet Command Line Interface* -- An easy automated way to log in to
[KotNet](https://admin.kuleuven.be/icts/english/kotnet).

## Purpose

Logging in on KotNet is a hassle. A method to autologin from within the
browser
[exists](https://code.google.com/p/kotnetloginextension/),
but although this way of logging in is very user-friendly, it also has
some downsides:

- The login speed is suboptimal as the webbrowser has to draw the 
website elements on the screen;
- You can't use a custom start page because KotNet will always redirect
you to netlogin.kuleuven.be when trying to open your custom start page;
- You have to first open a web browser before being able to do internet-
related stuff.

`kotnetcli` tries to overcome this. Its downsides, compared to the 
browser extension, are:

- No support for KU Leuven authentication portals. For example, if you
want to log in on Toledo, you'll still have to enter your credentials
there.
- There is no GUI method for changing your username/password
combination.

Of course, you can use both `kotnetloginextension` and `kotnetcli`. For
example, you can set `kotnetcli` to autologin at boot-time, so 
netlogin.kuleuven.be won't bother you when opening your web browser. 
When you go to Toledo, `kotnetloginextension` will do the login work.

Although ease-of-use is important, `kotnetcli` will probably stay
"poweruser-ish" for a while.

## Features

- Safety: we'll store your login settings safely in your operating
system's keyring;
- Speed: there is no need to draw the website elements, which makes the
login procedure faster;
- Scriptable: kotnetcli is a command-line program and can thus be used
in scripts to cater your needs. For example, you can put it in your
autostart settings to log in after booting your computer, waking from
sleep, etc. A `--quiet` mode and exit codes are planned for future
releases to make this even better.

## Installation

You can either install the dependencies and run the python file, or just
download
[the binary](https://github.com/GijsTimmers/kotnetcli/releases/latest).
The general steps to get the latest `kotnetcli.py` are listed below.
Currently, we only support Linux and Windows (x86).
If you decide to download the binary, skip steps 1 and 2.

1. Resolve the dependencies: see the next section for an overview and
platform-specific instructions
        
2. Clone this repository and change the directory:

        $ git clone https://github.com/GijsTimmers/kotnetcli.git
        $ cd kotnetcli
        
3. Mark kotnetcli.py as executable:

        $ chmod +x kotnetcli.py
        
4. Run kotnetcli.py:

        $ ./kotnetcli.py

When run for the first time, kotnetcli will ask you to unlock your keyring. For
maximum ease-of-use, just enter the password you use to login to your system. If
you do that, this keyring will only pop up once.
After that, you'll have to enter your KotNet s-number or r-number and password.
Both will be stored safely in the keyring of your desktop environment.

You can add kotnetcli to your autostart programs to log in to Kotnet
at boot-time.

## Dependencies overview

| Dependency | Rationale | Where to get it|
|------------|-----------|--------------|
| [Python 2](https://www.python.org) | The `kotnetcli` application is entirely 
written in python.  Since python is an interpreted language, running the 
`kotnetcli.py` script implies having a python interpreter installed. 
Running the compiled 
[binary](https://github.com/GijsTimmers/kotnetcli/releases/latest) however 
doesn't require having python installed. The newer `python3` isn't backwards 
compatible with `python2`. | Python2 is pre-installed on many UNIX systems.
If not most of them provide `python2` in the standard package manager.|
| [curses lib](https://docs.python.org/2/library/curses.html) | 
`kotnetcli` uses the `curses` library to display dynamic colorized 
progress-output  | Most UNIX versions are shipped with a version of the 
`ncurses` library. If not, most of them provide `ncurses` in the standard 
package manager. |
| [mechanize lib](https://pypi.python.org/pypi/mechanize/) | 
A library emulating a browser in python. This is used by `kotnetcli` to access
 the netlogin.kuleuven.be page | The following section lists platform specific 
 info to resolve this dependency.|
| [keyring lib](https://pypi.python.org/pypi/keyring) | `kotnetcli` uses the 
keyring library to securely save your kotnet credentials to your operating 
system specific keyring back-end. | The following section lists platform 
specific info to resolve this dependency.|

## Platform dependent instructions
This section lists the platform specific instructions to resolve the above dependencies:

  - Ubuntu:
  
            $ sudo apt-get install python-mechanize python-keyring
        
  - Arch:
  
            $ sudo pacman -S python2-mechanize python2-keyring
        
  - Pip:
  
            $ sudo pip install mechanize keyring
