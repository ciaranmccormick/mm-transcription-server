from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token
import numpy as np
import numpy.random as nprand


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
    flag = models.BooleanField(default=False)
    tag = models.CharField(max_length=512, blank=True)


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


class Recode(models.Model):
    recoder = models.ForeignKey(User)


class RecodeExtract(models.Model):
    extract = models.ForeignKey(Extract)
    recode = models.ForeignKey(Recode)
    recode_context = models.CharField(max_length=3)


def random_extracts(user):
    queryset = Extract.objects.all()
    all_extract_count = queryset.count()
    ten_percent_count = int(np.ceil(all_extract_count * 0.1))

    queryset = queryset.exclude(document__owner=user)
    user_extract_count = queryset.count()

    assert user_extract_count > ten_percent_count

    rand_list = nprand.randint(user_extract_count, size=ten_percent_count)

    return [queryset[xI] for xI in rand_list]


@receiver(post_save, sender=Recode)
def add_extracts_to_recode(sender, instance=None, created=False, **kwargs):
    if created:
        extracts = random_extracts(instance.recoder)
        for extract in extracts:
            RecodeExtract.objects.create(extract=extract, recode=instance,
                                         recode_context="noc")


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
