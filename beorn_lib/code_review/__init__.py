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
#    desc: Code Review.
#
#  author: peter
#    date: 04/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

from hunk import Hunk
from change import Change
from comment import Comment
from change_file import ChangeFile
from code_review import CodeReview
from code_reviews import CodeReviews
from local_code_reviews import LocalCodeReviews

registered_engines = {'LocalCodeReviews': LocalCodeReviews}

def registerEngine(engine_name, class_type):
	if engine_name not in registered_engines:
		registered_engines[engine_name] = class_type

def getSupportedEngines():
	return registered_engines.keys()

# vim: ts=4 sw=4 noexpandtab nocin ai
