# -*- coding: utf-8 -*-

import re
import sys
import pdb

def sizeCheck(word):
	total = 0
	t = len(word)
	t -= 1

	if len(word) == 1:
		total = 1

	while t > 0:
		total += 2**t
		t -= 1
	
	return total

def distanceCalculator(first_word, second_word):
	distance = 0.0
	iterations = 0
	min_length = 0
	size_check = 0
	i = 0

	if len(first_word) > len(second_word):
		iterations = len(second_word)
		size_check = sizeCheck(second_word)
	else:
		iterations = len(first_word)
		size_check = sizeCheck(first_word)
	
	min_length = iterations - 1

	if len(first_word) > 3 and len(second_word) > 3:
		while i < iterations:
			if second_word[i] != first_word[i]:
				distance += 2**min_length

			min_length -= 1
			i += 1
				
		distance /= size_check
	else:
		distance = 1.0
	
	return distance
		

try:
	headlines_file = open("./scrapped/headlines.csv", 'r')
	parsed_file = open("./parsed_headlines.csv", 'wr')
	ignored_words_file = open("./words_to_ignore/ignore.txt", 'r')
	grouped_file = open("./grouped_headlines.csv", 'wr')
except IOError:
	print "Could not open file"
	sys.exit()

punctuation = (',', '.', '\"', '-', '_', '{', '}', '[', ']', '+', '*', '!', '¡', 'º', 'ª', '\\', '·', '$',
				'%', '&', '/', '(', ')', '=', '?', '¿', '\'', '€', '<', '>', ';', ':', '–', '—', '…', '«',
				'»', '‘', '’', '\'')

ignore_words = ignored_words_file.readlines()	# List of words we have to ignore
ignored_words_file.close()

for i in range(0, len(ignore_words)):
	ignore_words[i] = ignore_words[i][:-1].lower()	# Delete last element of the word, the \n character

counted_words = dict()
accepted = list()
line = headlines_file.readline()

while line:
	words = line.lower().split()

	link = words[0]

	for i in range(1, len(words)):
		# First of all, we correct any possible punctuation mark 
		# that split may have missed
		for j in range(0, 4):
			if words[i][-1:] in punctuation:
				words[i] = str(words[i][:-1])
			if len(words[i]) > 0 and words[i][0] in punctuation:
				words[i] = str(words[i][1:])
		
		if words[i] not in ignore_words:
			list_of_links = list()

			accepted.append(words[i])

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

counted_words_list = list()
inception_list = list()

for elem in counted_words:
	inception_list = [elem, counted_words[elem][1], counted_words[elem][0]]
	counted_words_list.append(inception_list)

counted_words_list.sort(lambda x, y: cmp(y[1], x[1]))

#for elem in counted_words_list:
#	to_write = str(elem[0]) + ", " + str(elem[1]) + ", " + str(elem[2]) + "\n"
#	parsed_file.write(to_write)

for ppp in accepted:
	parsed_file.write(str(str(ppp) + "\n"))

parsed_file.close()
headlines_file.close()

accepted = list(set(accepted))	# Delete duplicated elements
accepted.sort(lambda x,y: cmp(len(x), len(y)))	# Sort list of accepted words according to length

common = dict()
first_word = str()
second_word = str()
distance = 0.0
iterations = len(accepted)
i = 0
j = 0
add_i = True
add_j = False

while i < iterations:
	first_word = str(accepted[i])
	all_common = list()

	if add_i:
		i += 1
	
	add_i = True
	
	while j < iterations:
		second_word = str(accepted[j])

		distance = distanceCalculator(first_word, second_word)
		
		if distance <= 0.001:
			all_common.append(second_word)

			add_i = False
			add_j = False

			del accepted[j]
			iterations -= 1
		else:
			add_j = True

		if add_j:
			j += 1
	else:
		j = 0

	common[first_word] = all_common

for elem in common:
	to_write = str(elem) + ": "
	
	for similar in common[elem]:
		to_write += str(similar) + ", "
	
	to_write += "\n"

	grouped_file.write(to_write)

grouped_file.close()
