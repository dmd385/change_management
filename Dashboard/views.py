from django.shortcuts import render
from home.models import *
from django.shortcuts import render, get_object_or_404
from .models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
from django.http import HttpResponse, HttpResponseRedirect
import logging
from django.utils import timezone


def tab(id, name, url, template):
    return {
        'id': id,
        'name': name,
        'url': url,
        'template': template
    }

tabCreate = tab('create', 'Create', 'create/', 'Dashboard/create.html')
tabView = tab('view', 'View', 'view/', 'Dashboard/view.html')
tabViewClosed = tab('viewClosed', 'View Closed', 'view_closed/', 'Dashboard/view.html')
tabNewUser = tab('new_user', 'Users', 'new_user/', 'Dashboard/new_user.html')
tabNewCompany = tab('new_company', 'Companies', 'new_company/', 'Dashboard/new_company.html')
tabNewInfra = tab('new_infra', 'Infrastructure', 'new_infra/', 'Dashboard/new_infra.html')
tabLogs = tab('log', 'Logs', 'log/', 'Dashboard/log.html')
tabHome = tab('home', 'Home', 'home/', 'Dashboard/home.html')
tabCalendar = tab('calendar', 'Calendar', 'calendar/', 'Dashboard/calendar.html')


def getTabs(user_id):
    user = User.objects.get(pk=user_id)

    if user.groups.filter(name='engineer').exists():
        return [tabHome,tabView, tabViewClosed, tabCreate, tabCalendar]
    elif user.groups.filter(name='client').exists():
        return [tabHome, tabView, tabViewClosed, tabCalendar]
    elif user.groups.filter(name='admin').exists():
        if user.super_admin == False:
            return [tabView, tabViewClosed, tabCreate, tabLogs, tabCalendar]
        else:
            return [tabView, tabViewClosed, tabCreate, tabNewCompany, tabNewUser, tabNewInfra, tabLogs, tabCalendar]
    else:
        return [tabView]


@login_required()
def emailNotification(request, subject, message):
    import smtplib

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("changeManagementSys", "Pushthebutton8*")
        message = 'Subject: {}\n\n{}'.format(subject, message)
        server.sendmail("changeManagementSys@gmail.com", "dduffy@pervasivesolutions.net", message)
        server.close()
    except:
        return HttpResponseRedirect("/")


