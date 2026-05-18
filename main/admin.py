from django.contrib import admin
from .models import LawCategory, Lawyer
from .models import LawCategory, Lawyer, ChatSession, Message, Review

admin.site.register(LawCategory)
admin.site.register(Lawyer)
admin.site.register(ChatSession)
admin.site.register(Message)
admin.site.register(Review)