from rest_framework import serializers

from .models import NotFollowerTwFriend

class NotFollowerTwFriendSerializer(serializers.ModelSerializer):
    ''' Serializer for NotFollowerTwFriend Model'''
    
    class Meta:
        model = NotFollowerTwFriend
        fields = ['id_str', 'screen_name', 'name', 'description', 'statuses_count',\
            'followers_count', 'friends_count', 'created_at', 'location', \
            'avg_tweetsperday', 'tff_ratio', 'need_unfollow']