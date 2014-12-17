# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from practices.models import Practice, Subject, Comment
from practices.forms import PracticeForm, CommentForm

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
        return reverse_lazy("practices:index", kwargs=self.kwargs)

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

class UpdateView(SubjectView, generic.UpdateView):
    pass

class DuplicateView(generic.View):
    def get(self, request, *args, **kwargs):
        practice = Practice.objects.get(pk = self.kwargs['pk'])
        practice.pk = None
        practice.author = request.user
        practice.save()
        return HttpResponseRedirect(reverse_lazy("practices:detail", kwargs={'subject_id': self.kwargs['subject_id'], 'pk': practice.pk}))

class CreateView(SubjectView, generic.CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)
    
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
