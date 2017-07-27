from django.db import models
from home.models import *


class InfraType(models.Model):
    """
    Holds all of the types of infrastructure to the system to allow for a dropdown menu
    """
    name = models.CharField(max_length=100)


class OS(models.Model):
    """
    Holds all of the types of OS that a system can be run on to allow for a dropdown menu
    """
    name = models.CharField(max_length=100)


class Infra(models.Model):
    """
    This represents infrastructure located at a specific location/company
    """
    name = models.CharField(unique=True, max_length=100)
    type = models.ForeignKey(InfraType)
    os = models.ForeignKey(OS)
    location = models.ForeignKey(Location)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Change(models.Model):
    """
    This model represents the change done to a specific infrastructure at a specific location with
    specific users interacting
    """
    infra = models.ForeignKey(Infra)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    justification = models.CharField(max_length=1000, null=True)
    neg_impact = models.CharField(max_length=1000, null=True)
    request_user = models.ForeignKey(User, related_name='request_user')
    project_manager = models.ForeignKey(User, related_name='project_manager')
    engineer = models.ForeignKey(User, null=True, related_name='engineer')
    request_date = models.DateField(null=True)
    est_time = models.IntegerField(null=True)
    act_time=models.IntegerField(null=True)
    work_date = models.DateTimeField(null=True)
    quote = models.FileField(null=True, upload_to=user_directory_path)
    open = models.BooleanField(default=True)
    close_user = models.ForeignKey(User, null=True)
    close_date = models.DateTimeField(null=True)
    customer_deny_exp = models.CharField(max_length=1000, null=True)
    internal_deny_exp = models.CharField(max_length=1000, null=True)
    internal_auth = models.BooleanField(default=False)
    internal_auth_user = models.ForeignKey(User, null=True, related_name='internal_auth')
    internal_auth_date=models.DateTimeField(null=True)
    customer_auth = models.BooleanField(default=False)
    customer_auth_user=models.ForeignKey(User, null=True, related_name='customer_auth')
    customer_auth_date=models.DateTimeField(null=True)
    work_done=models.BooleanField(default=False)
    work_done_stamp=models.DateTimeField(null=True)
    work_done_user=models.ForeignKey(User,null=True, related_name='work_done')
    active = models.BooleanField(default=True)