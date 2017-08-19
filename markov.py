"""
"""
import re
from pdb import set_trace
import random

# build starting distribution probability vector
# Make sure the key is sufficiently mangled.
start_vec = {'total_count': 0.0, 'all_words': []}
# 'word': count

# Current state, for transition matrix.
s_i = {}

def parse_twitter_txt(line):
    """
    """
    line = re.search(r'(?![0-9, ]+).+', line).group() # Remove twitter ID

    # Strip RT
    lead = re.match(r'RT @.+: ', line)
    if lead:
        line = line.lstrip(lead.group())

    # Findall returns a list.
    # Tokens: RT, URL's, words, puncutations, links, hashtags., these probably not necessary
    # Twitter Handles
    handles = re.findall(r'@[a-zA-Z]+', line)

    # Hashtags
    hastags = re.findall(r'#[a-zA-Z]+', line)

    # URL's
    urls = re.findall(r'https://[0-9a-zA-Z./]+', line)

    #
    words = line.split(' ')
    start_word = words[0]

    return start_word, words

def mk_probabilities(filename):
    """Build transition matrix from txt.
    """

    # Make start_vec, s_i
    with open(filename) as f:
        for line in f:
            start_word, words = parse_twitter_txt(line)

            # Tokens: RT, URL's, words, puncutations, links, hashtags.
            # build starting distribution probability vector
            if start_word in start_vec:
                start_vec['total_count'] += 1.0
                start_vec[start_word] += 1.0
            else:
                start_vec['total_count'] += 1.0
                start_vec[start_word] = 1.0
                start_vec['all_words'].append(start_word)

            # build transition matrix
            for w in range(0, len(words)-1):
                cword = words[w] # Current word
                nword = words[w+1] # Next word

                if cword in s_i:
                    subdict = s_i[cword]

                    subdict['total_count'] += 1.0
                    if nword in subdict['s_jcount']:
                        subdict['s_jcount'][nword] += 1.0
                    else:
                        subdict['s_j'].append(nword)
                        subdict['s_jcount'][nword] = 1.0
                else:
                    subdict = {'total_count': 1.0,
                                's_j' : [nword],
                                's_jcount': {nword: 1.0}}
                    s_i[cword] = subdict

class MarkovChain(object):

    def __init__(self, si, u = None):
        self.transition = si
        self.u = u
        if u:
            # print 'true'
            self.restart() # set self.current_state to initial
        # self.path()

    def restart(self):
        roll = random.random() # 'dice' roll to see which state we end up in
        for state in self.u['all_words']:
            prob = self.u[state] / self.u['total_count']
            if roll < prob:
                self.current_state = state
                break
            roll -= prob

    def next(self):
        roll = random.random()

        try:
            curr_row = self.transition[self.current_state]
        except KeyError:
            self.restart()
            curr_row = self.transition[self.current_state]

        for state in curr_row['s_j']:
            prob = curr_row['s_jcount'][state] / curr_row['total_count']

            if roll < prob:
                self.current_state = state
            roll -= prob

def mk_tweet(order):
    """make tweet of order 'order'
    """
    char_limit = 140

    # Make probabilities
    mk_probabilities('database/' + 'realdonaldtrump.txt')

    # Make Markov chain
    mkv = MarkovChain(s_i, start_vec)
    chain = mkv.current_state

    for i in range(0, 20):
        mkv.next()
        chain = chain + ' ' + mkv.current_state
        # print chain

        # set_trace()

    if len(chain) > 80:
        for i in range(0, len(chain)//20 + 1):
            print chain[80*i:80*(i+1)]
    # First step



if __name__ == '__main__':
    mk_tweet(1)
