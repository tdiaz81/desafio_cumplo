# Generated by Django 2.0.2 on 2018-11-16 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indices', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indice',
            options={'verbose_name': 'indice', 'verbose_name_plural': 'indices'},
        ),
        migrations.RemoveField(
            model_name='indice',
            name='content',
        ),
        migrations.RemoveField(
            model_name='indice',
            name='created',
        ),
        migrations.RemoveField(
            model_name='indice',
            name='order',
        ),
        migrations.RemoveField(
            model_name='indice',
            name='title',
        ),
        migrations.RemoveField(
            model_name='indice',
            name='updated',
        ),
    ]
