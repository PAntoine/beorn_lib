
                    ,--.
                    |  |-.  ,---.  ,---. ,--.--.,--,--,
                    | .-. '| .-. :| .-. ||  .--'|      \
                    | `-' |\   --.' '-' '|  |   |  ||  |
                     `---'  `----' `---' `--'   `--''--'

# Beorn Lib #
## version 2.1.0 ##

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
or
	`python test TestQuery test_getSourceTree`

which will run just the one test.

This takes the following parameters:
    -s       - only run the SCM tests
    -t       - only run the non-SCM tests
    -h       - print the help.
    -l       - print list of tests.

## Changes ##

Enhancements:
    - added getSourceTree to SCM
    - added new test for getSourceTree

Fixes:
    - made SCM tests work - looks like they weren't working.
    - disabled P4 tests - can't be bothered to set P4 up.
    - rejigged the SCM tests so the repo state is accessible in the tests.

## Licence and Copyright ##
                   Copyright (c) 2014-2022 Peter Antoine
                           All rights Reserved.
                     Released Under the MIT Licence
