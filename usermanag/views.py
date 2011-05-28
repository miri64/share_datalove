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

import util
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import Object, Location
from models import UserProfile, RegisterForm, ProfileForm, AdressForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.db import IntegrityError

def userlogin(request):
    if request.method == 'POST': # If the form has been submitted...
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.POST['next']
                if next != "":
                    return redirect(next)
                else:
                    return redirect("/")
            else:
                message = _("Login failed.The account is disabled")
        else:
            message = _("Username and/or password wrong")
        context = util.generateContext(request, contextType = 'RequestContext', message = message)
        return render_to_response('main/login.html', context)
    else:
        if request.method == 'GET':
            try:
                next = request.GET['next']
            except:
                next = ""
        context = util.generateContext(request, contextType = 'RequestContext', next=next)
        return render_to_response('main/login.html', context, title="Login")

def userlogout(request):
    logout(request)
    context = util.generateContext(request, contextType = 'RequestContext', message = _("You were successfully logged out"))
    return redirect('/')

def showlogin(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        context = util.generateContext(request, contextType = 'RequestContext')
        return render_to_response('main/login.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            secpassword = form.cleaned_data['secpassword']
            email = form.cleaned_data['email']
            if password == secpassword:
                try:
                    user = User.objects.create_user(username, email, password)
                except IntegrityError:
                    t = loader.get_template('main/register.html')
                    message = "Error: The Username is already taken"
                    context = util.generateContext(request, contextType = 'RequestContext', form=form, message=message)
                    return HttpResponseServerError(t.render(context))
                #user.profile = UserProfile(user=user)
                user.profile.save()
                profile = user.get_profile()
                profile.url = username
                print profile.url
                print username
                profile.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
            else:
                message = "Error: The Passwords didn't match"
        else:
            message = "There was a problem with the entered values"
        t = loader.get_template('main/register.html')
        context = util.generateContext(request, contextType = 'RequestContext', form=form, message=message)
        return HttpResponseServerError(t.render(context))
    else:
        form = RegisterForm()
        context = util.generateContext(request, contextType = 'RequestContext', form=form)
        return render_to_response('main/register.html', context)

def showUser(request, url=None):
    if url == None:
        if request.user.is_authenticated():
            return redirect('/user/show/{0}'.format(request.user.username))
        else:
            return redirect('/')
    else:
        user = get_object_or_404(User, username=url)
    print request.user.profile.url
    objectlist = Object.objects.all().filter(sender=user)
    context = util.generateContext(request, contextType = 'RequestContext', viewuser=user, objects=objectlist, title=user.username)
    return render_to_response('usermanag/show.html', context)

@login_required
def editProfile(request):
    title="Edit Profile"
    if request.method == 'POST':
        userform = ProfileForm(request.POST) # A form bound to the POST data
        adressform = AdressForm(request.POST)
        if userform.is_valid(): # All validation rules pass
            oldpassword = userform.cleaned_data['oldpassword']
            password = userform.cleaned_data['password']
            secpassword = userform.cleaned_data['secpassword']
            email = userform.cleaned_data['email']
            
        if adressform.is_valid():
            publicadress = adressform.cleaned_data['publicAdress']
            country = adressform.cleaned_data['country']
            city = adressform.cleaned_data['city']
            zipcode = adressform.cleaned_data['zipcode']
            street = adressform.cleaned_data['street']
            housenumber = adressform.cleaned_data['housenumber']
            userprofile = request.user.profile
            l = Location(country=country, city=city, zipcode=zipcode, street=street, housenumber=housenumber)
            l.save()
            userprofile.adress = l
            userprofile.publicAdress = publicadress
            userprofile.save()
    else:
        user = request.user
        try:
            userform = ProfileForm({'email': user.email,})
        except:
            userform = UserForm()
        try:
            adressform = AdressForm({
                                'publicAdress': user.profile.publicAdress,
                                'country': user.profile.adress.country,
                                'city': user.profile.adress.city, 
                                'zipcode': user.profile.adress.zipcode, 
                                'street': user.profile.adress.street, 
                                'housenumber': user.profile.adress.housenumber})
        except:
            adressform = AdressForm()
    context = util.generateContext(request, contextType = 'RequestContext', userform=userform, adressform=adressform, title=title)
    return render_to_response('usermanag/edit.html', context)
