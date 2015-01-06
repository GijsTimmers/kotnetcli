#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  https://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit https://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.


## Error numbers begin at BASE to reduce the possibility of
## clashing with other exit statuses that random programs may
## already return.  The meaning of the codes is approximately
## as follows:
##
## USAGE -- The command was used incorrectly, e.g., with
##     the wrong number of arguments, a bad flag, a bad
##     syntax in a parameter, or whatever.
## DATAERR -- The input data was incorrect in some way.
##     This should only be used for user's data & not
##     system files.
## NOINPUT -- An input file (not a system file) did not
##     exist or was not readable.  This could also include
##     errors like "No message" to a mailer (if it cared
##     to catch it).
## NOUSER -- The user specified did not exist.  This might
##     be used for mail addresses or remote logins.
## NOHOST -- The host specified did not exist.  This is used
##     in mail addresses or network requests.
## UNAVAILABLE -- A service is unavailable.  This can occur
##     if a support program or file does not exist.  This
##     can also be used as a catchall message when something
##     you wanted to do doesn't work, but you don't know
##     why.
## SOFTWARE -- An internal software error has been detected.
##     This should be limited to non-operating system related
##     errors as possible.
## OSERR -- An operating system error has been detected.
##     This is intended to be used for such things as "cannot
##     fork", "cannot create pipe", or the like.  It includes
##     things like getuid returning a user that does not
##     exist in the passwd file.
## OSFILE -- Some system file (e.g., /etc/passwd, /etc/utmp,
##     etc.) does not exist, cannot be opened, or has some
##     sort of error (e.g., syntax error).
## CANTCREAT -- A (user specified) output file cannot be
##     created.
## IOERR -- An error occurred while doing I/O on some file.
## TEMPFAIL -- temporary failure, indicating something that
##     is not really an error.  In sendmail, this means
##     that a mailer (e.g.) could not create a connection,
##     and the request should be reattempted later.
## PROTOCOL -- the remote system returned something that
##     was "not possible" during a protocol exchange.
## NOPERM -- You did not have sufficient permission to
##     perform the operation.  This is not intended for
##     file system problems, which should use NOINPUT or
##     CANTCREAT, but rather for higher level permissions.


OK          =  0  ## successful termination

BASE        = 64  ## base value for error messages

USAGE       = 64  ## command line usage error
DATAERR     = 65  ## data format error
NOINPUT     = 66  ## cannot open input
NOUSER      = 67  ## addressee unknown
NOHOST      = 68  ## host name unknown
UNAVAILABLE = 69  ## service unavailable
SOFTWARE    = 70  ## internal software error
OSERR       = 71  ## system error (e.g., can't fork)
OSFILE      = 72  ## critical OS file missing
CANTCREAT   = 73  ## can't create (user) output file
IOERR       = 74  ## input/output error
TEMPFAIL    = 75  ## temp failure; user is invited to retry
PROTOCOL    = 76  ## remote error in protocol
NOPERM      = 77  ## permission denied
CONFIG      = 78  ## configuration error

MAX         = 78  ## maximum listed value
