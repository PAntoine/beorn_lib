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
#    file: code_reviews
#    desc: This is the wrapper class that handles the file management staff.
#
#  author: peter
#    date: 06/12/2018
#---------------------------------------------------------------------------------
#                     Copyright (c) 2018 Peter Antoine
#                           All rights Reserved.
#                      Released Under the MIT Licence
#---------------------------------------------------------------------------------

import json
import base64
import urllib
import urllib2
from code_review import CodeReview
from review_engine import ReviewEngine, registerEngine

class SwarmReviewEngine(ReviewEngine):
	def __init__(self, configuration):
		super(SwarmReviewEngine, self).__init__(configuration)


		if 'swarm_server' in configuration:
			self.server_url = configuration['swarm_server']
		else:
			self.server_url = 'http://127.0.0.1:8080'

		if 'perforce_server' in configuration:
			self.perforce_server = configuration['perforce_server']
		else:
			self.perforce_server = '127.0.0.1:1888'

		# only interested in reviews the owner has authored.
		if 'as_author' in configuration:
			self.as_author = configuration['as_author']
		else:
			self.as_author = False

		if 'user_group' in configuration and configuration['user_group'] != []:
			self.user_group = configuration['user_group']
		else:
			self.user_group = [self.getUser()]

		self.key = "fred"

	@classmethod
	def getDefaultConfiguration(cls):
		return {'swarm_server': 'http://127.0.0.1:8080',
				'perforce_server': '127.0.0.1:1888',
				'poll_period': 60*60,					# Once an hour
				'as_author': False,
				'user_group': []
				}

	def __swarm_command(self, command, parameters):
		url = self.server_url + '/' + '/'.join(command)
		if parameters is None:
			request = urllib2.Request(url)
		else:
			request = urllib2.Request(url + '?' + urllib.urlencode(parameters, True))

		password = base64.encodestring('%s:%s' % (self.getUser(), self.key))[:-1]
		request.add_header("Authorization", "Basic " + password)

		try:
			handle = urllib2.urlopen(request)
			return json.loads(handle.read())

		except urllib2.URLError:
			return None
		except urllib2.HTTPError:
			return None

	def getName(self):
		return "Swarm Review"

	def postChanges(self):
		pass

	def pollServer(self):
		# Swarm is server based.
		return True

	def calcReviewState(self, state):
		if state['commitStatus'] != []:
			return CodeReview.CODE_REVIEW_STATUS_MERGE_ERROR

		elif len(state['commits']) > 0:
			return CodeReview.CODE_REVIEW_STATUS_MERGED

		elif state['state'] == 'approved':
			return CodeReview.CODE_REVIEW_STATUS_APPROVED

		elif state['state'] == 'needsReview' or state['state'] == 'needsRevision':
			return CodeReview.CODE_REVIEW_STATUS_OPEN

		elif state['state'] == 'rejected':
			return CodeReview.CODE_REVIEW_STATUS_ABANDONED

		else:
			return CodeReview.CODE_REVIEW_STATUS_UNKNOWN

	def updateReview(self, new_state):
		result = False

		if new_state['id'] in self:
			review = self[new_state['id']]
		else:
			review = CodeReview(new_state['id'], new_state['author'],new_state['updated'], True)
			self.addChild(review)

		if review.getLastUpdate() < int(new_state['updated']):
			if review.getState() != self.calcReviewState(new_state):
				review.setState(self.calcReviewState(new_state))

			# Check changes and add them to the review.
			# Skip the first commit as that is the initial CL
			for commit in new_state['commits'][1:]:
				if commit not in review:
					new_changes = self.scm.getChangeList(commit)
					review.addChange(new_changes)

			# Now get the comments
			command = ['comments']
			parameters = {'topic': 'reviews/' + new_state['id']}
			results = self.__swarm_command(command, parameters)

			for comment in results:
				# handle the comment and add to the review.
				# don't forget replies.
				pass

			result = True

#			new_state['commitStatus']
#			new_state['commits']
#			new_state['description']
#			new_state['id']
#			new_state['author']
#			new_state['participants']
#			new_state['updated']
		return result


	def updateReviews(self):
		""" This function will read the current reviews from the server. """
		result = False

		command = ['reviews']
		parameters = {'fields': 'state,commitStatus,commits,description,id,author,participants,updated'}

		if self.as_author:
			parameters['author'] = self.getUser()
		else:
			parameters['participants'] = [self.getUser()]

		results = self.__swarm_command(command, parameters)

		if results is not None:
			for item in results['reviews']:
				if item['id'] not in self:
					self.addReview(item)
					result = True
				else:
					result |= self.updateReview(item)

		return result

	def load(self):
		self.updateReviews()

	def save(self):
		if self.isDirty():
			self.postChanges()

	def update(self):
		if self.isDirty():
			self.postChanges()

		return self.updateReviews()

	def addReview(self, code_review):
		self.addChild(code_review)

registerEngine(SwarmReviewEngine)

# vim: ts=4 sw=4 noexpandtab nocin ai
