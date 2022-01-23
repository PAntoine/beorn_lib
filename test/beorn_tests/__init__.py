#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#
#                    ,--.
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,
#                    | .-. '| .-. :| .-. ||  .--'|      \
#                    | `-' |\   --.' '-' '|  |   |  ||  |
#                     `---'  `----' `---' `--'   `--''--'
#
#    file: __init__
#    desc: This is the init file for the test classes.
#
#  author: Peter Antoine
#    date: 04/01/2014
#---------------------------------------------------------------------------------
#                     Copyright (c) 2014 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

#from user_test import TestUser
from .notes_test import TestNotes
from .project_test import TestProject
from .test_source_tree import TestSourceTree
#from .project_plan_test import TestProjectPlan
from .text_dialog_test import TestTextDialog
from .html_dialog_test import TestHTMLDialog
from .tree_test import TestTree
#from test_code_review import TestCodeReview
from .nested_tree_test import TestNestedTree
from .config_test import TestConfig
from .test_timekeeper import TestTimeKeeper
from .test_swarm_reviews import TestSwarmCodeReview

# vim: ts=4 sw=4 noexpandtab nocin ai
