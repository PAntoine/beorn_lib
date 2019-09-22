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
#    file: notes_test
#    desc: This test holds the notes tests.
#
#  author: Peter Antoine
#    date: 05/01/2014
#---------------------------------------------------------------------------------
#                     Copyright (c) 2014 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import glob
import shutil
import getpass
import unittest
import platform
import beorn_lib.errors

from beorn_lib.notes import Notes

class TestNotes(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname = 'runTest', test_data = None, temp_data = None):
		self.test_data = test_data
		self.temp_data = temp_data

		# do the ground work for the test
		self.notes_dir = os.path.join(self.temp_data, 'notes')
		self.local_note_file = getpass.getuser() + '@' + platform.node()

		# initialise the test framework
		super(TestNotes, self).__init__(testname)

	def setUp(self):
		""" This function deletes all the files before the test runs """
		if os.path.isdir(self.notes_dir):
			# tidy up the test
			filelist = glob.glob(os.path.join(self.notes_dir,'*'))
			for dfile in filelist:
				os.remove(dfile)
		else:
			os.makedirs(self.notes_dir)

	def test_notes(self):
		""" Notes Tests

			This test exercises the system notes.
		"""
		# start the creation tests
		test_notes = Notes('NOTES', self.notes_dir)

		self.assertEqual(True, test_notes.addSubject('a subject'))

		# test negative get case
		a_subject = test_notes.getSubject('b subject')
		self.assertEqual(True, a_subject is None)

		# test positive get case
		a_subject = test_notes.getSubject('a subject')
		self.assertEqual(True, a_subject is not None)

		# can we create a note
		self.assertIsNotNone(test_notes.addNote(a_subject, 'a title', 'some text'))

		# should fail,  bad title
		self.assertIsNone(test_notes.addNote(a_subject, 'a = title', 'some text'))

		# test toggle
		subject = test_notes.getSubject('a subject')
		self.assertIsNotNone(subject)
		subject.toggle()

		# remove subject
		self.assertIsNotNone(test_notes.getSubject('a subject'))
		test_notes.removeSubject('a subject')
		self.assertEqual(None, test_notes.getSubject('a subject'))

	def test_NotesSave(self):
		""" Notes Test Save

			This test tests that we can save notes.
		"""
		# test load and save
		test_notes = Notes('NOTES', self.notes_dir)

		self.assertEqual(True, test_notes.addSubject('subject 1'))
		subject_1 = test_notes.getSubject('subject 1')
		self.assertIsNotNone(test_notes.addNote(subject_1, 'title 1', 'S11 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_1, 'title 2', 'S12 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_1, 'title 3', 'S13 some text'))

		self.assertEqual(True, test_notes.addSubject('subject 2'))
		subject_2 = test_notes.getSubject('subject 2')
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 1', 'S21 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 2', 'S22 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 3', 'S23 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 4', 'S24 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 5', 'S25 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 6', 'S26 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 7', 'S27 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 8', 'S28 some text'))

		self.assertEqual(True, test_notes.addSubject('subject 3'))
		subject_3 = test_notes.getSubject('subject 3')
		self.assertIsNotNone(test_notes.addNote(subject_3, 'a title 1', 'S31 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_3, 'a title 2', 'S32 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_3, 'a title 3', 'S33 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_3, 'a title 4', 'S34 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_3, 'a title 5', 'S35 some text'))

		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 9', 'S29 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_1, 'title 4', 'S14 some text'))
		self.assertIsNotNone(test_notes.addNote(subject_3, 'title 6', 'S36 some text'))

		# test the save
		self.assertTrue(test_notes.save())

	def test_NotesSingleLoad(self):
		""" Notes Test Single Load

			This test tests that we can load a single users notes.
		"""
		# test the load
		test_notes	 = Notes('NOTES', self.notes_dir)
		current_user = os.path.join(self.temp_data, 'notes', test_notes.current_user + '@')
		not_my_user  = os.path.join(self.temp_data, 'notes', 'not_my_user@')

		# single file load test
		shutil.copy(self.test_data + '/current_notes', not_my_user + test_notes.current_machine)
		shutil.copy(self.test_data + '/current_notes', current_user + test_notes.current_machine)

		test_notes.load()
		subject = test_notes.getSubject('subject 1')
		self.assertIsNotNone(subject)
		subject.toggle()
		subject = test_notes.getSubject('subject 2')
		self.assertIsNotNone(subject)
		subject.toggle()
		subject = test_notes.getSubject('subject 3')
		self.assertIsNotNone(subject)
		subject.toggle()

		note_lists = test_notes.listSubjects()
		self.assertEqual(4, len(note_lists))

	def test_NotesMultipleLoad(self):
		""" Notes Test Multiple Load

			This test tests that we can load a single users notes.
		"""
		# load the single user
		test = Notes('NOTES', self.notes_dir)
		note_lists = test.listSubjects()

		# multiple user load test
		test_notes = Notes('NOTES', self.notes_dir)
		current_user = os.path.join(self.temp_data, 'notes', test_notes.current_user + '@')

		shutil.copy(self.test_data + '/current_notes', current_user + test_notes.current_machine)

		# TODO: core has changed and does not load any other note set except the current
		# id this correct?
		shutil.copy(self.test_data + '/extra_notes', current_user + 'extra_notes')
		shutil.copy(self.test_data + '/extra_subjects', current_user + 'extra_subjects')
		shutil.copy(self.test_data + '/missing_subject', current_user + 'missing_subject')
		shutil.copy(self.test_data + '/extra_with_changes', current_user + 'extra_with_changes')

		test_notes.load()
		subject = test_notes.getSubject('subject 1')
		self.assertIsNotNone(subject)
		subject.toggle()
		subject = test_notes.getSubject('subject 2')
		self.assertIsNotNone(subject)
		subject.toggle()
		subject = test_notes.getSubject('subject 3')
		self.assertIsNotNone(subject)
		subject.toggle()

		# This exist in the extra files
		subject = test_notes.getSubject('subject 4')
		self.assertIsNone(subject)
		subject = test_notes.getSubject('subject 5')
		self.assertIsNone(subject)
		note_lists = test_notes.listSubjects()

		# TODO: should use getChildren on the children to test this.
		self.assertEqual(4, len(note_lists))
		self.assertEqual(1, len(note_lists[1][2]))
		self.assertEqual(1, len(note_lists[2][2]))
		self.assertEqual(1, len(note_lists[3][2]))
		#self.assertEqual(5, len(note_lists[4][2]))
		#self.assertEqual(5, len(note_lists[5][2]))

		# check that alternate version have been loaded
		#self.assertEqual(2, len(note_lists[5][2][1].getVersions()))
		#self.assertEqual(1, len(note_lists[5][2][3].getVersions()))

	def test_NotesTreeGeneration(self):
		""" Notes Test Tree Generation

			This test tests that we can use the tree get and update functions.
		"""
		# test the load
		test_notes	 = Notes('NOTES', self.notes_dir)
		current_user = os.path.join(self.temp_data, 'notes', test_notes.current_user + '@')
		not_my_user  = os.path.join(self.temp_data, 'notes', 'not_my_user@')

		# single file load test
		shutil.copy(self.test_data + '/current_notes', not_my_user + test_notes.current_machine)
		shutil.copy(self.test_data + '/current_notes', current_user + test_notes.current_machine)

		test_notes.load()

		subject_list = test_notes.getChildren()
		self.assertEqual(4, len(subject_list), "Tree probably did not load properly")

#		# TODO: Fix this need to create a lambda function to walk the tree and do the outout.
#		tree.walkTree(ssdsd

		# add a note to the tree
		subject_2 = test_notes.getSubject('subject 2')
		self.assertIsNotNone(test_notes.addNote(subject_2, 'title 9', 'S29 some text'))

		output = []
		#tree.renderTextTree(output)

# vim: ts=4 sw=4 noexpandtab nocin ai
