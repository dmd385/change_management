from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^view/(?P<view_id>[0-9]+)/revert/', views.revert, name='revert'),
    url(r'^view/(?P<view_id>[0-9]+)/export/', views.export, name='export'),
    url(r'^view/(?P<view_id>[0-9]+)/close/', views.close, name='close'),
    url(r'^view/(?P<view_id>[0-9]+)/internal_approve/', views.internal_accept, name='internal_accept'),
    url(r'^view/(?P<view_id>[0-9]+)/client_approve/', views.client_accept, name='client_accept'),
    url(r'^view/(?P<view_id>[0-9]+)/work_complete/', views.workDone, name='work_complete'),
    url(r'^view/(?P<view_id>[0-9]+)/delete/', views.delete, name='delete'),
    url(r'^view/(?P<view_id>[0-9]+)/', views.viewDetail, name='viewDetail'),
    url(r'^edit_user/(?P<edit_id>[0-9]+)/password_reset', views.passReset, name='passReset'),
    url(r'^edit_user/(?P<edit_id>[0-9]+)/', views.editUser, name='editUser'),
    url(r'^edit_location/(?P<location_id>[0-9]+)/delete/', views.deleteLocation, name='deleteLocation'),
    url(r'^edit_location/(?P<location_id>[0-9]+)/', views.editLocation, name='editLocation'),
    url(r'^edit_infra/(?P<infra_id>[0-9]+)/delete/', views.deleteInfra, name='deleteInfra'),
    url(r'^edit_infra/(?P<infra_id>[0-9]+)/', views.editInfra, name='editInfra'),
    url(r'^edit_company/(?P<company_id>[0-9]+)/delete/', views.deleteCompany, name= 'deleteCompany'),
    url(r'^edit_company/(?P<company_id>[0-9]+)/', views.editCompany, name= 'editCompany'),
    url(r'^log/export/', views.logExport, name='logExport'),
    url(r'^home/', views.home, name='home'),
    url(r'^log/', views.logs, name='logs'),
    url(r'^create/', views.create, name='create'),
    url(r'^view/', views.view, name='view'),
    url(r'^view_closed/', views.viewClosed, name='viewClosed'),
    url(r'^new_user/', views.newUser, name='newUser'),
    url(r'^new_company/', views.newCompany, name='newCompany'),
    url(r'^new_location/', views.newLocation, name='newLocation'),
    url(r'^new_infra/', views.newInfra, name='newInfra'),
    url(r'^new_inftype/', views.newInfraType, name='newInfraType'),
    url(r'^new_os/', views.newOS, name='newOs'),
    url(r'^calendar/', views.calendar, name='calendar'),
    url(r'^choose/', views.choose, name='choose'),
    url(r'^super_admin/', views.super_admin, name='super_admin'),
    url(r'^$', RedirectView.as_view(url='choose/')),
]