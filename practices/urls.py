from django.conf.urls import patterns, url
from practices import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^new$', views.CreateView.as_view(), name='new'),
    url(r'^(?P<pk>\d+)/edit$', views.UpdateView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete$', views.DeleteView.as_view(), name='delete'),
)
