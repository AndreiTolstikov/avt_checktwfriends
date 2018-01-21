"""
Test module for views
"""
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from ..models import NotFollowerTwFriend
from ..serializers import NotFollowerTwFriendSerializer


# Create your tests here.

# initialize the APIClient
client = APIClient()

# list for store NotFollowerTwFriend objects data between Test Cases
not_followers_tw_friends_list = list()


class NotAutorizedAccessTestCase(APITestCase):
    """
    Test that the API has user authorization.
    """

    def test_get_not_autorized_access(self):
        # initialize the APIClient for this TestCase
        not_auth_client = APIClient()

        # get API response
        response = not_auth_client.get(reverse('get_api_schema'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ObtainAuthTokenTestCase(APITestCase):
    """
    Test to obtain API authentication token
    """

    def setUp(self):
        # Create User object
        # NOTE: Only for testing purposes
        user = User.objects.create_user(
            username='test_user',
            email='support@anymail.com',
            password='top_secret'
        )

        # To bypass authentication entirely and force all requests
        # by the test client to be automatically treated as authenticated.
        # NOTE: Only for testing purposes
        client.force_authenticate(user=user)


    def test_post_obtain_auth_token(self):
        # Get the url for API response
        url = reverse('api-token')

        # Username and password for User object,
        # creating for testing with setUp()
        user_auth_data = {'username':'test_user', 'password':'top_secret'}

        # Get API response
        response = client.post(url, user_auth_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AutomaticallyGeneratedAPISchemaTestCase(APITestCase):
    """
    Test the API which return the explicitly defined schema view
    for automatically generated schema.
    """

    def setUp(self):
        # Create User object
        # NOTE: Only for testing purposes
        user = User.objects.create_user(
            username='test_user',
            email='support@anymail.com',
            password='top_secret'
        )

        # Token authentication example for this TestCase,
        # NOTE: Only for testing purposes.
        # Instead client.force_authenticate(user=user)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_automatically_generated_api_schema(self):
        # get API response
        response = client.get(reverse('get_api_schema'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIDocumentationTestCase(APITestCase):
    """
    Test the API which return the documentation page
    with automatically generated schema.
    """

    def setUp(self):
        # Create User object
        # NOTE: Only for testing purposes
        user = User.objects.create_user(
            username='test_user',
            email='support@anymail.com',
            password='top_secret'
        )

        # To bypass authentication entirely and force all requests
        # by the test client to be automatically treated as authenticated.
        # NOTE: Only for testing purposes
        client.force_authenticate(user=user)

    def test_get_api_documentation(self):
        # Get API response
        response = client.get('/api/v1/docs/', format='html')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotFollowersTwFriendsTestCase(APITestCase):
    """
    Test the API which return a list of all the existing Twitter friends
    who aren't followers
    """

    def setUp(self):
        # Create NotFollowerTwFriend objects
        # for testing purposes
        NotFollowerTwFriend.objects.create(
            id_str='1',
            screen_name='tw_user_1',
            name='Twitter User #1',
            description='I want to have many new followers and friends on Twitter',
            created_at='Mon Jan 01 00:00:00 +0000 2018'
        )

        NotFollowerTwFriend.objects.create(
            id_str='2',
            screen_name='tw_user_2',
            name='Twitter User #2',
            description='I want to have many new followers and friends on Twitter',
            created_at='Mon Jan 01 00:00:00 +0000 2018'
        )

        NotFollowerTwFriend.objects.create(
            id_str='3',
            screen_name='tw_user_3',
            name='Twitter User #3',
            description='I want to have many new followers and friends on Twitter',
            created_at='Mon Jan 01 00:00:00 +0000 2018'
        )

        # Create User object
        # NOTE: Only for testing purposes
        user = User.objects.create_user(
            username='test_user',
            email='support@anymail.com',
            password='top_secret'
        )

        # To bypass authentication entirely and force all requests
        # by the test client to be automatically treated as authenticated.
        # NOTE: Only for testing purposes
        client.force_authenticate(user=user)

    def test_get_all_not_followers_tw_friends(self):
        # Get API response
        response = client.get(reverse('get_not_followers_tw_friends'))

        # Get all NotFollowerTwFriend objects as queryset
        queryset = NotFollowerTwFriend.objects.all()
        serializer = NotFollowerTwFriendSerializer(queryset, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotFollowersTwFriendsCheckTestCase(APITestCase):
    """
    Test the API which return an updated list(after check) of all
    the existing Twitter friends who aren't followers.
    """

    def setUp(self):
        # Create User object
        # NOTE: Only for testing purposes
        user = User.objects.create_user(
            username='test_user',
            email='support@anymail.com',
            password='top_secret'
        )

        # To bypass authentication entirely and force all requests
        # by the test client to be automatically treated as authenticated.
        # NOTE: Only for testing purposes
        client.force_authenticate(user=user)

    def test_check_not_followers_tw_friends(self):
        # Get API response
        response = client.get(reverse('get_not_followers_tw_friends_check'))

         # Get all NotFollowerTwFriend objects as queryset
        queryset = NotFollowerTwFriend.objects.all()

        # Create 'not_followers_tw_friends_list' with
        # NotFollowerTwFriend objects
        for not_follower_tw_friend in queryset:
            not_followers_tw_friends_list.append(not_follower_tw_friend)

        serializer = NotFollowerTwFriendSerializer(queryset, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotFollowersTwFriendsNeedUnfollowTestCase(APITestCase):
    """
    Test the API which return a list of all the existing Twitter friends who aren't followers
    and selected for unfollow ('need_unfollow' field value is True).
    """

    def setUp(self):
        # Create NotFollowerTwFriend objects from
        # 'not_followers_tw_friends_list'
        # which store all data between Test Cases
        for not_follower_tw_friend in not_followers_tw_friends_list:
            NotFollowerTwFriend.objects.create(
                id_str=not_follower_tw_friend.id_str,
                screen_name=not_follower_tw_friend.screen_name,
                name=not_follower_tw_friend.name,
                description=not_follower_tw_friend.description,
                statuses_count=not_follower_tw_friend.statuses_count,
                followers_count=not_follower_tw_friend.followers_count,
                friends_count=not_follower_tw_friend.friends_count,
                created_at=not_follower_tw_friend.created_at,
                location=not_follower_tw_friend.location,
                avg_tweetsperday=not_follower_tw_friend.avg_tweetsperday,
                tff_ratio=not_follower_tw_friend.tff_ratio,
                need_unfollow=not_follower_tw_friend.need_unfollow
            )

        # Create User object
        # NOTE: Only for testing purposes
        user = User.objects.create_user(
            username='test_user',
            email='support@anymail.com',
            password='top_secret'
        )

        # To bypass authentication entirely and force all requests
        # by the test client to be automatically treated as authenticated.
        # NOTE: Only for testing purposes
        client.force_authenticate(user=user)


    def test_get_not_followers_tw_friends_need_unfollow(self):
        # Get API response
        response = client.get(reverse('get_not_followers_tw_friends_need_unfollow'))

        # Get all NotFollowerTwFriend objects as queryset
        not_followers_tw_friends_qset = NotFollowerTwFriend.objects.all()

        # Get NotFollowerTwFriend objects with 'need_unfollow=True'
        # (not_follower_tw_friends for unfollow)
        # as filtered queryset
        need_unfollow_tw_friends_qset = \
            not_followers_tw_friends_qset.filter(need_unfollow__exact=True)

        self.assertEqual(len(not_followers_tw_friends_qset), len(need_unfollow_tw_friends_qset))

        serializer = NotFollowerTwFriendSerializer(need_unfollow_tw_friends_qset, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotFollowersTwFriendsNeedUnfollowUpdateTestCase(APITestCase):
    """
    Test the API which update need_unfollow status for not_follower_tw_friend
    from 'not_unfollow_tw_friends_screen_name_list' with 'need_unfollow=False'
    (all the existing Twitter friends who aren't followers and not selected for unfollow)
    """

    # A test list that contains 'screen_names' of all the existing Twitter friends
    # who aren't followers and not selected for unfollow.
    # NOTE: To successfully run the test, you need specify
    # the screen names of REAL Twitter users.
    not_unfollow_tw_friends_screen_name_list = [
        '<real_tw_user_screen_name_1 from your account>',
        '<real_tw_user_screen_name_2 from your account>',
        '<real_tw_user_screen_name_3 from your account>',
        '<...>',
        '<real_tw_user_screen_name_N from your account>'
    ]

    def setUp(self):
        # Create NotFollowerTwFriend objects from
        # 'not_followers_tw_friends_list'
        # which store all data between Test Cases
        for not_follower_tw_friend in not_followers_tw_friends_list:
            NotFollowerTwFriend.objects.create(
                id_str=not_follower_tw_friend.id_str,
                screen_name=not_follower_tw_friend.screen_name,
                name=not_follower_tw_friend.name,
                description=not_follower_tw_friend.description,
                statuses_count=not_follower_tw_friend.statuses_count,
                followers_count=not_follower_tw_friend.followers_count,
                friends_count=not_follower_tw_friend.friends_count,
                created_at=not_follower_tw_friend.created_at,
                location=not_follower_tw_friend.location,
                avg_tweetsperday=not_follower_tw_friend.avg_tweetsperday,
                tff_ratio=not_follower_tw_friend.tff_ratio,
                need_unfollow=not_follower_tw_friend.need_unfollow
            )

        # Create User object
        # NOTE: Only for testing purposes
        user = User.objects.create_user(
            username='test_user',
            email='support@anymail.com',
            password='top_secret'
        )

        # To bypass authentication entirely and force all requests
        # by the test client to be automatically treated as authenticated.
        # NOTE: Only for testing purposes
        client.force_authenticate(user=user)


    def test_patch_not_followers_tw_friends_need_unfollow_update(self):
        # Get all NotFollowerTwFriend objects as queryset
        queryset = NotFollowerTwFriend.objects.all()

        # update need_unfollow status (need_unfollow=False) for not_follower_tw_friend
        # with 'screen_name' from not_unfollow_tw_friends_screen_name_list
        for not_follower_tw_friend in queryset:
            if not_follower_tw_friend.screen_name in self.not_unfollow_tw_friends_screen_name_list:
                url = reverse(
                    'patch_not_followers_tw_friends_need_unfollow_update',
                    kwargs={'screen_name': not_follower_tw_friend.screen_name}
                )
                update_data = {'need_unfollow': False}

                # Get API response
                response = client.patch(url, update_data)

                self.assertEqual(NotFollowerTwFriend.objects.get(
                    screen_name=not_follower_tw_friend.screen_name).need_unfollow, False)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update 'not_followers_tw_friends_list' as following:

        # 1. Get all NotFollowerTwFriend objects as updated queryset
        updated_queryset = NotFollowerTwFriend.objects.all()

        # 2. Delete all items from the 'not_followers_tw_friends_list'
        not_followers_tw_friends_list.clear()

        # 3. Append the NotFollowerTwFriend list items with updated 'need_unfollow' field values
        for not_follower_tw_friend in updated_queryset:
            not_followers_tw_friends_list.append(not_follower_tw_friend)


class NotFollowersTwFriendsUnfollowTestCase(APITestCase):
    """
    Test the API which delete of all the existing Twitter friends who aren't followers,
    and selected for unfollow ('need_unfollow' field value is True).
    """

    def setUp(self):
        # Create NotFollowerTwFriend objects from
        # 'not_followers_tw_friends_list'
        # which store all data between Test Cases
        for not_follower_tw_friend in not_followers_tw_friends_list:
            NotFollowerTwFriend.objects.create(
                id_str=not_follower_tw_friend.id_str,
                screen_name=not_follower_tw_friend.screen_name,
                name=not_follower_tw_friend.name,
                description=not_follower_tw_friend.description,
                statuses_count=not_follower_tw_friend.statuses_count,
                followers_count=not_follower_tw_friend.followers_count,
                friends_count=not_follower_tw_friend.friends_count,
                created_at=not_follower_tw_friend.created_at,
                location=not_follower_tw_friend.location,
                avg_tweetsperday=not_follower_tw_friend.avg_tweetsperday,
                tff_ratio=not_follower_tw_friend.tff_ratio,
                need_unfollow=not_follower_tw_friend.need_unfollow
            )

        # Create User object
        # NOTE: Only for testing purposes
        user = User.objects.create_user(
            username='test_user',
            email='support@anymail.com',
            password='top_secret'
        )

        # To bypass authentication entirely and force all requests
        # by the test client to be automatically treated as authenticated.
        # NOTE: Only for testing purposes
        client.force_authenticate(user=user)

    def test_delete_not_followers_tw_friends_unfollow(self):

        # Get all NotFollowerTwFriend objects as queryset
        not_followers_tw_friends_qset = NotFollowerTwFriend.objects.all()

        # Get NotFollowerTwFriend objects
        # with 'need_unfollow=True'
        # (ready to unfollow) as queryset
        need_unfollow_tw_friends_qset = \
            not_followers_tw_friends_qset.filter(need_unfollow__exact=True)

        # get 'not_followers_tw_friends' with 'need_unfollow=False'
        # Get NotFollowerTwFriend objects
        # with 'need_unfollow=False'
        # (not for unfollow) as queryset
        not_unfollow_tw_friends_qset = \
            not_followers_tw_friends_qset.filter(need_unfollow__exact=False)

        # If there are no 'not_followers_tw_friends' marked for unfollow,
        # then assertEqual() will be True
        len_need_unfollow_tw_friends_qset = len(need_unfollow_tw_friends_qset)
        if len_need_unfollow_tw_friends_qset == 0:
            self.assertEqual(len(not_followers_tw_friends_qset), len(not_unfollow_tw_friends_qset))
        else:
            self.assertNotEqual(
                len(not_followers_tw_friends_qset), len(not_unfollow_tw_friends_qset))

        # Get API response
        response = client.delete(reverse('delete_not_followers_tw_friends_unfollow'))

        serializer = NotFollowerTwFriendSerializer(not_unfollow_tw_friends_qset, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
