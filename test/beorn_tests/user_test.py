#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------
#                                                   
#                    , --.                                 
#                    |  |-.  , ---.  , ---. , --.--., --, --,   
#                    | .-. '| .-. :| .-. ||  .--'|      \ 
#                    | `-' |\   --.' '-' '|  |   |  ||  | 
#                     `---'  `----' `---' `--'   `--''--' 
#                                                    
#    file: user_tests
#    desc: This function tests the User classes.
#
#  author: Peter Antoine
#    date: 04/01/2014
#---------------------------------------------------------------------------------
#                     Copyright (c) 2014 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import beorn_lib.errors
import unittest
from beorn_lib.pack import Pack
from beorn_lib.users import Users

class TestUser(unittest.TestCase):
	""" User Tests """
	def __init__(self, testname = 'runTest', test_data = None):
		self.test_data = test_data
		
		# initialise the test framework
		super(TestUser, self).__init__(testname)

	def test_CreateUsers(self):
		""" Create Users

			This will test to see if a Users structure can be created.
		"""
		users = Users()
		self.assertIsNotNone(users)

	def test_User(self):
		""" User Tests

			 This function will create a User in the User list and run some
			 basic tests on the simple functionality.
		"""
		users = Users()

		test_user = 'test_user'
		bad_user_name = 'test user'

		# Should be able to add the user first time
		self.assertEqual(OK, users.addUser(test_user, "Test User Name",  'hellomoto',  ['read', 'write'],  ['test', 'marsshot']))

		# Should fail to add the same user again.
		self.assertNotEqual(OK, users.addUser(test_user, "Test User Name",  'hellomoto',  ['read', 'write'],  ['test', 'marsshot']))

		# Might aswell check the password here
		self.assertEqual(OK, users.checkPassword(test_user, 'hellomoto'))

		# Might slight typo in the name - valid password
		self.assertNotEqual(OK, users.checkPassword(bad_user_name, 'hellomoto'))

		# And to make sure that the negative case works
		self.assertNotEqual(OK, users.checkPassword(test_user, 'rumplestiltskin'))

		# does if find the permission it needs.
		self.assertEqual(OK, users.checkPermission(test_user, 'read'))
		self.assertEqual(OK, users.checkPermission(test_user, 'write'))

		# has it not got the permission?
		self.assertNotEqual(OK, users.checkPassword(test_user, 'walk'))

		# does if find the permission it needs.
		self.assertEqual(OK, users.checkGroup(test_user, 'test'))
		self.assertEqual(OK, users.checkGroup(test_user, 'marsshot'))

		# has it not got the permission?
		self.assertNotEqual(OK, users.checkGroup(test_user, 'walk'))

		# add group - new group (duplicate group is also not a problem)
		self.assertEqual(OK, users.addGroup(test_user, 'test'))
		self.assertEqual(OK, users.addGroup(test_user, 'test_1'))

		self.assertEqual(OK, users.checkGroup(test_user, 'test_1'))
		self.assertEqual(OK, users.checkGroup(test_user, 'test'))
		self.assertEqual(OK, users.checkGroup(test_user, 'marsshot'))

		# add permissions - new group (duplicate group is also not a problem)
		self.assertEqual(OK, users.addPermission(test_user, 'read'))
		self.assertEqual(OK, users.addPermission(test_user, 'append'))

		self.assertEqual(OK, users.checkPermission(test_user, 'append'))
		self.assertEqual(OK, users.checkPermission(test_user, 'read'))
		self.assertEqual(OK, users.checkPermission(test_user, 'write'))

		# remove group
		self.assertEqual(OK, users.removeGroup(test_user, 'test'))
		self.assertEqual(OK, users.removeGroup(test_user, 'test_1'))

		self.assertNotEqual(OK, users.checkGroup(test_user, 'test_1'))
		self.assertNotEqual(OK, users.checkGroup(test_user, 'test'))
		self.assertEqual(OK, users.checkGroup(test_user, 'marsshot'))

		# remove permission
		self.assertEqual(OK, users.removePermission(test_user, 'write'))
		self.assertEqual(OK, users.removePermission(test_user, 'append'))

		self.assertNotEqual(OK, users.checkPermission(test_user, 'write'))
		self.assertNotEqual(OK, users.checkPermission(test_user, 'append'))
		self.assertEqual(OK, users.checkGroup(test_user, 'marsshot'))

	def test_UserSave(self):
		""" Users Save

			This test will test that the user save feature works.
		"""
		users = Users()

		# No file name,  no users should fail.
		self.assertNotEqual(OK, users.saveUsers())

		test_filename = os.path.join(self.test_data,'test_save_file.uf')

		# Give a filename - see what happens
		self.assertEqual(OK, users.saveUsers(test_filename))

		# Ok,  lets try that again with some users
		#  Double test,  checks that it uses previous name.
		self.assertEqual(OK, users.addUser('test_user_01', "Test User Name",  'hellomoto01',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_02', "Test User Name",  'hellomoto02',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_03', "Test User Name",  'hellomoto03',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_04', "Test User Name",  'hellomoto04',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_05', "Test User Name",  'hellomoto05',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_06', "Test User Name",  'hellomoto06',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_07', "Test User Name",  'hellomoto07',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_08', "Test User Name",  'hellomoto08',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_09', "Test User Name",  'hellomoto09',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_10', "Test User Name",  'hellomoto10',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_11', "Test User Name",  'hellomoto11',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_12', "Test User Name",  'hellomoto12',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_13', "Test User Name",  'hellomoto13',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_14', "Test User Name",  'hellomoto14',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.addUser('test_user_15', "Test User Name",  'hellomoto15',  ['read', 'write'],  ['test', 'marsshot']))
		self.assertEqual(OK, users.saveUsers())


	def test_UserLoad(self):
		""" Load User File.

			This test simply loads a User file and checks that all the users are there and the passwords can be used.
		"""
		users = Users()

		# load the user file
		test_filename = os.path.join(self.test_data,'test_load_file.uf')

		# Give a filename - see what happens
		self.assertEqual(OK, users.loadUsers(test_filename))

		password_format = "hellomoto%02d"
		username_format = "test_user_%02d"

		for item in range(1, 15):
			password = password_format % item
			username = username_format % item

			self.assertNotEqual(OK, users.checkPassword(username, 'walk'))
			self.assertEqual(OK, users.checkPassword(username, password))

	def test_UserPack(self):
		""" Test User Package.

			This test will check that the unpacking and packing of the user packages work,  and two users can create two packages and
			they dont decode and generate the same data.
		"""
		pack = Pack()
		pack_1 = Pack()

		# create the package
		pack.create('test-user', 'hellomoto', 'test-project')

		# get the package
		encoded_package = pack.toString()

		# should produce the same string when repeated
		self.assertEqual(encoded_package, pack.toString())

		# now load the package
		pack.load('hellomoto', encoded_package)

		# should produce the same string when repeated
		self.assertEqual(encoded_package, pack.toString())

		# should work when load somewhere else
		pack_1.load('hellomoto', encoded_package)
		self.assertEqual(encoded_package, pack_1.toString())

		# now encrypt some data - should not generate the same encoding twice
		data_string = "This is a simple test string to see if this works"
		encoded = pack.encodeData(data_string)
		encoded_1 = pack.encodeData(data_string)
		self.assertNotEqual(encoded, encoded_1)

		# decode the data to see if it is correct.
		decode = pack.decodeData(encoded)
		decode_1 = pack.decodeData(encoded_1)
		decode_2 = pack_1.decodeData(encoded)

		self.assertEqual(decode, decode_1)
		self.assertEqual(decode_1, decode_2)


# vim: ts=4 sw=4 noexpandtab nocin ai
