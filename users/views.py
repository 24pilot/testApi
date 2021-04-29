import json
import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Подключаем статус
from rest_framework import status, filters, generics
# Подключаем компонент для ответа
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView
# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny
# Подключаем модель User
from .models import User, Item, Transaction
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, ItemSerializer, TransactionSerializer, BalanceSerializer
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

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

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class BalanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Transaction.objects.all()
    serializer_class = BalanceSerializer
    filter_backends = [DjangoFilterBackend] # [filters.SearchFilter]
    filterset_fields = ['item', 'customer', 'created_at']
    permission_classes = [permissions.IsAuthenticated]


def index(request):
    return HttpResponse("Hello, world. You're at the testAPI index.")


def report_user_year_month(request, customer, year, month):

    logger.error(request.user)
    print(request.user)

    balance = Transaction.objects\
        .filter(customer=customer)\
        .filter(created_at__year=year)\
        .filter(created_at__month=month)

    serializer = TransactionSerializer(balance, context={'request': request}, many=True)
    return JsonResponse(serializer.data, safe=False)


def report_user_year(request, customer, year):
    logger.error(request.user)
    print(request.user)

    balance = Transaction.objects\
        .filter(customer=customer)\
        .filter(created_at__year=year)

    serializer = TransactionSerializer(balance, context={'request': request}, many=True)
    return JsonResponse(serializer.data, safe=False)

