# Generated by Django 3.0.7 on 2020-09-24 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200919_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceModel',
            fields=[
                ('idno', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
    ]
