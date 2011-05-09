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

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#handler500 = 'main.views.errorview'

urlpatterns = patterns('',
    # Example:
    # (r'^share_datalove/', include('share_datalove.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    (r'^$', 'main.views.mainview'),
    (r'^newobject/$', 'main.views.newObject'),
    (r'^newhop/$', 'main.views.newHop'),
    (r'^object/(?P<url>.*)$', 'main.views.singleObject'),
    
    
    (r'^user/login/$', 'usermanag.views.userlogin'),
    (r'^user/logout/$', 'usermanag.views.userlogout'),
    (r'^user/register/$', 'usermanag.views.register'),
    (r'^user/edit/$', 'usermanag.views.editProfile'),
    (r'^user/$', 'usermanag.views.showUser'),
    (r'^user/show/$', 'usermanag.views.showUser'),
    (r'^user/show/(?P<url>.*)$', 'usermanag.views.showUser'),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
