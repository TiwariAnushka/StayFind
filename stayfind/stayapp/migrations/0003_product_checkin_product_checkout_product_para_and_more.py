# Generated by Django 5.0.6 on 2024-08-01 04:15

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stayapp', '0002_product_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='checkin',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='checkout',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='para',
            field=models.CharField(default=0, max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='pimage2',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Booked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1)),
                ('pid', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='stayapp.product')),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
