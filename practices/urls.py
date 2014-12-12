from django.conf.urls import patterns, url
from django.views.generic import ListView
from practices import views, models

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model = models.Subject), name='subject_index'),
    url(r'^(?P<subject_id>\d+)/$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<subject_id>\d+)/practice/(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<subject_id>\d+)/practice/new$', views.CreateView.as_view(), name='new'),
    url(r'^(?P<subject_id>\d+)/practice/(?P<pk>\d+)/edit$', views.UpdateView.as_view(), name='edit'),
    url(r'^(?P<subject_id>\d+)/practice/(?P<pk>\d+)/delete$', views.DeleteView.as_view(), name='delete'),
)
