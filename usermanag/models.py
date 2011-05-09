# coding: utf-8 

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from main.models import Location, AdressForm
from django import forms

class UserProfile(models.Model):
    url = models.SlugField(_('URL'), max_length=200)
    publicAdress = models.BooleanField(blank=True)
    adress = models.OneToOneField(Location, blank=True)
    user = models.ForeignKey(User, unique=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    secpassword = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)

class ProfileForm(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    secpassword = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)

class AdressForm(forms.Form):
    publicAdress = forms.BooleanField(required=False)
    country = forms.CharField(max_length=60, required=False)
    city = forms.CharField(max_length=60, required=False)
    zipcode = forms.CharField(max_length=8, required=False)
    street = forms.CharField(max_length=60, required=False)
    housenumber = forms.CharField(max_length=8, required=False)

class PAdressForm(AdressForm):
    publicAdress = forms.BooleanField()
