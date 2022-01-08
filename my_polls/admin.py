from django.contrib import admin
from .import models


class PollAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj):
        if obj is not None:
            return ('start_date', )
        else:
            return ()


admin.site.register(models.Poll, PollAdmin)
admin.site.register(models.Question)
admin.site.register(models.CustomPoll)
admin.site.register(models.RespondentAnswer)