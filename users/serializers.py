# Подключаем класс для работы со сериалайзер
import logging

from rest_framework import serializers
# Подключаем модель user
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
    class Meta:
        model = Transaction
        fields = ['id', 'customer', 'item', 'created_at', 'item']
        customer = serializers.ReadOnlyField(source='customer.username')


class BalanceSerializer(serializers.HyperlinkedModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    item_price = serializers.ReadOnlyField(source='item.price')
    customer_name = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Transaction
        fields = ['id', 'customer', 'item', 'created_at', 'item_name', 'item_price', 'customer_name']
