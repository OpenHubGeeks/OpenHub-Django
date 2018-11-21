from django.contrib import admin

from .models import RepoDetails, Contributors


class RepoAdmin(admin.ModelAdmin):
    pass


class ContributorAdmin(admin.ModelAdmin):
    pass

admin.site.register(RepoDetails, RepoAdmin)
admin.site.register(Contributors, ContributorAdmin)
