import sys
import json
import string
from collections import defaultdict
import operator


def norm_word(word):
    exclude = set(string.punctuation)
    word = ''.join(ch for ch in word.lower() if ch not in exclude)
    return word

def update_dict(h_tags,h_dict):
    for hashtag in h_tags:
        if hashtag in h_dict:
            h_dict[hashtag] += 1
        else:
            h_dict[hashtag] = 1

def top_ten (tweet_file):
    h_dict = defaultdict()
    for line in tweet_file:
        d = json.loads(line.encode('utf-8'))
        hashtags = d['entities']['hashtags']
        h_tags = []
        for tags in hashtags:
            h_tags.append(norm_word(tags['text'].encode('utf-8')))
        update_dict(h_tags, h_dict)
    h_dict = sorted(h_dict.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(10):
        print h_dict[i][0], h_dict[i][1]

def main():
    tweet_file = open(sys.argv[1])
    top_ten(tweet_file)

if __name__ == '__main__':
    main()