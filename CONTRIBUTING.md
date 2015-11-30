# kotnetcli

This is the contribute.md of our project. Great to have you here. Here are a
few ways you can help make this project better!

## Team members
- [Gijs Timmers](https://github.com/GijsTimmers)
- [Jo Van Bulck](https://github.com/jovanbulck)

## Wanted
### Testers
It doesn't matter which platform you're using. Linux, Mac OS, Windows, ...
we would love to hear your mileage on running `kotnetcli`. Bugs are welcome
[here](https://github.com/GijsTimmers/kotnetcli/issues)

### Translators
Are you able and willing to tranlate for us? Please use `.po` files. You can
edit them using programs like [`virtaal`](http://virtaal.translatehouse.org/)
and [`poedit`](https://poedit.net/). Just create a new branch, edit the
default.po file, save as <yourlanguageabbreviation>.po and request a merge.

For example:

```
$ git clone https://github.com/GijsTimmers/kotnetcli.git
$ cd kotnetcli
$ cd po
$ cp default.po ru.po
$ virtaal ru.po  ## make some changes here
```
Sounds too hard? You can always send me your po files:
gijs.timmers@student.kuleuven.be

### Graphic designers
We're looking for slick icons for `kotnetcli`. You can show off in
[this thread](https://github.com/GijsTimmers/kotnetcli/issues/74).

### Coders
If you see anything that can be improved, please write an
[issue](https://github.com/GijsTimmers/kotnetcli/issues) or open a pull 
request! Some guidelines to keep everything cohesive:
1. Indentation: always use 4 spaces. No tabs.
2. The lines shouldn't exceed 80 characters. Use backslashes to spread commands
over multiple lines.
2. Quotation marks: use double quotation marks (`"like this"`) except for
 when you want or need to combine both of them. So:
  - Allowed: `print "Single quotation marks are evil"`
  - Allowed: `print 'The developer thinks that double
   quotation marks are "evil"'`
  - Not allowed: `print 'I want to print something'`
3. Commenting: use `#` to enable/disable lines, use `## `
(__with__ a trailing space) to write a comment. If the commment doesn't fit on
the line, you can just write it above/under the line you want to write a comment
on.