@login_required()
def calendar(request, user_id):
    user = User.objects.get(pk=user_id)
    content = {}
    if request.method == 'POST':
        pass
    else:
        content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'tab': tabCalendar
        }
        if user.groups.filter(name='admin').exists() or user.groups.filter(name='engineer'):
            content['dates'] = Change.objects.order_by('work_date')
        else:
            content['dates'] = Change.objects.filter(request_user=user)

    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def newUser(request, user_id):
    companys = Company.objects.all()
    success = ""
    vet = request.user
    if request.method == 'POST':
        try:
            user = User.objects.create_user(request.POST.get('username'), password=request.POST.get('password'),
                                            fName=request.POST.get('fName'), lName=request.POST.get('lName'),
                                            email=request.POST.get('email'),
                                            company=Company.objects.get(name=request.POST.get('company')))
        except IntegrityError as e:
            content = {'userr': request.user,
                       'tabs': getTabs(user_id),
                       'userz': User.objects.order_by('company__name'),
                       'tab': tabNewUser,
                       'company': companys,
                       'message': "Username already taken"
                       }
            return render(request, 'Dashboard/dash.html', content)
        if request.POST.get('type') == 'Administrator':
            user.create_admin(user)
        elif request.POST.get('type') == 'Engineer':
            user.create_engineer(user)
        else:
            user.create_client(user)
        success = "User created successfully"
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+vet.username+" createdUser "+user.company.name+": "+user.username)
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)
    content = {'userr': user,
               'tabs': getTabs(user_id),
               'userz': User.objects.all(),
               'tab': tabNewUser,
               'company': companys,
               'good': success
               }
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def editUser(request, user_id, edit_id):
    user = User.objects.get(pk=user_id)
    edit = User.objects.get(pk=edit_id)
    companys = Company.objects.all()
    content = {'userr': user,
               'tabs': getTabs(user_id),
               'userz': User.objects.all(),
               'tab': tabNewUser,
               'company': companys,
               'username': edit.username,
               'fName': edit.fName,
               'lName': edit.lName,
               'email': edit.email,
               'id': edit.id,
               'companyy': edit.company,
               }
    if edit.groups.filter(name='admin').exists():
        content['group'] = 'Administrator'
    elif edit.groups.filter(name='engineer').exists():
        content['group'] = 'Engineer'
    else:
        content['group'] = 'Client'
    if request.method == "GET":
        content['edit'] = "edit"
    else:
        edit.fName = request.POST.get('fName')
        edit.lName = request.POST.get('lName')
        edit.email = request.POST.get('email')
        edit.save()
        content['good'] = "Edited user: "+edit.username
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
        user.username + " editedUser " + edit.company.name + ": " + edit.username + " " )

    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def choose(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.groups.filter(name='admin').exists():

        return HttpResponseRedirect('/dash/'+str(user_id)+'/view/')
    else:
        return HttpResponseRedirect('/dash/' + str(user_id) + '/home/')


@login_required()
def home(request, user_id):
    edit = User.objects.get(pk = user_id)
    companys = Company.objects.order_by('name')
    content = {'userr': edit,
               'tabs': getTabs(user_id),
               'userz': User.objects.all(),
               'tab': tabHome,
               'company': companys,
               'username': edit.username,
               'fName': edit.fName,
               'lName': edit.lName,
               'email': edit.email,
               'id': edit.id,
               'companyy': edit.company,
               }
    if edit.groups.filter(name='admin').exists():
        content['group'] = 'Administrator'
    elif edit.groups.filter(name='engineer').exists():
        content['group'] = 'Engineer'
    else:
        content['group'] = 'Client'
    if request.method == "GET":
        content['edit']="edit"
    else:
        edit.fName=request.POST.get('fName')
        edit.lName=request.POST.get('lName')
        edit.email =request.POST.get('email')
        edit.save()
        content['good'] = "Edited user: "+edit.username
        dataLogger= logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
        edit.username + " updatedInfo ")
    content['locs'] = Location.objects.filter(company=edit.company)
    content['name'] = edit.company.name
    content['infras'] = Infra.objects.order_by('location__company__name')
    if edit.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def passReset(request, user_id, edit_id):
    user=request.user = User.objects.get(pk = user_id)
    companys = Company.objects.order_by('name')
    if request.method == "GET":
        edit = User.objects.get(pk=edit_id)
        edit.set_password('Password99!')
        edit.save()
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
            user.username + " resetPassword " + edit.company.name + ":" + edit.username)
        content = {'userr': user,
                   'tabs': getTabs(user_id),
                   'userz': User.objects.all(),
                   'tab': tabNewUser,
                   'company': companys,
                   'good': "Password reset for: " + edit.username
                   }
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def newCompany(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        try:

            company = Company(name=request.POST.get('compName'))
            company.save()
            dataLogger = logging.getLogger("dataLogger")
            dataLogger.info(datetime.today().strftime("%m/%d/%Y %H:%M")+": "+
                user.username + " createdCompany " + company.name )
        except IntegrityError as e:
            pass
        content = {'userr': user,
               'tabs': getTabs(user_id),
               'tab': tabNewCompany,
               'locs': Location.objects.order_by('company__name'),
               'good': "Company created successfully",
               'comps': Company.objects.all()}
        return render(request, 'Dashboard/dash.html', content)
    else:
        content = {'userr': user,
                'tabs': getTabs(user_id),
                'tab': tabNewCompany,
                'locs': Location.objects.order_by('company__name'),
                'comps': Company.objects.order_by('name')
                }
        if user.groups.filter(name='admin').exists():
            content['admin'] = "tru"
        return render(request, 'Dashboard/dash.html', content)


@login_required()
def editLocation(request, user_id, location_id):
    user = User.objects.get(pk=user_id)
    location = Location.objects.get(pk=location_id)
    content = {'userr': user,
               'tabs': getTabs(user_id),
               'tab': tabNewCompany,
               'locs': Location.objects.order_by('company__name'),
               'comps': Company.objects.all(),

               'co': location.company,
               'street': location.street,
               'town': location.town,
               'zip': location.zipCode,
               'phone': location.phone,
               'state':location.state,
               'id':location_id
               }
    if request.method=="GET":
        content['edit'] = "e"
    else:
        location.street=request.POST.get('street')
        location.town=request.POST.get('town')
        location.zipCode=request.POST.get('zipCode')
        location.state=request.POST.get('state')
        location.phone=request.POST.get('phone')
        location.save()
        content['good']="Edited location: " +location.company.name + ": "+location.street
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
            user.username + " editedLocation " + location.company.name+": "+location.street)
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def deleteLocation(request,user_id,location_id):
    user=User.objects.get(pk=user_id)
    location=Location.objects.get(pk=location_id)
    sti = location.company.name+": "+location.street
    location.delete()
    dataLogger = logging.getLogger("dataLogger")
    dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
        user.username + " deletedLocation " + sti )
    content = {'userr': user,
               'tabs': getTabs(user_id),
               'tab': tabNewCompany,
               'locs': Location.objects.order_by('company__name'),
               'comps': Company.objects.all()
               }
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def newLocation(request, user_id):
    user = User.objects.get(pk=user_id)
    bet = 0
    if request.method == 'POST':
        try:
            company = Company.objects.get(name=request.POST.get('company'))

            location = Location(street=request.POST.get('street'), town=request.POST.get('town'),
                                zipCode=request.POST.get('zipCode'), state=request.POST.get('state'),
                                phone=request.POST.get('phone'), company=company)
            location.save()
            dataLogger = logging.getLogger("dataLogger")
            dataLogger.info(datetime.today().strftime("%m/%d/%Y %H:%M")+": "+
                user.username + " createdLocation " + location.company.name+": " + location.street)
            bet = 1
        except IntegrityError as e:
            pass
    else:
        pass
    content = {'userr': user,
               'tabs': getTabs(user_id),
               'tab': tabNewCompany,
               'comps': Company.objects.order_by('name'),
               'locs': Location.objects.all()
               }
    if bet == 1:
        content['good'] = "New Location created successfully"
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def dashboard(request, user_id):
    user = User.objects.get(pk=user_id)
    content = {'userr': user,
               'tabs': getTabs(user_id),
               'tab': tabView}
    if user.groups.filter(name='admin').exists():
        content['admin'] = "true"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def newInfra(request, user_id):
    bet = 0
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        street = request.POST.get('location')

        new = Infra(type=InfraType.objects.get(name=request.POST.get('type')),
                        os=OS.objects.get(name=request.POST.get('os')),
                        name=request.POST.get('name'),
                        location=Location.objects.get(street=street))
        new.save()
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
            user.username + " createdInfrastructure " + new.location.company.name+": " + new.name)
        bet = 1
    else:
        pass
    content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'company': Company.objects.order_by('name'),
            'oss': OS.objects.all(),
            'infts': InfraType.objects.all(),
            'locs': Location.objects.order_by('company__name'),
            'infs': Infra.objects.order_by('location__company__name'),
            'tab': tabNewInfra
        }
    if bet == 1:
        content['good'] = "Infrastructure created successfully"
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def editInfra(request, user_id, infra_id):
    user = User.objects.get(pk=user_id)
    infra = Infra.objects.get(pk=infra_id)
    content = {
        'userr': user,
        'tabs': getTabs(user_id),
        'company': Company.objects.order_by('name'),
        'oss': OS.objects.all(),
        'infts': InfraType.objects.all(),
        'locs': Location.objects.order_by('company__name'),
        'infs': Infra.objects.order_by('location__company__name'),
        'name': infra.name,
        'type': infra.type,
        'osi': infra.os,
        'location': infra.location,
        'id': infra_id,
        'tab': tabNewInfra
    }
    if request.method == "GET":
        content['edit'] = "Edit"
    else:
        street = request.POST.get('location')
        street = street.split(": ")[1]
        infra.name = request.POST.get('name')
        infra.os = OS.objects.get(name=request.POST.get('os'))
        infra.type = InfraType.objects.get(name=request.POST.get('type'))
        infra.location = Location.objects.get(street=street)
        infra.save()
        content['good'] = "Edited Infrastructure: " + infra.location.company.name+"-"+infra.name
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
            user.username + " editedInfrastructure " + infra.location.company.name+": "+infra.name)
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def deleteInfra(request, user_id, infra_id):
    user = User.objects.get(pk=user_id)
    infra = Infra.objects.get(pk=infra_id)
    name = infra.location.company.name+"-"+infra.name
    infra.delete()
    content = {
        'userr': user,
        'tabs': getTabs(user_id),
        'company': Company.objects.all(),
        'oss': OS.objects.all(),
        'infts': InfraType.objects.all(),
        'locs': Location.objects.order_by('company__name'),
        'infs': Infra.objects.order_by('location__company__name'),
        'tab': tabNewInfra,
        'message': "Deleted Infrastructure: "+name
    }
    dataLogger = logging.getLogger("dataLogger")
    dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
        user.username + " deleted infrastructure " + name)
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def newOS(request, user_id):
    user = User.objects.get(pk=user_id)
    new = OS(name=request.POST.get('os'))
    new.save()
    dataLogger = logging.getLogger("dataLogger")
    dataLogger.info(datetime.today().strftime(
        "%m/%d/%Y %H:%M")+": "+
        user.username + " createdOS " + new.name)
    content = {
        'userr': user,
        'tabs': getTabs(user_id),
        'company': Company.objects.all(),
        'oss': OS.objects.all(),
        'infts': InfraType.objects.all(),
        'locs': Location.objects.order_by('company__name'),
        'infs': Infra.objects.order_by('location__company__name'),
        'tab': tabNewInfra
    }
    content['good'] = "OS created successfully"
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def newInfraType(request, user_id):
    bet = 0
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        new = InfraType(name=request.POST.get('inf_type'))
        new.save()
        bet = 1
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
            user.username + " createdType " + new.name )
    else:
        pass
    user = request.user
    content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'company': Company.objects.all(),
            'oss': OS.objects.all(),
            'infts': InfraType.objects.all(),
            'locs': Location.objects.order_by('company__name'),
            'infs': Infra.objects.order_by('location__company__name'),
            'tab': tabNewInfra
        }
    if bet==1:
        content['good'] = "Infrastructure Type created successfully"
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def viewDetail(request, user_id, view_id):
    set=0
    view = Change.objects.get(pk=view_id)
    user = User.objects.get(pk=user_id)
    dataLogger = logging.getLogger("dataLogger")
    if request.method == 'POST':
        if(request.POST.get('denyyy') is None and request.POST.get('denyyy')!=""):
            if user.groups.filter(name='admin').exists():
                view.internal_auth=False
                view.internal_auth_date=datetime.today()
                view.internal_auth_user=user
                view.internal_deny_exp=request.POST.get('denyyy')
                dataLogger.info(datetime.today().strftime(
                    "%m/%d/%Y %H:%M") + ": " +
                                user.username + " deniedChange " + view.infra.location.company.name + ": " + view.infra.location.street + ": " + view.title)
                set=1
                joke = "Admin " + str(view.internal_auth_user.username) + " denied change " + str(
                    view.title) + ' because "' + str(view.internal_deny_exp) + '" at ' + str(
                    view.internal_auth_date.strftime("%m/%d/%Y %H:%M"))
                subject = "Customer Denied Change " + str(view.title)
                emailNotification(request, subject, joke)
            else:
                view.customer_auth=False
                view.customer_auth_date=datetime.today()
                view.customer_auth_user=user
                view.customer_deny_exp = request.POST.get('denyyy')
                dataLogger.info(datetime.today().strftime(
                    "%m/%d/%Y %H:%M") + ": " +
                                user.username + " deniedChange " + view.infra.location.company.name + ": " + view.infra.location.street + ": " + view.title)
                set=1
                joke = "Client " + str(view.customer_auth_user.username) + " denied change " + str(
                    view.title) + ' because "' + str(view.customer_deny_exp) + '" at ' + str(
                    view.customer_auth_date.strftime("%m/%d/%Y %H:%M"))
                subject = "Customer Denied Change " + str(view.title)
                emailNotification(request, subject, joke)
        else:
            view.description = request.POST.get('description')
            view.justification = request.POST.get('justification')
            view.neg_impact = request.POST.get('neg')
            view.request_user = User.objects.get(username=request.POST.get('request_user').split(": ")[1])
            view.project_manager = User.objects.get(username=request.POST.get('project_user').split(": ")[1])
            view.engineer = User.objects.get(username=request.POST.get('engineer').split(": ")[1])
            view.request_date = datetime.strptime(request.POST.get('request_date'), "%m/%d/%Y").date()
            view.work_date = datetime.strptime(request.POST.get('work_date'), "%m/%d/%Y %H:%M")
            view.est_time = request.POST.get('est_time')
            view.act_time = request.POST.get('act_time')
            dataLogger.info(datetime.today().strftime("%m/%d/%Y %H:%M") + ": " +
                        user.username + " editedChange " + view.infra.location.company.name + ": " + view.infra.location.street + ": " + view.title)
        view.save()
        content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'company': Company.objects.all(),
            'locs': Location.objects.order_by('company__name'),
            'users': User.objects.order_by('company__name'),
            'cusers': User.objects.filter(company= Company.objects.get(name='Pervasive Solutions')),
            'infra': Infra.objects.get(pk=view.infra_id),
            'titlee': view.title,
            'neg': view.neg_impact,
            'desc': view.description,
            'just': view.justification,
            'request': datetime.strftime(view.request_date, "%m/%d/%Y"),
            'work': datetime.strftime(view.work_date, "%m/%d/%Y") + " "+datetime.strftime(view.work_date, "%H:%M"),
            'engineer': view.engineer,
            'project': view.project_manager,
            'requestU': view.request_user,
            'customer_accept': view.customer_auth,
            'internal_accept': view.internal_auth,
            'open': view.open,
            'id': view.id,
            'est_time': view.est_time,
            'act_time':view.act_time,
            'view': view,
            'tab': tabView
        }
        if user.groups.filter(name='admin').exists():
            content['company'] = Company.objects.all()
            content['admin'] = 'ya'
            if set == 1:
                content['message'] = "Denied change request"
            else:
                content['good'] = view.title+" saved"
        elif user.groups.filter(name='engineer').exists():
            content['company'] = Company.objects.all()
            content['holy'] = "engineer"
            if set == 1:
                content['message'] = "Denied change request"
            else:
                content['good'] = view.title+" saved"
        else:
            if set == 1:
                content['message'] = "Denied change request"
            content['company'] = Company.objects.filter(name=user.company.name)
            content['locs'] = Location.objects.filter(company=user.company)

    else:
        content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'company': Company.objects.all(),
            'locs': Location.objects.order_by('company__name'),
            'changes': Change.objects.filter(open=True).order_by('infra__location__company__name'),
            'cusers': User.objects.filter(company=Company.objects.get(name='Pervasive Solutions')),
            'users': User.objects.order_by('company__name'),
            'neg': view.neg_impact,
            'desc': view.description,
            'just': view.justification,
            'request': datetime.strftime(view.request_date, "%m/%d/%Y"),
            'work': datetime.strftime(view.work_date, "%m/%d/%Y")+ " "+datetime.strftime(view.work_date, "%H:%M"),
            'engineer': view.engineer,
            'project': view.project_manager,
            'requestU': view.request_user,
            'infra': Infra.objects.get(pk=view.infra_id),
            'customer_accept': view.customer_auth,
            'internal_accept': view.internal_auth,

            'open': view.open,
            'est_time': view.est_time,
            'act_time': view.act_time,
            'id': view.id,
            'view': view,
            'tab': tabView
            }
        if (user.groups.filter(name='admin').exists()and view.open is True and view.work_done is False):
            content['admin'] = 'ya'
        elif(user.groups.filter(name='engineer').exists() and view.open is True and view.work_done is False):
            content['holy']='ya'
        else:
            content['changes'] = Change.objects.filter(infra__location__company=user.company, open=True)
            content['locs'] = Location.objects.filter(company=user.company)
    if user.groups.filter(name='admin').exists() and view.work_done is False:
        content['admin'] = "ad"
    if user.groups.filter(name='admin').exists():
        content['ad'] = ' '
    elif user.groups.filter(name='engineer').exists() and view.work_done is False:
        content['holy'] = "aaa"
    elif user.groups.filter(name='client').exists():
        content['baby'] = "dd"
    if (user.groups.filter(name='admin').exists() or user.groups.filter(name='engineer')) and view.work_done is True:
        content['adminn']="add"
    if view.work_done is True:
        content['w_done'] = " "
        content['w_date'] = datetime.strftime(view.work_done_stamp, "%m/%d/%Y %H/%m")
        content['w_user'] = user
    if view.act_time is None:
        content['act_time'] = 0
    content['view'] = 'True'
    content['titlee'] = view.title
    content['den_reason']=view.customer_deny_exp
    if view.customer_auth_date is None:
        content['customer_deny'] = "good"
    else:
        content['cust_date']=datetime.strftime(view.customer_auth_date, "%m/%d/%Y %H:%M")
        content['cust_user']= view.customer_auth_user.username
    if view.customer_auth is True:
        content['c_ya'] = 'ya'
    elif view.internal_auth is True:
        content['i_ya'] = 'ya'
    if view.internal_auth_date is None:
        content['internal_deny'] = "good"
    else:
        content['int_date']=datetime.strftime(view.internal_auth_date, "%m/%d/%y %H:%M")
        content['int_user']=view.internal_auth_user.username
    if view.open is False:
        content['oh'] = "ya"
        content['tab'] = tabViewClosed
        content['close'] = datetime.strftime(view.close_date, "%m/%d/%Y %H:%M")
        content['closeU'] = view.close_user.username
    if view.customer_auth is False and view.customer_auth_date is None:
        content['denied'] = " dd"
        content['cust_deny']=view.customer_deny_exp
    if view.internal_auth is False and view.internal_auth_date is None:
        content['idenied'] = "dd"
        content['int_deny'] = view.internal_deny_exp

    return render(request, 'Dashboard/dash.html', content)


