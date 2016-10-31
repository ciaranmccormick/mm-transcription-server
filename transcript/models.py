from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Document(models.Model):
    owner = models.ForeignKey(User)
    filename = models.CharField(max_length=200)
    mp3_filename = models.CharField(max_length=200)
    duration = models.IntegerField()
    date = models.DateField()
    typist = models.CharField(max_length=10)


class Line(models.Model):
    document = models.ForeignKey(Document, related_name='lines')
    line_num = models.IntegerField()
    text = models.CharField(max_length=1000)


class Extract(models.Model):
    document = models.ForeignKey(Document, related_name='extracts')
    context = models.CharField(max_length=3)
    completed = models.BooleanField(default=False)


class ExtractLines(models.Model):
    extract = models.ForeignKey(Extract, related_name='extract_lines')
    line = models.ForeignKey(Line)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
