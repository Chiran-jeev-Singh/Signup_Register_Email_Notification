from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


# Create your views here.


####### index ########
def index(request):
    return render(request, 'user/index.html', {'title': 'index'})


######## register here #########
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            #### mail system #####
            html_template = get_template('user/email.html')
            context = {'username': username}
            subject, from_email, to = 'Welcome', 'djnagoemailverify@gmail.com', email
            html_content = html_template.render(context)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            ######################

            messages.success(request, f"Your account has been created. You are now able to log in")
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title':'register here'})

####### Login Form ########

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f"Welcome {username}")
            return redirect('index')
        else:
            messages.info(request, f"Account does not exists. Please Sign Up")
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form, 'title': 'log in'})