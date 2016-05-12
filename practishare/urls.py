from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import TemplateView
from practishare import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'practishare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^what_for$', TemplateView.as_view(template_name="what_for.html"), name='what_for'),
    url(r'^who_are_we$', TemplateView.as_view(template_name="who_are_we.html"), name='who_are_we'),
    url(r'^terms$', TemplateView.as_view(template_name="terms.html"), name='terms'),
    url(r'^support$', TemplateView.as_view(template_name="support.html"), name='support'),
    url(r'^subject/', include("practices.urls", namespace="practices")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