@login_required()
def export(request, user_id, view_id):

    response = HttpResponse(content_type='text/csv')
    view = Change.objects.get(pk=view_id)
    dynamic = 'attachment; filename="change_request_'+view.title+'_'+datetime.today().strftime("%m/%d/%Y")+'.csv"'
    response['Content-Disposition'] = dynamic
    user = User.objects.get(pk=user_id)
    change = Change.objects.get(pk=view_id)
    writer = csv.writer(response)
    writer.writerow(['User: ', user.username])
    writer.writerow(['Company: ', change.infra.location.company.name])
    writer.writerow(['Location: ', change.infra.location.street+", "+change.infra.location.town+", "+change.infra.location.state+", "+str(change.infra.location.zipCode)])
    writer.writerow(['Infrastructure: ', change.infra.name+": "+change.infra.type.name+": "+change.infra.os.name])
    writer.writerow(['Title: ', change.title])
    writer.writerow(['Description: ', change.description])
    writer.writerow(['Negative Impact: ', change.neg_impact])
    writer.writerow(['Justification: ', change.justification])
    writer.writerow(['Request Date: ', change.request_date, 'Complete Date: ', change.work_date.strftime("%m/%d/%Y %H:%M")])
    writer.writerow(['Request User: ', change.request_user.company.name+": "+change.request_user.fName+" "+change.request_user.lName])
    writer.writerow(['Project Manager: ',
                     change.project_manager.company.name + ": " + change.project_manager.fName + " " + change.project_manager.lName])
    writer.writerow(['Engineer: ',
                     change.engineer.company.name + ": " + change.engineer.fName + " " + change.engineer.lName])
    writer.writerow(['Client: ', change.request_user.company.name, 'User: ', change.request_user.username])
    if change.customer_auth==True:
        writer.writerow(['Client Authorized: ', datetime.strftime(change.customer_auth_date, "%m/%d/%Y %H:%M"), 'by: ', change.customer_auth_user.username])
    elif change.customer_auth is True and change.customer_auth_date is None:
        writer.writerow(['Client Denied: ', datetime.strftime(change.customer_auth_date, "%m/%d/%Y %H:%M")])
        writer.writerow(['Reason: ', change.customer_deny_exp])
    if change.internal_auth is True:
        writer.writerow(['Internally Authorized: ', datetime.strftime(change.internal_auth_date, "%m/%d/%Y %H:%M"), 'by: ', change.internal_auth_user.username])
    elif change.internal_auth is True and change.internal_auth_date is None:
        writer.writerow(['Internally Denied: ', datetime.strftime(change.customer_auth_date, "%m/%d/%Y %H:%M")])
        writer.writerow(['Reason: ', change.internal_deny_exp])
    if change.open is False:
        writer.writerow(['Close Date: ', datetime.strftime(change.close_date, "%m/%d/%Y"), " by: ", change.close_user.username])
    dataLogger = logging.getLogger("dataLogger")
    dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
        user.username + " exportedChange " + view.infra.location.company.name + ": " + view.infra.location.street + ": " + view.title )
    return response


