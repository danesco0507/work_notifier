__author__ = 'Daniel'

from django.contrib import admin
from notifier.models import Work, Affected, WorkPlan, ContingencyPlan, Acceptance, Client, ClientEmail


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