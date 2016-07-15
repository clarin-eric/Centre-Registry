# -*- coding: utf-8 -*-

from django.conf.urls import include, url, patterns
from django.contrib import admin
from centre_registry import views_ui, views_api

admin.autodiscover()

urlpatterns = patterns('',
                        # include('django.contrib.admindocs.urls')),
                        url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
                        url(r'^admin/', include(admin.site.urls)),  # admin site

                        ## REST API v1.
                        url(r'^restxml/$',
                            views_api.get_all_centres),
                        url(r'^restxml/(?P<centre_id>\d+)[/]?$',
                            views_api.get_centre),

                        ## REST API v2.
                        url(r'^api/KML/(?P<types>([A-Z]){0,6})$',
                            views_api.get_centres_kml),
                        url(r'^api/model/(?P<model>\S+)$',
                            views_api.get_model),

                        ## Custom REST API v2. Currently unused.
                        #url(r'^api/SPF$',
                        #    views_api.get_spf),

                        ## UI views.
                        # url(r'^/(?P<view_name>\s+)$', views_ui.view),
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
                        url(r'^spf$', views_ui.get_spf),
)
