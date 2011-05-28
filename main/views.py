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
import random
import string
import datetime
from models import Location, Object, Hop, ObjectForm, AdressForm, HopForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required

def mainview(request):
    objectlist = Object.objects.all()
    context = util.generateContext(request, contextType = 'RequestContext', objects = objectlist)
    return render_to_response('main/standard.html', context)

def singleObject(request, url):
    singleObject = get_object_or_404(Object, id=url)
    hoplist = Hop.objects.filter(objectID=singleObject)
    title = singleObject.name
    context = util.generateContext(request, contextType = 'RequestContext', object = singleObject, hops = hoplist, title=title)
    return render_to_response('main/single.html', context)

@login_required
def newObject(request):
    title = "New Object"
    if request.method == 'POST': # If the form has been submitted...
        form = ObjectForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            street = form.cleaned_data['street']
            housenumber = form.cleaned_data['housenumber']
            lon, lat = util.getLonLat(country, city, zipcode, street, housenumber)
            l = Location(
                        country = country,
                        city = city,
                        zipcode = zipcode,
                        street = street,
                        housenumber = housenumber,
                        longitude = lon,
                        latitude = lat
            )
            l.save()
            randID = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(10))
            o = Object(
                        name = form.cleaned_data['name'],
                        description = form.cleaned_data['description'],
                        secretID = randID,
                        submissionDate = datetime.datetime.now(),
                        sender = request.user,
                        destination = l
            )
            o.save()
            return HttpResponseRedirect('/object/{0}'.format(o.id)) # Redirect after POST
        else:
            message = "The entered information wasn't valid. please check it."
            t = loader.get_template('main/newobject.html')
            ontext = util.generateContext(request, contextType = 'RequestContext', form=form, message=message, title=title)
            return HttpResponseServerError(t.render(context))
    else:
        form = ObjectForm() # An unbound form
    context = util.generateContext(request, contextType = 'RequestContext', form = form, title=title)
    return render_to_response('main/newobject.html', context)

def newHop(request):
    title = "New Hop"
    if request.method=='POST':
        form = HopForm(request.POST)
        if form.is_valid():
            secretID = form.cleaned_data['secretID']
            oid = request.POST['object']
            object = get_object_or_404(Object, id=int(oid))
            if secretID == object.secretID:
                country = form.cleaned_data['country']
                city = form.cleaned_data['city']
                zipcode = form.cleaned_data['zipcode']
                street = form.cleaned_data['street']
                housenumber = form.cleaned_data['housenumber']
                longitude, latitude = util.getLonLat(country, city, zipcode, street, housenumber)
                l = Location(
                            country = country,
                            city = city,
                            zipcode = zipcode,
                            street = street,
                            housenumber = housenumber,
                            longitude = longitude,
                            latitude = latitude
                )
                l.save()
                note = form.cleaned_data['note']
                hop = Hop(objectID=object, user=request.user, location=l, note=note, submissionDate=datetime.datetime.now())
                hop.save()
                return redirect("/object/{0}".format(object.id))
            else:
                message = "The SecretID wasn't correct. Are you shure you have the object?"
        else:
            message = "The entered information wasn't valid. please check it."
        t = loader.get_template('main/newhop.html')
        context = util.generateContext(request, contextType = 'RequestContext', form=form, message=message, title=title)
        return HttpResponseServerError(t.render(context))
    else:
        form = HopForm()
        if request.method == 'GET':
            try:
                object = request.GET['obj']
            except:
                return redirect("/")
    context = util.generateContext(request, contextType = 'RequestContext', form = form, obj=object, title=title)
    return render_to_response('main/newhop.html', context)
