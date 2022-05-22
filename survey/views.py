from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.views.generic import CreateView
from .models import SurveyQuestion,Week
from django.forms import formset_factory
from .forms import SurveyForm
from django.urls import reverse
from .forms import QuestionForm

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
        return redirect(reverse('survey:log_in'))

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
            return redirect(reverse('survey:week_questions', args=[1]))


def home_page(request):
    return render(request,'survey/home.html')

def week_questions(request, week):

    questions = SurveyQuestion.objects.filter(week=week).all()
    questionCount = SurveyQuestion.objects.count()

    SurveyFormSet = formset_factory(SurveyForm, extra=questionCount)
    formset =  SurveyFormSet()

    questionForm = zip(questions,formset)

    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            for i in range(questionCount-1):
                var = 'form-' + str(i) + '-score'
                score = request.POST.get(var , 0)

                if score == 0:
                    continue
                else:
                    if score == 'option1':
                        score = 1
                    elif score == 'option2':
                        score = 2
                    elif score == 'option3':
                        score = 3
                    elif score == 'option4':
                        score = 4
                    else:
                        score = 5
                    question = questions[i]
                    question.total_responses += 1
                    question.total_score += score
                    question.average_score = (question.total_score / question.total_responses)
                    question.save()

            return redirect(reverse('survey:home_page'))
        else:
            print(form.errors)
            return render(request,'survey/week_questions.html', context={'questions' : questions, 'week' : week, 'questionForm' : questionForm})

    else:
        if questions:
            return render(request,'survey/week_questions.html', context={'questions' : questions, 'week' : week, 'questionForm' : questionForm})
        else:
            return render(request,'survey/week_questions.html', context={'questions' : questions, 'week' : week, 'error':
                                                                                                        'No questions for this week!'})

def createQuestion(request, week): 

    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            SurveyQuestion.objects.create(question=request.POST.get('question'), week=Week.objects.get(week_number=week))
            return redirect(reverse('survey:week_questions', args=[week]))
        
    return render(request, 'survey/create_question.html', context={'form':form})

def updateQuestion(request,pk):

    question = SurveyQuestion.objects.get(id=pk)
    form = QuestionForm(instance=question)
    week = question.week

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(reverse('survey:week_questions', args=[week]))

    return render(request, 'survey/create_question.html',context={'form':form})

def deleteQuestion(request,pk):

    question = SurveyQuestion.objects.get(id=pk)
    week = question.week

    if request.method == "POST":
        question.delete()
        return redirect(reverse('survey:week_questions', args=[week]))

    return render(request, 'survey/delete.html' , context={'item':question, 'week':week})