#!/bin/python
#---------------------------------------------------------------------------------
#
#                    ,--.
#                    |  |-.  ,---.  ,---. ,--.--.,--,--,
#                    | .-. '| .-. :| .-. ||  .--'|      \
#                    | `-' |\   --.' '-' '|  |   |  ||  |
#                     `---'  `----' `---' `--'   `--''--'
#
#         file: errors
#  description: This file contains the list of standard errors.
#
#       author: Peter Antoine
#         date: 06/09/2013
#---------------------------------------------------------------------------------
#                     Copyright (c) 2013 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import __builtin__

errors = []

def add_error_code(error_text):
	errors.append(error_text)
	return len(errors) - 1

__builtin__.OK									= add_error_code('Ok')
__builtin__.ERROR_FAILED						= add_error_code('Generic Failure.')
__builtin__.ERROR_NO_FILENAME_SPECIFIED			= add_error_code('You have not specified a filename')
__builtin__.ERROR_USER_DOES_NOT_EXIST			= add_error_code('User does not exist')
__builtin__.ERROR_USER_ALREADY_EXISTS			= add_error_code('User already exists')
__builtin__.ERROR_PERMISSION_DENIED				= add_error_code('Permission denied')
__builtin__.ERROR_NOT_A_GROUP_MEMBER			= add_error_code('User is not a member of that group.')
__builtin__.ERROR_FAILED_TO_WRITE_TO_FILE		= add_error_code('Problem writing to the required file')
__builtin__.ERROR_FAILED_TO_READ_FROM_FILE		= add_error_code('Problem reading from the required file')
__builtin__.ERROR_FAILED_MUST_HAVE_PASSWORD		= add_error_code('A password must be supplied')
__builtin__.ERROR_USERS_ALREADY_LOADED			= add_error_code('Will not re-initialise the user database.')
__builtin__.ERROR_PROJECT_ALREADY_INITIALISED	= add_error_code('Project is already initialised')
__builtin__.ERROR_ALREADY_LOADED				= add_error_code('Has been loaded already, cannot reload')
__builtin__.ERROR_CORRUPT_PROJECT_FILE			= add_error_code('Corrupt Project file.')
__builtin__.ERROR_UNKNOWN_FIELD					= add_error_code('Unknown field. Project needs checking.')
__builtin__.ERROR_EMPTY_PROJECT_FILE			= add_error_code('Empty project file')
__builtin__.ERROR_MISSING_MANDATORY_FIELD		= add_error_code('Mandatory field missing')
__builtin__.ERROR_PARENT_MESSAGE_MISSING		= add_error_code('Parent of the message does not exist.')
__builtin__.ERROR_PROJECT_EXISTS				= add_error_code('Project exists already, cannot create.')
__builtin__.ERROR_FAILED_TO_CREATE_DIRECTORY	= add_error_code('Failed to create directory.')
__builtin__.ERROR_SCM_NOT_DEFINED				= add_error_code('No repository attached, need a repository for that action')
__builtin__.ERROR_SCM_ACTION_FAILED				= add_error_code('Problem actioning that request on the repository')
__builtin__.ERROR_NAME_ALREADY_EXISTS			= add_error_code('Name not unique and already exists.')
__builtin__.ERROR_NAME_DOES_NOT_EXISTS			= add_error_code('Name does not exist.')
__builtin__.ERROR_INVALID_NAME 					= add_error_code('Name is invalid, probably contains illegal characters.')
__builtin__.ERROR_ACTION_FAILED					= add_error_code('Failed to action request.')
__builtin__.ERROR_FILE_NOT_FOUND				= add_error_code('Failed to find file.')
__builtin__.ERROR_BADLY_FORMATTED_FILE			= add_error_code('File badly formatted.')
__builtin__.ERROR_BADLY_FORMATTED_RECORD		= add_error_code('File record badly formatted.')
__builtin__.ERROR_VERSION_HAS_NO_CHANGES		= add_error_code('No changes in the version supplied from the previous.')
__builtin__.ERROR_UNKNOWN_ENTRY					= add_error_code('Unknown/non-existent entry.')
__builtin__.ERROR_DUPLICATE_ENTRY				= add_error_code('Duplicate entry.')
__builtin__.ERROR_FAILED_LOAD					= add_error_code('Failed to Load Item.')

__builtin__.ERROR_FAILED_USER_OR_PASSWORD_INVALID	= add_error_code('User or Password is invalid or incorrect')

