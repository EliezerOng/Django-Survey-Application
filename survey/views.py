from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate

# Create your views here.

def sign_up(request):
    #Enter selected emails to register an account
    allowed_emails = ['test1@gmail.com', 'test2@gmail.com']
    if request.method == 'POST':
        #Checking if passwords match
        if request.POST['password1'] == request.POST['password2']:
            #Checking if email is allowed to create an account
            if request.POST['email'] in allowed_emails:
                try:
                    user = User.objects.create_user(request.POST['username'], 
                                                    email=request.POST['email'],
                                                    password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('home_page')

                except IntegrityError:
                    return render(request , 'survey/signup.html' , {'form': UserCreationForm()
                                                            , 'error':'Username Taken'})
            else:
                return render(request , 'survey/signup.html' , {'form': UserCreationForm()
                                                         , 'error':'Not authorised to create an account'})
        else:
            return render(request , 'survey/signup.html' , {'form': UserCreationForm()
                                                         , 'error':'Passwords did not match'})

    else:   
        return render(request , 'survey/signup.html' , {'form': UserCreationForm()})

def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home_page')

def log_in(request):
    if request.method == 'GET':
        return render(request, 'survey/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], 
                                     password=request.POST['password'])
        if user is None:
            return render(request, 'survey/login.html',{'form':AuthenticationForm(),
                                                        'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home_page')



def home_page(request):
    return render(request,'survey/home.html')
