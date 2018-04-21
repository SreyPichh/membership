# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-25 13:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid
import web.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('phone', models.IntegerField()),
                ('password', models.CharField(max_length=100)),
                ('profile_pic', models.ImageField(default='blank-profile-picture.png', upload_to=web.models.handle_upload_profile)),
                ('validation_type', models.CharField(choices=[('IDC', 'Identity Card'), ('PSP', 'PASSPORT')], max_length=50)),
                ('validation_img', models.ImageField(upload_to=web.models.handle_upload_validation_img)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('house_num', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_num', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('BUNGALOW DOUBLE ROOM', 'Bungalow Double Room'), ('BUNGALOW TWIN ROOM', 'Bungalow Twin Room'), ('VILLA JASMINE', 'Villa Jasmine'), ('VILLA SUITE', 'Villa Suite'), ('KHMER COTTAGE', 'Khmer cottage'), ('LUXURY TENT', 'Luxury Tent'), ('PIPE ROOM', 'Pipe Room'), ('CAMPING', 'Camping')], max_length=100)),
                ('amount', models.IntegerField()),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField(default=2)),
                ('detail', models.TextField(max_length=1000)),
                ('image', models.FileField(upload_to='Accommodation/')),
                ('image_360', models.FileField(blank=True, upload_to='Accommodation/image_360/')),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=150)),
                ('price', models.CharField(max_length=150)),
                ('detail', models.CharField(max_length=1000)),
                ('image', models.FileField(upload_to=web.models.handle_upload_activity_img)),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='b_room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BookingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('reservation_no', models.CharField(default=web.models.handle_reservation_number, max_length=15)),
                ('checkin_date', models.CharField(max_length=100)),
                ('checkout_date', models.CharField(max_length=100)),
                ('detail_data', models.CharField(max_length=1000, null=True)),
                ('b_price', models.FloatField()),
                ('room_data', models.CharField(max_length=1000, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Confirm'), (2, 'Operated'), (3, 'Cancelled'), (4, 'Completed')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MemberType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('picture', models.ImageField(upload_to=web.models.handle_upload_membership_img)),
                ('description', models.CharField(max_length=2000)),
                ('n_member', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPoint',
            fields=[
                ('pid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('ammount', models.FloatField(default=0.0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='bookinginfo',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='b_room',
            name='booking_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.BookingInfo'),
        ),
        migrations.AddField(
            model_name='b_room',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Accommodation'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='member_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.MemberType'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
