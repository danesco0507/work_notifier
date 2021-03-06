from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import notifier
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'work_notifier.views.home', name='home'),
    # url(r'^work_notifier/', include('work_notifier.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^notifier/', include('notifier.urls')),

    url(r'^$', RedirectView.as_view(url='/notifier/')),
)
