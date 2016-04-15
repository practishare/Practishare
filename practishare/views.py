from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from practishare.models import User

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form,})

class UserReset(generic.DetailView):
    template_name = "templates/registration/password_reset_done.html"
    model = User
    slug_field = "username"
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        password = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        self.object.set_password(password)
        self.object.is_valid = True
        self.object.save()
        
        form = PasswordResetForm()
        form.cleaned_data = {'email': self.object.email}
        form.save(domain_override=request.get_host())
        
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)