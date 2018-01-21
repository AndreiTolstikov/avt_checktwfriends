"""
    1. Analysis with Twitter API the existing friends who aren't followers for Twitter account
    2. Count the average number of tweets per day
    3. Count the TFF Ratio (Twitter Follower-Friend Ratio)
    4. Synchronization (Create, Update, Destroy) the NotFollowerTwFriend objects
"""
from datetime import datetime, date
from django.conf import settings
import twitter
from .models import NotFollowerTwFriend


def count_avg_tweets_per_day(tw_account):
    """
    Count the average number of tweets per day
    that were created by the 'tw_account'.
    For the whole period from the moment of creation of his account until today.

    1. From Twitter developer docs:
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
    Tweet data dictionaries -> User Object -> User Data Dictionary
    Attribute	    Type    Description
    created_at 	String 	The UTC datetime that the user account was
                    created on Twitter.
    Example: "created_at": "Mon Nov 29 21:18:15 +0000 2010"

    2. From Python developer docs:
    https://docs.python.org/3/library/datetime.html?highlight=date#module-datetime
    classmethod datetime.strptime(date_string, format)
    Return a datetime corresponding to date_string,
    parsed according to format.
    This is equivalent to datetime(*(time.strptime(date_string, format)[0:6])).
    ValueError is raised if the date_string and format can’t be parsed
    by time.strptime() or if it returns a value which isn’t a time tuple.
    For a complete list of formatting directives,
    see strftime() and strptime() Behavior.
    8.1.8. strftime() and strptime() Behavior
    https://docs.python.org/3/library/datetime.html?highlight=date#strftime-strptime-behavior
    >>> # Using datetime.strptime()
    >>> dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
    >>> dt
    datetime.datetime(2006, 11, 21, 16, 30)

    Arguments:
        tw_account {twitter.User object} -- The following fields are used:
                                            created_at
                                            statuses_count

    Returns:
        float -- The average number of tweets per day
    """

    # Get a current data
    today = date.today()
    num_days_1 = today.toordinal()

    # Date of account creation in Twitter
    tw_account_created_at_dt = datetime.strptime(
        tw_account.created_at, '%a %b %d %H:%M:%S %z %Y')
    num_days_2 = tw_account_created_at_dt.toordinal()

    # The lifetime of a Twitter account in days
    tw_account_lifetime_days = num_days_1 - num_days_2

    # The average number of tweets per day
    avg_tweets_per_day = tw_account.statuses_count / tw_account_lifetime_days
    avg_tweets_per_day = round(avg_tweets_per_day, 2)

    return avg_tweets_per_day

def count_tw_tff_ratio(tw_account):
    """
    Count the TFF Ratio (Twitter Follower-Friend Ratio)
    TFF Ratio (Twitter Follower-Friend Ratio) is the ratio
    of your followers to friends (or people who you follow).
    Info about TFF Ratio get from http://tffratio.com/

    Arguments:
        tw_account {twitter.User object} -- The following fields are used:
                                            followers
                                            friends

    Returns:
        float -- TFF Ratio (Twitter Follower-Friend Ratio)
        string -- TFF Ratio description
    """
    try:
        tw_tff_ratio = tw_account.followers_count / tw_account.friends_count
    except ZeroDivisionError:
        tw_tff_ratio = 0.00
    finally:
        tw_tff_ratio = round(tw_tff_ratio, 2)

    return tw_tff_ratio

def get_not_unfollow_tw_friend_ids():
    """
    Return list of the all friends who aren't followers
    with 'need_unfollow=False' (list of exceptions for unfollow).

    Arguments:
        None

    Returns:
        list -- the all friends who aren't followers with 'need_unfollow=False'
    """

    # Get all NotFollowerTwFriend objects as queryset
    queryset = NotFollowerTwFriend.objects.all()

    # Get NotFollowerTwFriend objects
    # with 'need_unfollow=False'(not_follower_tw_friends not for unfollow)
    # as filtered queryset
    queryset = queryset.filter(need_unfollow__exact=False)

    not_unfollow_tw_friend_ids_lst = []
    for not_unfollow_tw_friend in queryset:
        not_unfollow_tw_friend_ids_lst.append(int(not_unfollow_tw_friend.id_str))

    return not_unfollow_tw_friend_ids_lst


