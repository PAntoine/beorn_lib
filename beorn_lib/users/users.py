#!/usr/bin/env python
#---------------------------------------------------------------------------------
#                                                   
#                    ,--.                                 
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,  
#                    | .-. '| .-. :| .-. ||  .--'|      \ 
#                    | `-' |\   --.' '-' '|  |   |  ||  | 
#                     `---'  `----' `---' `--'   `--''--' 
#                                                    
#    file: users
#    desc: User Control
#    		This module holds the class that manages the BEORN users.
#    		The Users are based on a standard ini for for the users and this
#    		file contains all the relevant details that are required for managing
#    		the users.
#
#    		The class acts as a model for managing the users.
#
#  author: 
#    date: 02/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import beorn_lib.errors
from user import User as User 

class Users:
	""" User Control class """

	def __init__(self):
		self.users = {}
		self.filename = None

	def loadUsers(self, filename):
		""" Load Users
			
			loadUsers(filename) -> result_code

			This function will load the user dictionary. It will expect the file to exist and be
			in the correct format as produced by the User.toString() function. This will load the
			users from the given file, also it will remember the filename and will use this name
			for updating the user list later.
		"""
		result = OK

		# we don't want to re-initialise a user database.
		if self.filename is not None:
			result = ERROR_USERS_ALREADY_LOADED

		elif filename is None:
			result = ERROR_NO_FILENAME_SPECIFIED

		else:
			self.filename = filename

			try:
				# now open the project file
				user_file = open(self.filename,'r')

				for line in user_file:
					parts = line.partition(" = ")
					self.users[parts[0]] = User(parts[0],parts[2].rstrip('\n'))

				user_file.close()

			except IOError:
				self.filename = None
				result = ERROR_FAILED_TO_READ_FROM_FILE
				
		return result
	
	def saveUsers(self, filename = None):
		""" Save Users

			saveUsers([filename]) -> result_code
			
			This function will save the list of users to the given user file.
			If the 'filename' is given then the user list will be stored to this file. If this
			is not supplied then it will use either the file that was used for loading the user
			database or the filename of the last save. It will overwrite the username with the
			new name if given.

		"""
		if self.filename is None and filename is None:
			result = ERROR_NO_FILENAME_SPECIFIED

		else:
			if filename is not None:
				self.filename = filename

			result = OK

			try:
				user_file = open(self.filename,'wb')

				for user in self.users:
					user_file.write(self.users[user].toString())

				# write the footer and close the file
				user_file.close()
				result = OK

				user_file.close()

			except IOError:
				result = ERROR_FAILED_TO_WRITE_TO_FILE

		return result

	def addUser(self, user_name, real_name, password, permissions, groups):
		""" Add User

			addUser(user_name, real_name, password, permissions[], groups[]) -> result code

			This function will add a user to the user list. This function does not update the
			user file, this should be done in a separate step.
		"""
		# TODO: proper password validation here
		if password is None or password == '':
			result = ERROR_FAILED_MUST_HAVE_PASSWORD

		else:
			if user_name in self.users:
				result = ERROR_USER_ALREADY_EXISTS

			else:
				self.users[user_name] = User(user_name)
				self.users[user_name].real_name		= real_name
				self.users[user_name].permissions	= permissions
				self.users[user_name].groups		= groups
				self.users[user_name].changePassword(password)

				result = OK

		return result

	def listUsers(self):
		""" List Users

			This function will list the current user list.
		"""
		result = []

		for user in self.users:
			result.append(self.users[user].getDetails())

		return result

	def getUser(self, user_name):
		""" This function will return the user details of a specific
			user. It will return None if the user does not exist.
		"""
		if user_name in self.users:
			return self.users[user_name].getDetails()
		else:
			return None

	def checkPassword(self, user_name, password):
		""" Check Password

			This function will check to see if the password matches that given, for the
			given user.
		"""
		result = ERROR_FAILED_USER_OR_PASSWORD_INVALID

		if user_name in self.users:
			if self.users[user_name].checkPassword(password):
				result = OK

		return result

	def checkPermission(self, user_name, permission):
		""" Check Permission

			checkPermission(user_name, permission) -> result_code

			If the user has the permission that is required then the function will return OK.
		"""
		result = ERROR_PERMISSION_DENIED

		if user_name in self.users:
			if permission in self.users[user_name].permissions:
				result = OK

		return result

	def checkGroup(self, user_name, group):
		"""	Check Group

			checkGroup(user_name, group_name) -> result_code

			If the user is a member of the group then the function will return OK.
		"""
		result = ERROR_NOT_A_GROUP_MEMBER

		if user_name in self.users:
			if group in self.users[user_name].groups:
				result = OK

		return result

	def addGroup(self, user_name, group):
		""" Add Group

			addGroup(user_name, group_name) -> result

			If the user exists it will be added to this group.
		"""
		result = ERROR_USER_DOES_NOT_EXIST
		
		if user_name in self.users:
			result = OK

			if group not in self.users[user_name].groups:
				self.users[user_name].groups.append(group)

		return result

	def addPermission(self, user_name, permission):
		""" Add Permission

			addPermission(user_name, permission_name) -> result

			If the user exists it will be added to this permission.
		"""
		result = ERROR_USER_DOES_NOT_EXIST

		if user_name in self.users:
			result = OK

			if permission not in self.users[user_name].permissions:
				self.users[user_name].permissions.append(permission)

		return result

	def removeGroup(self, user_name, group):
		""" Remove Group

			removeGroup(user_name, group_name) -> result

			If the user exists it will be removed to this group.
		"""
		result = ERROR_USER_DOES_NOT_EXIST

		if user_name in self.users:
			result = OK

			if group in self.users[user_name].groups:
				self.users[user_name].groups.remove(group)

		return result

	def removePermission(self, user_name, permission):
		""" Remove Permission

			removePermission(user_name, permission_name) -> result

			If the user exists it will be removed to this permission.
		"""
		result = ERROR_USER_DOES_NOT_EXIST

		if user_name in self.users:
			result = OK

			if permission in self.users[user_name].permissions:
				self.users[user_name].permissions.remove(permission)

		return result

