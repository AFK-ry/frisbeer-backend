from django.contrib import admin
from django.contrib.admin.models import LogEntry
from frisbeer.models import *


class PlayerInGameInline(admin.TabularInline):
    model = GamePlayerRelation


class GameAdmin(admin.ModelAdmin):
    inlines = [PlayerInGameInline, ]

    def get_changeform_initial_data(self, request):
        return {'season': Season.current().id }


class PlayerInTeamInline(admin.TabularInline):
    model = TeamPlayerRelation


class TeamAdmin(admin.ModelAdmin):
    inlines = [PlayerInTeamInline]


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag']
    list_filter = ['action_time', 'user', 'action_flag']
    search_fields = ['user__username', 'object_repr', 'object_id']
    readonly_fields = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Player)
admin.site.register(Game, GameAdmin)
admin.site.register(GameRules)
admin.site.register(Location)
admin.site.register(Rank)
admin.site.register(Season)
admin.site.register(SeasonRules)
admin.site.register(Team, TeamAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
