<<<<<<< HEAD
# Generated by Django 4.2.3 on 2024-11-22 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
=======
# Generated by Django 5.1.3 on 2024-11-18 22:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
>>>>>>> 017b213125275a288e064125325fe8a7e5d2dcf0


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
=======
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
>>>>>>> 017b213125275a288e064125325fe8a7e5d2dcf0
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_checked_out', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
=======
>>>>>>> 017b213125275a288e064125325fe8a7e5d2dcf0
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='marketing_analytics.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing_analytics.product')),
            ],
        ),
    ]
