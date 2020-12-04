
                    ,--.
                    |  |-.  ,---.  ,---. ,--.--.,--,--,
                    | .-. '| .-. :| .-. ||  .--'|      \
                    | `-' |\   --.' '-' '|  |   |  ||  |
                     `---'  `----' `---' `--'   `--''--'

# Beorn Lib #
## version 1.4.0 ##

This is a platform independent library that has the goal of supplying components for supporting
text editor plugins. It is designed to allow for coder oriented text plugins to be build and
ported other text editors.

It has been written python.

## Release status ##
- Missing Logging, It's starting to show.
- Need to remove some unused and useless features.
- Documentation is lacking and comments are crap and scarce.

## running tests ##

    `python test`

This takes the following parameters:
    -s       - only run the SCM tests
    -t       - only run the non-SCM tests
    -h       - print the help.
    -l       - print list of tests.

## Changes ##
Major Changes:
-   NestedTreeNode: walkTree() action function now has a new parameter "parameter" this is not
    backwards compatible and will cause problems. It allows for the colour finding function
    to use the walkTree function which is important for the new feature of the walk function
    to walk the tree in diffrent orders. The code for colour finding was getting complicated
    and had too many corner cases.

-   NestedTreeNode: As mentioned above the walk can now be ordered from the same tree in one
    of three ways. Parent first, Parent Last or in normal order. This allows for listings that
    have directories first/last. It needed quite a few changes throughtout the NestedTreeNode.

Minor Changes:
-   Perforce: (the obligatory - *sucks*) first issues with it not requiring a password for some
    setups. Also fixed a couple of other issues with it.

-   SourceTree: It had a bad default where the items were all flagged as dirs. This caused a
    bug with some of the changes with the NestedTree order.

-   Tests: Fixed some of the tests and added a list command that will surprisingly list the tests.

-   SCM: Added a flag for checking the server. This is mostly for P4 (see above) and want two
    diffent schedules for checking the server to reduce the load. But don't want to reduce the
    usefulness of checking against a qucker (and local) SCM like Git. Also it will allow for the
    upstream branch (on the remote) to also be checked at a less frequent rate. The Git server
    changes are place holders for now, will fix this at next version.

-   SCM: Let P4 use the env variables if they exist.

-   Other bug fixes.

## Licence and Copyright ##
                   Copyright (c) 2014-2020 Peter Antoine
                           All rights Reserved.
                     Released Under the MIT Licence

