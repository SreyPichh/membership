    # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, MemberType, Accommodation, Activity, UserPoint, BookingInfo, BookingActivity
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'email', 'phone', 'validation_img', 'created', 'updated')

class UserPointAdmin(admin.ModelAdmin):
    list_display = ('pid', 'ammount')

class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('aid', 'name', 'type')


admin.site.register(User, UserAdmin)
admin.site.register(MemberType)
admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(Activity)
admin.site.register(UserPoint, UserPointAdmin)
admin.site.register(BookingInfo)
admin.site.register(BookingActivity)
