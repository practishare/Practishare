from django.conf.urls import patterns, include, url
from django.contrib import admin
from practishare import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'practishare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^accounts/', include('django.contrib.auth.urls', namespace="accounts")),
    url('^register$', views.register),
    url(r'^', include("practices.urls", namespace="practices")),
)
