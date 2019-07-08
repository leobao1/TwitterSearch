#%%
import itertools, collections
import tweepy as tw
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import networkx

def remove_stopwords(wordlist):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    return [word for word in wordlist if not word in stop_words]


def killurl(string):
    ret_string = re.sub("([^0-9A-Za-z#' \t])", ' ', string)
    return re.sub("(@[A-Za-z0-9_]+)|(\w+:\/\/\S+)|([#\"”“.,])", "", string)

def print_progress(return_text, count):
    print(f'Tweets searched: {count}', end='\r')
    return return_text

def retrieve_tweets(user):
    try:
        tweets = tw.Cursor(api.user_timeline, id=user, tweet_mode='extended').items()
        tweet_words = [print_progress(killurl(tweet.full_text).lower().split(), i) for i, tweet in enumerate(tweets) if not tweet.full_text.lower().startswith('rt')]
        print()
        return list(itertools.chain(*tweet_words))
    except tw.TweepError as e:
        print("Error, twitter handle likely mistyped")
        print(f'Error message: {e.response.text}')
        return None
    

def count_search(user, term, *unused):
    word_list = retrieve_tweets(user)
    if word_list == None:
        return
    countSearch = word_list.count(term)
    print(f'Number of times {user} tweeted {term}: {countSearch}')

def chart(user, keep_stopwords=0, num=None):
    word_list = retrieve_tweets(user)
    if word_list == None:
        return
    if not int(keep_stopwords):
        word_list = remove_stopwords(word_list)
    word_counter = collections.Counter(word_list)
    list_sz = num
    if num != None:
        list_sz = int(num)
    df = pd.DataFrame(word_counter.most_common(list_sz), columns=['word', 'count'])
    df.set_index('word', inplace=True)
    print(df)

def exit_program(*unused):
    print('program ending')
    exit()


def print_help(*unused):
    print('Program can either search a use for a word or chart out the most common words they tweet')
    print('Format for search is:')
    print("search 'twitter handle' 'search term'")
    print('ex: search elonmusk energy')
    print('Format for charting is:')
    print("chart 'twitter handle' optional: 0 to keep all words, 1 to remove stopwords, leaving empty will remove stopwords' 'optional: amount of results to display, leaving empty will print all'")
    print('ex: chart microsoft 1 10')
    print('Note: Order matters!')
    print("Also, type 'exit' to quit program")

func = {
    'search': count_search,
    'chart': chart,
    'exit': exit_program,
    'help': print_help
}
# --------------------------------------------------AUTHORIZING---------------------------------------------

# fill in twitter api auth data here
cons_key = ''
cons_secr = ''
access_tok = ''
access_secr = ''

auth = tw.OAuthHandler(cons_key, cons_secr)
auth.set_access_token(access_tok, access_secr)
api = tw.API(auth)

try: 
    test = api.home_timeline()
except tw.TweepError as e:
    print('Check authentication data')
    print(f'Error message: {e.response.text}')
    exit()

# --------------------------------------------------SEARCH---------------------------------------------
print('type help for commands')
print('input:')
while(1):
    user_input = input()
    input_list = user_input.lower().split()
    input_list.extend([None, True, None])
    # the extend is to assure the list is long enough, i don't really like this implementation but i can't think of a better way
    func[input_list[0]](input_list[1], input_list[2], input_list[3])
    print('input:')
#%%
