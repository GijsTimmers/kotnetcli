# kotnetcli

This is the contribute.md of our project. Great to have you here. Here are a
few ways you can help make this project better!

## Team members
Gijs Timmers
Jo Van Bulck

## Adding new features

Some coding guidelines:

1. Indentation: always use 4 spaces. No tabs.
2. The lines shouldn't exceed 80 characters. Use backslashes to spread commands
over multiple lines.
2. Quotation marks: use double quotation marks (`"like this"`) except for
 when you want or need to combine both of them. So:
  - Allowed: `print "Single quotation marks are evil"`
  - Allowed: `print 'The developer thinks that double
   quotation marks are "evil"'`
  - Not allowed: `print('I want to print something')`
3. Commenting: use `#` to enable/disable lines, use `## `
(__with__ a trailing space) to write a comment. If the commment doesn't fit on
the line, you can just write it above/under the line you want to write a comment
on.

Don’t get discouraged! We estimate that the response time from the
maintainers is around two days.

# Bug triage

You can notify us about bugs here:
https://github.com/GijsTimmers/kotnetcli/issues

# Translations

Translations are needed. We would like you to use .po files to translate
`kotnetcli` in your language. Just create a new branch, edit the default.po file
, save as <yourlanguageabbreviation>.po and request a merge.

For example:

```
$ git clone https://github.com/GijsTimmers/kotnetcli.git
$ cd kotnetcli
$ cd po
$ cp default.po ru.po
$ nano ru.po  ## make some changes here

Sounds too hard? You can always send me your po files:
gijs.timmers@student.kuleuven.be

# Documentation

Not needed at the moment. Maybe there will be a `man` page in the future.