@login_required()
def client_accept(request, user_id,view_id):
    user = User.objects.get(pk=user_id)
    if request.method == "GET":
        view = Change.objects.get(pk=view_id)
        view.customer_auth = True
        view.customer_auth_user = user
        view.customer_auth_date=datetime.today()
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime("%m/%d/%Y %H:%M")+": "+
            user.username + " acceptedChange " + view.infra.location.company.name + ": " +
                        view.infra.location.street + ": " + view.title )
        view.save()
    joke = "Client " + str(view.customer_auth_user.username) + " accepted change " + str(view.title) +  " at " + \
           str(view.customer_auth_date.strftime("%m/%d/%Y %H:%M"))
    subject = "Customer Accepted Change " + str(view.title)
    emailNotification(request, subject, joke)
    return HttpResponseRedirect('/dash/' + str(user.id) + '/view/'+str(view_id)+'/?accept')


@login_required()
def workDone(request, user_id, view_id):
    user=User.objects.get(pk=user_id)
    view=Change.objects.get(pk=view_id)
    view.work_done = True
    view.work_done_stamp = datetime.today()
    view.work_done_user=user
    view.save()
    dataLogger = logging.getLogger("dataLogger")
    dataLogger.info(datetime.today().strftime("%m/%d/%Y %H:%M") + ": " +
                    user.username + " workComplete " + view.infra.location.company.name + ": " +
                    view.infra.location.street + ": " + view.title)
    joke = "Engineer " + str(view.customer_auth_user.username) + " completed work on " + str(view.title) + \
           " at " + str(view.work_date.strftime("%m/%d/%Y %H:%M"))
    subject = "Work Complete " + str(view.title)
    emailNotification(request, subject, joke)
    return HttpResponseRedirect('/dash/' + str(user.id) + '/view/'+str(view.id)+'/?work')


