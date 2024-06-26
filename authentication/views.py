from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from . import forms
from django.views.generic import View

# Login Form View - Credit and insperation: https://openclassrooms.com/en/courses/7107341-intermediate-django/7263527-create-a-login-page-with-class-based-views
class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('post_list')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})
  
    
def logout_user(request):
    logout(request)
    return redirect('login')


# Sign up Form View - Credit and insperation: https://openclassrooms.com/en/courses/7107341-intermediate-django/7263818-create-a-sign-up-page
def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})
