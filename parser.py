# -*- coding: utf-8 -*-

import re
import sys
import pdb; 

try:
	headlines_file = open("./scrapped/headlines.csv", 'r')
	parsed_file = open("./parsed_headlines.csv", 'wr')
	ignored_words_file = open("./words_to_ignore/ignore.txt", 'r')
	grouped_file = open("./grouped_headlines.csv", 'wr')
except IOError:
	print "Could not open file"
	sys.exit()

punctuation = (',', '.', '\"', '-', '_', '{', '}', '[', ']', '+', '*', '!', '¡', 'º', 'ª', '\\', '·', '$', '%', '&', '/', '(', ')', '=', '?', '¿', '\'', '€', '<', '>', ';', ':', '–', '—', '…', '«', '»', '‘', '’', '\'')

ignore_words = ignored_words_file.readlines()	# List of words we have to ignore
ignored_words_file.close()

for i in range(0, len(ignore_words)):
	ignore_words[i] = ignore_words[i][:-1].lower()	# Delete last element of the word, the \n character

counted_words = dict()
line = headlines_file.readline()

while line:
	words = line.lower().split()

	link = words[0]

	for i in range(1, len(words)):
		if words[i] not in ignore_words:
			list_of_links = list()
			# pdb.set_trace()
			# First of all, we correct any possible punctuation mark 
			# that split may have missed
			for j in range(0, 3):
				if words[i][-1:] in punctuation:
					words[i] = str(words[i][:-1])
				if len(words[i]) > 0 and words[i][0] in punctuation:
					words[i] = str(words[i][1:])

			if words[i] in counted_words:
				list_of_links = counted_words[words[i]][0]

				if link not in list_of_links:
					list_of_links.append(link)

				# If the word is already in the dictionary, we just change the number of times it appears
				counted_words[words[i]] = (list_of_links, counted_words[words[i]][1] + 1)
			else:
				list_of_links.append(link)

				# The dictionaries store the link, the word and the number of times it appears
				counted_words[words[i]] = (list_of_links, 1)


	line = headlines_file.readline()	

for elem in counted_words:
	to_write = str(elem) + ", " + str(counted_words[elem][1]) + ", " + str(counted_words[elem][0]) + "\n"
	parsed_file.write(to_write)

parsed_file.close()
headlines_file.close()

common = dict()

for elem in counted_words:
	all_common = list()

	for check in counted_words:
		if elem[0:4] == check[0:4]:
			all_common.append(check)

	common[elem] = all_common

for elem in common:
	to_write = str(elem) + ", " + str(common[elem]) + "\n"
	grouped_file.write(to_write)

grouped_file.close()
