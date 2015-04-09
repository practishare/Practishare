# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from practices.models import Practice, Subject, Comment
from practices.forms import PracticeForm, CommentForm, getInlines

### Mixins ###
class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class SubjectView(generic.base.ContextMixin):
    u"""Generic view inside a subject"""
    model = Practice
    form_class = PracticeForm
    def dispatch(self, *args, **kwargs):
        self.subject = get_object_or_404(Subject, pk=self.kwargs['subject_id'])
        return super(SubjectView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        """Adds the subject in the template context"""
        context = super(SubjectView, self).get_context_data(**kwargs)
        context['subject'] = self.subject
        #for form view, add inline forms in the context
        if hasattr(self, 'object'):
            context['inlines'] = getInlines(self.subject, practice=self.object)
        return context
    def get_object(self, *args, **kwargs):
        u"""Checks that the practice is in the subject"""
        practice = super(SubjectView, self).get_object(*args, **kwargs)
        if practice.subject != self.subject:
            raise Http404
        return practice
    def get_success_url(self):
        u"""Returns to the subject view after form handling"""
        return reverse_lazy("practices:index", kwargs={'subject_id': self.subject.id})
    
    def form_valid(self, form, axis_form, field_form):
        """If the form is valid, save the associated models"""
        form.instance.subject = self.subject
        form.instance.author = self.request.user
        self.object = form.save()
        axis_form.instance = self.object
        axis_form.save()
        field_form.instance = self.object
        field_form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def post(self, request, *args, **kwargs):
        """Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity."""
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        [axis_form, field_form] = getInlines(self.subject, data=self.request.POST, practice=self.object)
        if form.is_valid() and axis_form.is_valid() and field_form.is_valid():
            return self.form_valid(form, axis_form, field_form)
        else:
            return self.form_invalid(form)

### Definition of the actual views ###
class IndexView(SubjectView, generic.ListView):
    u"""Lists all the practices of a subject"""
    def get_queryset(self):
        return self.subject.practice_set.all()
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        axis = self.subject.axis_set.all()
        context['rows'] = axis[0].axisvalue_set.all()
        context['columns'] = axis[1].axisvalue_set.all()
        return context

class DetailView(SubjectView, generic.DetailView):
    u"""Shows the detail of a practice"""
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class UpdateView(LoginRequiredMixin, SubjectView, generic.UpdateView):
    u"""Updates a practice"""
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateView, self).post(request, *args, **kwargs)

class CreateView(LoginRequiredMixin, SubjectView, generic.CreateView):
    u"""Creates a new practice"""
    def post(self, request, *args, **kwargs):
        self.object = None
        return super(CreateView, self).post(request, *args, **kwargs)

class DuplicateView(CreateView):
    u"""Creates a new practice as a copy of the given one"""
    def get_initial(self):
        practice = Practice.objects.get(pk = self.kwargs['pk'])
        practice.pk = None
        return model_to_dict(practice)
    
class DeleteView(LoginRequiredMixin, SubjectView, generic.DeleteView):
    u"""Deletes a given practice"""
    pass

class CommentView(LoginRequiredMixin, generic.CreateView):
    u"""Adds a comment on a practice"""
    model = Comment
    form_class = CommentForm
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("practices:detail", kwargs=kwargs))
    def get_success_url(self):
        return reverse_lazy("practices:detail", kwargs=self.kwargs)
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.practice_id = self.kwargs['pk']
        return super(CommentView, self).form_valid(form)
