from django.conf.urls import url, handler404, handler500
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    #url(r'^login/member/$', views.member_user_login, name='member_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^booking/$', views.booking, name='booking'),
    url(r'^superadminactivity/$', views.superadminactivity, name='superadminactivity'),
    url(r'^superadmin/$', views.superadmin, name='superadmin'),
    url(r'^superadmin/create/$', views.accommodation_create, name='accommodationCreate'),
    url(r'^superadmin/(?P<pk>\d+)/update/$', views.accommodation_update, name='accommodation_update'),
    url(r'^superadmin/(?P<pk>\d+)/delete/$', views.accommodation_delete, name='accommodation_delete'),
    url(r'^index_search/$', views.search, name='search'),
    url(r'^search/$', views.accommodation_autocomplete, name='accommodation_autocomplete'),
    url(r'^cancel_booking/(?P<reservation_no>[0-9A-Za-z_\-]+)/$', views.cancel_booking, name='cancel_booking'),
    url(r'^activity/$', views.activity, name='activity'),
    url(r'^invoice/$', views.handle_invoice, name='invoice'),
    url(r'^invoice/download/(?P<bidb64>[0-9A-Za-z_\-]+)/$', views.invoice_download, name='invoice_download'),
    url(r'^accommodation/$', views.accommodation, name='accommodation'),
    url(r'^accommodation/(?P<name>[\w|\W]+)/(?P<date>\d{2}-\d{2}-\d{4})/$', views.get_availability, name='get_availability'),
    url(r'^forgotpassword/$', views.forgotpassword, name='forgotpassword'),
    url(r'^handle_booking/$', views.handle_booking, name='handle_booking'),
    url(r'^reset_new_password/(?P<uidb64>[0-9A-Za-z_\-]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.reset_password, name='resetpassword'),
    url(r'^accommodation_detail/$', views.accommodationdetail, name='accommodationdetail'),
    url(r'^edit_user_info_profile/$', views.edit_user_info_profile, name='edit_user_info_profile'),
    url(r'^edit_address_profile/$', views.edit_address_profile, name='edit_address_profile'),
    url(r'^edit_profile_picture/$', views.edit_profile_picture, name='edit_profile_picture'),
    
]


handler404 = views.handler404
handler500 = views.handler500
