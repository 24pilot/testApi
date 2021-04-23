from django.db import models  # Подключаем работу с моделями
# Подключаем классы для создания пользователей
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Создаем класс менеджера пользователей
class MyUserManager(BaseUserManager):
    # Создаём метод для создания пользователя
    def _create_user(self, email, username, password, **extra_fields):
        # Проверяем есть ли Email
        if not email:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Email")
        # Проверяем есть ли логин
        if not username:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Логин")
        # Делаем пользователя
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем всё остальное
        user.save(using=self._db)
        # Возвращаем пользователя
        return user

    # Делаем метод для создание обычного пользователя
    def create_user(self, email, username, password):
        # Возвращаем нового созданного пользователя
        return self._create_user(email, username, password)

    # Делаем метод для создание админа сайта
    def create_superuser(self, email, username, password):
        # Возвращаем нового созданного админа
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
# Создаём класс User


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    username = models.CharField(max_length=50, unique=True)  # Логин
    email = models.EmailField(max_length=100, unique=True)  # Email
    is_active = models.BooleanField(default=True)  # Статус активации
    is_staff = models.BooleanField(default=False)  # Статус админа

    USERNAME_FIELD = 'email'  # Идентификатор для обращения
    REQUIRED_FIELDS = ['username']  # Список имён полей для Superuser

    objects = MyUserManager()  # Добавляем методы класса MyUserManager

    # Метод для отображения в админ панели
    def __str__(self):
        return (self.email)


class Item(TimeStampMixin, models.Model ):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=1)



class Transaction(TimeStampMixin, models.Model ):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    customer = models.ForeignKey(to='users.User', editable=False, null=True,blank=True, related_name='users_transactions', on_delete=models.CASCADE)
    item = models.ForeignKey(to='users.Item', on_delete=models.CASCADE)
