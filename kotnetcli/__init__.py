## Numeric version for clean packaging
__src_url__ = "https://github.com/GijsTimmers/kotnetcli"
__version__ = "1.3.0"

## Human-readable version. Development versions should be suffixed with -dev;
## release versions should be followed with "Name" as well. Some examples:
## __version__ = '1.2.1 "American Craftsman"'   (A release)
## __version__ = '1.2.1-dev'                    (A development version)
__version_str__ = "{0}-dev".format(__version__)

__descr__ = "An easy automated way to log in to KotNet"

## Resolve relative to the package root (http://stackoverflow.com/a/5423147).
import os
__root__ = os.path.abspath(os.path.dirname(__file__))

def resolve_path(rel_path):
    return os.path.join(__root__, rel_path)
