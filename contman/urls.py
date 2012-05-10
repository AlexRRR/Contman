from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'contman.views.home', name='home'),
    # url(r'^contman/', include('contman.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^entry/$', 'content.views.sms_entrance'),
    url(r'^content/(?P<hash>\w+)/$', 'content.views.tempurl'),
    url(r'^reports/log/$', 'reports.views.show_log'),
    url(r'^reports/search/$', 'reports.views.search'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
