from django.contrib import admin
from .models import RobloxProject, codeScan,securityIssue

admin.site.register(RobloxProject)
admin.site.register(codeScan)
admin.site.register(securityIssue)
