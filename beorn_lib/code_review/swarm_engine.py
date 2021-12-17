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

import os
import json
import base64
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
from beorn_lib.scm import SCM_P4
from .change import Change
from .comment import Comment
from .hunk import Hunk
from .change_file import ChangeFile
from .code_review import CodeReview
from .review_engine import ReviewEngine, registerEngine

class SwarmReviewEngine(ReviewEngine):
	def __init__(self, configuration, password_function=None):
		super(SwarmReviewEngine, self).__init__(configuration, password_function)

		if 'swarm_server' in configuration:
			self.server_url = configuration['swarm_server']
		else:
			self.server_url = 'http://192.168.168.40'

		if 'perforce_server' in configuration:
			self.perforce_server = configuration['perforce_server']
		else:
			self.perforce_server = '192.168.168.31:1666'

		# only interested in reviews the owner has authored.
		if 'as_author' in configuration:
			self.as_author = configuration['as_author']
		else:
			self.as_author = False

		if 'user_group' in configuration and configuration['user_group'] != []:
			self.user_group = configuration['user_group']
		else:
			self.user_group = []

		if 'user' in configuration and configuration['user'] != '':
			self.user = configuration['user']
		else:
			self.user = self.getUser()

		if 'working_directory' in configuration and configuration['working_directory'] != '':
			self.working_directory = configuration['working_directory']
		else:
			# TODO: HACK - remove this - we should get the path passed in.
			self.working_directory = os.path.realpath('.')

		self.scm = SCM_P4(repo_url=self.perforce_server, working_dir=self.working_directory)

		# BUG: Here -- the key returned is not valid
		if password_function is not None:
			self.scm.setPasswordFunction(password_function)
			self.key = self.scm.getUserKey(self.user)

	@classmethod
	def getDefaultConfiguration(cls):
		return {'swarm_server': 'http://192.168.178.40',
				'perforce_server': '192.168.178.31:1666',
				'user': '',
				'poll_period': str(60*60),					# Once an hour
				'as_author': False,
				'user_group': []}

	@classmethod
	def getDialogLayout(cls):
		button_list = [('as_author', 'Only return authors')]

		return [('TextField', 'text', 'swarm_server', "Swarm Server"),
				('TextField', 'text', 'perforce_server', "Perforce Server Address"),
				('TextField', 'text', 'user', "Perforce User Name"),
				('TextField', 'numeric', 'poll_period', "How often to poll swarm"),
				('TextField', 'text', 'user_group', "User group to pay attention to."),
				('ButtonList', 'multiple', 'options', "Options", button_list)]

	def __swarm_command(self, command, parameters):
		url = self.server_url + '/api/v9/' + '/'.join(command)

		if parameters is None:
			request = urllib.request.Request(url)
		else:
			request = urllib.request.Request(url + '?' + urllib.parse.urlencode(parameters, True))

		if self.key is not None and len(self.key) == 32:
			password = base64.encodestring('%s:%s' % (self.user, self.key))[:-1]
			request.add_header("Authorization", "Basic " + password)
		elif self.key == "'login' not necessary, no password set for this user.":
			# TODO: need to add logging.
			print("ahhh --- magic user I can't handled these.")
			return None
		else:
			return None

		try:
			handle = urllib.request.urlopen(request, timeout=10)
			return json.loads(handle.read())

		except urllib.error.URLError:
			# TODO: need to add logging.
			return None

		except urllib.error.HTTPError:
			# TODO: need to add logging.
			# TODO: Also this is the error if it fails to logon.
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

		elif state['state'] == 'archived':
			return CodeReview.CODE_REVIEW_STATUS_ABANDONED

		else:
			return CodeReview.CODE_REVIEW_STATUS_UNKNOWN

	def updateReview(self, new_state):
		result = False

		if new_state['id'] in self:
			review = self[new_state['id']]
		else:
			review = CodeReview(new_state['id'], new_state['author'], new_state['updated'], True)
			self.addChildNode(review)

		if review.getLastUpdate() < int(new_state['updated']):
			if review.getState() != self.calcReviewState(new_state):
				review.setState(self.calcReviewState(new_state))

			# Check changes and add them to the review.
			# Skip the first commit as that is the initial CL
			for commit in new_state['commits'][1:]:
				if commit not in review:
					change = self.scm.getChangeList(commit)
					if change is not None:
						review.addChange(change)

			result = True

		self.updateVotes(review, new_state['participants'])
		self.updateComments(review)

		return result

	def updateReviews(self):
		""" This function will read the current reviews from the server. """
		result = False

		command = ['reviews']
		parameters = {}				#'fields': 'state,commitStatus,commits,description,id,author,participants,updated'}

		#if self.as_author:
		parameters['author'] = self.user
		#elif len(self.user_group) > 0:
		#	parameters['participants'] = self.user_group

		results = self.__swarm_command(command, parameters)

		if results is not None:
			for item in results['reviews']:
				if item['id'] not in self:
					self.addReview(item)
					result = True
				else:
					result |= self.updateReview(item)

		return result

	def save(self):
		if self.isDirty():
			self.postChanges()

	def update(self):
		if self.isDirty():
			self.postChanges()
		return self.updateReviews()

	def getChangeByVersion(self, code_review_obj, version):
		result = None
		count = 0

		# TODO: count in reverse order.
		for item in code_review_obj:
			if type(item) == Change:
				count += 1
				if count == version:
					result = item
					break

		return result

	def updateVotes(self, code_review_object, participants):
		for user in participants:
			if participants[user] != []:
				change = self.getChangeByVersion(code_review_object, participants[user]['vote']['version'])

				vote_value = (participants[user]['vote']['value' ] == 1)

				if change is not None and change.getVote(user) != vote_value:
					change.vote(user, vote_value)

	def updateComments(self, code_review_obj):
		command = ['comments']
		parameters = {'topic': 'reviews/' + str(code_review_obj.getID())}
		results = self.__swarm_command(command, parameters)

		if results is not None:
			for comment in results['comments']:
				if 'context' in comment and comment['context'] != [] and 'version' in comment['context']:
					change = self.getChangeByVersion(code_review_obj, comment['context']['version'])
				else:
					change = None

				text = comment['body'].splitlines()

				if 'rightLine' in comment['context'] and comment['context']['rightLine']:
					line = int (comment['context']['rightLine'])
					pre_side = False
				elif 'leftLine' in comment['context'] and comment['context']['rightLine']:
					line = int (comment['context']['leftLine'])
					pre_side = True
				else:
					line = 0
					pre_side = False

				new_comment = Comment(comment['user'], int(comment['updated']), text, line, pre_side, int(comment['id']))
				if change is None:
					code_review_obj.addChildNode(new_comment)
				else:
					for item in change.getChildren():
						if type(item) == ChangeFile:
							if 'file' in comment['context'] and comment['context']['file'] and comment['context']['file'].endswith(item.getName()):
								if new_comment not in item:
									for child in item.getChildren():
										if type(child) == Hunk and child.isLineInHunk(line):
											if new_comment not in child:
												child.addChildNode(new_comment)
											break
									else:
										item.addChildNode(new_comment)
								break
					else:
						#if new_comment not in item:
						change.addChildNode(new_comment)

	def addReview(self, code_review):
		new_review = CodeReview(code_review['id'], code_review['author'], code_review['updated'])
		new_review.setState(self.calcReviewState(code_review))

		desc = code_review['description'].splitlines()
		new_review.setTitle(desc[0][:80])

		for commit in code_review['changes'][1:]:
			change_list = self.scm.getChangeList(str(commit))

			if change_list is not None:
				new_review.addChange(change_list)
			else:
				# TODO: need to add logging.
				# print "problem with: ", code_review['id'], " commit:", str(commit)
				pass

		self.updateVotes(new_review, code_review['participants'])
		self.updateComments(new_review)
		self.addChildNode(new_review)

registerEngine(SwarmReviewEngine)

# vim: ts=4 sw=4 noexpandtab nocin ai
