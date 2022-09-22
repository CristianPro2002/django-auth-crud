from django.forms import ModelForm #ModelForm sirve para crear un formulario a partir de un modelo
from .models import Task
from django import forms

class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']  #fields sirve para indicar que campos queremos que se muestren en el formulario
        labels = {'title': 'Titulo', 'description': 'Descripcion', 'important': 'Importante'}   #labels sirve para cambiar el nombre de los campos en el formulario
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo'}), 'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripcion'}), 'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})} 
           