from django.urls import path
# import all views here
from . import views
# define name of app
app_name= 'polls'
# define all url patterns here
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('user_home/', views.user_home, name='user_home'),
    path('error_user_home/', views.error_user_home, name='error_user_home'),
    path('addpoll/', views.addpoll, name='addpoll'),
    path('<int:question_id>/editpoll/', views.editpoll, name='editpoll'),
    path('<int:question_id>/editchoice/', views.editchoice, name='editchoice'),
    path('<int:question_id>/deletepoll/', views.deletepoll, name='deletepoll'),
    path('<int:question_id>/deletechoice/', views.deletechoice, name='deletechoice'),
    path('addchoice/', views.addchoice, name='addchoice'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('search/', views.search, name='search'),
]