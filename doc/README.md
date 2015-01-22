This directory contains information on `kotnetcli`'s' internals. It's intended for developers.

#### Contents

- `sw_design.md` documents the overall software design in a textual format, combined with UML diagrams.
- `extending.md` sketches how to incorporate several possible extensions in `kotnetcli`'s software design.
- `kotnetcli_modelio_project` is a directory containing the [modelio](https://www.modelio.org/) project that generated the UML diagrams.
- `diagrams` is a directory containing the generated UML diagrams in png format.

#### Design process

`kotnetcli` has been designed with readability, extensibility, portability and elagancy in mind. It follows the object oriented approach with a cohesive set of classes, each one focusing on its own explicit job: the UNIX philosophy - *do one thing and do it good*. 

`kotnetcli`'s software design process follows a bottom-up open source spirit. Developers are encouraged to participate in the design process, to propose enhancements, discuss caveats, enhance the documentation, etc.

All diagrams presented here are created with the cross-platform tool [`modelio 3.2.1`](https://www.modelio.org/), which is free software. The project is included in the `kotnetcli_modelio_project` directory.
