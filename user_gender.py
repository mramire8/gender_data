__author__ = 'maru'


def robust_request():
    pass

def connect(config):
    pass


def get_config(config_file):
    pass

def name_gender(name):
    return None

def load_gender_files():
    pass


def extract_users(list_tweets):
    pass

def collect_tweets():
    pass

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
    g = gender.UserGender('../../data/names/')
    print g.get_gender('lllll')


if __name__ == "__main__":
    main()