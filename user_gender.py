__author__ = 'maru'
import ConfigParser
from TwitterAPI import TwitterAPI
import sys
import json
import time


def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request.
      params ..... A parameter dictionary for the request.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        elif request.status_code == 404 or request.status_code == 34 or "Not authorized" in request.text:
            return None
        else:
            print >> sys.stderr, 'Got error:', request.text, '\nsleeping for 15 minutes.'
            sys.stderr.flush()
            time.sleep(60 * 15)


def get_user_timeline(user_id, twitter):
    """ Return Twitter screen names for all accounts followed by screen_name. Returns the first 200 users.
    See docs at: https://dev.twitter.com/docs/api/1.1/get/friends/list
    Args:
      user_id ... The query account.
      twitter ....... The TwitterAPI object.
    Returns:
      A list of Twitter screen names.
    """

    parameters = {'screen_name': user_id, 'count': 200, 'contributor_details': True}
    # get list of friends aka following accounts.


    timeline = []

    finished = False
    max_id = 0
    since = 0
    empty = False
    request = None

    while not empty: ## the 3200 limits returns a valid request with an empty iterator
        ids = []
        request = robust_request(twitter, 'statuses/user_timeline',
                                 parameters, max_tries=5)

        if validate_request(request):  # if I didnt get an error
            empty = True
            ids = []
            for r in request.get_iterator(): # get all tweets
                empty = False
                if 'user' in r:
                    timeline.append(r)
                    ids.append(r['id'])
            if len(ids) > 0:  ##  save ids
                # since = max(since, max(ids))
                # max_id = min(ids) - 1
                since = ids[-1]
                max_id = ids[0]
        parameters['since_id'] = since
        parameters['max_id'] = max_id

    return timeline


def get_all_timeline():
    pass


def collect_timeline(user, gender, twitter, output):

    import os
    timeline = get_user_timeline(user, twitter)

    output_name = output + "/" + gender + "/" + user + ".txt"
    if not os.path.exists(output_name):
        os.makedirs(output + "/" + gender + "/")

    f = open(output_name, 'w')
    for t in timeline:
        s = "%s\n" % json.dumps(t)
        f.write(s)
    f.close()


def create_dataset(users, twitter, output_dir):

    for i, user in enumerate(users):
        print "user: %s" % i
        collect_timeline(user[0], user[2], twitter)


def validate_request(request):
    if request is None:
        return False
    elif 'errors' in request:
        return False
    else:
        return True


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
        parts = tweet['user']['screen_name']
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
        names.update([uname])
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

    return users


def load_tweet_file(file_name):
    import json
    f = open(file_name)
    with f:
        lines = f.readlines()

    tweets = []
    for line in lines:
        tweets.append(json.loads(line))
    return tweets


def load_users_file(file_name):
    f = open(file_name)
    with f:
        lines = f.readlines()

    users = [l.split("\t") for l in lines]

    return users


def main():
    import gender
    # gender = gender.UserGender('../../data/names/')
    gender = gender.UserGender(None)
    # print gender.get_gender('lllll')

    twitter = get_twitter('../twitter.cfg')

    # tweets = sample_tweets(twitter, 5000, gender, save=True, file_name='gender_tweets.txt')
    tweets = load_tweet_file('gender_tweets.txt')

    # users = extract_users(tweets, gender, save=True, file_name='gender_users.txt')
    users = load_users_file('gender_users.txt')

    # create_dataset(users, tweets, "./data")

    tm = get_user_timeline('jessstumpf', twitter)

if __name__ == "__main__":
    main()