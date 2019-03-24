#!/bin/python
#---------------------------------------------------------------------------------
#                                                   
#                    ,--.                                 
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,  
#                    | .-. '| .-. :| .-. ||  .--'|      \ 
#                    | `-' |\   --.' '-' '|  |   |  ||  | 
#                     `---'  `----' `---' `--'   `--''--' 
#                                                    
#         file: pack
#  description: This class defines the pack for the user.
#               The pack is used to control access to the user local encrypted
#               content.
#
#               The format of the encrypted package is the following:
#
#                [16 bytes-IV][AES encoded package]
#               
#               This is Base64 encoded.
#
#               This package contains the following:
#
#               <user-name>:<project-name>:<key>
#
#               The key is used for all encoding and decodings. The above is
#               protected by the given key.
#
#       author: Peter Antoine
#         date: 07/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import os
import string
import hashlib
from Crypto.Cipher import AES as AES
from base64 import b64encode, b64decode


# TODO: remove the password from the object, should never hold this in plain text

class Pack(object):
	""" Pack class """
	PACKAGE_KEY_LENGTH		= 32
	AES_IV_LENGTH			= 16

	# user package format
	PACKAGE_USER_NAME		= 0
	PACKAGE_PROJECT_NAME	= 1
	PACKAGE_KEY				= 2

	def __init__(self):
		self.user_name	= None
		self.project	= None
		self.key		= None
		self.password	= None
		self.pack_iv	= None

	def create(self,user_name,password,project):
		""" Create User Pack

			createUserPack(user_name,password,project) -> result code

			This function will create a package that is use for signing the notes and messages for the user
			for this project. It basically will generate the signing package for that combination.
		"""
		# create the inital package
		self.user_name	= user_name
		self.project	= project
		self.key		= os.urandom(self.PACKAGE_KEY_LENGTH)

		# password needs to be 32 chars, matching the block size, so SHA256 to let the users password be any length.
		pass_hash = hashlib.sha256()
		pass_hash.update(password)
		self.password = pass_hash.digest()

		return OK

	def load(self,password,user_pack):
		""" Load Encryption Package

			load (password,user_pack) ->  result code

			This function will take the user pack string and decode it to a unencrypted string.
			This string can be passed into the encrypt and decrypt functions.
		"""
		# upack the package
		package_encypted = b64decode(user_pack)
		self.pack_iv	= package_encypted[0:self.AES_IV_LENGTH]
		data_encrypted  = package_encypted[self.AES_IV_LENGTH:]

		# do the user sting
		pass_hash = hashlib.sha256()
		pass_hash.update(password)

		# create the decoder
		aes = AES.new(pass_hash.digest(), AES.MODE_CFB, self.pack_iv)
		package = string.split(aes.decrypt(data_encrypted),':')

		# now set up the values
		self.user_name	= package[self.PACKAGE_USER_NAME]
		self.project	= package[self.PACKAGE_PROJECT_NAME]
		self.key		= b64decode(package[self.PACKAGE_KEY])
		self.password	= pass_hash.digest()

		return OK

	def toString(self):
		""" To String

			toString() -> encoded package

			This function will generate an encoded package suitable for storage.

			We store the IV as the same package should be repeatable as far as 
			creating the same package without change.

			If the object is not valid it will return an empty string.
		"""
		if self.key is None:
			return ""

		else:
			if self.pack_iv is None:
				self.pack_iv = os.urandom(self.AES_IV_LENGTH)

			# create the encoder - not sure if the shortening is secure.
			aes = AES.new(self.password, AES.MODE_CFB, self.pack_iv)
			data = aes.encrypt("%s:%s:%s" % (self.user_name, self.project,  b64encode(self.key)))

			return b64encode("%s%s" % (self.pack_iv , data))

	def encodeData(self, data):
		""" Encode Data

			encodeData(string) -> encrypted string

			This function will encrypt a datum using the user pack that is supplied.
			It will encrypt this data with the key that is stored in the user pack.
			It will return an encrypted package with the Nonce that was used to 
			encrypt the package. Every time the data is passed into this function it
			will use a new Nonce to encode the data with. The nonce will be included
			in the resulting string.

			The resulting string is formatted to be able to be decoded, it should be
			passed to other functions in the same format.
		"""

		if self.key is None:
			return ""

		else:
			IV = os.urandom(self.AES_IV_LENGTH)
			aes = AES.new(self.key,AES.MODE_CFB, IV)
		
			return b64encode(IV + aes.encrypt(data))
		
	def decodeData(self, encoded_string):
		""" Decode Data

			decodeData(opened_user_pack, encoded_string) -> decoded_string

			This function will take the encoded string and the user package that has
			been opened with the password and generate the decoded string of data that
			was passed into the function.
		"""
		if self.key is None:
			return ""	

		else:
			data = b64decode(encoded_string)

			aes = AES.new(self.key,AES.MODE_CFB,data[0:self.AES_IV_LENGTH])

			return aes.decrypt(data[self.AES_IV_LENGTH:])


