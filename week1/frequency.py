import sys
import json
import string

from collections import defaultdict

def dictionary_constructor(sent_file):
    afinnfile = open(sent_file)
    scores = {}  # initialize an empty dictionary
    for line in afinnfile:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    return scores


def norm_word(word):
    exclude = set(string.punctuation)
    word = ''.join(ch for ch in word.lower() if ch not in exclude)
    return word

def get_sent_score(sent_dict, line):
    sent_score = 0
    not_sent_words = []
    for word in line.split(' '):
        if word in sent_dict:
            sent_score += sent_dict[word]
        else:
            not_sent_words.append(word)
    return sent_score, not_sent_words

def update_dict(dict, tweet):
	for word in tweet.split():
		if word in dict:
			dict[word] += 1
		else:
			dict[word] = 1

def frequency (dict, tweet_file):
    for line in tweet_file:
        d = json.loads(line.encode('utf8'))
        if 'text' in d.keys():
            update_dict(dict, norm_word(d['text'].encode('utf8')))

    freq = sum(dict.values())
    for word in dict.keys():
        print word, dict[word] / float(freq)

def main():
    dict = defaultdict()
    tweet_file = open(sys.argv[1])
    frequency(dict, tweet_file)

if __name__ == '__main__':
    main()
