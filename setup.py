from distutils.core import setup
setup(
  name = "kotnetcli",
  packages = ["kotnetcli"], # this must be the same as the name above
  version = "1.3.0",
  description = "An easy automated way to log in on Kotnet",
  author = "Gijs Timmers and Jo Van Bulck",
  author_email = "gijs.timmers@student.kuleuven.be",
  url = "https://github.com/GijsTimmers/kotnetcli", # use the URL to the github repo
  download_url = "https://github.com/GijsTimmers/kotnetcli/releases/tag/1.3.0", # I'll explain this in a second
  keywords = ["kotnet", "login", "kotnetlogin", "leuven", "kuleuven"], # arbitrary keywords
  install_requires=[
          "mechanize",
          "keyring",
          "notify2",
          "colorama",
          "python2-pythondialog",
          "beautifulsoup4"
                    ],
  classifiers = [],
)
