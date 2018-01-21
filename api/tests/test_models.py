"""
Test module for NotFollowerTwFriend model
"""
from django.test import TestCase
from ..models import NotFollowerTwFriend

# Create your tests here.

class NotFollowerTwFriendTestCase(TestCase):
    """
    Test class for NotFollowerTwFriend model
    """
    def setUp(self):
        NotFollowerTwFriend.objects.create(
            id_str='123456789',
            screen_name='tw_user',
            name='Twitter User',
            created_at='Mon Jan 01 00:00:00 +0000 2018'
        )

    def test_create_not_follower_tw_friend(self):
        self.assertEqual(NotFollowerTwFriend.objects.count(), 1)
        self.assertEqual(NotFollowerTwFriend.objects.get().id_str, '123456789')
        self.assertEqual(NotFollowerTwFriend.objects.get().screen_name, 'tw_user')
        self.assertEqual(NotFollowerTwFriend.objects.get().name, 'Twitter User')
        self.assertEqual(NotFollowerTwFriend.objects.get().description, '')
        self.assertEqual(NotFollowerTwFriend.objects.get().statuses_count, 0)
        self.assertEqual(NotFollowerTwFriend.objects.get().followers_count, 0)
        self.assertEqual(NotFollowerTwFriend.objects.get().friends_count, 0)
        self.assertEqual(
            NotFollowerTwFriend.objects.get().created_at, 'Mon Jan 01 00:00:00 +0000 2018')
        self.assertEqual(NotFollowerTwFriend.objects.get().location, '')
        self.assertEqual(NotFollowerTwFriend.objects.get().avg_tweetsperday, 0.00)
        self.assertEqual(NotFollowerTwFriend.objects.get().tff_ratio, 0.00)
        self.assertEqual(NotFollowerTwFriend.objects.get().need_unfollow, True)
