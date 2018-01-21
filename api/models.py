from django.db import models

# Create your models here.
class NotFollowerTwFriend(models.Model):
    '''
    Model for Twitter friend who aren't follower
    '''

    id_str = models.CharField(max_length=25, unique=True, primary_key=True)
    screen_name = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=25)
    description = models.TextField(default='')
    statuses_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    friends_count = models.PositiveIntegerField(default=0)
    created_at = models.CharField(max_length=50)
    location = models.CharField(max_length=100, default='')
    avg_tweetsperday = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tff_ratio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    need_unfollow = models.BooleanField(default=True)

    def __str__(self):
        return self.id_str
