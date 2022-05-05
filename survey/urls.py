from django.urls import path
from . import views

urlpatterns = [
    #AUTH
    path('signup/', views.sign_up,name='sign_up'),
    path('logout/',views.log_out,name='log_out'),
    path('login',views.log_in,name='log_in'),
    #SURVEY
    path('home/', views.home_page, name='home_page')

]