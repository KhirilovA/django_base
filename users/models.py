import logging
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    timezone = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        if self.user.email is not None:
            return self.user.email
        return "Profile"

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None


class UserFriends(models.Model):
    user = models.ForeignKey(User, related_name='friendships_initiated', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friendships_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('blocked', 'Blocked')],
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} is friends with {self.friend} (Status: {self.status})"

    def accept(self):
        """Accept a pending friend request."""
        if self.status == 'pending':
            self.status = 'accepted'
            self.save()

    def block(self):
        """Block a friend."""
        self.status = 'blocked'
        self.save()


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    logger.debug(f"POST_SAVE.User create_profile: {instance}")
    if created:
        Profile.objects.create(user=instance)
