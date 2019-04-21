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
from login.views import LoginManager, AdminLoginManager
from portfolio.views import PortfolioManager
from artist.views import GetPersonalInformationOfArtist,ArtistRegister
from customer.views import GetPersonalInformationOfCustomer, GetPublicInformationOfCustomer, CustomerRegister
from offer.views import OfferManage, CreateOffer, PaymentCode,NumOffers
from portfolioModule.views import PortfolioModuleManager, CreatePortfolioModule
from user.views import UserManage
from artist.views import ListArtist,ArtistRegister
from user.views import UserManage, ListUsers
from offers.views import ListArtistOffers, ListCustomerOffers
from paymentPackage.views import PaymentPackageByArtist, PaymentPackageManager, CreatePaymentPackage,CreateCustomPackage,CreateFarePackage,CreatePerformancePackage
from calendars.views import CalendarByArtist, CalendarManager, CreateCalendar
from artistGender.views import ArtisticGenderManager, CreateArtisticGender, ListArtisticGenders
from zone.views import ZoneManager, CreateZone, ListZones
from eventLocation.views import EventLocationManager, CreateEventLocation
from rating.views import GetRatings, PostRating
from utils.utils import TermsAndConditions, Privacy, AboutUs
from braintrees.views import BraintreeViews
from emails.views import SendMailDataBreach
from rest_framework.authtoken.views import obtain_auth_token
from utils.utils import TermsAndConditions
from chat.views import index, room
from languageChooser.views import LanguageChooser
from adminBoard.views import GetRegisteredArtistsAllTime, GetRegisteredCustomersAllTime, GetPendingOffersAllTime, \
    GetRejectedOffersAllTime, GetContractMadeOffersAllTime, GetPaymentOffersAllTime, GetContractMadeOffersLastMonth, \
    GetPaymentOffersLastMonth, GetPendingOffersLastMonth, GetRejectedOffersLastMonth, GetRegisteredCustomersLastMonth, GetRegisteredArtistsLastMonth

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
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
    url(r'^user/$', UserManage.as_view()),
    url(r'^artist/calendar/(?P<pk>[0-9]+)/$', CalendarByArtist.as_view()),
    url(r'^artists/$', ListArtist.as_view()),
    url(r'^artist/personalInformation/$', GetPersonalInformationOfArtist.as_view()),
    url(r'^customer/personalInformation/$', GetPersonalInformationOfCustomer.as_view()),
    url(r'^customer/publicInformation/(?P<pk>[0-9]+)/$', GetPublicInformationOfCustomer.as_view()),
    url(r'^calendar/(?P<pk>[0-9]+)/$', CalendarManager.as_view()),
    url(r'^calendar/$', CreateCalendar.as_view()),
    url(r'^artisticGender/$', CreateArtisticGender.as_view()),
    url(r'^artisticGenders/$', ListArtisticGenders.as_view()),
    url(r'^artisticGender/(?P<pk>[0-9]+)/$', ArtisticGenderManager.as_view()),
    url(r'^zone/$', CreateZone.as_view()),
    url(r'^zone/(?P<pk>[0-9]+)/$', ZoneManager.as_view()),
    path('api/login/', LoginManager.as_view(), name='login'),
    path('api/admin/login/', AdminLoginManager.as_view(), name='admin_login'),
    url(r'^paymentCode/$', PaymentCode.as_view()),
    url(r'^signupArtist/$', ArtistRegister.as_view()),
    url(r'^signupCustomer/$', CustomerRegister.as_view()),
    url(r'^artist/offers/$', ListArtistOffers.as_view()),
    url(r'^customer/offers/$', ListCustomerOffers.as_view()),
    url(r'^artist/(?P<pk>[0-9]+)/$', ArtistRegister.as_view()),
    url(r'^customer/(?P<pk>[0-9]+)/$', CustomerRegister.as_view()),
    url(r'^artist/ratings/(?P<pk>[0-9]+)/$', GetRatings.as_view()),
    url(r'^customer/rating/(?P<pk>[0-9]+)/$', PostRating.as_view()),
    url(r'^paymentCode/$', PaymentCode.as_view()),
    url(r'^artist/(?P<pk>[0-9]+)/$', ArtistRegister.as_view()),
    url(r'^customer/(?P<pk>[0-9]+)/$', CustomerRegister.as_view()),

    url(r'^fare/$', CreateFarePackage.as_view()),
    url(r'^performance/$', CreatePerformancePackage.as_view()),
    url(r'^custom/$', CreateCustomPackage.as_view()),

    url(r'^fare/(?P<pk>[0-9]+)/$', CreateFarePackage.as_view()),
    url(r'^performance/(?P<pk>[0-9]+)/$', CreatePerformancePackage.as_view()),
    url(r'^custom/(?P<pk>[0-9]+)/$', CreateCustomPackage.as_view()),
    url(r'^zones/$', ListZones.as_view()),

    url(r'^numOffers/$', NumOffers.as_view()),
    url(r'^terms$', TermsAndConditions.as_view()),
    url(r'^privacy$', Privacy.as_view()),
    url(r'^about$', AboutUs.as_view()),
    url(r'^braintree_token/$', BraintreeViews.as_view()),

    # TODO:delete chat urls later
    url(r'^chat/$', index),
    url(r'^chat/(?P<room_name>[^/]+)/$', room, name='room'),

    url(r'^send_breach_notification/$', SendMailDataBreach.as_view()),
    url(r'^users/$', ListUsers.as_view()),
    url(r'^language/$', LanguageChooser.as_view()),

    url(r'^admin/totalArtists/$', GetRegisteredArtistsAllTime.as_view()),
    url(r'^admin/totalCustomers/$', GetRegisteredCustomersAllTime.as_view()),
    url(r'^admin/ratioPending/$', GetPendingOffersAllTime.as_view()),
    url(r'^admin/ratioRejected/$', GetRejectedOffersAllTime.as_view()),
    url(r'^admin/ratioContractMade/$', GetContractMadeOffersAllTime.as_view()),
    url(r'^admin/ratioPaymentMade/$', GetPaymentOffersAllTime.as_view()),
    url(r'^admin/totalArtistsLastMonth/$', GetRegisteredArtistsLastMonth.as_view()),
    url(r'^admin/totalCustomersLastMonth/$', GetRegisteredCustomersLastMonth.as_view()),
    url(r'^admin/ratioPendingLastMonth/$', GetPendingOffersLastMonth.as_view()),
    url(r'^admin/ratioRejectedLastMonth/$', GetRejectedOffersLastMonth.as_view()),
    url(r'^admin/ratioContractMadeLastMonth/$', GetContractMadeOffersLastMonth.as_view()),
    url(r'^admin/ratioPaymentMadeLastMonth/$', GetPaymentOffersLastMonth.as_view())


]