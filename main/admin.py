from django.contrib import admin
from .models import LawCategory, Lawyer
from .models import Consultation

admin.site.register(LawCategory)
admin.site.register(Lawyer)
admin.site.register(Consultation)