@login_required()
def internal_accept(request, user_id,view_id):
    user=User.objects.get(pk=user_id)
    if request.method=="GET":
        change = Change.objects.get(pk=view_id)
        change.internal_auth = True
        change.internal_auth_user = user
        change.internal_auth_date=datetime.today()
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime("%m/%d/%Y %H:%M")+": "+
                        user.username + " acceptedChange " + change.infra.location.company.name + ": " +
                        change.infra.location.street + ": " + change.title)
        change.save()
    joke = "Admin " + str(change.internal_auth_user.username) + " accepted change " + str(change.title) +  " at " + \
           str(change.internal_auth_date.strftime("%m/%d/%Y %H:%M"))
    subject = "Admin Accepted Change " + str(change.title)
    emailNotification(request, subject, joke)
    return HttpResponseRedirect('/dash/'+str(user.id)+'/view/'+str(view_id)+'/?accept')


@login_required()
def revert(request, user_id, view_id):
    user = User.objects.get(pk=user_id)
    view = Change.objects.get(pk=view_id)

    if user.groups.filter(name='admin').exists():
        view.internal_auth=False
        view.internal_auth_date=None
        view.internal_auth_user=None
    elif user.groups.filter(name='engineer').exists():
        view.work_done=False
        view.work_done_stamp=None
        view.work_done_user=None
    else:
        view.customer_auth=False
        view.customer_auth_user=None
        view.customer_auth_date=None
    view.save()
    return HttpResponseRedirect('/dash/'+str(user_id)+'/view/'+str(view_id)+'/')


