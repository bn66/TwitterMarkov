"""
"""
import re
from pdb import set_trace
import random

directory = 'database/'

class MarkovVector(object):
    """Represents a vector/column/row for Markov probabilities.
    The initial state probability vector is a single MarkovVector object
    https://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/Chapter11.pdf
    """

    def __init__(self):
        self.total_count = 0.0
        self.state_list = []
        self.state_cts = {} # histogram

    def add_state(self, state):
        self.total_count += 1.0
        if state in self.state_cts:
            self.state_cts[state] += 1.0
        else:
            self.state_list.append(state)
            self.state_cts[state] = 1.0

class MarkovMatrix(object):
    """Represents a Matrix for Markov probabilities.
    The trans matrix is just a dictionary of MarkovVectors
    https://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/Chapter11.pdf
    """

    def __init__(self):
        self.states = {} # s_j

    def add_state(self, cstate, nstate):

        if cstate in self.states:
            self.states[cstate].add_state(nstate)
        else:
            mv = MarkovVector()
            mv.add_state(nstate)
            self.states[cstate] = mv

class MarkovChain(object):

    def __init__(self, initial, sij):
        self.trans = sij # MarkovMatrix, transition Matrix
        self.initial_state = initial
        self.restart() # Set current state
        # self.path()

    def restart(self):
        # Sents current state

        if type(self.initial_state) == MarkovVector: # Is initial state vector
            roll = random.random() # 'dice' roll to pick a state
            u_vec = self.initial_state

            for state in u_vec.state_list:
                prob = u_vec.state_cts[state] / u_vec.total_count
                if roll < prob:
                    self.current_state = state
                    break
                roll -= prob
        else: # Is an initial state
            self.current_state = self.initial_state


    def next(self):
        roll = random.random()

        try:
            # There is a next word
            curr_vec = self.trans.states[self.current_state]
        except KeyError:
            # There is no next word
            self.restart()
            curr_vec = self.trans.states[self.current_state]

        for state in curr_vec.state_list:
            prob = curr_vec.state_cts[state] / curr_vec.total_count
            # print roll, prob

            if roll < prob:
                self.current_state = state
                break
            roll -= prob

def parse_twitter_txt(line):
    """Will parse a line in the twitter txt file output by parsetwitter.py
    """
    line = re.search(r'(?![0-9, ]+).+', line).group() # Remove twitter ID

    # Strip RT
    lead = re.match(r'RT @.+: ', line)
    if lead:
        line = line.lstrip(lead.group())

    # Findall will return a list; These are all currently unused
    # Twitter Handles
    handles = re.findall(r'@[a-zA-Z]+', line)
    # Hashtags
    hastags = re.findall(r'#[a-zA-Z]+', line)
    # URL's
    urls = re.findall(r'https://[0-9a-zA-Z./]+', line)

    words = line.split(' ')
    start_word = words[0]

    return start_word, words

def mk_probs(filename, order):
    """Makes probabilities...
    """
    # Starting distribution probability vector
    u_vec = MarkovVector()
    s_i = MarkovMatrix() # Dictionary of MarkovVectors

    # Make start_vec, s_i
    with open(filename) as f:
        for line in f:
            start_word, words = parse_twitter_txt(line)

            # Build starting distribution probability vector
            u_vec.add_state(start_word)

            # Build trans matrix
            for w in range(0, len(words)-1):
                cword = words[w] # Current word
                nword = words[w+1] # Next word

                s_i.add_state(cword, nword)

    return u_vec, s_i

def mk_tweet(filename, order, num):
    """Makes 'num' tweets of order 'order', using 'filename' for probabilities.
    """
    char_limit = 140

    # Make probabilities
    a, b = mk_probs(directory + filename, order)

    # Make Markov chain
    for i in range(0, num):
        mkv = MarkovChain(a, b)
        chain = mkv.current_state

        chain_len = len(chain)
        while chain_len < char_limit:
            # print chain
            mkv.next()
            txt = mkv.current_state
            if (len(txt) + chain_len) <= char_limit:
                chain = chain + ' ' + mkv.current_state
                chain_len = len(chain)
            else:
                break

        # Print wrapping for powershell
        # print_mx = 80
        # for j in range(0, chain_len//print_mx + 1):
        #     print chain[print_mx*j:print_mx*(j+1)]
        print chain
        # set_trace()

if __name__ == '__main__':
    mk_tweet( 'realdonaldtrump.txt', 1, 20)
