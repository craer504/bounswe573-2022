# Generated by Django 4.0.4 on 2022-05-24 09:14

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('learnApp', '0007_alter_message_message_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_body',
            field=tinymce.models.HTMLField(),
        ),
    ]
