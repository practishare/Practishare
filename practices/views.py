# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from practices.models import Practice, Subject
from practices.forms import PracticeForm

class SubjectView(generic.base.ContextMixin):
    model = Practice
    form_class = PracticeForm
    def get_context_data(self, **kwargs):
        ctx = super(SubjectView, self).get_context_data(**kwargs)
        ctx['subject'] = Subject.objects.get(pk=self.kwargs['subject_id'])
        return ctx
    def get_form(self, form_class):
        return form_class(Subject.objects.get(pk=self.kwargs['subject_id']), **self.get_form_kwargs())
    def get_success_url(self):
        return reverse_lazy("practices:index", kwargs={'subject_id':self.kwargs['subject_id']})

class IndexView(SubjectView, generic.ListView):
    pass

class DetailView(SubjectView, generic.DetailView):
    pass

class UpdateView(SubjectView, generic.UpdateView):
    pass

class CreateView(SubjectView, generic.CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)
    
class DeleteView(SubjectView, generic.DeleteView):
    pass
