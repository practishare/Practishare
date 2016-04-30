from django.conf.urls import patterns, url
from django.views.generic import ListView
from practices import views, models

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset = models.Subject.objects.filter(public=True)), name='subject_index'),
    url(r'^new/$', views.SubjectCreate.as_view(), name="subject_create"),
    url(r'^(?P<subject_id>\w+)/axis/$', views.EditAxis.as_view(), name='axis_edit'),
    url(r'^(?P<subject_id>\w+)/$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<subject_id>\w+)/practice/(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<subject_id>\w+)/practice/new/$', views.CreateView.as_view(), name='new'),
    url(r'^(?P<subject_id>\w+)/practice/(?P<pk>\d+)/edit/$', views.UpdateView.as_view(), name='edit'),
    url(r'^(?P<subject_id>\w+)/practice/(?P<pk>\d+)/duplicate/$', views.DuplicateView.as_view(), name='duplicate'),
    url(r'^(?P<subject_id>\w+)/practice/(?P<pk>\d+)/delete/$', views.DeleteView.as_view(), name='delete'),
    url(r'^(?P<subject_id>\w+)/practice/(?P<pk>\d+)/comment/$', views.CommentView.as_view(), name='comment'),
)