@login_required()
def close(request, user_id,view_id):
    user = User.objects.get(pk=user_id)
    if request.method=="GET":
        view = Change.objects.get(pk=view_id)
        view.open = False
        view.close_user=user
        view.close_date=datetime.today()
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
                        user.username + " closedChange " + view.infra.location.company.name + ": " + view.infra.location.street + ": " + view.title)
        view.save()
    return HttpResponseRedirect('/dash/'+str(user.id)+'/view/?close')


@login_required()
def viewClosed(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        street = request.POST.get('location')
        location = Location.objects.get(street=street)
        content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'company': Company.objects.order_by('name'),
            'locs': Location.objects.order_by('company__name'),
            'closi': "ya",
            'tab': tabViewClosed
        }
        if user.groups.filter(name='admin').exists() or user.groups.filter(name='engineer').exists():
            content['changes'] = Change.objects.filter(infra__location=location, open=False).order_by('-id')
            content['company'] = Company.objects.all()
        else:
            content['changes'] = Change.objects.filter(infra__location__company=user.company, infra__location=location, open=False).order_by('-id')
            content['company'] = Company.objects.filter(name=user.company.name)
            content['locs'] = Location.objects.filter(company=user.company)
            content['client'] = 'ya'
            content['company'] = user.company
    else:
        content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'company': Company.objects.order_by('name'),
            'locs': Location.objects.order_by('company__name'),
            'changes': Change.objects.filter(open=False).order_by('infra__location__company__name'),
            'tab': tabViewClosed
            }

        if user.groups.filter(name='admin').exists() or user.groups.filter(name='engineer').exists():
            content['changes'] = Change.objects.filter(open=False).order_by('-id')
        else:
            content['changes'] = Change.objects.filter(infra__location__company=user.company, open=False).order_by('-id')
            content['locs'] = Location.objects.filter(company=user.company)
            content['client'] = 'ya'
            content['company'] = user.company
    content['closi'] = "how"
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def view(request, user_id):
    user = User.objects.get(pk=user_id)
    open = None
    if request.method == 'POST':
        street = request.POST.get('location')
        location = Location.objects.get(street=street)
        content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'company': Company.objects.order_by('name'),
            'locs': Location.objects.order_by('company__name'),
            'tab': tabView

        }
        if user.groups.filter(name='admin').exists() or user.groups.filter(name='engineer').exists():

            content['changes'] = Change.objects.filter(infra__location=location,open=True).order_by('-id')
            content['company'] = Company.objects.order_by('name')
        else:

            content['changes'] = Change.objects.filter(infra__location__company=user.company, infra__location=location, open=True).order_by('-id')
            content['company'] = Company.objects.order_by('name').filter(name=user.company.name)
            content['locs'] = Location.objects.filter(company=user.company)
            content['client'] = 'ya'
            content['company'] = user.company
    else:
        content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'company': Company.objects.order_by('name'),
            'locs': Location.objects.order_by('company__name'),
            'changes': Change.objects.filter(open=True).order_by('infra__location__company__name'),
            'tab': tabView
            }
        if user.groups.filter(name='admin').exists() or user.groups.filter(name='engineer').exists():
            content['changes'] = Change.objects.filter(open=True).order_by('-id')
        else:
            content['changes'] = Change.objects.filter(infra__location__company=user.company, open=True).order_by('-id')
            content['locs'] = Location.objects.filter(company=user.company)
            content['client'] = 'ya'
            content['company'] = user.company
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def create(request, user_id):
    user = User.objects.get(pk=user_id)
    bet=0
    if request.method == 'POST':
        infra = request.POST.get('infra')
        loc = request.POST.get('location')

        nam = infra.split(": ")[0]
        this = Infra.objects.get(location=Location.objects.get(street=loc), name=nam)
        new = Change(infra=this, title=request.POST.get('title'), description=request.POST.get('description'),
                     justification=request.POST.get('justification'), neg_impact=request.POST.get('neg'),
                     request_user=User.objects.get(username=request.POST.get('request_user').split(": ")[1]),
                     project_manager=User.objects.get(username=request.POST.get('project_user').split(": ")[1]),
                     engineer=User.objects.get(username=request.POST.get('engineer').split(": ")[1]),
                     request_date=datetime.strptime(request.POST.get('request_date'),"%m/%d/%Y").date(),
                     work_date=datetime.strptime(request.POST.get('work_date'),"%m/%d/%Y %H:%M"),
                     est_time=request.POST.get('est_time'))
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
                        user.username + " createdChange " + new.infra.location.company.name + ": " + new.infra.location.street + ": " + new.title)
        new.save()
        bet=1
    else:
        pass
    content = {
        'userr': user,
        'user': request.user,
        'tabs': getTabs(user_id),
        'users': User.objects.order_by('company__name'),
        'cusers': User.objects.filter(company=Company.objects.get(name='Pervasive Solutions')),
        'infra': Infra.objects.order_by('location__company__name'),
        'companies': Company.objects.order_by('name'),
        'locs': Location.objects.order_by('company__name'),
        'tab': tabCreate
    }
    if bet==1:
        content['good'] = "Change created"
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def delete(request, user_id, view_id):
    content = {}
    user = User.objects.get(pk=user_id)
    if request.method == 'GET':
        view = Change.objects.get(pk=view_id)
        dataLogger = logging.getLogger("dataLogger")
        dataLogger.info(datetime.today().strftime(
            "%m/%d/%Y %H:%M")+": "+
                        user.username + " deletedChange " + view.infra.location.company.name + ": " + view.infra.location.street + ": " + view.title )
        view.delete()
        content = {
            'userr': user,
            'tabs': getTabs(user_id),
            'locs': Location.objects.order_by('company__name'),
            'changes': Change.objects.filter(open=True).order_by('infra__location__company__name'),
            'tab': tabView,
            'message': "Change request deleted"
        }
        if user.groups.filter(name='admin').exists():
            content['company'] = Company.objects.all()
        else:

            content['locs'] = Location.objects.filter(company=user.company)
    if user.groups.filter(name='admin').exists():
        content['admin'] = "tru"
    return render(request, 'Dashboard/dash.html', content)