def check_tw_friends():
    """
    1. Analysis with Twitter API the existing friends who aren't followers for Twitter account
    2. Count the average number of tweets per day
    3. Count the TFF Ratio (Twitter Follower-Friend Ratio)
    4. Synchronization (Create, Update, Destroy) the NotFollowerTwFriend objects

    Arguments:
        None
    """

    # Create a Twitter Api instance.
    api = twitter.Api(
        consumer_key=settings.CONSUMER_KEY,
        consumer_secret=settings.CONSUMER_SECRET,
        access_token_key=settings.ACCESS_TOKEN,
        access_token_secret=settings.ACCESS_TOKEN_SECRET
    )

    # Initialize variables for analysis not follower (useless) friends(followings)
    # for Twitter account
    next_cursor = -1
    users_per_page = 100
    not_followers_tw_friends_list = []
    not_follower_tw_friend_ids_list = []
    not_unfollow_tw_friend_ids_lst = get_not_unfollow_tw_friend_ids()

    # Get follower IDs list for Twitter account
    follower_ids_list = api.GetFollowerIDs()

    # Start analysis not follower friends(followings) for Twitter account
    while next_cursor != 0:
        friends_paged_t = api.GetFriendsPaged(cursor=next_cursor, count=users_per_page)

        # Analyze friends from next paged cursor
        for friend in friends_paged_t[2]:

            # If a friend is not a follower, then add it to the database
            if friend.id not in follower_ids_list:

                # Count the average number of tweets per day for Twitter Account
                average_tweets_per_day = count_avg_tweets_per_day(friend)

                # Count TFF Ratio (Twitter Follower-Friend Ratio) for Twitter Account
                tw_follower_friend_ratio = count_tw_tff_ratio(friend)

                # If 'not_follower_tw_friend' with 'need_unfollow=False'
                # (not_followers_tw_friends for not unfollow)
                # already has in db
                if friend.id in not_unfollow_tw_friend_ids_lst:
                    # Create a new NotFollowerTwFriend object with
                    # explicit field value 'need_unfollow=False'
                    not_follower_tw_friend = NotFollowerTwFriend(
                        id_str=friend.id,
                        screen_name=friend.screen_name,
                        name=friend.name,
                        description=friend.description,
                        statuses_count=friend.statuses_count,
                        followers_count=friend.followers_count,
                        friends_count=friend.friends_count,
                        created_at=friend.created_at,
                        location=friend.location,
                        avg_tweetsperday=average_tweets_per_day,
                        tff_ratio=tw_follower_friend_ratio,
                        need_unfollow=False,
                    )
                # else if 'not_follower_tw_friend'
                # with 'need_unfollow=False'
                # (not_followers_tw_friends for not unfollow)
                # is absent in db
                else:
                    # Create a new NotFollowerTwFriend object with
                    # implicit default field value 'need_unfollow=True'
                    not_follower_tw_friend = NotFollowerTwFriend(
                        id_str=friend.id,
                        screen_name=friend.screen_name,
                        name=friend.name,
                        description=friend.description,
                        statuses_count=friend.statuses_count,
                        followers_count=friend.followers_count,
                        friends_count=friend.friends_count,
                        created_at=friend.created_at,
                        location=friend.location,
                        avg_tweetsperday=average_tweets_per_day,
                        tff_ratio=tw_follower_friend_ratio,
                    )
                # add 'not_follower_tw_friend' object to 'not_followers_tw_friends_list'
                not_followers_tw_friends_list.append(not_follower_tw_friend)
                not_follower_tw_friend_ids_list.append(not_follower_tw_friend.id_str)

        # set new value for next paged cursor
        next_cursor = friends_paged_t[0]

    # Get all NotFollowerTwFriend objects as queryset
    queryset = NotFollowerTwFriend.objects.all()
    queryset_len = len(queryset)
    if queryset_len == 0:
        # db is empty
        # need to create new records
        for not_follower_tw_friend in not_followers_tw_friends_list:
            not_follower_tw_friend.save()
    else:
        # db is not empty
        # need to synchronize records from the db
        # with 'not_followers_tw_friends_list'

        # SYNC_STEP_1
        # deleting all records from the db,
        # in which 'id_str' is not in the 'not_follower_tw_friend_ids_list'
        for not_follower_tw_friend in queryset:
            if not_follower_tw_friend.id_str not in not_follower_tw_friend_ids_list:
                NotFollowerTwFriend.objects.filter(
                    id_str__exact=not_follower_tw_friend.id_str).delete()

        # SYNC_STEP_2
        # create and update all records in the db
        # with objects from 'not_followers_tw_friends_list'
        for not_follower_tw_friend in not_followers_tw_friends_list:
            not_follower_tw_friend.save()
