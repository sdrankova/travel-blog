# Generated by Django 3.1.4 on 2020-12-10 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='current_user',
        ),
        migrations.RenameField(
            model_name='destination',
            old_name='user',
            new_name='current_user',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='user',
            new_name='current_user',
        ),
    ]