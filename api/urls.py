from django.conf.urls import url

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from . import views

schema_view = get_schema_view(title='avt_checktwfriends API schema')

urlpatterns = [

    # /api/v1/schema/
    # Return the explicitly defined schema view for automatically generated schema.
    url(
        r'^api/v1/schema/$',
        schema_view,
        name='get_api_schema'
    ),

    # /api/v1/docs/
    # Return the documentation page with automatically generated schema.
    # Generate schema with valid `request` instance.
    url(
        regex=r'^api/v1/docs/',
        view=include_docs_urls(title='avt_checktwfriends API docs', public=False),
        name='get_api_docs'
    ),

    # /api/v1/not_followers_tw_friends/
    # Return a list of all the existing Twitter friends who aren't followers
    # from local db.
    url(
        regex=r'^api/v1/not_followers_tw_friends/$',
        view=views.NotFollowersTwFriends.as_view(),
        name='get_not_followers_tw_friends'
    ),

    # /api/v1/not_followers_tw_friends/check/
    # Return an updated list(after check) of all the existing Twitter friends
    # who aren't followers.
    url(
        regex=r'^api/v1/not_followers_tw_friends/check/$',
        view=views.NotFollowersTwFriendsCheck.as_view(),
        name='get_not_followers_tw_friends_check'
    ),

    # /api/v1/not_followers_tw_friends/need_unfollow/
    # Return a list of all the existing Twitter friends who aren't followers
    # and selected for unfollow ('need_unfollow' field value is True).
    url(
        regex=r'^api/v1/not_followers_tw_friends/need_unfollow/$',
        view=views.NotFollowersTwFriendsNeedUnfollow.as_view(),
        name='get_not_followers_tw_friends_need_unfollow'
    ),

    # /api/v1/not_followers_tw_friends/
    # need_unfollow/update/tw_friend_screen_name/ need_unfollow=(True|False)
    #
    # Update 'need_unfollow' status for 'not_follower_tw_friend'
    # with 'screen_name=tw_friend_screen_name'
    url(
        regex=r'^api/v1/not_followers_tw_friends/need_unfollow/update/(?P<screen_name>[A-Za-z0-9_]+)/$',
        view=views.NotFollowersTwFriendsNeedUnfollowUpdate.as_view(),
        name='patch_not_followers_tw_friends_need_unfollow_update'
    ),

    # /api/v1/not_followers_tw_friends/unfollow/
    # Unfollow 'not_followers_tw_friends' with 'need_unfollow=True'
    # and return a list of all the existing Twitter friends
    # who aren't followers with 'need_unfollow=False'.
    url(
        regex=r'^api/v1/not_followers_tw_friends/unfollow/$',
        view=views.NotFollowersTwFriendsUnfollow.as_view(),
        name='delete_not_followers_tw_friends_unfollow'
    )
]
