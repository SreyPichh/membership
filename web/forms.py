from django import forms
from .models import User, VALIDATION_TYPES, BookingInfo, Accommodation, BookingActivity


class RegisterForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput, label='name')
    email = forms.EmailField(widget=forms.EmailInput, label='email')
    phone = forms.IntegerField(widget=forms.NumberInput, label='phone')
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    # confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    validation_type = forms.ChoiceField(choices=VALIDATION_TYPES, label='validation_type')
    validation_img = forms.ImageField(widget=forms.FileInput, label='validation_img')

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'validation_type', 'validation_img']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        # if 'password' in self.cleaned_data and 'confirm' in self.cleaned_data:
        #     if self.cleaned_data['password'] != self.cleaned_data['confirm']:
        #         raise forms.ValidationError("Password doesn't match!!")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        fields = ['email', 'password']


class OdooMemberAuth(forms.Form):
    """docstring for OdooMemberAuth"""
    email = forms.EmailField(widget=forms.EmailInput, label="Username")

    class Meta:
        fields = ['email']


class EditProfileImage(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput, label="Profile Picture")

    class Meta:
        model = User
        fields = ['profile_pic']


class EmailForgotPassword(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, label="Forgot Password Email")

    class Meta:
        fields = ['email']


class ResetPassword(forms.Form):
    """
    A form that lets a user change set their password without entering the old password
    """

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }

    password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        fields = ['password', 'confirm']

    def clean_new_confirm(self):
        new_password = self.cleaned_data.get('password')
        new_confirm = self.cleaned_data.get('confirm')

        if new_password and new_confirm:
            if new_password != new_confirm:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return new_confirm


class BookingList(forms.Form):
    """
    Booking List in index page and accommodation.
    """

    class Meta:
        fields = ['checkin_date', 'checkout_date', 'list_booking']


class BookingRecord(forms.ModelForm):
    """
    Booking Information for each booking record.
    """

    class Meta:
        model = BookingInfo
        fields = ['checkin_date', 'checkout_date', 'detail_data', 'b_price', 'room_data']


class BookingRecordActivity(forms.ModelForm):
    class Meta:
        model = BookingActivity
        fields = ['checkin_date', 'checkout_date', 'detail_data', 'b_price', 'act_data']


class AccForm(forms.ModelForm):
    """docstring for AccForm"""

    class Meta:
        model = Accommodation
        fields = ['name', 'type', 'amount', 'price', 'quantity', 'detail', 'image']
        # image = forms.ImageField()
