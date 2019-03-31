"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url, include
from login.views import LoginManager
from portfolio.views import PortfolioManager
from artist.views import GetPersonalInformationOfArtist
from customer.views import GetPersonalInformationOfCustomer, GetPublicInformationOfCustomer
from offer.views import OfferManage, CreateOffer, PaymentCode
from portfolioModule.views import PortfolioModuleManager, CreatePortfolioModule
from artist.views import ListArtist
from offers.views import ListOffers
from paymentPackage.views import PaymentPackageByArtist, PaymentPackageManager, CreatePaymentPackage
from calendars.views import CalendarByArtist, CalendarManager, CreateCalendar
from artistGender.views import ArtisticGenderManager, CreateArtisticGender
from zone.views import ZoneManager, CreateZone
from eventLocation.views import EventLocationManager, CreateEventLocation
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    url(r'^offer/$', CreateOffer.as_view()),
    url(r'^offer/(?P<pk>[0-9]+)/$', OfferManage.as_view()),
    url(r'^eventlocation/$', CreateEventLocation.as_view()),
    url(r'^eventlocation/(?P<pk>[0-9]+)/$', EventLocationManager.as_view()),
    url(r'^portfolio/(?P<pk>[0-9]+)/$', PortfolioManager.as_view()),
    url(r'^portfolioModule/$', CreatePortfolioModule.as_view()),
    url(r'^portfolioModule/(?P<pk>[0-9]+)/$', PortfolioModuleManager.as_view()),
    url(r'^artist/paymentPackages/(?P<pk>[0-9]+)/$', PaymentPackageByArtist.as_view()),
    url(r'^paymentPackage/$', CreatePaymentPackage.as_view()),
    url(r'^paymentPackage/(?P<pk>[0-9]+)/$', PaymentPackageManager.as_view()),
    url(r'^artist/calendar/(?P<pk>[0-9]+)/$', CalendarByArtist.as_view()),
    url(r'^artists/$', ListArtist.as_view()),
    url(r'^artist/personalInformation/$', GetPersonalInformationOfArtist.as_view()),
    url(r'^customer/personalInformation/$', GetPersonalInformationOfCustomer.as_view()),
    url(r'^customer/publicInformation/(?P<pk>[0-9]+)/$', GetPublicInformationOfCustomer.as_view()),
    url(r'^calendar/(?P<pk>[0-9]+)/$', CalendarManager.as_view()),
    url(r'^calendar/$', CreateCalendar.as_view()),
    url(r'^artisticGender/$', CreateArtisticGender.as_view()),
    url(r'^artisticGender/(?P<pk>[0-9]+)/ ', ArtisticGenderManager.as_view()),
    url(r'^zone/$', CreateZone.as_view()),
    url(r'^zone/(?P<pk>[0-9]+)/$', ZoneManager.as_view()),
    path('api/login/', LoginManager.as_view(), name='login'),
    url(r'^offers/$', ListOffers.as_view()),
    url(r'^paymentCode/$', PaymentCode.as_view())


]
