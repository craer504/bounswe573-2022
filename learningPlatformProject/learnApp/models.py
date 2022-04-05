from django.db import models
from django.contrib.auth.models import User


class Workspace(models.Model):
    workspace_host = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    workspace_subject = models.ForeignKey(
        'Subject', on_delete=models.SET_NULL, null=True)
    workspace_name = models.CharField(max_length=200)
    workspace_description = models.TextField(null=True, blank=True)
    workspace_lecturers = models.ManyToManyField(
        User, related_name='lecturers', blank=True)
    workspace_lastupdated = models.DateTimeField(auto_now=True)
    workspace_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-workspace_lastupdated', '-workspace_created']

    def __str__(self):
        return self.workspace_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=200)

    def __str__(self):
        return self.subject_name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    message_body = models.TextField()
    message_lastupdated = models.DateTimeField(auto_now=True)
    message_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message_body[0:50]
