"""fobbage URL Configuration

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
from django.urls import path, include
from django.conf import settings

from rest_framework.routers import DefaultRouter

from fobbage.quizes.router import router as quizes_router


router = DefaultRouter()

router.registry.extend(quizes_router.registry)

# sort the endpoints alphabetically
router.registry.sort(key=lambda x: x[0])

urlpatterns = [
    path('api/',  include('fobbage.accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]


if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
