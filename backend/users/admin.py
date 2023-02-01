from django.contrib import admin
from .models import User, Subscription

admin.site.register(Subscription)


@admin.register(User)
class TagAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('username', 'email')
