from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    #AUTH
    path('signup/', views.sign_up,name='sign_up'),
    path('logout/',views.log_out,name='log_out'),
    path('login',views.log_in,name='log_in'),
    #SURVEY
    path('home/', views.home_page, name='home_page'),
    path('week/<int:week>', views.week_questions, name='week_questions'),
    path('create_question/<int:week>', views.createQuestion, name='create_question'),
    path('update_question/<str:pk>', views.updateQuestion, name='update_question'),
    path('delete_question/<str:pk>', views.deleteQuestion, name='delete_question'),
]