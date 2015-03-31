__author__ = 'maru'
import ConfigParser
from TwitterAPI import TwitterAPI
import sys
import json

def robust_request():
    pass


def connect(config):
    pass


def get_twitter(config_file):
    """ Read the config_file and construct an instance of TwitterAPI.
    Args:
      config_file ... A config file in ConfigParser format with Twitter credentials
    Returns:
      An instance of TwitterAPI.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    twitter = TwitterAPI(
        config.get('twitter', 'consumer_key'),
        config.get('twitter', 'consumer_secret'),
        config.get('twitter', 'access_token'),
        config.get('twitter', 'access_token_secret'))
    return twitter


def get_first_name(tweet):
    if 'user' in tweet and 'name' in tweet['user']:
        parts = tweet['user']['name'].split()
        if len(parts) > 0:
            return parts[0].lower()


def get_screen_name(tweet):
    if 'user' in tweet and 'name' in tweet['user']:
        parts = tweet['user']['scree_name']
        return parts


def sample_tweets(twitter, limit, gender, save=True, file_name=''):
    tweets = []
    while True:
        try:
            # Restrict to U.S.
            for response in twitter.request('statuses/filter',
                        {'locations':'-124.637,24.548,-66.993,48.9974'}):
                if 'user' in response:
                    name = get_first_name(response)
                    if gender.get_gender(name) in ['male', 'female']:
                        tweets.append(response)
                        if len(tweets) % 100 == 0:
                            print 'found %d tweets' % len(tweets)
                            if save:
                                save_tweets(file_name, tweets[-100:])
                        if len(tweets) >= limit:
                            return tweets
        except:
            print "Unexpected error:", sys.exc_info()[0]
    return tweets


def save_tweets(file_name, tweets):
    f = open(file_name, 'a')
    for t in tweets:
        tweet = json.dumps(t) + "\n"
        f.write(tweet)
    f.close()
    return True


def extract_users(list_tweets, gender, save=False, file_name=''):
    from collections import Counter
    names = Counter()

    users = []
    for tweet in list_tweets:
        uname =get_screen_name(tweet)
        fname = get_first_name(tweet)
        names.update(uname)
        gend = gender.get_gender(fname)
        users.append([uname, fname, gend])
        print uname, fname, gend

    if save:
        f=open(file_name, 'w')
        for user in users:
            if user[0] in names.elements():
                ## user name, first name, gender
                f.write("%s\t%s\t%s\n" % (user[0], user[1], user[2]))
                del names[user[0]]
        f.close()

def get_user_gender():
    # get config
    # get connection
    # Get genders
    # while limit
        # get random tweets
        # get users
        # get genders
        # save users

    pass

def main():
    import gender
    # gender = gender.UserGender('../../data/names/')
    gender = gender.UserGender(None)
    # print gender.get_gender('lllll')

    twitter = get_twitter('../twitter.cfg')

    tweets = sample_tweets(twitter, 5000, gender, save=True, file_name='gender_tweets.txt')

    extract_users(tweets, gender, save=True, file_name='gender_users.txt')

if __name__ == "__main__":
    main()