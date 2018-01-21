from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import NotFollowerTwFriend
from .serializers import NotFollowerTwFriendSerializer
from .check_not_followers_tw_friends import check_tw_friends
from .unfollow_not_followers_tw_friends import unfollow_tw_friends

# Create your views here.

class NotFollowersTwFriends(generics.ListAPIView):
    """
    Return a list of all the existing Twitter friends who aren't followers.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = NotFollowerTwFriendSerializer

    def get_queryset(self):
        """
        Returns the queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.

        Returns:
            QuerySet object(s) -- Returning all NotFollowerTwFriend objects
                                  from this view.
        """
        queryset = NotFollowerTwFriend.objects.all()

        return queryset

    def list(self, request):
        """
        Return a list of all the existing Twitter friends who aren't followers as
        a Response object

        Arguments:
            request {Request} -- Not using

        Returns:
            Response object {TemplateResponse} -- Renders to content type (JSON)
            as requested by the client.
        """

        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = NotFollowerTwFriendSerializer(queryset, many=True)
        return Response(serializer.data)


class NotFollowersTwFriendsCheck(generics.ListAPIView):
    """
    Return an updated list(after check) of all the existing Twitter friends
    who aren't followers.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = NotFollowerTwFriendSerializer

    def get_queryset(self):
        """
        Returns the queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.

        Returns:
            QuerySet objects  -- Returning all NotFollowerTwFriend objects
                                 from this view.
        """
        queryset = NotFollowerTwFriend.objects.all()

        return queryset

    def list(self, request):
        """
        This method performs the following main tasks:
        1. Analysis with Twitter API the existing friends who aren't followers for Twitter account
        2. Count the average number of tweets per day
        3. Count the TFF Ratio (Twitter Follower-Friend Ratio)
        4. Synchronization (Create, Update, Destroy) the NotFollowerTwFriend objects

        Arguments:
            request {Request} -- Not using

        Returns:
            Response object {TemplateResponse} -- An updated list of
                                                the NotFollowerTwFriend objects
                                                who aren't followers
        """

        # 1. Analysis with Twitter API the existing friends who aren't followers for Twitter account
        # 2. Count the average number of tweets per day
        # 3. Count the TFF Ratio (Twitter Follower-Friend Ratio)
        # 4. Synchronization (Create, Update, Destroy) the NotFollowerTwFriend objects
        check_tw_friends()

        # 5. An updated list of the NotFollowerTwFriend objects who aren't followers.
        queryset = self.get_queryset()
        serializer = NotFollowerTwFriendSerializer(queryset, many=True)

        return Response(serializer.data)


class NotFollowersTwFriendsNeedUnfollow(generics.ListAPIView):
    """
    Return a list of all the existing Twitter friends who aren't followers
    and selected for unfollow ('need_unfollow' field value is True).
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = NotFollowerTwFriendSerializer
    lookup_field = 'screen_name'

    def get_queryset(self):
        """
        Returns the queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.

        Returns:
            QuerySet object(s) -- Returning NotFollowerTwFriend objects
                                  with 'need_unfollow=True'(not_follower_tw_friends for unfollow)
                                  as filtered queryset from this view
        """

        queryset = NotFollowerTwFriend.objects.all()
        queryset = queryset.filter(need_unfollow__exact=True)

        return queryset


    def list(self, request):
        """
        Return a list of all the existing Twitter friends who aren't followers
        and selected for unfollow ('need_unfollow' field value is True).

        Arguments:
            request {Request} -- Not using

        Returns:
            Response object {TemplateResponse} -- Renders to content type (JSON)
                                                    as requested by the client.
        """

        queryset = self.get_queryset()
        serializer = NotFollowerTwFriendSerializer(queryset, many=True)

        return Response(serializer.data)


class NotFollowersTwFriendsNeedUnfollowUpdate(generics.UpdateAPIView):
    """
    Update 'need_unfollow' field value for the specified Twitter friend who aren't follower
    """

    queryset = NotFollowerTwFriend.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = NotFollowerTwFriendSerializer
    lookup_field = 'screen_name'

    def partial_update(self, request, *args, **kwargs):
        """
        1. Get NotFollowerTwFriend object's instance with self.get_object() by
           lookup_field = 'screen_name'
        2. Validate and Partial Update serializer.data for getting instance
           with new 'need_unfollow' field value

        Arguments:
            request {Request object} -- request.data attribute handles data
                                        for 'need_unfollow' field value
            *args {[type]} -- not using
            **kwargs {[type]} -- not using

        Returns:
            Response object {TemplateResponse} -- Renders to content type (JSON)
                                as requested by the client.
                                Validated and Partial Updated serializer.data by
                                request.data (need_unfollow=(False|True))
        """

        # Get NotFollowerTwFriend object's instance
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotFollowersTwFriendsUnfollow(generics.DestroyAPIView):
    """
    Unfollow (destroy friendships in Twitter API) all the existing Twitter friends
    who aren't followers and selected for unfollow ('need_unfollow' field value is True).
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = NotFollowerTwFriendSerializer


    def get_queryset(self):
        """
        Returns the queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.

        Returns:
            QuerySet object(s) -- Returning NotFollowerTwFriend objects
                                    with 'need_unfollow=False'
                                    (not_followers_tw_friends for not unfollow)
                                    as filtered queryset from this view
        """

        queryset = NotFollowerTwFriend.objects.all()
        queryset = queryset.filter(need_unfollow__exact=False)

        return queryset


    def destroy(self, request, *args, **kwargs):
        """
        This method performs the following main tasks:
        1. Unfollow (destroy friendships in Twitter API) all the existing Twitter friends
           who aren't followers and selected for unfollow ('need_unfollow' field value is True).
        2. Delete(destroy) the appropriate NotFollowerTwFriend objects from db.

        Arguments:
            request {Request object} -- not used
            *args {[type]} -- not used
            **kwargs {[type]} -- not used

        Returns:
            Response object {TemplateResponse} -- All remaining after delete from db
                                                    NotFollowerTwFriend objects
                                                    with 'need_unfollow=False'
                                                    (not_followers_tw_friends for not unfollow)
                                                    as serializer.data
        """

        # 1. Unfollow with Twitter API the existing friends who aren't followers,
        #    and have 'need_unfollow = True' field value
        #    from authenticated Twitter account (destroy friendships in Twitter API)
        # 2. Delete all unfollow friends as NotFollowerTwFriend objects from db
        unfollow_tw_friends()

        # All remaining after delete from db NotFollowerTwFriend objects
        # with 'need_unfollow=False'
        queryset = self.get_queryset()
        serializer = NotFollowerTwFriendSerializer(queryset, many=True)

        return Response(serializer.data)
