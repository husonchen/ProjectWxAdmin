"""LouisXIV_Translator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import *
from shop_admin.util.UrlDiscovery import Site
from django.conf.urls.static import static
from django.conf import settings
import shop_admin.controller.index
from shop_admin.controller.wx_controller import redirct_from_wx

site = Site()
site.autodiscover()

urlpatterns = [
    url(r'^$',shop_admin.controller.index.hello),
    url(r'^', include(site.urls)),
    url(r'^wx/open/shops/([0-9]{1})/([0-9]{5})/$',redirct_from_wx)
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


