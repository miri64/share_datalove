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

import urllib2
from xml.dom import minidom
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.core.mail import send_mail

def generateContext(request, contextType = 'Context', **kwargs):
	if contextType.lower() == 'requestcontext':
		context = getattr(__import__('django').template, contextType)(request, kwargs)
	else:
		context = getattr(__import__('django').template, contextType)(kwargs)
	try:
		context['infoMessage'] = request.session['nextInfo']
		request.session['nextInfo'] = None
	except KeyError:
		pass

	return context

def getLonLat(country=None, city=None, zipcode=None, street=None, housenumber=None):
    url = u"http://nominatim.openstreetmap.org/search?q="
    print type(housenumber)
    print housenumber
    if housenumber != "":
        url += housenumber
    if street != "":
        url += u",+{0}".format(street)
    if city != "":
        url += u",+{0}".format(city)
    if country != "":
        url += u",+{0}".format(country)
    url += u"&format=xml"
    xml = urllib2.urlopen(url.encode("ascii", "ignore"))
    xml = xml.read()
    print xml
    dom = minidom.parseString(xml)
    result = dom.getElementsByTagName("searchresults")[0]
    print result.getElementsByTagName("place")
    if result.getElementsByTagName("place") != []:
        place = result.getElementsByTagName("place")[0]
        longitude = place.getAttribute("lon")
        latitude = place.getAttribute("lat")
        return longitude, latitude
    else:
        return "", ""
    
