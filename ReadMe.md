
                    ,--.
                    |  |-.  ,---.  ,---. ,--.--.,--,--,
                    | .-. '| .-. :| .-. ||  .--'|      \
                    | `-' |\   --.' '-' '|  |   |  ||  |
                     `---'  `----' `---' `--'   `--''--'

# Beorn Lib #
## version 1.4.1 ##

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

- SCM normalisation

  The different SCMs were not correct. The parameters should have been
  the same. This change was to make sure that settings parameters function
  was correctly passed and the parameters could be recovered from the
  SCM instance.

- Fix for symlinks in scm

  Switched all the things to abspath. As realpath decoded symlinks
  where causing problems with the SCM in symlinks and the path decoding.
  Normalising was hard.

- Tree walk fix - one item in the tree fix

- P4 fixes and a bug in source_tree

  P4 will be P4. The other is the tree issue was assuming that if it had
  children it was a directory. Now checking to see if it was actually a directory.

## Licence and Copyright ##
                   Copyright (c) 2014-2020 Peter Antoine
                           All rights Reserved.
                     Released Under the MIT Licence
