# Generated by Django 4.0.4 on 2022-05-24 10:02

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learnApp', '0009_alter_message_message_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
