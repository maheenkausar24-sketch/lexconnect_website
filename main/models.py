from django.db import models


class LawCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Lawyer(models.Model):

    name = models.CharField(max_length=100)

    specialization = models.ForeignKey(
        LawCategory,
        on_delete=models.CASCADE
    )

    experience = models.IntegerField()

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    location = models.CharField(max_length=150)   # NEW FIELD

    def __str__(self):
        return self.name


class Consultation(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    issue = models.TextField()
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    

class Consultation(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    issue = models.TextField()

    lawyer = models.ForeignKey(
        'Lawyer',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)



class Message(models.Model):

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE
    )

    sender = models.CharField(max_length=20)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)