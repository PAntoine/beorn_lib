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
#    file: html_dialog_test
#    desc: This function will test the html dialog.
#
#  author: Peter Antoine
#    date: 13/09/2015
#---------------------------------------------------------------------------------
#                     Copyright (c) 2015 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import unittest
import beorn_lib
import beorn_lib.errors
from test.utils.build_dialog import buildDialog

class TestHTMLDialog(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname='runTest', test_data=None, temp_data=None):
		self.test_data = test_data

		# initialise the test framework
		super(TestHTMLDialog, self).__init__(testname)

	def setUp(self):
		""" This function creates the dialog """
		self.dialog = buildDialog(beorn_lib.dialog.DIALOG_TYPE_HTML)
		self.assertIsNotNone(self.dialog)
		self.dialog.resetDialog()

	def test_HTMLDialog(self):
		""" Test the Dialog.

		    As the dialog simply produces a form, there is only one test to do and that
			is call reader screen on the HTML dialog and test that is matches what we
			expect.
		"""
		test = self.dialog.getScreen()
		self.assertNotEqual([], test)
		#for line in test:
		#	print line



# vim: ts=4 sw=4 noexpandtab nocin ai
