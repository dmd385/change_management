from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class Company(models.Model):
    """
    This model holds all of the information for companies in the system.
    """
    name = models.CharField(max_length=100)


class Location(models.Model):
    """
    This model represents a physical location that is linked to a company
    """
    street = models.CharField(max_length=50)
    town = models.CharField(max_length=30)
    zipCode = models.IntegerField(null=True)
    state = models.CharField(max_length=2)
    phone = models.CharField(max_length=10)
    company = models.ForeignKey(Company)


class User(AbstractUser):
    """
    This is the base user case for the system. This holds the information that
    holds all of the base information for users in this system.
    """
    fName = models.CharField(max_length=30)
    lName = models.CharField(max_length=30)
    company = models.ForeignKey(Company)

    def create_admin(self, user):
        user.groups.add(Group.objects.get(name='admin'))

        user.save()

    def create_engineer(self, user):
        user.groups.add(Group.objects.get(name='engineer'))
        user.save()

    def create_client(self, user):
        user.groups.add(Group.objects.get(name='client'))
        user.save()

