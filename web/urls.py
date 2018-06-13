from django.conf.urls import url, handler404, handler500
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^booking/$', views.booking, name='booking'),
    url(r'^booking_activity/$', views.booking_activity, name='booking_activity'),
    url(r'^handle_booking_activity/$', views.handle_booking_activity, name='handle_booking_activity'),
    url(r'^superadminactivity/$', views.superadminactivity, name='superadminactivity'),
    url(r'^superadmin/$', views.superadmin, name='superadmin'),
    url(r'^superadmin/create/$', views.accommodation_create, name='accommodationCreate'),
    url(r'^superadmin/(?P<pk>\d+)/update/$', views.accommodation_update, name='accommodation_update'),
    url(r'^superadmin/(?P<pk>\d+)/delete/$', views.accommodation_delete, name='accommodation_delete'),
    url(r'^index_search/$', views.search, name='search'),
    url(r'^index_search_activity/$', views.search_activity, name='search_activity'),
    url(r'^search/$', views.accommodation_autocomplete, name='accommodation_autocomplete'),
    url(r'^search_activity/$', views.activity_autocomplete, name='activity_autocomplete'),
    url(r'^cancel_booking/(?P<reservation_no>[0-9A-Za-z_\-]+)/$', views.cancel_booking, name='cancel_booking'),
    url(r'^cancel_booking_activity/(?P<reservation_no>[0-9A-Za-z_\-]+)/$', views.cancel_booking_activity, name='cancel_booking_activity'),
    url(r'^activity/$', views.activity, name='activity'),
    url(r'^invoice/$', views.handle_invoice, name='invoice'),
    url(r'^accommodation_invoice/$', views.handle_invoice_accommodation, name='accommodation_invoice'),
    url(r'^activity_invoice/$', views.handle_invoice_activity, name='activity_invoice'),
    url(r'^invoice/download/(?P<bidb64>[0-9A-Za-z_\-]+)/$', views.invoice_download, name='invoice_download'),
    url(r'^activity_invoice/download/(?P<bidb64>[0-9A-Za-z_\-]+)/$', views.activity_invoice_download, name='activity_invoice_download'),
    url(r'^accommodation/$', views.accommodation, name='accommodation'),
    url(r'^accommodation/(?P<checkin>\d{4}-\d{2}-\d{2})&(?P<checkout>\d{4}-\d{2}-\d{2})/$', views.get_availability, name='get_availability'),
    url(r'^activity/(?P<name>[\w|\W]+)/(?P<date>\d{2}-\d{2}-\d{4})/$', views.get_availability_activity, name='get_availability_activity'),
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
