from django.forms import ModelForm
from .models import Workspace

class WorkspaceForm(ModelForm):
    class Meta:
        model = Workspace
        fields = '__all__'
        exclude = ['workspace_host', 'workspace_lecturers']