from django.urls import path
from . import views

urlpatterns = [
    path('', views.signIn, name='signIn'),
    path('signup/', views.signup, name='signup'),
    path('forgetPass/', views.forgetPass, name='forgetPass'),
    path('main/', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout, name='logout'),
    path('get_ai_response/', views.get_ai_response, name='get_ai_response'),
    path('get_ai_response/', views.get_ai_response, name='get_ai_response'),
    path('journal/', views.journal_page, name='journal'),
    path('save_journal/', views.save_journal, name='save_journal'),
    path('get_journal_entries/', views.get_journal_entries, name='get_journal_entries'),
    path('get_mood_data/', views.get_mood_data, name='get_mood_data'),

]

