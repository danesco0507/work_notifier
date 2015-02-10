__author__ = 'Daniel'
from django.conf.urls import patterns, include, url
from notifier import views

urlpatterns = patterns('',
    url(r'^$', views.import_excel_view, name='import_excel_view'),
    url(r'^(?P<work_id>\d+)/$', views.work_view, name='import_excel_view'),
    url(r'^acceptance/(?P<acceptance_token>\w+)/$', views.accept_view, name='accept_view'),
)