import pytest
import users.models
from users.models import Item, Transaction
from users.views import summa_all

@pytest.mark.django_db
def test_summa_all():
  Item.objects.create( name='birn', price = 1, )
  Item.objects.create( name='apple', price = 1, )
  Transaction.objects.create(item=users.models.Item.objects.get(id=1))
  Transaction.objects.create(item=users.models.Item.objects.get(id=2))
  Transaction.objects.create(item=users.models.Item.objects.get(id=2))

  rez=summa_all(request="")

  assert rez.content==b'3'