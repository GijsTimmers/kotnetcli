# A crash-course to extending `kotnetcli`

This document sketches the actions needed to implement a common `kotnetcli` extension integrated in the design, described in `sw_design.md`. It is intended to help developers avoid common pitfalls, keeping the code uniform and clean.


### Writing a new parser

This is probably the most probable extension to `kotnetcli`, as KotNet web pages are likely to change. Moreover, by writing a new parser `kotnetcli`'s framework can ultimately be used for parsing totally other things.

Writing a new parser, requires you to extend the `KotnetBrowser` class, overriding any methods of your interest. In order to use the new parser, you'll probably want to add a new `Worker` and/or command line option too, see below.

### Adding a new `Communicator`

Simply extend the `QuietCommunicator` class in the communicator hierarchy described above. Your new communicator then overrides the methods you want to visualize. Focus on visualizing only, the rest will be handled by the other classes. Take a look at the existing communicators in `Communicator.py`. They should give a good understanding of how this works.

In order to use the new communicator, you'll probably want to add a new command line option too, see below.

### Adding a new command line option

Adding new command line options is useful to enable new behavior.

When editing command line arguments, `kotnetcli.py` is the class you should look into first. Look into the classes below when the internal behavior for the new command line option cannot be accomplished with the existing `Worker` classes.

### Writing an input GUI

This extension is a bit more tricky. An input GUI (or any other *user input interface* for that matter) will require you to write a new `kotnetcli.py` file. Such a `kotnetgui.py` or so then handles user input to ultimately call the correct (`Worker`, `Communicator`) combination at some point.

Note that integrating the output in the GUI shouldn't be too hard neither, by writing a new `Communicator` (see above). Such a communicator then acts a kind of callback to the GUI, reporting progress.
