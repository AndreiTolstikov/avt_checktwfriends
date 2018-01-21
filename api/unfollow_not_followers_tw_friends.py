"""
Unfollow (destroy friendships in Twitter API)
the existing friends who aren't followers for Twitter account
"""
from django.conf import settings
import twitter
from .models import NotFollowerTwFriend

def unfollow_tw_friends():
    """
    1. Unfollow with Twitter API the existing friends who aren't followers,
       and have 'need_unfollow = True' field value
       from authenticated Twitter account (destroy friendships in Twitter API)
    2. Delete all unfollow friends as NotFollowerTwFriend objects from db

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

    # Get all NotFollowerTwFriend objects as queryset
    queryset = NotFollowerTwFriend.objects.all()

    # Get NotFollowerTwFriend objects
    # with 'need_unfollow=True'(not_follower_tw_friends for unfollow)
    # as filtered queryset
    queryset = queryset.filter(need_unfollow__exact=True)

    # Unfollow not_follower_tw_friends with 'need_unfollow = True' field value
    # from authenticated Twitter account
    # with DestroyFriendship(user_id=None, screen_name=None) method from 'python-twitter' lib
    # https://python-twitter.readthedocs.io/en/latest/twitter.html#twitter.api.Api.DestroyFriendship
    for need_unfollow_tw_friend in queryset:
        api.DestroyFriendship(int(need_unfollow_tw_friend.id_str))

    # delete NotFollowerTwFriend objects with 'need_unfollow = True' from db
    NotFollowerTwFriend.objects.filter(need_unfollow__exact=True).delete()

