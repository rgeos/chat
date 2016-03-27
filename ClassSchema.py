#!/usr/bin/env python

import sqlite3 as sql


class ClassSchema(object):
	"""
	A class that handles the storage method of the chat
	"""

	def __init__(self, bot_name):
		self.bot_name = bot_name
		self.table = ""
		self.col = ""
		self.text = ""

	def getBot(self):
		"""
		Retrieve the name of the bot
		:return:    string
		"""
		return self.bot_name

	def __query(self, q, r=False):
		"""
		This function will perform queries.
		It takes as arguments a string representing the SQL query and
		an optional boolean parameter for returning the results.
		:param q:   string
		:param r:   boolean
		:return:    list
		"""
		db = self.bot_name
		conn = sql.connect(db)

		try:
			c = conn.cursor()
			c.execute(q)
			conn.commit()

			if r:
				results = c.fetchone()
				c.close()
				return results
			else:
				c.close()
		# todo - add a proper exception message
		except:
			pass

	def createSchema(self, tmp=False):
		"""
		This function creates an SQL schema.
		Optionally there is a boolean parameter which creates a temporary table.
		:param tmp:     boolean
		:return:        none
		"""
		words       = 'CREATE TABLE words (word TEXT UNIQUE)'
		sentences   = 'CREATE TABLE sentences (sentence TEXT UNIQUE, count INT NOT NULL DEFAULT 0)'
		assoc       = 'CREATE TABLE associations (word_id INT NOT NULL, sentence_id INT NOT NULL, weight REAL NOT NULL)'
		temp        = 'CREATE TABLE results(sentence_id INT, sentence TEXT, weight REAL)'

		if tmp:
			self.__query(temp)
		else:
			self.__query(words)
			self.__query(sentences)
			self.__query(assoc)

	def __setTableName(self, newTableName):
		"""
		Set the name of the table
		:param newTableName:    string
		:return:                none
		"""
		self.table = newTableName

	def __getTableName(self):
		"""
		Retrieve the name of the table
		:return:    string
		"""
		return self.table

	def __setColName(self, newColName):
		"""
		Set the name of the column
		:param newColName:  string
		:return:            none
		"""
		self.col = newColName

	def __getColName(self):
		"""
		Retrieve the name of the column
		:return:    string
		"""
		return self.col

	def __setText(self, newText):
		"""
		Set text
		:param newText: string
		:return:        none
		"""
		self.text = newText

	def __getText(self):
		"""
		Retrieve text
		:return: string
		"""
		return self.text

	def insertValues(self, name, text):
		"""
		Insert values in the DB.
		This function takes two string arguments,
		one is the name of the table and the other one is for insertion parameters
		:param name:    string
		:param text:    string
		:return:        none
		"""
		self.__setTableName(name)
		self.__setText(text)

		q_insert = 'INSERT INTO %s %s' % (self.__getTableName(), self.__getText())
		# print q_insert
		self.__query(q_insert)

	def selectValues(self, col, name, text=""):
		"""
		Select values from DB.
		This function takes three arguments. A column name, a table name
		and optional parameters for selection.
		It returns a list with one result retrieved from the DB
		:param col:     string
		:param name:    string
		:param text:    string
		:return:        list
		"""
		self.__setTableName(name)
		self.__setText(text)
		self.__setColName(col)

		q_select = 'SELECT %s FROM %s %s' % (self.__getColName(), self.__getTableName(), self.__getText())
		# print q_select
		return self.__query(q_select.strip(), r=True)

	def updateValues(self, name, text):
		"""
		Update values in the DB.
		This function takes two arguments representing the table name and the update arguments.
		:param name:    string
		:param text:    string
		:return:        none
		"""
		self.__setTableName(name)
		self.__setText(text)

		q_update = 'UPDATE %s SET %s' % (self.__getTableName(), self.__getText())

		return self.__query(q_update)

	def dropTable(self, name):
		"""
		Remove a table from the DB.
		This function will take one argument representing the name of the table to be dropped.
		:param name: string
		:return:     none
		"""
		self.__setTableName(name)

		q_drop = 'DROP TABLE %s' % self.__getTableName()

		return self.__query(q_drop)

	def getId(self, name, text):
		"""
		Retrieve the entry ID of a certain row in the DB.
		The function takes two arguments representing the name of the table and the condition.
		It will return an integer which is the rowid of the queried entry.
		:param name:    string
		:param text:    string
		:return:        integer
		"""
		self.__setTableName(name)
		self.__setText(text)

		table   = self.__getTableName() + 's'
		column  = self.__getTableName()

		q_select = 'SELECT rowid FROM %s WHERE %s = "%s"' % (table, column, self.__getText())
		q_insert = 'INSERT INTO %s (%s) VALUES ("%s")' % (table, column, self.__getText())
		q_last   = 'SELECT MAX(rowid) from %s' % table

		row = self.__query(q_select, r=True)

		if row:
			return row[0]
		else:
			self.__query(q_insert)
			return self.__query(q_last, r=True)[0]


