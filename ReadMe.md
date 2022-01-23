
                    ,--.
                    |  |-.  ,---.  ,---. ,--.--.,--,--,
                    | .-. '| .-. :| .-. ||  .--'|      \
                    | `-' |\   --.' '-' '|  |   |  ||  |
                     `---'  `----' `---' `--'   `--''--'

# Beorn Lib #
## version 2.0.1 ##

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

    - Fix: fixed indigobuggie issues and updated the tests
    - Fix: removed `project_plan` test it is not required
    - Fix: Python3 defaults to bytes[] when the file is opened "wb" so changed to "w".

## Licence and Copyright ##
                   Copyright (c) 2014-2022 Peter Antoine
                           All rights Reserved.
                     Released Under the MIT Licence
