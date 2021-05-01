"""testapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from djoser.urls.base import router
from rest_framework import routers, serializers, viewsets
from users import views, models
from users.views import RegistrUserView, ItemViewSet, TransactionViewSet, UserViewSet #, BalanceViewSet

from django.urls import path, include
from users.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.



# ViewSets define the view behavior.



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'transactions', TransactionViewSet)
# router.register(r'balance', BalanceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('registr/', RegistrUserView.as_view(), name='registr'),
    path('', include(router.urls)),
    path('report/<int:customer>/<int:year>/<int:month>/', views.report_user_year_month),
    path('report/<int:customer>/<int:year>/', views.report_user_year),
    path('summa/<int:customer>/<int:item>/', views.summa_user_item),
    # path('balance/', BalanceViewSet.as_view()),
]
