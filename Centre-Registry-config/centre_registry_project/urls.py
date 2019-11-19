from centre_registry import views_api
from centre_registry import views_ui
from django.conf import settings
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

admin.autodiscover()
admin.site.site_header = settings.ADMIN_TITLE

urlpatterns = patterns(  # pylint: disable=invalid-name
    '',
    url(r'^admin/', include(admin.site.urls)),

    # REST API v1.
    url(r'^restxml/$', views_api.get_all_centres),
    url(r'^restxml/(?P<centre_id>\d+)[/]?$', views_api.get_centre),

    # REST API v2.
    url(r'^api/KML/(?P<types>([A-Z]){0,6})$', views_api.get_centres_kml),
    url(r'^api/model/(?P<model>\S+)$', views_api.get_model),

    # UI views.
    url(r'^$', views_ui.get_all_centres),
    url(r'^centre/(?P<centre_id>\d+)$', views_ui.get_centre),
    url(r'^all_centres$', views_ui.get_all_centres),
    url(r'^about$', views_ui.get_about),
    url(r'^contacting$', views_ui.get_contacting),
    url(r'^contact/(?P<contact_id>\d+)$', views_ui.get_contact),
    url(r'^centres_contacts$', views_ui.get_centres_contacts),
    url(r'^consortia$', views_ui.get_consortia),
    url(r'^fcs$', views_ui.get_fcs),
    url(r'^map', views_ui.get_map),
    url(r'^oai_pmh$', views_ui.get_oai_pmh),
    url(r'^spf$', views_ui.get_spf), )
