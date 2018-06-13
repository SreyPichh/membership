# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import string
import uuid as uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.crypto import random
import logging
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)
# Create your models here.

today = datetime.today()

VALIDATION_TYPES = (
    ('IDC', 'Identity Card'),
    ('PSP', 'PASSPORT')
)

ROOM_TYPES = (
    ('BUNGALOW DOUBLE ROOM', 'Bungalow Double Room'),
    ('BUNGALOW TWIN ROOM', 'Bungalow Twin Room'),
    ('VILLA JASMINE', 'Villa Jasmine'),
    ('VILLA SUITE', 'Villa Suite'),
    ('KHMER COTTAGE', 'Khmer cottage'),
    ('LUXURY TENT', 'Luxury Tent'),
    ('PIPE ROOM', 'Pipe Room'),
    ('CAMPING', 'Camping')
)


def random_string(length, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(length))


def handle_upload_profile(instance, filename):
    filename_string = random_string(30, string.ascii_lowercase + string.digits) + ".png"
    return "{}/{}/{}/{}".format(instance.uuid, 'profile', today.strftime('%Y/%m/%d'),
                                str(instance.uuid) + filename_string)


def handle_upload_validation_img(instance, filename):
    filename_string = random_string(30, string.ascii_lowercase + string.digits) + ".png"
    return "{}/{}/{}/{}".format(instance.uuid, 'validation_image', today.strftime('%Y/%m/%d'),
                                str(instance.uuid) + filename_string)


def handle_upload_membership_img(instance, filename):
    filename_string = random_string(30, string.ascii_lowercase + string.digits) + ".png"
    return "{}/{}/{}/{}".format(instance.mid, 'membership', today.strftime('%Y/%m/%d'),
                                str(instance.mid) + filename_string)


def handle_upload_activity_img(instance, filename):
    filename_string = random_string(30, string.ascii_lowercase + string.digits) + ".png"
    return "{}/{}/{}/{}".format(instance.actid, 'activity', today.strftime('%Y/%m/%d'),
                                str(instance.actid) + filename_string)


# Handle Default Member type
def handle_default_member():
    return MemberType.objects.get(name='Brown')


# Handle member type amount
def handle_number_of_user_brown():
    brown = MemberType.objects.get(name='Brown')
    n_brown = User.object.filter(member_type=brown).count()
    return n_brown


# Handle Reservation number generator
def handle_reservation_number():
    """
    Reservation Number format: R + Current_Year + 5 digit number (00001, 00002, 00003, .....)
    get the last reservation number by get all objects in BookingInfo
    :return:
    """

    current_year = str(datetime.now().year)
    if (len(BookingInfo.objects.all()) > 0):
        all_record = BookingInfo.objects.all()
        last_item = all_record[len(all_record) - 1]
        last_reservation_no = last_item.reservation_no
        last_number = last_reservation_no[5:]
        last_reservation_year = last_reservation_no[1:5]
        new_number = int(last_number) + 1
        if last_reservation_year == current_year:
            new_reservation = 'R' + last_reservation_year + '{0:05}'.format(new_number)
        else:
            new_reservation = 'R' + current_year + '{0:05}'.format(1)
        return new_reservation
    else:
        new_reservation = 'R' + current_year + '{0:05}'.format(1)
        return new_reservation


def handle_reservation_number_activity():
    current_year = str(datetime.now().year)
    if (len(BookingActivity.objects.all()) > 0):
        all_record = BookingActivity.objects.all()
        last_item = all_record[len(all_record) - 1]
        last_reservation_no = last_item.reservation_no
        last_number = last_reservation_no[5:]
        last_reservation_year = last_reservation_no[1:5]
        new_number = int(last_number) + 1
        if last_reservation_year == current_year:
            new_reservation = 'R' + last_reservation_year + '{0:05}'.format(new_number)
        else:
            new_reservation = 'R' + current_year + '{0:05}'.format(1)
        return new_reservation
    else:
        new_reservation = 'R' + current_year + '{0:05}'.format(1)
        return new_reservation


class WebUserManager(BaseUserManager):
    def create_user(self, name, email, phone, password=None, **kwargs):
        if not name:
            raise ValueError('User must have a name')
        if not email:
            raise ValueError('User must have an email')
        if not phone:
            raise ValueError('User must have a phone number')
        user = self.model(
            name=name,
            email=email,
            phone=phone,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone, password, **kwargs):
        u = self.create_user(name, email, phone, password=password, **kwargs)
        u.is_admin = True
        u.save(using=self._db)
        return u


