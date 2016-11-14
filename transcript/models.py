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


class IType(models.Model):
    PERSONAL = 'PR'
    SENSITIVE = 'SN'
    BOTH = "BO"
    I_TYPE_CHOICES = (
        (PERSONAL, 'Personal'),
        (SENSITIVE, 'Sensitive'),
        (BOTH, 'Both')
    )
    extract = models.OneToOneField(Extract, related_name='i_type')
    type = models.CharField(max_length=2, choices=I_TYPE_CHOICES)


class IMode(models.Model):
    AUTOMATICS = "AU"
    MANUAL = "MN"
    I_MODE_CHOICES = (
        (AUTOMATICS, 'Automatic'),
        (MANUAL, "Manual")
    )
    extract = models.OneToOneField(Extract, related_name='i_mode')
    mode = models.CharField(max_length=2, choices=I_MODE_CHOICES)


class Purpose(models.Model):
    extract = models.ForeignKey(Extract, related_name='i_purpose')
    purpose = models.CharField(max_length=300)


class RoleRelationship(models.Model):
    extract = models.ForeignKey(Extract, related_name='relationships')
    relationship = models.CharField(max_length=300)


class RoleExpectation(models.Model):
    extract = models.ForeignKey(Extract, related_name='expectations')
    expectation = models.CharField(max_length=300)


class PlaceLocation(models.Model):
    extract = models.ForeignKey(Extract, related_name='locations')
    location = models.CharField(max_length=300)


class PlaceNorm(models.Model):
    extract = models.ForeignKey(Extract, related_name='norms')
    norm = models.CharField(max_length=300)


class IAttrRef(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=512)
    label = models.CharField(max_length=100)


class IAttr(models.Model):
    attr = models.ForeignKey(IAttrRef)
    extract = models.ForeignKey(Extract, related_name='i_attrs')
    isAttr = models.BooleanField(default=False)


class InformationFlow(models.Model):
    SENDER_SUB = 'SS'
    SENDER_REC = 'SR'
    THIRD_PARTY = 'TP'
    FEEDBACK = 'FB'
    ALL = 'AL'
    NO_FLOW = 'NF'

    INFORMATION_FLOW_CHOICES = (
        (SENDER_SUB, 'Sender-Subject'),
        (SENDER_REC, 'Sender-Receiver'),
        (THIRD_PARTY, 'Third-Party'),
        (FEEDBACK, 'Feedback'),
        (ALL, 'All'),
        (NO_FLOW, 'No-Flow')
    )
    extract = models.OneToOneField(Extract, related_name='info_flow')
    flow = models.CharField(max_length=2, choices=INFORMATION_FLOW_CHOICES)


@receiver(post_save, sender=IAttrRef)
def add_attr_to_extract(sender, instance=None, created=False, **kwargs):
    if created:
        extracts = Extract.objects.all()
        for extract in extracts:
            IAttr.objects.create(attr=instance, extract=extract)


@receiver(post_save, sender=Extract)
def create_attrs(sender, instance=None, created=False, **kwargs):
    if created:
        attrs = IAttrRef.objects.all()
        for attr in attrs:
            IAttr.objects.create(attr=attr, extract=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
