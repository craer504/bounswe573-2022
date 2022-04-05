from django.contrib import admin

from .models import Workspace, Subject, Message

admin.site.register(Workspace) #register the model to admin panel
admin.site.register(Subject)
admin.site.register(Message)