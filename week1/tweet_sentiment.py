import sys
import json
import string


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
    for word in line.split(' '):
        if word in sent_dict:
            sent_score += sent_dict[word]
    return sent_score

def lines (sent_dict, tweet_file):
    for line in tweet_file:
        d = json.loads(line.encode('utf8'))
        if 'text' in d.keys():
            norm_tweet = norm_word(d['text'].encode('utf8'))
            print get_sent_score(sent_dict, norm_tweet)
def main():
    sent_dict = dictionary_constructor(sys.argv[1])
    tweet_file = open(sys.argv[2])
    lines(sent_dict, tweet_file)


if __name__ == '__main__':
    main()
