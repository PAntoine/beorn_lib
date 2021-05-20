
                    ,--.
                    |  |-.  ,---.  ,---. ,--.--.,--,--,
                    | .-. '| .-. :| .-. ||  .--'|      \
                    | `-' |\   --.' '-' '|  |   |  ||  |
                     `---'  `----' `---' `--'   `--''--'

# Beorn Lib #
## version 1.5.0 ##

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

- Added return result to update

- Fixed broken scm test

- Add rebase tree functionality
    This might need more work, not sure if more the items from the
    old root need copying to the new root. But I think all that
    needs copying are the children and that is it.

- fixed missing default items from nested tree.

- removed state checks
    Not sure why these were there, maybe a little too defensive
    coding. But these were getting in the way of the rebase of the
    tree.

## Licence and Copyright ##
                   Copyright (c) 2014-2020 Peter Antoine
                           All rights Reserved.
                     Released Under the MIT Licence
