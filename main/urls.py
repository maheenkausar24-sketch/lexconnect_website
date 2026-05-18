from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # User Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Chatbot
    path('chatbot/', views.chatbot, name='chatbot'),
    path('ask-lexora/', views.ask_lexora, name='ask_lexora'),

    # Lawyers
    path('lawyers/<int:category_id>/', views.lawyers_by_category, name='lawyers_by_category'),
    path('lawyer/profile/<int:lawyer_id>/', views.lawyer_profile, name='lawyer_profile'),

    # Consultation / Booking
    path('consult/<int:lawyer_id>/', views.consult_lawyer, name='consult_lawyer'),
    path('book/<int:lawyer_id>/', views.book_lawyer, name='book_lawyer'),

    # Chat system
    path('chat/start/<int:lawyer_id>/', views.start_chat, name='start_chat'),
    path('chat-room/<int:chat_id>/', views.chat_page, name='chat_page'),
    path('my-chats/', views.user_chats, name='user_chats'),
    path('chat/<int:chat_id>/', views.chat_page),

    # Lawyer Auth
    path('lawyer/register/', views.lawyer_register, name='lawyer_register'),
    path('lawyer/login/', views.lawyer_login, name='lawyer_login'),
    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),

    # Success page
    path('request-success/', views.request_success, name='request_success'),

    path("pay/<int:lawyer_id>/", views.pay_lawyer, name="pay_lawyer"),
]