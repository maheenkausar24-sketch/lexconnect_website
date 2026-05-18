from django.db import models
from django.contrib.auth.models import User


class LawCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Lawyer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    category = models.ForeignKey(LawCategory, on_delete=models.CASCADE)

    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    location = models.CharField(max_length=100)

    certification = models.CharField(max_length=200)
    certificate_file = models.FileField(upload_to='certificates/')

    is_verified = models.BooleanField(default=False)

    rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)

    consultation_fee = models.IntegerField(default=500)

    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ✅ CONSULTATION MODEL (IMPORTANT)
class Consultation(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    issue = models.TextField()

    def __str__(self):
        return self.client_name


# ✅ CHAT SESSION
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lawyer.name}"


# ✅ MESSAGE

class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="chat_files/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

# ✅ REVIEW
class Review(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


# ✅ BOOKING / PAYMENT
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)

    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_chats")
    lawyer = models.ForeignKey('Lawyer', on_delete=models.CASCADE, related_name="lawyer_chats")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.lawyer}"