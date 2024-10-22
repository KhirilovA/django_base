from django.contrib import admin

from users.models import UserFriends, Profile


admin.site.register([UserFriends, Profile])
