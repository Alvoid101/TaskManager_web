from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [ 'title', 'description', 'delivery_date', 'finished']
        labels = {
            'title': 'Título',
            'description' : 'Descripción',
            'delivery_date' : 'Fecha de finalización',
            'finished' : 'finalizada',
        }

        widgets = {
            'title':forms.TextInput(attrs={'id': 'title'}),
            'description': forms.Textarea(attrs={'id':'description', 'rows': 6}),
            'delivery_date': forms.DateTimeInput(attrs={'id':'delivery_date', 'type': 'datetime-local'}),
            'finished' : forms.CheckboxInput(attrs={'id':'finished'}),
        }