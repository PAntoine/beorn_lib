#!/usr/bin/env python
#---------------------------------------------------------------------------------
#                                                   
#                    ,--.                                 
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,  
#                    | .-. '| .-. :| .-. ||  .--'|      \ 
#                    | `-' |\   --.' '-' '|  |   |  ||  | 
#                     `---'  `----' `---' `--'   `--''--' 
#                                                    
#    file: user
#    desc: User Class.
#    		This class describes a user. It has the functions that are required 
#    		to handle the interaction with the specific users.
#
#  author: 
#    date: 02/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import bcrypt
import string
from collections import namedtuple as namedtuple

UserDetails = namedtuple('UserDetails', ['uid', 'name', 'permissions', 'groups'])

class User:
	""" User class """

	# constants
	PASSWORD_ROUNDS			= 10
	NONCE_LENGTH			= (512/8)

	# user record format
	USER_RECORD_REAL_NAME	= 0
	USER_RECORD_PERMISSIONS	= 1
	USER_RECORD_GROUPS		= 2
	USER_RECORD_PASSWORD	= 3
	USER_RECORD_SIZE		= 4		# this should match the highest index

	def __init__(self, user_name = 'unknown', details = None):
		# TODO: This information needs to be validated, and the user permissions/projects are 
		#       valid for use. Possibly worth doing after the user database has loaded.
		if details is None:
			self.user_name		= user_name
			self.real_name		= 'Unknown User'
			self.permissions	= []
			self.groups			= []
			self.password		= None
		else:
			values = string.split(details,',')
			self.user_name 		= user_name
			self.real_name		= values[self.USER_RECORD_REAL_NAME]
			self.permissions	= string.split(values[self.USER_RECORD_PERMISSIONS],'$')
			self.groups			= string.split(values[self.USER_RECORD_GROUPS],'$')
			self.password		= values[self.USER_RECORD_PASSWORD]

	def getDetails(self):
		""" getDetails

			This function will export the user data into a safe tuple that can be used for displaying
			the user. It does not export the password.
		"""
		return UserDetails(self.user_name, self.real_name, self.permissions, self.groups)

	def toString(self):
		""" toString

			This function will export the user data into string format so that it can be saved in a
			user database, it will return a CSV formatted string. The string should not be amended as
			the loadUser() function expects this format of string to load the user data.
		"""
		ini_format = "%s = %s,%s,%s,%s\n"
		return ini_format % (self.user_name, self.real_name, string.join(self.permissions,'$'), string.join(self.groups,'$'), self.password)

	def changePassword(self, password):
		""" Change Password

			This function will change the password for the user. It is not the password that is used to
			store the user_pack as that password is never part of the user, and will not be serialised
			when the user is stored and/or loaded.
		"""
		self.password = bcrypt.hashpw(password, bcrypt.gensalt(self.PASSWORD_ROUNDS))
		return True

	def checkPassword(self, password):
		""" Check Password

			This function will simply check the given password against that that is in the user. It will
			return True or False depending on if the password matches.
		"""
		if self.password is None:
			return False
		else:
			return bcrypt.checkpw(password,self.password)

