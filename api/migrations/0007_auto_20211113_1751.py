# Generated by Django 3.2.9 on 2021-11-13 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devis',
            name='fullid',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='facture',
            name='fullid',
            field=models.CharField(max_length=16),
        ),
    ]
