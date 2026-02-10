from centre_registry import views_api
from centre_registry import views_ui
from django.urls import include, re_path
from django.conf import settings
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularJSONAPIView

admin.autodiscover()
admin.site.site_header = settings.ADMIN_TITLE

urlpatterns = [  # pylint: disable=invalid-name
    path('admin/', admin.site.urls),
    re_path(r'^api/(?:v1/)?schema/openapi.json', SpectacularJSONAPIView.as_view()),

    # REST API.
    re_path(r'^restxml/(?:v1/)?$', views_api.get_all_centres),
    re_path(r'^restxml/(?:v1/)?(?P<centre_id>\d+)[/]?$', views_api.get_centre),

    # JSON API.
    re_path(r'^api/(?:v1/)?KML/(?P<types>([A-Z]){0,6})$', views_api.get_centres_kml),
    re_path(r'^api/(?:v1/)?model/(?P<model>\S+)$', views_api.get_model),
    re_path(r'^api/(?:v1/)?all_centres_full', views_api.get_all_centres_full),

    # UI views.
    re_path(r'^$', views_ui.get_all_centres),
    re_path(r'^centre/(?P<centre_id>\d+)$', views_ui.get_centre),
    re_path(r'^all_centres$', views_ui.get_all_centres),
    re_path(r'^about$', views_ui.get_about),
    re_path(r'^contacting$', views_ui.get_contacting),
    re_path(r'^contact/(?P<contact_id>\d+)$', views_ui.get_contact),
    re_path(r'^centres_contacts$', views_ui.get_centres_contacts),
    re_path(r'^consortia$', views_ui.get_consortia),
    re_path(r'^fcs$', views_ui.get_fcs),
    re_path(r'^map', views_ui.get_map),
    re_path(r'^oai_pmh$', views_ui.get_oai_pmh),
    re_path(r'^spf$', views_ui.get_spf),

    # DRF SPECTACULAR

    ]
