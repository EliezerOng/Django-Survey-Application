from sqlite3 import IntegrityError
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.views.generic import CreateView
from .models import SurveyQuestion,Week,Comment
from django.forms import formset_factory
from .forms import CommentForm, SurveyForm
from django.urls import reverse
from .forms import QuestionForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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
                    return redirect(reverse('survey:week_questions', args=[1]))

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

    comments = Comment.objects.filter(week=week).all()

    SurveyFormSet = formset_factory(SurveyForm, extra=questionCount)
    formset =  SurveyFormSet()

    questionForm = zip(questions,formset)

    commentForm = CommentForm()

    if request.method == "POST":
        form = SurveyForm(request.POST)
        comment = CommentForm(request.POST)
        if form.is_valid() and comment.is_valid():
            commentText = comment.cleaned_data['comment']
            Comment.objects.create(comment=commentText,week=Week.objects.get(week_number=week))
            for i in range(questionCount):
                var = 'form-' + str(i) + '-score'
                score = request.POST.get(var , 0)

                if score == 0:
                    continue
                else:
                    question = questions[i]
                    if score == 'option1':
                        question.option_1_count += 1 
                        score = 1
                    elif score == 'option2':
                        question.option_2_count += 1 
                        score = 2
                    elif score == 'option3':
                        question.option_3_count += 1 
                        score = 3
                    elif score == 'option4':
                        question.option_4_count += 1 
                        score = 4
                    else:
                        question.option_5_count += 1 
                        score = 5
                    question.total_responses += 1
                    question.total_score += score
                    question.average_score = (question.total_score / question.total_responses)
                    question.save()

            return redirect(reverse('survey:thank_you'))
        else:
            print(form.errors)
            return render(request,'survey/week_questions.html', context={'questions' : questions, 'week' : week, 'questionForm' : questionForm})

    else:
        if questions:
            return render(request,'survey/week_questions.html', context={'questions' : questions, 'week' : week, 'questionForm' : questionForm
                                                                        ,'comment' : commentForm, 'comments':comments})
        else:
            return render(request,'survey/week_questions.html', context={'questions' : questions, 'week' : week, 
                                                        'error':'No questions for this week!','comment' : commentForm,'comments':comments})

def createQuestion(request, week): 

    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            SurveyQuestion.objects.create(question=request.POST.get('question'), week=Week.objects.get(week_number=week))
            return redirect(reverse('survey:week_questions', args=[week]))
        
    return render(request, 'survey/create_question.html', context={'form':form})

def updateQuestion(request,pk):

    question = get_object_or_404(SurveyQuestion, pk=pk)
    form = QuestionForm(instance=question)
    week = question.week

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(reverse('survey:week_questions', args=[week]))

    return render(request, 'survey/create_question.html',context={'form':form})

def deleteQuestion(request,pk):

    question = get_object_or_404(SurveyQuestion, pk=pk)
    week = question.week

    if request.method == "POST":
        question.delete()
        return redirect(reverse('survey:week_questions', args=[week]))

    return render(request, 'survey/delete.html' , context={'item':question, 'week':week})

@login_required
def resultsData(request, obj):

    votedata = []

    question = SurveyQuestion.objects.get(id=obj)
    option1 = question.option_1_count
    option2 = question.option_2_count
    option3 = question.option_3_count
    option4 = question.option_4_count
    option5 = question.option_5_count
    votedata = {'1':option1,'2':option2,'3':option3,'4':option4,'5':option5}

    return JsonResponse(votedata, safe=False)

@login_required
def resultsPage(request, obj):

    question = get_object_or_404(SurveyQuestion, pk=obj)

    week = question.week

    return render(request, 'survey/results.html', {'question' : question ,'week' : week})
