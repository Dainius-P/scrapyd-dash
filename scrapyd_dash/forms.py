from django import forms
from .models import ScrapydServer, ScrapydProject, Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "project", "spider", "server")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = ScrapydProject.objects.none()

        if 'server' in self.data:
            try:
                server_id = int(self.data.get('server'))
                self.fields['project'].queryset = ScrapydProject.objects.filter(server_id=server_id).order_by('name')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['project'].queryset = self.instance.server.project_set.order_by('name')