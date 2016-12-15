![banner](https://raw.githubusercontent.com/GijsTimmers/kotnetcli/dev/kotnetcli/data/banner.jpg)

[![Build Status](https://travis-ci.org/GijsTimmers/kotnetcli.svg?branch=master)](https://travis-ci.org/GijsTimmers/kotnetcli) [![Code Health](https://landscape.io/github/GijsTimmers/kotnetcli/dev/landscape.svg?style=flat)](https://landscape.io/github/GijsTimmers/kotnetcli/dev) [![license](http://img.shields.io/:license-gpl3-orange.svg)](https://gnu.org/licenses/gpl.html)

## Purpose

Logging in on [KotNet](https://admin.kuleuven.be/icts/english/kotnet) is a hassle. A method to autologin from within the
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

You can find more information about the kotnecli features [in the wiki!](https://github.com/GijsTimmers/kotnetcli/wiki/Features)
## Installation

You can either download pre-built
[binaries](https://github.com/GijsTimmers/kotnetcli/releases/latest) for the
latest stable release, or install from source. After cloning the git repository,
you can run kotnetcli locally through the `xxx-runner.py` entry points, or
install system-wide as follows:

1. Clone this repository and change the directory:

        $ git clone https://github.com/GijsTimmers/kotnetcli.git
        $ cd kotnetcli
                
2. Install system-wide:

        $ sudo python2 setup.py install

   The above command automatically resolves the base dependencies. We refer to
   the [wiki](https://github.com/GijsTimmers/kotnetcli/wiki/Dependencies-overview)
   for optional communicator-specific dependencies, or in case you want to
   install manually.

The kotnetcli package consists of a number of shell commands, which are
explained below:

1. *kotnetcli*: the core command, logs you in to KotNet.
2. *kotnetgui*: a GUI front-end for the kotnetcli application.
3. *kotnetsrv*: an elementary webserver, intended for developers on localhost.

When run for the first time, kotnetcli will ask you to unlock your keyring. For
maximum ease-of-use, just enter the password you use to login to your system. If
you do that, this keyring will only pop up once.
After that, you'll have to enter your KotNet s-number or r-number and password.
Both will be stored safely in the keyring of your desktop environment.

You can add kotnetcli to your autostart programs to log in to Kotnet
at boot-time.

## Platform dependent instructions
This section lists the platform specific instructions to resolve the above dependencies:


[Additional instructions for Gnome users that want to use the Gnome keyring back-end with the latest version of `python-keyring`:]

      $  sudo pip2 install keyrings.alt

Create a `keyringrc.cfg` file with the following content:
```
[backend]
default-keyring=keyrings.alt.Gnome.Keyring
```

To determine where the config file is stored, run the following:

     $ python2 -c "import keyring.util.platform_; print(keyring.util.platform_.config_root())"


  - Ubuntu:
  
        $ sudo apt-get install python-pip
        $ sudo pip install requests keyring notify2 \
          colorama python2-pythondialog beautifulsoup4 \
          argcomplete cursor

        
  - Arch:

        $ sudo pacman -S python2-pip
        $ sudo pip install requests keyring notify2 \
          colorama python2-pythondialog beautifulsoup4 \
          argcomplete cursor

        
  - Mac OS X (using [Homebrew](http://brew.sh/)):

        $ brew install ncurses dialog \
          homebrew/python/python-dbus
        $ sudo pip install requests keyring notify2 \
          colorama python2-pythondialog beautifulsoup4 \
          argcomplete cursor


  - Pip:

        $ sudo pip install requests keyring notify2 \
          colorama python2-pythondialog beautifulsoup4 \
          argcomplete cursor

[Why do we need these dependencies?](https://github.com/GijsTimmers/kotnetcli/wiki/Dependencies-overview)

## Contributing
We're currently looking for 
[translators](https://github.com/GijsTimmers/kotnetcli/issues/46)
and graphic designers (to create an elegant iconset). If you feel like you can
do this, feel free to fork the project and show us your work!

Regular developers: please take a look at the 
[coding guidelines](https://github.com/GijsTimmers/kotnetcli/blob/master/CONTRIBUTING.md).

<sub><sup>Tags: kotnetcli, kotnet, login, autologin, automatisch, automatic.</sup></sub>
