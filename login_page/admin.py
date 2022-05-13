from django.contrib import admin
from .models import *

admin.site.register(Q_A)
admin.site.register(multiple_choices)
admin.site.register(interview_info)




# -----------------------
# https://stackoverflow.com/questions/37618473/how-can-i-log-both-successful-and-failed-login-and-logout-attempts-in-django

@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip', 'time',]
    list_filter = ['action',]

# -----------------------