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
#    file: build_dialog
#    desc: This helper function will build the dialog for the dialog tests.
#
#  author: Peter Antoine
#    date: 13/09/2015
#---------------------------------------------------------------------------------
#                     Copyright (c) 2015 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import beorn_lib
from beorn_lib.dialog import Element

def buildDialog(dialog_type):
	""" This simply builds a returns a dialog """
	# negative test first
	drop_down_lines = ['line 1', 'line 2', 'line 3', 'line 4', 'line 5', 'line 6', 'line 7', 'line 8', 'line 9', 'line a']

	button_list = [	(False, 'This is the first line'),
					(False, 'This is really not a thing 1'),
					(True,	'This is really not a thing 2'),
					(True,	'This is really not a thing 3'),
					(False, 'This is really not a thing 4'),
					(True,	'This is really not a thing 5'),
					(False, 'This is really not a thing 6')]

	test_layout = [
		Element('TextBox',  {'name':'test_1', 'title':'Text Box', 'x':3, 'y':1, 'width':64, 'default': 'one', 'height': 10}),
		Element('TextField',{'name':'test_2', 'title':'Text Field', 'x':1, 'y':12, 'width':32, 'default': 'two'}),
		Element('TextField',{'name':'test_3', 'title':'Numeric', 'x':4, 'y':14, 'width':32, 'default': 'three' ,'input_type':'numeric'}),
		Element('TextField',{'name':'test_4', 'title':'Secret', 'x':5, 'y':16, 'width':32, 'input_type':'secret'}),
		Element('Button',{'name':'test_5', 'title':'OK', 'x':5, 'y':18}),
		Element('DropDown',{'name':'test_6', 'title':'Drop Down', 'x':5, 'y':20, 'height':5, 'default':3, 'items':drop_down_lines}),
		Element('ButtonList',{'name':'test_7', 'title':'Button List (single)', 'x':5, 'y':26, 'items':button_list}),
		Element('ButtonList',{'name':'test_8', 'title':'Button List (multiple)', 'x':5, 'y':36, 'items':button_list, 'type':'multiple'}),
		Element('TextBox',  {'name':'test_9', 'title':'Text Box', 'x':3, 'y':46, 'width':64, 'default': 'one', 'height': 10, 'word-wrap':True, 'list':True}),
	]
		
	return beorn_lib.Dialog(dialog_type, test_layout)

# vim: ts=4 sw=4 noexpandtab nocin ai
