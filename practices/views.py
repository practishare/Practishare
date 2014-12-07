from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from practices.models import Practice
from practices.forms import PracticeForm

class IndexView(generic.ListView):
    model = Practice

class DetailView(generic.DetailView):
    model = Practice

class UpdateView(generic.UpdateView):
    model = Practice

class CreateView(generic.CreateView):
    model = Practice
    form_class = PracticeForm
    success_url = reverse_lazy("practices:index")
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)
    
class DeleteView(generic.DeleteView):
    model = Practice
    success_url = reverse_lazy("practices:index")
