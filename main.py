#!/usr/bin/env python

# documentation
# http://courses.ischool.berkeley.edu/i256/f06/projects/bonniejc.pdf
# http://codegolf.stackexchange.com/questions/20914/who-is-this-chatbot

import ClassSchema as cs
import ClassText as ct

q = cs.ClassSchema("data.db")
q.createSchema()

bot = ct.ClassText()
human = ct.ClassText()

while True:

	# the greeting from the bot (Botty)
	print "B: %s" % bot.getText()

	# input from the human
	human.setText(raw_input("H: ").strip())

	# exit if below is true
	if human.getText() == "" or human.getText().lower() == "bye":
		break

	bot_words = bot.getTextCount()
	bot_words_weight = bot.getTextWeight()

	human_words = human.getTextCount()
	human_words_weight = human.getTextWeight()

	sentence_id = q.getId('sentence', human.getText())

	# create associations between Botty's words and human's sentence
	for bot_word, bot_weight in bot_words_weight.iteritems():
		word_id = q.getId("word", bot_word)
		q.insertValues("associations", "VALUES (%s)" % (",".join(str(x) for x in [word_id, sentence_id, bot_weight])))

	# create a temporary table to store possible answers
	q.createSchema(tmp=True)

	# build a list in the temp table with possible sentences to answer based on the words from the human
	for human_word, human_weight in human_words_weight.iteritems():
		q.insertValues("results", "SELECT associations.sentence_id, sentences.sentence, %s * associations.weight / ("
		                          "%d + sentences.count) FROM words INNER JOIN associations ON associations.word_id = "
		                          "words.rowid INNER JOIN sentences ON sentences.rowid = associations.sentence_id "
		                          "WHERE words.word = '%s'" % (human_weight, 3, human_word))

	# retrieve the best sentence
	best = q.selectValues("sentence_id, sentence, SUM(weight) as sum_weight", "results", "GROUP BY sentence_id ORDER "
	                                                                                     "BY sum_weight DESC LIMIT 1")
	# remove the table
	q.dropTable("results")

	# if there is no best sentence, randomly chose one
	if best is None:
		best = q.selectValues("rowid, sentence", "sentences", "WHERE count = (SELECT MIN(count) FROM sentences) "
		                                                      "ORDER BY RANDOM() LIMIT 1")

	# assign the best answer to Botty
	bot.setText(best[1])

	# update the number of times that sentence was used in conversation
	q.updateValues("sentences", "count = count + 1 WHERE rowid = %d" % best[0])

