from django.contrib import admin

from dates.models import User, Follower


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass
