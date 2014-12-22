# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from practices.models import Practice, Subject, Comment
from practices.forms import PracticeForm, CommentForm

class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class SubjectView(generic.base.ContextMixin):
    model = Practice
    form_class = PracticeForm
    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['subject'] = Subject.objects.get(pk=self.kwargs['subject_id'])
        return context
    def get_form(self, form_class):
        return form_class(Subject.objects.get(pk=self.kwargs['subject_id']), **self.get_form_kwargs())
    def get_success_url(self):
        return reverse_lazy("practices:index", kwargs={'subject_id': self.kwargs['subject_id']})

class IndexView(SubjectView, generic.ListView):
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        axis = Subject.objects.get(pk=self.kwargs['subject_id']).axis_set.all()[1]
        columns=[axis.value1, axis.value2, axis.value3, axis.value4]
        columns.sort()
        context['columns'] = columns
        return context

class DetailView(SubjectView, generic.DetailView):
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class UpdateView(LoginRequiredMixin, SubjectView, generic.UpdateView):
    pass

class CreateView(LoginRequiredMixin, SubjectView, generic.CreateView):
    def form_valid(self, form):
        form.instance.subject = Subject.objects.get(pk=self.kwargs['subject_id'])
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class DuplicateView(CreateView):
    def get_initial(self):
        practice = Practice.objects.get(pk = self.kwargs['pk'])
        practice.pk = None
        return model_to_dict(practice)
    
class DeleteView(SubjectView, generic.DeleteView):
    pass

class CommentView(generic.CreateView):
    model = Comment
    form_class = CommentForm
    def get_success_url(self):
        return reverse_lazy("practices:detail", kwargs=self.kwargs)
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.practice_id = self.kwargs['pk']
        return super(CommentView, self).form_valid(form)
