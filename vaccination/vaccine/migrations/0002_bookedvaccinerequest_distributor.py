# Generated by Django 5.0.2 on 2024-04-13 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedvaccinerequest',
            name='distributor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vaccine.distributor'),
            preserve_default=False,
        ),
    ]
