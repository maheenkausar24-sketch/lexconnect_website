from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('chatbot/', views.chatbot, name='chatbot'),
    path('ask-lexora/', views.ask_lexora, name='ask_lexora'),

    # ADD THIS
    path('lawyers/<int:category_id>/', views.lawyers_by_category, name='lawyers_by_category'),
    

    # ADD THIS
    path('consult/<int:lawyer_id>/', views.consult_lawyer, name='consult_lawyer'),

    path("chat/<int:consultation_id>/",views.consultation_chat,name="consultation_chat")

]