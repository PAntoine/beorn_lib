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
#    file: logging
#    desc: This class handles the logging for the beorn library.
#
#  author: Peter Antoine
#    date: 02/02/2014
#---------------------------------------------------------------------------------
#                     Copyright (c) 2014 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import time
from . import errors

class Logging(object):
	""" Beorn Logging Class

		This class handles the logging for the beorn classes.

		It is a very simple logger, there are four log levels:

			name               description
			----------------   ----------------------------------------------------
			LOG_LEVEL_NONE     This level should not be selected for comments and
			                   this level cannot be blocked.
			LOG_LEVEL_FATAL    This is a fatal error and the system will stop.
			LOG_LEVEL_ERROR    This is an error.
			LOG_LEVEL_WARNING  You might guess what this is.
			LOG_LEVEL_INFO     For informational messages.
			LOG_LEVEL_DEBUG    For messages that are not required in production.

		The level can be changed at run time, this does mean that the amount of logging
		should be monitored as it will still slow down the system, even when the logging
		level is changed (obviously not that much as not io).

		Logging level defaults to LOG_LEVEL_INFO.

		Simple usage:

			log = Logging('file_name')
			log.setLevel(LOG_LEVEL_DEBUG)

			...

			log.message(LOG_LEVEL_WARNING, 'This is a warning message')

			...
	"""

	# Logging levels
	LOG_LEVEL_NONE		= 0
	LOG_LEVEL_FATAL		= 1
	LOG_LEVEL_ERROR		= 2
	LOG_LEVEL_WARNING	= 3
	LOG_LEVEL_INFO		= 4
	LOG_LEVEL_DEBUG		= 5

	def  __init__(self, file_name):
		""" __init__

			This function will create the logging object and open the logging file.
		"""
		self.log_file = None
		self.log_level = Logging.LOG_LEVEL_INFO

		try:
			self.log_file = open(file_name, 'w')
		except IOError:
			print("Failed to open logfile - logging won't be enabled.")

	def __del__(self):
		""" __del__

			This will close the logging file.
		"""
		if self.log_file is not None:
			self.log_file.close()

	def setLoggingLevel(self, log_level):
		""" Set Logging Level

			This function will set the current logging level.
		"""
		if log_level >= Logging.LOG_LEVEL_NONE and log_level <= Logging.LOG_LEVEL_DEBUG:
			self.log_level = log_level

	def message(self, log_level, message):
		""" Message

			This function will write a log message to the log.
		"""
		if log_level <= self.log_level:
			if self.log_file is not None:
				time_string = time.strftime("%Y-%m-%d %H:%M:%S +0000: ", time.gmtime())

				if type(message) == list:
					for line in message:
						self.log_file.write(time_string + line + '\n')
				else:
					self.log_file.write(time_string + message + '\n')

				self.log_file.flush()

	def error(self, log_level, error_code):
		""" Error

			This function will write a log an error message to the log.
		"""
		if log_level <= self.log_level:
			if self.log_file is not None:
				time_string = time.strftime("%Y-%m-%d %H:%M:%S +0000: ", time.gmtime())

				self.log_file.write(time_string + errors.errors[error_code] + '\n')
				self.log_file.flush()

# vim: ts=4 sw=4 noexpandtab nocin ai
