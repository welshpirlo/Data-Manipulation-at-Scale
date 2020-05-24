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
    for word in line.split(' '):
        if word in sent_dict:
            sent_score += sent_dict[word]
    return sent_score


def geo_info(tweet):
    try:

        if tweet['place']['country_code'] == 'US':
            state = tweet['place']['full_name'][-2:]
            return True, state
        else:
            return False, ''
    except:
        pass
    return False, ''

def happy_state (sent_dict, tweet_file):
    state_happy_index = defaultdict()
    total_tweet_count = 0

    for line in tweet_file:
        d = json.loads(line.encode('utf-8'))
        try:
            if d['lang'] == 'en':
                if 'text' in d.keys():
                    norm_tweet = norm_word(d['text'].encode('utf-8'))
                    is_US, state = geo_info(d)
                    if is_US:
                        total_tweet_count += 1
                        sent_score = get_sent_score(sent_dict, norm_tweet)
                        if state in state_happy_index:
                            state_happy_index[state] += sent_score
                        else:
                            state_happy_index[state] = sent_score
        except:
            pass

    happiest_state = 'XX'
    happy_score = -1
    saddest_state = 'YY'
    sad_score = 99999

    for state, score in state_happy_index.items():
        if score > happy_score:
            happy_score = score
            happiest_state = state
        if score < saddest_state:
            saddest_state = state
            sad_score = score
    print happiest_state

def main():
    sent_dict = dictionary_constructor(sys.argv[1])
    tweet_file = open(sys.argv[2])
    happy_state (sent_dict, tweet_file)



if __name__ == '__main__':
    main()