@login_required()
def logs(request, user_id):
    me = User.objects.get(pk=user_id)
    content = {}
    if request.method=="GET":
        content['tabs'] = getTabs(user_id)
        content['tab'] = tabLogs
        content['userr'] = me
        content['users'] = User.objects.order_by('company__name')
        if me.groups.filter(name='admin').exists():
            content['admin'] = "tru"
        return render(request, 'Dashboard/dash.html', content)
    else:
        processed_lines = []
        searchUser = None
        eventType = None
        if request.POST.get('user') != '':
            searchUser = User.objects.get(username=request.POST.get('user'))
        if request.POST.get('type') != '':
            eventType = request.POST.get('type')
        with open("change_management_system.log") as f:
            lines=f.readlines()
        logString=""
        start = datetime.strptime(request.POST.get('start'), "%m/%d/%Y %H:%M")
        end = datetime.strptime(request.POST.get('end'), "%m/%d/%Y %H:%M")
        for line in lines:
            split_line=line.split(" ")
            time = datetime.strptime(line.split(": ")[0], "%m/%d/%Y %H:%M")
            if (((searchUser is None) or (searchUser.username == split_line[2])) and
                    ((eventType is None) or eventType == split_line[3]) and
                    ((start <= time) and (end >= time))):
                processed_lines.append(split_line)
        for chosen_one in processed_lines:
            for one in chosen_one:
                logString += one
                logString += " "

        if logString == "":
            logString = "No logs available for the current filter"
        if "filter" in request.POST:
            return HttpResponse(logString, content_type="text/plain")
        elif "export" in request.POST:
            user=request.user
            response = HttpResponse(content_type='text/csv')
            dynamic = 'attachment; filename="log_export_' + datetime.today().strftime(
                "%m/%d/%Y") + '.csv"'
            response['Content-Disposition'] = dynamic
            writer = csv.writer(response)
            writer.writerow(['Exported By: ', user.username])
            writer.writerow(['Date: ', datetime.today().strftime("%m/%d/%Y %H:%M")])
            writer.writerow([logString])
            return response


@login_required()
def logExport(request, user_id):
    user = User.objects.get(pk=user_id)
    response = HttpResponse(content_type='text/csv')
    dynamic = 'attachment; filename="log_export_' + datetime.today().strftime(
        "%m/%d/%Y") + '.csv"'
    response['Content-Disposition'] = dynamic
    writer = csv.writer(response)
    writer.writerow(['Exported By: ', user.username])
    writer.writerow(['Date: ', datetime.today().strftime("%m/%d/%Y %H:%M")])
    logString = ""
    with open("change_management_system.log") as f:
        lines = f.readlines()
    for line in lines:
        split_line = line.split()
        for one in split_line:
            logString += one
            logString += " "
        writer.writerow([logString])
        logString = ""
    return response


@login_required()
def super_admin(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.super_admin is True:
        user.super_admin = False
    else:
        user.super_admin = True
    user.save()
    return HttpResponseRedirect('/dash/' + str(user.id) + '/view/')



