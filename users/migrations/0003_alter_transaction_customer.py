# Generated by Django 3.2 on 2021-04-23 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_item_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='customer',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_transactions', to=settings.AUTH_USER_MODEL),
        ),
    ]
