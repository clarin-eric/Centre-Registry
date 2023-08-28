from centre_registry import views_api
from centre_registry import views_ui
from django.conf import settings
from django.contrib import admin
from django.urls import re_path

admin.autodiscover()
admin.site.site_header = settings.ADMIN_TITLE

urlpatterns = [  # pylint: disable=invalid-name
    re_path(r'admin/', admin.site.urls),

    # REST API v1.
    re_path(r'^restxml/$', views_api.get_all_centres),
    re_path(r'^restxml/(?P<centre_id>\d+)[/]?$', views_api.get_centre),

    # REST API v2.
    re_path(r'^api/KML/(?P<types>([A-Z]){0,6})$', views_api.get_centres_kml),
    re_path(r'^api/model/(?P<model>\S+)$', views_api.get_model),

    # UI views.
    re_path(r'^$', views_ui.get_all_centres),
    re_path(r'^centre/(?P<centre_id>\d+)$', views_ui.get_centre),
    re_path(r'^all_centres$', views_ui.get_all_centres),
    re_path(r'^all_kcentres$', views_ui.get_all_kcentres),
    re_path(r'^about$', views_ui.get_about),
    re_path(r'^contacting$', views_ui.get_contacting),
    re_path(r'^contact/(?P<contact_id>\d+)$', views_ui.get_contact),
    re_path(r'^centres_contacts$', views_ui.get_centres_contacts),
    re_path(r'^consortia$', views_ui.get_consortia),
    re_path(r'^fcs$', views_ui.get_fcs),
    re_path(r'^map', views_ui.get_map),
    re_path(r'^oai_pmh$', views_ui.get_oai_pmh),
    re_path(r'^spf$', views_ui.get_spf),
    ]
