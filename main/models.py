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
from django import forms

class ObjectForm(forms.Form):
    name = forms.CharField(max_length=300)
    description = forms.CharField()
    country = forms.CharField(max_length=60)
    city = forms.CharField(max_length=60)
    zipcode = forms.CharField(max_length=8, required=False)
    street = forms.CharField(max_length=60, required=False)
    housenumber = forms.CharField(max_length=8, required=False)

class AdressForm(forms.Form):
    country = forms.CharField(max_length=60, required=False)
    city = forms.CharField(max_length=60, required=False)
    zipcode = forms.CharField(max_length=8, required=False)
    street = forms.CharField(max_length=60, required=False)
    housenumber = forms.CharField(max_length=8, required=False)

class HopForm(AdressForm):
    note = forms.CharField(required=False)
    secretID = forms.CharField()

class Location(models.Model):
    country = models.CharField(_('country'), max_length=60)
    city = models.CharField(_('city'), max_length=60)
    zipcode = models.CharField(_('zipcode'), max_length=8)
    street = models.CharField(_('street'), max_length=60, blank=True, null=True)
    housenumber = models.CharField(_('housenumber'), max_length=8, blank=True, null=True)
    longitude = models.CharField(_('longitude'), max_length=10, blank=True, null=True)
    latitude = models.CharField(_('latitude'), max_length=10, blank=True, null=True)
    
    def __unicode__(self):
        return self.country + ", " + self.city

class Object(models.Model):
    secretID = models.CharField(_('secret ID'), max_length=10)
    name = models.CharField(_('name'), max_length=300)
    description = models.TextField(_('description'))
    
    submissionDate = models.DateTimeField(_('submission date'), auto_now_add=True)
    
    sender = models.ForeignKey(User, verbose_name = _('sender'))
    destination = models.ForeignKey(Location, verbose_name = _('destination'))
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('object')
        verbose_name_plural = _('objects')
        ordering = ['-submissionDate']
    
    def lastuser(self):
        hoplist = Hop.objects.filter(objectID=self)[:1]
        if hoplist.count() == 0:
            return self.sender
        else:
            return hoplist[0].user
    
    def getlon(self):
        hoplist = Hop.objects.filter(objectID=self)[:1]
        print hoplist, self.sender.profile.adress
        if hoplist.count() == 0:
            return self.sender.profile.adress.longitude
        else:
            return hoplist[0].location.longitude

    def getlat(self):
        hoplist = Hop.objects.filter(objectID=self)[:1]
        print hoplist, self.sender.profile.adress
        if hoplist.count() == 0:
            return self.sender.profile.adress.latitude
        else:
            return hoplist[0].location.latitude
    
    def getstreet(self):
        hoplist = Hop.objects.filter(objectID=self)[:1]
        print hoplist, self.sender.profile.adress
        if hoplist.count() == 0:
            return self.sender.profile.adress.street + " " + self.sender.profile.adress.housenumber
        else:
            return hoplist[0].location.street + " " + hoplist[0].location.housenumber
    
    def getcity(self):
        hoplist = Hop.objects.filter(objectID=self)[:1]
        print hoplist, self.sender.profile.adress
        if hoplist.count() == 0:
            return self.sender.profile.adress.zipcode + " " + self.sender.profile.adress.city
        else:
            return hoplist[0].location.zipcode + " " + hoplist[0].location.city

class Hop(models.Model):
    objectID = models.ForeignKey(Object, verbose_name = _('Object'))
    user = models.ForeignKey(User, verbose_name = _('user'))
    location = models.ForeignKey(Location, verbose_name = _('locatiom'))
    note = models.TextField(_('note'))
    submissionDate = models.DateTimeField(_('date'), auto_now_add=True)
    
    def __unicode__(self):
        return self.objectID.name + " " + self.user.username
