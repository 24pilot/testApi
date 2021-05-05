import json
import logging

from django.core import serializers
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum, Count
from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Подключаем статус
from rest_framework import status, filters, generics
# Подключаем компонент для ответа
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView
# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny
# Подключаем модель User
from .models import User, Item, Transaction
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, ItemSerializer, TransactionSerializer, \
    UserSerializer #, SummaSerializer  # , BalanceSerializer
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum

logger = logging.getLogger(__name__)


# Создаём класс RegistrUserView
class RegistrUserView(CreateAPIView):
    # Добавляем в queryset
    queryset = User.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]

    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = UserRegistrSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]  # [filters.SearchFilter]
    filterset_fields = ['item', 'customer', 'created_at']
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



"""
class BalanceViewSet(viewsets.ModelViewSet):

    queryset = Transaction.objects.all()
    serializer_class = BalanceSerializer
    filter_backends = [DjangoFilterBackend]  # [filters.SearchFilter]
    filterset_fields = ['item', 'customer', 'created_at']
    permission_classes = [permissions.IsAuthenticated]
"""


def index(request):
    return HttpResponse("Hello, world. You're at the testAPI index.")


def report_user_year_month(request, customer, year, month):
    logger.error(request.user)

    t = Transaction.objects \
        .filter(customer=customer) \
        .filter(created_at__year=year) \
        .filter(created_at__month=month)

    summa = t.aggregate(Sum('item__price'))

    #serializer = TransactionSerializer(t, context={'request': request}, many=True)
    #return JsonResponse(serializer.data, safe=False)

    tmpJson = serializers.serialize("json", t)
    tmpObj = json.loads(tmpJson)
    summa['transactions'] = tmpObj
    return JsonResponse(summa, safe=False)


def report_user_year(request, customer, year):
    logger.error(request.user)

    t = Transaction.objects \
        .filter(customer=customer) \
        .filter(created_at__year=year)

    summa = t.aggregate(Sum('item__price'))

    #serializer = TransactionSerializer(t, context={'request': request}, many=True)
    #return JsonResponse(serializer.data, safe=False)

    tmpJson = serializers.serialize("json", t)
    tmpObj = json.loads(tmpJson)
    summa['transactions'] = tmpObj
    return JsonResponse(summa, safe=False)


def summa_user_item(request, customer, item):
    logger.error(request.user)

    t = Transaction.objects.filter(customer=customer).filter(item=item)
    summa = t.aggregate(Sum('item__price'))#.get('item__price__sum')

    print(t.all())
    print(summa)
# --------- Experiment
    #s = Transaction.objects.filter(customer=customer).values('customer', 'item').annotate(Sum('item__price')).get(item=item)
    #print(s)
# ---------------

    #serializer = TransactionSerializer(t, context={'request': request}, many=True)
    #serializer = SummaSerializer(queryset, context={'request': request}, many=True)
    #return JsonResponse(serializer.data, safe=False)

    tmpJson = serializers.serialize("json", t)
    tmpObj = json.loads(tmpJson)
    summa['transactions'] = tmpObj
    return JsonResponse(summa, safe=False)

def summa_all(request):

    t = Transaction.objects.all()
    summa = t.aggregate(Sum('item__price')).get('item__price__sum')

    return JsonResponse(summa, safe=False)