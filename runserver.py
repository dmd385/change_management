
from Dashboard.models import *
company = Company(name='Pervasive Solutions')
company.save()
Group.objects.create(name='admin')
Group.objects.create(name='engineer')
Group.objects.create(name='client')
user=User.objects.create_user('admin',password='admin',company=company)
user.create_admin(user)
