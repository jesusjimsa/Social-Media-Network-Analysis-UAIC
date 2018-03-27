# -*- coding: utf-8 -*- 

import re
import sys

try:
	headlines_file = open("./scrapped/headlines.csv", 'r')
	parsed_file = open("./parsed_headlines.csv", 'wr')
	ignored_words_file = open("./words_to_ignore/ignore.txt", 'r')
except IOError:
	print "Could not open file"
	sys.exit()

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