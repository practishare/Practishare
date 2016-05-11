# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict, inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from practices.models import Practice, Subject, Comment, Axis, PracticeAxisValue, PracticeFieldValue, AxisValue, Field
from practices.forms import PracticeForm, CommentForm, AxisForm, FieldForm

### Mixins ###
class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class MultipleFormMixin(object):
    """Adds multiple forms and formsets capability to a FormView"""
    def get_context_data(self, **kwargs):
        #for form views, add inline forms in the context
        if hasattr(self, 'object'):
            kwargs['forms'] = self.get_forms()
        return super(MultipleFormMixin, self).get_context_data(**kwargs)
        
    def form_valid(self, forms):
        """If the form is valid, save the associated models"""
        for form in forms:
            if self.object:
                if not form.instance.pk:
                    form.instance = self.object
                form.save()
            else:
                self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_forms(self, extra_forms=[]):
        form_class = self.get_form_class()
        return [self.get_form(form_class)] + extra_forms
    
    def post(self, request, *args, **kwargs):
        """Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity."""
        forms = self.get_forms()
        if all([form.is_valid() for form in forms]):
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms[0])

class SubjectMixin(generic.base.ContextMixin):
    u"""Generic view inside a subject"""
    model = Practice
    form_class = PracticeForm
    def dispatch(self, *args, **kwargs):
        self.subject = get_object_or_404(Subject, pk=self.kwargs['subject_id'])
        return super(SubjectMixin, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        """Adds the subject in the template context"""
        kwargs['subject'] = self.subject
        return super(SubjectMixin, self).get_context_data(**kwargs)
    def get_object(self, *args, **kwargs):
        u"""Checks that the practice is in the subject"""
        practice = super(SubjectMixin, self).get_object(*args, **kwargs)
        if practice.subject != self.subject:
            raise Http404
        return practice
    def get_success_url(self):
        u"""Returns to the subject view after form handling"""
        return reverse_lazy("practices:index", kwargs={'subject_id': self.subject.id})
    
    def get_forms(self, extra_forms=[]):
        """Generates formsets for the practice, depending on the subject"""
        # don't exclude practice if it's None, because it would exclude axis that don't have any practice yet
        # -1 is known to be an impossible value
        axis_list = map(lambda a: {'axis': a.id}, self.subject.axis_set.exclude(practiceaxisvalue__practice = self.object or -1))
        field_list = map(lambda f: {'field': f.id}, self.subject.field_set.exclude(practicefieldvalue__practice = self.object or -1))
        
        AxisFormSet = inlineformset_factory(Practice, PracticeAxisValue, can_delete=False, form=AxisForm, extra=len(axis_list), max_num=self.subject.axis_set.count())
        FieldFormSet = inlineformset_factory(Practice, PracticeFieldValue, can_delete=False, form=FieldForm, extra=len(field_list), max_num=self.subject.field_set.count())
        
        data = self.request.POST or None
        forms = [AxisFormSet(data, initial=axis_list, instance=self.object),
            FieldFormSet(data, initial=field_list, instance=self.object)] + extra_forms
        return super(SubjectMixin, self).get_forms(forms)
    
    def form_valid(self, forms):
        """If the form is valid, save the associated models"""
        forms[0].instance.subject = self.subject
        forms[0].instance.author = self.request.user
        return super(SubjectMixin, self).form_valid(forms)

### Definition of the actual views ###
class IndexView(SubjectMixin, generic.ListView):
    u"""Lists all the practices of a subject"""
    def get_queryset(self):
        return self.subject.practice_set.all()
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        axis = self.subject.axis_set.all()
        context['rows'] = axis[0].axisvalue_set.all()
        context['columns'] = axis[1].axisvalue_set.all()
        return context

class DetailView(SubjectMixin, generic.DetailView):
    u"""Shows the detail of a practice"""
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class UpdateView(LoginRequiredMixin, SubjectMixin, MultipleFormMixin, generic.UpdateView):
    u"""Updates a practice"""
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateView, self).post(request, *args, **kwargs)

class CreateView(LoginRequiredMixin,SubjectMixin, MultipleFormMixin, generic.CreateView):
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
    
class DeleteView(LoginRequiredMixin, SubjectMixin, generic.DeleteView):
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

class BaseSubjectEdit(LoginRequiredMixin, MultipleFormMixin):
    u"""Base for edition of a subject"""
    model = Subject
    fields = ['title', 'public']
    def get_success_url(self):
        return reverse_lazy("practices:axis_edit", kwargs={"pk":self.object.id})
    
    def form_valid(self, forms):
        """If the form is valid, save the associated models"""
        forms[0].instance.author = self.request.user
        return super(BaseSubjectEdit, self).form_valid(forms)
    
    def get_forms(self, extra_forms=[]):
        AxisFormSet = inlineformset_factory(Subject, Axis, can_delete=False, extra=2, max_num=2)
        FieldFormSet = inlineformset_factory(Subject, Field, extra=1)
        data = self.request.POST or None
        forms = [AxisFormSet(data, instance=self.object),
            FieldFormSet(data, instance=self.object)] + extra_forms
        return super(BaseSubjectEdit, self).get_forms(forms)

class SubjectCreate(BaseSubjectEdit, generic.CreateView):
    u"""Creation of a subject"""
    def post(self, request, *args, **kwargs):
        self.object = None
        return super(SubjectCreate, self).post(request, *args, **kwargs)

class SubjectUpdate(BaseSubjectEdit, generic.UpdateView):
    u"""Modification of a subject"""
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SubjectUpdate, self).post(request, *args, **kwargs)
    def get_object(self, queryset = None):
        subject = super(SubjectUpdate, self).get_object(queryset)
        if subject.author != self.request.user:
            raise PermissionDenied
        return subject

class EditAxis(LoginRequiredMixin, MultipleFormMixin, generic.UpdateView):
    u"""Edit a subject"""
    model = Subject
    fields = []
    def get_success_url(self):
        return reverse_lazy("practices:index", kwargs={"subject_id":self.object.id})
    
    def get_forms(self, extra_forms=[]):
        AxisValueFormSet = inlineformset_factory(Axis, AxisValue, extra=1)
        data = self.request.POST or None
        forms = [AxisValueFormSet(data, instance=axis, prefix="axis%s"%axis.id) for axis in self.object.axis_set.all()] + extra_forms
        return super(EditAxis, self).get_forms(forms)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EditAxis, self).post(request, *args, **kwargs)

    def get_object(self, queryset = None):
        subject = super(EditAxis, self).get_object(queryset)
        if subject.author != self.request.user:
            raise PermissionDenied
        return subject