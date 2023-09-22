from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.apps import apps
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf.urls import url
from cryptopay import urls as cryptocurrency_payment_urls
from django.conf.urls import re_path
from users import views

handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'
handler403 = 'home.views.error_403'
handler400 = 'home.views.error_400'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tickets/', include('ticket.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    path('accounts/login/', views.customlogin, name='customlogin'),
    path('accounts/', include("allauth.urls")),
    url(r'^kyc/', include('kyc.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('wallet/', include('wallets.urls', namespace="wallet")),
    url(r"register=(?P<use>\w{0,50})/", views.referalsignup, name="refersignup"),
    path('contact/', TemplateView.as_view(template_name='contact.html')),
    path('plan/', RedirectView.as_view(url=staticfiles_storage.url("IPM_23July_Final_Presentation-1.pdf")),),
    path('', TemplateView.as_view(template_name='apnabase.html')),
    path('soon/', TemplateView.as_view(template_name='users/coming_soon.html')),
    path('users/', include('users.urls', namespace="users")),
    path('level/', include('level.urls', namespace="level")),
    path('panel/', include('panel.urls', namespace="panel")),
    path('search/', include("search.urls", namespace="searchy")),
    path("signup/onboarding/", views.signuponboarding, name="signup-onboarding"),
    url(r'^crypto/', include(cryptocurrency_payment_urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]