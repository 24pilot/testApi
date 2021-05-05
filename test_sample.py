from re import search

import pytest
from requests import request

import users.models
from users.models import Item, Transaction, User
from users.views import summa_user_item


@pytest.mark.django_db
def test_summa_all():
    User.objects.create(username='User1')
    Item.objects.create(name='birn', price=1, )
    Item.objects.create(name='apple', price=2, )
    Transaction.objects.create(item=users.models.Item.objects.get(id=1), customer=users.models.User.objects.get(id=1))
    Transaction.objects.create(item=users.models.Item.objects.get(id=2), customer=users.models.User.objects.get(id=1))
    Transaction.objects.create(item=users.models.Item.objects.get(id=2), customer=users.models.User.objects.get(id=1))
    request.user = 'null'

    rez = summa_user_item(request, customer=1, item=2)
    ref = '"item__price__sum": 4'

    assert search(ref, str(rez.content))