class MemberType(models.Model):
    """
    Membership Information and Type
    """
    mid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=handle_upload_membership_img)
    description = models.CharField(max_length=2000)
    n_member = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_default_type(self):
        default = MemberType(name='Brown')
        return default


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, unique=True, max_length=250, blank=False)
    phone = models.IntegerField(null=False, blank=False)
    password = models.CharField(blank=False, max_length=100, null=False)
    profile_pic = models.ImageField(upload_to=handle_upload_profile, default='blank-profile-picture.png')
    validation_type = models.CharField(max_length=50, choices=VALIDATION_TYPES)
    validation_img = models.ImageField(upload_to=handle_upload_validation_img, null=False, blank=False)
    state = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    street = models.CharField(blank=True, null=True, max_length=100)
    house_num = models.CharField(blank=True, null=True, max_length=100)
    zip_num = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(blank=True, default=False)
    member_type = models.ForeignKey(MemberType, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    object = WebUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', ]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_profile_pic(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return '/media/blank-profile-picture.png'

    def get_full_name(self):
        return self.name.strip()

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class UserPoint(models.Model):
    """
    User Point Allocation
    this part need to add more, just demo only
    """
    pid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ammount = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)


class Accommodation(models.Model):
    """
    Accommodation Detail
    Status = True  ==> Available
    Status = False ==> Reserved
    """
    aid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=ROOM_TYPES)
    amount = models.IntegerField()
    price = models.FloatField()
    quantity = models.IntegerField(default=2)
    detail = models.TextField(max_length=1000)
    image = models.FileField(upload_to='Accommodation/')
    image_360 = models.FileField(upload_to='Accommodation/image_360/', blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_default_status(self):
        return self.status

    def get_current_status(self):
        return self.status

    def get_short_detail(self):
        detail = self.detail[:250]
        return detail

    def get_room_amount(self):
        amount = range(0, self.amount + 1)
        return amount


class Activity(models.Model):
    aid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=150)
    amount = models.IntegerField(default=2)
    quantity = models.IntegerField(default=2)
    price = models.IntegerField()
    detail = models.TextField(max_length=1000)
    image = models.FileField(upload_to=handle_upload_activity_img)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_price(self):
        return self.price

    def get_short_detail(self):
        detail = self.detail[:250]
        return detail


class BookingActivity(models.Model):
    BOOKING_STATUS = (
        (1, 'Confirm'),
        (2, 'Operated'),
        (3, 'Cancelled'),
        (4, 'Completed')
    )

    bid = models.UUIDField(default=uuid.uuid4, editable=False)
    reservation_no = models.CharField(default=handle_reservation_number_activity, max_length=15)
    checkin_date = models.CharField(max_length=100)
    checkout_date = models.CharField(max_length=100)
    detail_data = models.CharField(max_length=100)
    act_data = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    b_price = models.FloatField()
    status = models.IntegerField(default=1, choices=BOOKING_STATUS)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.reservation_no

    def __unicode__(self):
        return self.reservation_no

    def get_activity_data(self):
        data = []
        detail_data = json.loads(self.detail_data)
        act_data = json.loads(self.act_data)
        for i in range(0, len(act_data)):
            name = act_data[i]['name']
            act = Activity.objects.get(name=name)
            data.append({'act': act})

            # amount
            amount = act_data[i]['amount']
            data[i]['amount'] = amount

        return data


class BookingInfo(models.Model):
    """
    Booking Information
    this field is going to delete activity column
    """

    BOOKING_STATUS = (
        (1, 'Confirm'),
        (2, 'Operated'),
        (3, 'Cancelled'),
        (4, 'Completed')
    )

    bid = models.UUIDField(default=uuid.uuid4, editable=False)
    reservation_no = models.CharField(default=handle_reservation_number, max_length=15)
    checkin_date = models.CharField(max_length=100)
    checkout_date = models.CharField(max_length=100)
    detail_data = models.CharField(max_length=1000, null=True)
    b_price = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    room_data = models.CharField(max_length=1000, null=True)
    status = models.IntegerField(default=1, choices=BOOKING_STATUS)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.reservation_no

    def __unicode__(self):
        return self.reservation_no

    def get_adult_data(self):
        adult = 0
        detail_data = json.loads(self.detail_data)
        for i in detail_data:
            adult = int(i['data-adult']) + adult

        return adult

    def get_child_data(self):
        child = 0
        detail_data = json.loads(self.detail_data)
        for i in detail_data:
            child = int(i['data-child']) + child

        return child

    def get_room_data(self):

        data = []
        room_data = json.loads(self.room_data)
        detail_data = json.loads(self.detail_data)
        for i in range(0, len(room_data)):
            # get room
            name = room_data[i]['name']
            room = Accommodation.objects.get(name=name)
            data.append({'room': room})

            # add amount
            amount = room_data[i]['amount']
            data[i]['amount'] = amount

            # add guest number
            child = int(detail_data[i]['data-child'])
            adult = int(detail_data[i]['data-adult'])
            guest_num = child + adult
            data[i]['guest_num'] = guest_num

            # add price
            nor_price = room.price
            num_night = int((datetime.strptime(self.checkout_date, "%b. %d, %Y") - datetime.strptime(self.checkin_date,
                                                                                                     "%b. %d, %Y")).days)
            price = int(nor_price) * num_night * int(amount)
            data[i]['price'] = price

            # add index
            data[i]['index'] = i + 1
        logging.debug(data)
        return data


class b_room(models.Model):
    """
    Number of room in each booking record.
    """
    booking_info = models.ForeignKey(BookingInfo, on_delete=models.CASCADE)
    room = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
