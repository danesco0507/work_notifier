__author__ = 'Daniel'

from django.contrib import admin
from notifier.models import *


class ClientEmailInline(admin.StackedInline):
    model = ClientEmail
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientEmailInline]

admin.site.register(WorkPlan)
admin.site.register(Work)
admin.site.register(Affected)
admin.site.register(ContingencyPlan)
admin.site.register(Acceptance)
admin.site.register(Client, ClientAdmin)
admin.site.register(Area)
admin.site.register(Department)
admin.site.register(Municipality)
admin.site.register(Impact)
admin.site.register(Cause)
admin.site.register(WorkGroup)