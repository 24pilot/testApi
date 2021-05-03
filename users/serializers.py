# Подключаем класс для работы со сериалайзер
import logging

from django.db.models import Sum
from rest_framework import serializers
# Подключаем модель user
from rest_framework.serializers import ModelSerializer

from .models import User, Item, Transaction


# Создаём класс UserRegistrSerializer


class UserRegistrSerializer(serializers.ModelSerializer):
    # Поле для повторения пароля
    password2 = serializers.CharField()

    # Настройка полей
    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['email', 'username', 'password', 'password2']

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            email=self.validated_data['email'],  # Назначаем Email
            username=self.validated_data['username'],  # Назначаем Логин
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'created_at', 'items_transactions']  # , 'transaction_set'


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    item_price = serializers.ReadOnlyField(source='item.price')
    customer_name = serializers.ReadOnlyField(source='customer.username')

    # summa = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'customer', 'item', 'created_at', 'item_name', 'item_price', 'customer_name']


"""
    def get_summa(self, *args, **kwargs):
        t=Transaction.objects
        print(t)
        sum_b = t.aggregate(Sum('item__price'))#.get('item__price__sum')
        return sum_b
"""


class UserSerializer(serializers.HyperlinkedModelSerializer):
    transactions_count = serializers.SerializerMethodField()
    transactions_summa = serializers.SerializerMethodField()
    users_transactions = TransactionSerializer(required=False, many=True)
    # items_list = ItemSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'users_transactions', 'transactions_count',
                  'transactions_summa']

    def get_transactions_count(self, obj):
        return obj.users_transactions.count()

    def get_transactions_summa(self, obj):
        t = obj.users_transactions.all()
        print(t)
        sum_b = t.aggregate(Sum('item__price')).get('item__price__sum')
        return sum_b
"""
# ------------- Try summa via serialiser
class SummaSerializer(ModelSerializer):
    transactions = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('url', 'transactions')
#---------------------------------


class BalanceSerializer(serializers.HyperlinkedModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    item_price = serializers.ReadOnlyField(source='item.price')
    customer_name = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Transaction
        fields = ['id', 'customer', 'item', 'created_at', 'item_name', 'item_price', 'customer_name']
"""
