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
#    file: dialog_test
#    desc: This function will test the text dialog.
#
#  author: Peter Antoine
#    date: 08/01/2014
#---------------------------------------------------------------------------------
#                     Copyright (c) 2014 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import unittest
import beorn_lib
import beorn_lib.errors
#from beorn_lib.dialog import TextDialog
from test.utils.build_dialog import buildDialog

class TestTextDialog(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname = 'runTest', test_data = None, temp_data = None):
		self.test_data = test_data
		self.temp_data = temp_data

		# initialise the test framework
		super(TestTextDialog, self).__init__(testname)

	def helper_displayScreen(self, screen, cursor):
		print(cursor)

		screen[cursor[1]] = screen[cursor[1]][0:cursor[0]-1] + '@' + screen[cursor[1]][cursor[0]:]

		for line in screen:
			print(line)

	def setUp(self):
		""" This function creates the dialog """
		self.dialog = buildDialog(beorn_lib.dialog.DIALOG_TYPE_TEXT)

		self.assertIsNotNone(self.dialog)

		self.dialog.resetDialog()


	def test_TextField(self):
		""" Text Dialog

			This test simple creates a text dialog to see if the basic
			class works.
		"""
		self.dialog.focusElement('test_4')

		for char in "abdc":
			self.dialog.handleKeyboardInput(char)

		self.dialog.focusElement('test_2')

		for char in "abc12345fdfd67890":
			self.dialog.handleKeyboardInput(char)

		self.dialog.focusElement('test_3')

		for char in "abc12345fdfd67890":
			self.dialog.handleKeyboardInput(char)

		# tab testing
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_TAB)

		# navigation test around the text_field
		self.dialog.focusElement('test_2')
		self.dialog.current_element.is_dirty = True
		self.dialog.repaint()

		# move left
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)

		# move right
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)

		# these will do nothing
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)

		# lets do a backspace (should remove the 0)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_BACKSPACE)

		# lets do a delete (move 3 left, and delete) - removes the 7
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DELETE)

	def test_TextBox(self):
		""" Text Box Test """
		# moving around the text box
		self.dialog.focusElement('test_1')
		self.dialog.current_element.is_dirty = True
		self.dialog.repaint()

		self.dialog.handleKeyboardInput('a')
		self.dialog.handleKeyboardInput('b')
		self.dialog.handleKeyboardInput('c')
		self.dialog.handleKeyboardInput('d')
		self.dialog.handleKeyboardInput('.')
		self.dialog.handleKeyboardInput(' ')

		for char in "A real test to see what works. This is a test and it should then wrap around onto the next line and to the end of the box.":
			self.dialog.handleKeyboardInput(char)

		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)

		# should stop at the top
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)

		# Ok, test delete
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DELETE)

		# Ok, test backspace
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_BACKSPACE)

		# Ok, test insert mode
		self.dialog.setInputMode(self.dialog.DIALOG_INPUT_MODE_REPLACE)
		self.dialog.handleKeyboardInput('a')
		(exit_dialog, refresh) = self.dialog.handleKeyboardInput('b')

	def test_DropDown(self):
		""" Drop Down Test """
		# drop down test
		self.dialog.focusElement('test_6')
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)

		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)

		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)

	def test_ButtonList(self):
		""" Button List Test """

		# test the button list (single)
		self.dialog.focusElement('test_7')

		# go up, should stop at the top
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RETURN)

		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RETURN)

		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RETURN)

		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RETURN)

		# test the button list (single)
		self.dialog.focusElement('test_8')

		# clear the current item
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RETURN)

		# go up, should stop at the top
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RETURN)

		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RETURN)

		# test the results of the dialog
		self.assertEqual({	'test_1': 'one',
							'test_2': 'two',
							'test_3': 0,
							'test_4': '',
							'test_5': False,
							'test_6': 3,
							'test_7': [False, False, False, True, False, False, False],
							'test_8': [True, True, False, True, False, True, False],
							'test_9': ['one']}, self.dialog.getResult())

	def test_TextBoxWordWrap(self):
		""" Word Wrap Test """
		# test word-wrap text box.
		#  This is the same test as for TextBox (test_1)
		self.dialog.focusElement('test_9')
		self.dialog.current_element.is_dirty = True
		self.dialog.repaint()

		self.dialog.handleKeyboardInput('a')
		self.dialog.handleKeyboardInput('b')
		self.dialog.handleKeyboardInput('c')
		self.dialog.handleKeyboardInput('d')
		self.dialog.handleKeyboardInput('.')
		self.dialog.handleKeyboardInput(' ')

		for char in "A real test to see what works. This is a test and it should then wrap around onto the next line and to the end of the box.":
			self.dialog.handleKeyboardInput(char)

		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DOWN)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_LEFT)

		# should stop at the top
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RIGHT)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_UP)

		# Ok, test delete
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_DELETE)

		# Ok, test backspace
		self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_BACKSPACE)

		# Ok, test insert mode
		self.dialog.setInputMode(self.dialog.DIALOG_INPUT_MODE_REPLACE)
		self.dialog.handleKeyboardInput('a')
		self.dialog.handleKeyboardInput('b')

		self.dialog.repaint()
		screen = self.dialog.getScreen()

	def test_TextButton(self):
		# button test
		self.dialog.focusElement('test_5')
		self.dialog.repaint()

		# should do nothing
		self.assertEqual((False, False), self.dialog.handleKeyboardInput('a'))
		self.assertEqual((False, False), self.dialog.handleKeyboardInput('b'))
		self.assertEqual((False, False), self.dialog.handleKeyboardInput('c'))

		# should call exit
		(exit_dialog, refresh) = self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_RETURN)
		self.assertTrue(exit_dialog)

		# should call exit (again)
		(exit_dialog, refresh) = self.dialog.handleKeyboardInput(self.dialog.DIALOG_SPECIAL_KEYS_ESCAPE)
		self.assertTrue(exit_dialog)

	def test_TextWraping(self):
		# Text box wrap function test
		text_to_wrap =	'This is the hour of our discontent. Why can nobody remember more that the beginning' \
						' words of that speech, it is really interesting that only the first few words are'   \
						' ever mentioned. Like the MLK speech, all the metal bits of the speech is at the '   \
						' beginning and gets missed.'

		tb = self.dialog.element_types['TextBox'].create({'name':'test_wrap',
												'title':'Text Box',
												'x':3, 'y':1,
												'width':64,
												'default': text_to_wrap,
												'word-wrap': True,
												'height': 10})

		result_list = tb.wordWrapText()

		# test with is sort'ish
		self.assertEqual([(0, 64), (65, 118), (119, 180), (181, 245), (246, 272)], result_list)

		tb = self.dialog.element_types['TextBox'].create({'name':'test_wrap',
												'title':'Text Box',
												'x':3, 'y':1,
												'width':31,
												'default': text_to_wrap,
												'word-wrap': True,
												'height': 10})

		result_list = tb.wordWrapText()

		# test width same size as the text.
		self.assertEqual([(0, 23), (24, 50), (51, 73), (74, 105), (106, 135), (136, 164), (165, 193), (194, 223), (224, 255), (256, 272)],
							result_list)

		tb = self.dialog.element_types['TextBox'].create({'name':'test_wrap',
												'title':'Text Box',
												'x':3, 'y':1,
												'width':272,
												'default': text_to_wrap,
												'word-wrap': True,
												'height': 10})

		result_list = tb.wordWrapText()

		self.assertEqual([(0, 272)], result_list)

		# test width is less than a length of any one word.
		tb = self.dialog.element_types['TextBox'].create({'name':'test_wrap',
												'title':'Text Box',
												'x':3, 'y':1,
												'width':10,
												'default': text_to_wrap,
												'word-wrap': True,
												'height': 10})

		result_list = tb.wordWrapText()

		self.assertEqual([(0, 7), (8, 16), (17, 23), (24, 34), (34, 43), (44, 50), (51, 59), (60, 69), (70, 73), (74, 83), (84, 92),
						 (93, 97), (98, 108), (109, 118), (119, 129), (129, 135), (136, 144), (145, 154), (155, 164), (165, 169),
						 (170, 180), (181, 189), (190, 193), (194, 201), (202, 209), (210, 220), (221, 227), (228, 237), (238, 245),
						 (246, 255), (256, 264), (265, 272)], result_list)

# vim: ts=4 sw=4 noexpandtab nocin ai
