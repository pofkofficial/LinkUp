from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Event)
admin.site.register(Flags)
admin.site.register(FlagRequest)
admin.site.register(OrgStatus)
admin.site.register(OrganizersRq)
admin.site.register(RelationRq)
admin.site.register(Steeze)
admin.site.register(SteezeCom)
admin.site.register(SteezeLikes)
admin.site.register(Userprofile)
admin.site.register(VerificationRq)
admin.site.register(VerificationStatus)
"""
# For Userprofile, you might want to show linked fields in the admin
class UserprofileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'username', 'fname', 'sname', 'dob']
    search_fields = ['user__username', 'phone', 'username', 'fname', 'sname']

admin.site.register(Userprofile, UserprofileAdmin)"""