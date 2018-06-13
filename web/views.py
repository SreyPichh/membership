# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import xmlrpclib
from datetime import datetime
import requests
from requests import Session, Request

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as user_login, authenticate, logout as user_logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template.context import Context
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from weasyprint import CSS, HTML
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import RegisterForm, AccForm, AuthenticationForm, EditProfileImage, EmailForgotPassword, ResetPassword, \
    BookingList, BookingRecord, BookingRecordActivity
from .models import User, MemberType, UserPoint, Accommodation, BookingInfo, Activity, BookingActivity

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)

# url = "http://110.74.203.150"
# db = 'Asia2Asia'
# username = 'admin'
# password = 'admin73'

# common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
# uid = common.authenticate(db, username, password, {})
# models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

b_url = "http://10.10.1.2:8069/"
# or "http://201.100.100.12:8069" (or whatever the ip is)
url = "{}web/session/authenticate".format(b_url)

db = "TokyoHotel"
user = "admin"
passwd = "admin_odoo"


# Create your views here.

def accommodation_autocomplete(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        accommodations = Accommodation.objects.filter(name__icontains=query)
        results = []
        for accommodation in accommodations:
            place_json = accommodation.name
            results.append(place_json)
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


def activity_autocomplete(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        activitys = Activity.objects.filter(name__icontains=query)
        results = []
        for activity in activitys:
            place_json = activity.name
            results.append(place_json)
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        accommodation = Accommodation.objects.all()
        # page = request.GET.get('page',1)
        # logging.debug(page)
        # paginator = Paginator(accommodation, 4)

        # try:
        #     per_page = paginator.page(page)
        # except PageNotAnInteger:
        #     logging.debug("Fallback in PageNotInteger Exception")
        #     per_page = paginator.page(1)
        # except EmptyPage:
        #     logging.debug("Fallback in EmptyPage Exception")
        #     per_page = paginator.page(paginator.num_pages)

        bookinglist = BookingList()
        logging.debug(bookinglist)
        return render(request, 'index.html', context={'accommodation': accommodation, 'bookinglist': bookinglist})


def search(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        query = request.GET.get("search")
        if query:
            # logging.debug(query)
            accommodation = Accommodation.objects.filter(name__icontains=query)
            logging.debug(accommodation)
            return render(request, 'accommodation.html', {'accommodation': accommodation})
        else:
            logging.debug("Fallback to else")
            accommodation = None
            not_found = "Not Found"
            return render(request, 'index.html', {'not_found': not_found, 'accommodation': accommodation})


def search_activity(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        query = request.GET.get("search")
        if query:
            logging.debug(query)
            activity = Activity.objects.filter(name__icontains=query)
            logging.debug(activity)
            return render(request, 'activity.html', {'activity': activity})
        else:
            logging.debug("Fallback to else")
            activity = None
            not_found = "Not Found"
            return render(request, 'activity.html', {'not_found': not_found, 'activity': activity})


def superadmin(request):
    if request.user.is_authenticated() and request.user.is_admin:
        accommodation = Accommodation.objects.all()
        return render(request, 'superadmin.html', {'accommodation': accommodation})
    else:
        if request.method == 'POST':
            logging.debug("Request use post method")
            form = AuthenticationForm(data=request.POST)
            logging.debug('Pre Check form')
            if form.is_valid():
                logging.debug('Form already Check')
                logging.debug((request.POST['email']))
                logging.debug((request.POST['password']))
                user = authenticate(email=request.POST['email'], password=request.POST['password'])
                logging.debug(user)
                if user is not None:
                    if user.is_active:
                        user_login(request, user)
                        return redirect('/profile/', {'user': user})
                else:
                    error_message = "your email or password is incorrect"
                    return render(request, 'login.html', {'error_message': error_message})
        else:
            logging.debug("Request use get method.")
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def superadminactivity(request):
    activity = Activity.objects.all()
    return render(request, 'superadminactivity.html', {'activity': activity})


def save_accommodation_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            status = form.save()
            data['form_is_valid'] = True
            accommodations = Accommodation.objects.all()
            data['html_accommodation_list'] = render_to_string('superadmin.html', {
                'accommodations': accommodations
            })
        else:
            data['form_is_valid'] = False

    context = {
        'form': form
    }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def save_or_update(request, action, method, data=None, pk=None, files=None):
    context = dict()
    if action == 'create':
        logging.debug('CREATE RECORD')
        if method == 'POST':
            logging.debug('CREATE RECORD => POST')
            if files is not None:
                form = AccForm(data, files)
            else:
                form = AccForm(data)
            logging.debug(form)
            if form.is_valid():
                saved_record = form.save()
                rendered_record = render_to_string('partial_accommodation_list_item.html',
                                                   {'accommodation': saved_record}, request=request)
                context.update({
                    'form_is_valid': True,
                    'action': 'create',
                    'saved_record': rendered_record
                })
                return context

            else:
                logging.debug("RECORD DOESNT SAVE")
                context.update({
                    'form_is_valid': False,
                    'error': {
                        'code': 405,
                        'message': 'method not allowed'
                    }

                })
                return context
        elif method == 'GET':
            form = AccForm()
            rendered_form = render_to_string('partial_accommodation_create.html', {'form': form}, request=request)
            context.update({
                'form_is_valid': True,
                'action': 'create',
                'html_form': rendered_form
            })
            return context

    elif action == 'update':
        if not pk:
            context.update({
                'form_is_valid': False,
                'action': 'update'
            })
            return context

        accommodation = get_object_or_404(Accommodation, pk=pk)

        if method == 'POST':
            if not data:
                context.update({
                    'form_is_valid': False,
                    'action': 'update'
                })
                return context

            # form = AccForm(data, instance=accommodation)
            if files is not None:
                form = AccForm(data, files, instance=accommodation)
            else:
                form = AccForm(data)

            if form.is_valid():
                updated_record = form.save()
                rendered_record = render_to_string('partial_accommodation_list_item.html',
                                                   {'accommodation': updated_record}, request=request)
                context.update({
                    'form_is_valid': True,
                    'action': 'update',
                    'updated_record': rendered_record
                })
                logging.debug(context)
                return context
        elif method == 'GET':
            form = AccForm(instance=accommodation)
            rendered_form = render_to_string('partial_accommodation_update.html', {'form': form}, request=request)
            context.update({
                'form_is_valid': True,
                'action': 'update',
                'html_form': rendered_form
            })

            return context


def accommodation_create(request):
    context = dict()
    if request.method == 'POST':
        data = request.POST
        logging.debug(data)
        logging.debug(request.FILES)
        logging.debug("CREATE DATA")
        create_status = save_or_update(request, 'create', 'POST', data, files=request.FILES)
        return JsonResponse(create_status)

    elif request.method == 'GET':
        rendered_form = save_or_update(request, 'create', 'GET')
        return JsonResponse(rendered_form)
    else:
        context.update({
            'form_is_valid': False,
            'error': {
                'code': 405,
                'message': 'method not allowed.'
            }
        })
        return JsonResponse(data)


def accommodation_update(request, pk):
    context = dict()
    if request.method == 'POST':
        data = request.POST
        updated_status = save_or_update(request=request, action='update', method='POST', data=data, files=request.FILES,
                                        pk=pk)
        return JsonResponse(updated_status)

    elif request.method == 'GET':
        rendered_form = save_or_update(request=request, action='update', method='GET', pk=pk)
        return JsonResponse(rendered_form)

    else:
        context.update({
            'form_is_valid': False,
            'error': {
                'code': 405,
                'message': 'method not allowed.'
            }
        })
        return JsonResponse(data)


def accommodation_delete(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    data = dict()
    if request.method == 'POST':
        accommodation.delete()
        data.update({
            'form_is_valid': True,
            'action': 'delete'
        })
    else:
        context = {'accommodation': accommodation}
        data['html_form'] = render_to_string('partial_accommodation_delete.html',
                                             context,
                                             request=request,
                                             )

        return JsonResponse(data)


# LOGIN A USER TO A WEB
def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == 'POST':
            logging.debug("Request use post method")
            form = AuthenticationForm(data=request.POST)
            logging.debug('Pre Check form')
            if form.is_valid():
                logging.debug('Form already Check')
                logging.debug((request.POST['email']))
                logging.debug((request.POST['password']))
                user = authenticate(email=request.POST['email'], password=request.POST['password'])
                logging.debug(user)
                if user is not None:
                    if user.is_active:
                        user_login(request, user)
                        return redirect('/profile/', {'user': user})
                else:
                    error_message = "your email or password is incorrect"
                    return render(request, 'login.html', {'error_message': error_message})
        else:
            logging.debug("Request use get method.")
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


@csrf_protect
def logout(request):
    """
    Logout
    :param request:
    :return:
    """
    user_logout(request)
    return redirect("/")


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None, request.FILES or None)
        print (form)
        if form.is_valid():
            print ("Yes You done it")
            save_it = form.save(commit=False)
            save_it.save()
            user = User.object.get(email=request.POST['email'])
            logging.debug(user)
            # member_type = MemberType.objects.get(name='Brown')
            # member_type = get_object_or_404(MemberType, pk=mid)
            # user.member_type = member_type
            # user.save()
            # point = UserPoint(pid=user)
            # point.save()

            # THIS IS VERIFICATION EMAIL
            # send_mail(subject, message, from_email, to_list, fail_silently=True)
            # subject = 'Thank you for using vkirirom service'
            # message = 'Welcome to vkirirom Pine Resort!'
            # from_email = settings.EMAIL_HOST_USER
            # to_list = [save_it.email]
            # send_mail(subject, message, from_email, to_list, fail_silently=True)
            # messages.success(request, 'Thank you for using our service.')
            print ("Yes Form save")
            return redirect('/login')
        else:
            print ("Form not save")
            return render(request, 'signup.html', {'form': form})

    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})


@csrf_protect
def forgotpassword(request):
    '''
    Forgot password
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = EmailForgotPassword(data=request.POST)
        logging.debug(form)
        if form.is_valid():
            logging.debug('Form is valid')
            logging.debug(request.POST['email'])
            user = User.object.get(email=request.POST['email'])
            if user:
                logging.debug("User is exist")
                # send_mail(subject, messages, from_email, to_list, fail_silently=True)
                token = default_token_generator.make_token(user)
                logging.debug(token)
                current_site = get_current_site(request)
                logging.debug(current_site.domain)
                subject = 'Reset new password'
                from_email = 'vKirirom@kit.com'
                to_list = [form.cleaned_data['email']]
                logging.debug(form.cleaned_data['email'])
                message = render_to_string('change_pass_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': user.uuid,
                    'token': token
                })
                logging.debug(message)
                if send_mail(subject, message, from_email, to_list, fail_silently=True):
                    messages.success(request, "thank you so much")
                    return render(request, 'forgot-password-success.html', {})
                else:
                    return
            else:
                error_message = 'Sorry, we cannot find your email in our database.'
                return render(request, 'forgot-password.html', {'error_message': error_message})
    else:
        form = EmailForgotPassword()
        return render(request, 'forgot-password.html', {'form': form})


@csrf_protect
def reset_password(request, uidb64=None, token=None, *args):
    if request.method == 'POST':
        form = ResetPassword(data=request.POST)
        if form.is_valid():
            try:
                password = form.clean_new_confirm()
                logging.debug(password)
            except ValidationError:
                message_error = "The two password fields didn't match."
                return render(request, 'reset-password.html',
                              {'form': form, 'uid': uidb64, 'token': token, 'message_error': message_error})
            logging.debug(password)
            user = User.object.get(uuid=uidb64)
            user.set_password(password)
            user.save()
            logging.debug(user.password)
            return redirect('/login')
    else:
        uidb64 = uidb64
        user = User.object.get(uuid=uidb64)
        logging.debug(user)
        logging.debug(default_token_generator.check_token(user, token))
        if user and default_token_generator.check_token(user, token):
            form = ResetPassword()
            return render(request, 'reset-password.html', {'form': form, 'uid': uidb64, 'token': token})
        else:
            logging.debug('token is not correct')
            return


@csrf_protect
def profile(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    else:
        form = EditProfileImage()
        return render(request, 'profile.html', {'form': form})


@csrf_protect
def edit_user_info_profile(request):
    """
    Edit user information by AJAX
    :param request:
    :return:
    """
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']

        user = User.object.get(id=request.user.id)
        user.name = name
        user.email = email
        user.phone = phone
        user.save()
        return HttpResponse('Information Updated!')


@csrf_protect
def edit_address_profile(request):
    """
    Edit User address by AJAX
    :param request:
    :return:
    """
    if request.method == 'POST':
        state = request.POST['state']
        city = request.POST['city']
        street = request.POST['street']
        house_number = request.POST['house_number']
        zip_num = request.POST['zip']

        user = User.object.get(id=request.user.id)
        if state is not None:
            user.state = state
        if city is not None:
            user.city = city
        if street is not None:
            user.street = street
        if house_number is not None:
            user.house_num = house_number
        if zip_num is not None:
            user.zip_num = zip_num
        user.save()
        return HttpResponse('Address Information Updated')


@csrf_protect
def edit_profile_picture(request):
    """
    Edit Profile Picture
    :param request:
    :return:
    """
    # if request.is_ajax():
    #     logging.debug(request.is_ajax())
    #     logging.debug(request.method)
    #     if request.method == 'POST':
    #         logging.debug()
    #         return JsonResponse({'datasaved': True})
    #     else:
    #         return JsonResponse({'notpost': 'test'})
    #
    # else:
    #     return JsonResponse({'notajax': 'test'})

    if request.method == "POST":
        form = EditProfileImage(data=request.POST, files=request.FILES)
        logging.debug(form)
        logging.debug(request.FILES)
        logging.debug(request.POST)
        if form.is_valid():
            logging.debug('Form is valid!!')
            image = request.FILES['profile_pic']
            logging.debug(image)
            user = User.object.get(id=request.user.id)
            logging.debug(user)
            user.profile_pic = image
            user.save()
            logging.debug(user.profile_pic.url)
            return redirect('/profile')
        else:
            return JsonResponse({'FormInvalid': True})


def accommodationdetail(request):
    return render(request, 'accommodation-detail.html', {})


@csrf_protect
def booking(request):
    if request.method == 'POST':
        logging.debug(request.POST)
        form = BookingList(data=request.POST)
        logging.debug(type(form))
        if form.is_valid():
            logging.debug("form is valid.")
            booking_list = json.loads(request.POST['list-booking'])
            logging.debug(booking_list)
            logging.debug(len(booking_list))
            selected_room = []
            total_price = 0
            for i in range(0, len(booking_list)):
                room = Accommodation.objects.get(name=booking_list[i]['name'])
                logging.debug(room)
                logging.debug(type(room.price))
                logging.debug((type(room.quantity)))
                # selected room
                selected_room.append({"room": room})
                logging.debug(selected_room)
                logging.debug(selected_room[i])
                # calculate price
                night = int((datetime.strptime(request.POST['checkout-date'], "%m/%d/%Y") - datetime.strptime(
                    request.POST['checkin-date'], "%m/%d/%Y")).days)
                total_price = room.price * int(booking_list[i]['value']) * night
                logging.debug(total_price)
                selected_room[i]['total_price'] = total_price
                # person_choice for each room
                total_person_per_room = int(booking_list[i]['value']) * room.quantity
                logging.debug(total_person_per_room)
                room_amount = int(booking_list[i]['value'])
                logging.debug(room_amount)
                selected_room[i]['amount'] = room_amount

                # room_id
                selected_room[i]['room_id'] = 'room' + str(i + 1)
                logging.debug(selected_room[i])
                logging.debug(len(selected_room))

            logging.debug(selected_room)

            # checkin and checkout date
            checkin = datetime.strptime(request.POST['checkin-date'], "%m/%d/%Y")
            logging.debug(checkin)
            logging.debug(type(checkin))
            checkout = datetime.strptime(request.POST['checkout-date'], "%m/%d/%Y")
            logging.debug(checkout)
            logging.debug(type(checkout))

            # number of night
            night_num = checkout - checkin
            logging.debug(night_num.days)

            # total price
            totally_price = 0
            for a in selected_room:
                totally_price = totally_price + a['total_price']
                logging.debug(totally_price)

            # user
            user = User.object.get(id=request.user.id)
            logging.debug(user)
            booking_record = BookingRecord()
            return render(request, 'booking.html',
                          {'selected_room': selected_room, 'checkin': checkin, 'checkout': checkout, 'user': user,
                           'night_num': night_num.days, 'totally_price': totally_price,
                           'booking_record': booking_record})
        else:
            logging.debug("form is not valid")
    else:
        return redirect("/")


@csrf_protect
def booking_activity(request):
    if request.method == 'POST':
        logging.debug(request.POST)
        form = BookingList(data=request.POST)
        logging.debug(form)
        logging.debug(type(form))
        if form.is_valid():
            logging.debug("form is valid.")
            booking_list = json.loads(request.POST['list-booking'])
            logging.debug(booking_list)
            logging.debug(len(booking_list))
            selected_activity = []
            total_price = 0
            for i in range(0, len(booking_list)):
                activity = Activity.objects.get(name=booking_list[i]['name'])
                logging.debug(activity)
                logging.debug(type(activity.price))
                logging.debug((type(activity.quantity)))
                # selected activity
                selected_activity.append({"activity": activity})
                logging.debug(selected_activity)
                logging.debug(selected_activity[i])
                # calculate price
                pax = int((datetime.strptime(request.POST['checkout-date'], "%m/%d/%Y") - datetime.strptime(
                    request.POST['checkin-date'], "%m/%d/%Y")).days)
                total_price = activity.price * int(booking_list[i]['value']) * pax
                logging.debug(total_price)
                selected_activity[i]['total_price'] = total_price
                # person_choice for each activity
                total_person_per_activity = int(booking_list[i]['value']) * activity.quantity
                logging.debug(total_person_per_activity)
                # activity_choice = ACM_Choice.get_person_choice(total_person_per_activity)
                # logging.debug(activity_choice)
                # selected_activity[i]['activity_choice'] = activity_choice
                # selected activity amount
                activity_amount = int(booking_list[i]['value'])
                logging.debug(activity_amount)
                selected_activity[i]['amount'] = activity_amount

                # activity_id
                selected_activity[i]['activity_id'] = 'activity' + str(i + 1)
                logging.debug(selected_activity[i])
                logging.debug(len(selected_activity))

            logging.debug(selected_activity)

            # checkin and checkout date
            checkin = datetime.strptime(request.POST['checkin-date'], "%m/%d/%Y")
            logging.debug(checkin)
            logging.debug(type(checkin))
            checkout = datetime.strptime(request.POST['checkout-date'], "%m/%d/%Y")
            logging.debug(checkout)
            logging.debug(type(checkout))

            # number of pax
            pax_num = checkout - checkin
            logging.debug(pax_num.days)

            # total price
            totally_price = 0
            for a in selected_activity:
                logging.debug("IN LOOP")
                logging.debug(a['total_price'])
                totally_price = totally_price + a['total_price']
                logging.debug(totally_price)

            # user
            user = User.object.get(id=request.user.id)
            logging.debug(user)
            booking_record = BookingRecordActivity()
            logging.debug(booking_record)
            return render(request, 'booking_activity.html',
                          {'selected_activity': selected_activity, 'checkin': checkin, 'checkout': checkout,
                           'user': user,
                           'pax_num': pax_num.days, 'totally_price': totally_price,
                           'booking_record': booking_record})
        else:
            logging.debug("form is not valid")
    else:
        return redirect("/")


@csrf_protect
def handle_booking_activity(request):
    if request.method == "POST":
        logging.debug(request.POST)
        form = BookingRecordActivity(data=request.POST)
        logging.debug(form)
        if form.is_valid():
            logging.debug("Form is valid")
            booking_activity = form.save(commit=True)
            logging.debug(booking_activity)
            logging.debug(booking_activity.checkin_date)
            booking_activity.user = User.object.get(id=request.user.id)
            logging.debug(booking_activity.user)
            booking_activity.save()
            logging.debug("I have save form")
            subject = 'Booking accommodation'
            message = 'Hello Administrator! I am sending this to alert you that user name %s has booked %s' % (
            booking_activity.user, booking_activity.act_data)

            from_email = settings.EMAIL_HOST_USER
            receiver = ['phansreypich15@kit.edu.kh']
            logging.debug("this is here and just here!")

            send_mail(subject, message, from_email, receiver, fail_silently=True)
            logging.debug("successfully send email!")
            logging.debug(receiver)
        else:
            logging.debug("Form is Invalid")
        return redirect("/invoice")


@csrf_protect
def handle_booking(request):
    if request.method == "POST":
        logging.debug(request.POST)
        form = BookingRecord(data=request.POST)
        logging.debug("------------*****-------------")
        logging.debug(form)
        if form.is_valid():
            logging.debug("Form is valid")
            booking_info = form.save(commit=True)
            logging.debug(booking_info)
            logging.debug(booking_info.checkin_date)
            booking_info.user = User.object.get(id=request.user.id)
            logging.debug(booking_info.user)
            booking_info.save()
            logging.debug("I have save form")

            subject = 'Booking accommodation'
            message = 'Hello Administrator! I am sending this to alert you that user name %s has booked accommodation' % (
                request.user)
            from_email = settings.EMAIL_HOST_USER
            receiver = ['phansreypich15@kit.edu.kh']
            logging.debug("this is here and just here!")
            send_mail(subject, message, from_email, receiver, fail_silently=True)
            logging.debug("successfully send email!")
            logging.debug(receiver)
        else:
            logging.debug("Form is Invalid")

        return redirect("/invoice")


# @csrf_protect
# def handle_booking(request):
#     if request.method == "POST":
#         logging.debug(request.POST)
#         form = BookingRecord(data=request.POST)
#         if form.is_valid():
#             logging.debug("Form is valid")
#             booking_info = form.save(commit=True)
#             logging.debug(booking_info)
#             logging.debug(booking_info.checkin_date)
#             booking_info.user = User.object.get(id=request.user.id)
#             logging.debug(booking_info.user)
#             booking_info.save()
#             logging.debug("I have save form")
#         else:
#             logging.debug("Form is Invalid")
#
#         subject = 'Booking accommodation'
#
#         message = 'Hello Administrator! I am sending this to alert you that user name %s has booked accommodation' % (
#             request.user)
#         from_email = settings.EMAIL_HOST_USER
#         receiver = ['phansreypich15@kit.edu.kh']
#         send_mail(subject, message, from_email, receiver, fail_silently=True)
#         return redirect("/invoice")


def handle_invoice(request):
    if request.method == 'GET':
        return render(request, "invoice.html")


def handle_invoice_accommodation(request):
    if request.method == "GET":
        logging.debug(request.user)
        invoices = []
        user = User.object.get(id=request.user.id)
        all_invoice = BookingInfo.objects.filter(user=user, status=1)
        logging.debug(all_invoice)
        for invoice in all_invoice:
            if int(invoice.status) == 1:
                invoices.append(invoice)
        return render(request, 'accommodation_invoice.html', {'invoices': invoices})


def handle_invoice_activity(request):
    if request.method == "GET":
        logging.debug(request.user)
        invoices = []
        user = User.object.get(id=request.user.id)
        all_invoice = BookingActivity.objects.filter(user=user)
        logging.debug(all_invoice)
        for invoice in all_invoice:
            if int(invoice.status) == 1:
                logging.debug("you go your invoice.")
                # add invoice into invoices
                invoices.append(invoice)
                logging.debug(invoice)
                logging.debug(invoices)
            else:
                logging.debug("Holy moly shit invoice.")
        return render(request, 'activity_invoice.html', {'invoices': invoices})


def activity(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        activity = Activity.objects.all()
    return render(request, 'activity.html', {'activity': activity})


def accommodation(request):
    accommodation = Accommodation.objects.all()
    return render(request, 'accommodation.html', {'accommodation': accommodation})


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


# Get Availability
def get_availability(request, checkin, checkout):
    date_str = datetime.strptime(checkin, "%Y-%m-%d").strftime("%b. %d, %Y")
    logging.debug(date_str)
    date_checkin = datetime.strptime(date_str, "%b. %d, %Y")
    logging.debug(date_checkin)
    date_string = datetime.strptime(checkout, "%Y-%m-%d").strftime("%b. %d, %Y")
    date_checkout = datetime.strptime(date_string, "%b. %d, %Y")
    logging.debug(date_checkout)

    s = Session()

    data = {
        'jsonrpc': '2.0',
        'params': {
            'context': {},
            'db': db,
            'login': user,
            'password': passwd,
        },
    }
    json_data = json.dumps(data)

    headers = {
        'Content-type': 'application/json'
    }

    req = Request('POST', url, data=json_data, headers=headers)

    logging.debug(req)

    prepped = req.prepare()
    logging.debug("0000000000")

    resp = s.send(prepped)

    session_id = json.loads(resp.text)['result']['session_id']
    logging.debug(session_id)

    date = {'check_in': '2018-05-08 07:00:00', 'check_out': '2018-05-10 12:00:00'}
    get_room_availabilities = 'get_room_availabilities/' + str(date)
    logging.debug(get_room_availabilities)
    res = requests.get(b_url + get_room_availabilities, cookies={'session_id': str(session_id)})

    logging.info("***************************")

    return HttpResponse(res.text)
    # if request.method == "POST":
    #     availability = 0
    #     reserved = 0
    #     date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%b. %d, %Y")
    #     date_checkin = datetime.strptime(date_str, "%b. %d, %Y")
    #     query_rooms = BookingInfo.objects.filter(status__in=[1, 2])
    #     #logging.debug(query_rooms)
    #     for room in query_rooms:
    #         #logging.debug(date_checkin < datetime.strptime(str(room.checkout_date), '%b. %d, %Y'))
    #         if date_checkin < datetime.strptime(str(room.checkout_date), '%b. %d, %Y'):
    #             #logging.debug(room.room_data)
    #             room_data = json.loads(room.room_data)
    #             #logging.debug(room_data)
    #
    #             for data in room_data:
    #                 if (data['name']).lower() == name.lower():
    #                     reserved = reserved + int(data['amount'])
    #
    #     accom = Accommodation.objects.get(name=name)
    #     availability = int(accom.amount) - reserved
    #     logging.debug('this is return value:')
    #     logging.debug(availability)
    #
    #     return HttpResponse(availability)


# def get_availability_accommodation(request, name, date):
#     if request.method == "POST":
#         availability = 0
#         reserved = 0
#         date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%b. %d, %Y")
#         date_checkin = datetime.strptime(date_str, "%b. %d, %Y")
#         query_rooms = BookingInfo.objects.filter(status__in=[1, 2])
#         #logging.debug(query_rooms)
#         for room in query_rooms:
#             #logging.debug(date_checkin < datetime.strptime(str(room.checkout_date), '%b. %d, %Y'))
#             if date_checkin < datetime.strptime(str(room.checkout_date), '%b. %d, %Y'):
#                 #logging.debug(room.room_data)
#                 room_data = json.loads(room.room_data)
#                 #logging.debug(room_data)
#
#                 for data in room_data:
#                     if (data['name']).lower() == name.lower():
#                         reserved = reserved + int(data['amount'])
#
#         accom = Accommodation.objects.get(name=name)
#         availability = int(accom.amount) - reserved
#         logging.debug('this is return value:')
#         logging.debug(availability)
#
#     return HttpResponse(availability)

def get_availability_activity(request, name, date):
    if request.method == "POST":
        logging.debug(type(date))
        availability = 0
        reserved = 0
        date_str = datetime.strptime(date, "%m-%d-%Y").strftime("%b. %d, %Y")
        date_checkin = datetime.strptime(date_str, "%b. %d, %Y")
        logging.debug(type(date_checkin))
        query_activity = BookingActivity.objects.filter(status__in=[1, 2])
        logging.debug(query_activity)
        for activity in query_activity:
            logging.debug(datetime.strptime(str(activity.checkout_date), '%b. %d, %Y'))
            if date_checkin:
                logging.debug(date_checkin)
                logging.debug(activity.act_data)
                act_data = json.loads(activity.act_data)
                logging.debug(act_data)

                for data in act_data:
                    if (data['name']).lower() == name.lower():
                        reserved = reserved + int(data['amount'])
                        logging.debug(reserved)

        activiti = Activity.objects.get(name=name)
        availability = int(activiti.amount) - reserved
        logging.debug('this is return value:')
        logging.debug(availability)

        return HttpResponse(availability)


def invoice_download(request, bidb64=None, *args):
    invoice = BookingInfo.objects.get(bid=bidb64)

    context = {
        'invoice': invoice
    }

    html_string = render_to_string('p_invoice.html', {'invoice': invoice})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/%s.pdf' % invoice.reservation_no)

    fs = FileSystemStorage('/tmp')
    with fs.open('%s.pdf' % invoice.reservation_no) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice_%s.pdf"' % invoice.reservation_no
        return response


def activity_invoice_download(request, bidb64=None, *args):
    invoice = BookingActivity.objects.get(bid=bidb64)

    context = {
        'invoice': invoice
    }

    html_string = render_to_string('activity_pdf_invoice.html', {'invoice': invoice})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/%s.pdf' % invoice.reservation_no)

    fs = FileSystemStorage('/tmp')
    with fs.open('%s.pdf' % invoice.reservation_no) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice_%s.pdf"' % invoice.reservation_no
        return response


def cancel_booking(request, reservation_no):
    """
    : Cancel Booking by changing status to Cancelled
    :param request:
    :param reservation_no:
    :return:
    :status:(1, 'Confirm'),
            (2, 'Operated'),
            (3, 'Cancelled'),
            (4, 'Completed')
    """
    # delete object in Booking_Info
    booking_item = BookingInfo.objects.get(reservation_no=reservation_no)
    booking_item.status = 3
    booking_item.save()
    subject = 'Canceling booked accommodation'
    message = 'Hello Administrator! I am sending this to alert you that user name %s has canceled booked' % (
        request.user)
    from_email = settings.EMAIL_HOST_USER
    receiver = ['phansreypich15@kit.edu.kh']
    logging.debug("this is here and just here!")
    send_mail(subject, message, from_email, receiver, fail_silently=True)
    logging.debug("successfully send email!")
    logging.debug(receiver)
    return redirect('/accommodation_invoice')


def cancel_booking_activity(request, reservation_no):
    """
    : Cancel Booking by changing status to Cancelled
    :param request:
    :param reservation_no:
    :return:
    :status:(1, 'Confirm'),
            (2, 'Operated'),
            (3, 'Cancelled'),
            (4, 'Completed')
    """
    # delete object in Booking_Info
    booking_item = BookingActivity.objects.get(reservation_no=reservation_no)
    logging.debug(booking_item)
    booking_item.status = 3
    booking_item.save()
    subject = 'Canceling booked accommodation'
    message = 'Hello Administrator! I am sending this to alert you that user name %s has canceled booked' % (
        request.user)
    from_email = settings.EMAIL_HOST_USER
    receiver = ['phansreypich15@kit.edu.kh']
    logging.debug("this is here and just here!")
    send_mail(subject, message, from_email, receiver, fail_silently=True)
    logging.debug("successfully send email!")
    logging.debug(receiver)
    return redirect('/activity_invoice')

