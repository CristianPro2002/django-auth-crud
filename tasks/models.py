from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)    #CharField es para campos de texto
    description = models.TextField(blank=True)    #TextField es para campos de texto largo
    created = models.DateTimeField(auto_now_add=True)   #DateTimeField es para campos de fecha y hora, el auto_now_add sirve para que se guarde la fecha y hora actual al momento de enviar el formulario y no le pasamos ese dato
    datecompleted = models.DateTimeField(null=True, blank=True)   #null=True sirve para que el campo sea opcional, blank=True sirve para que el campo sea opcional en el formulario
    important = models.BooleanField(default=False)  #BooleanField es para campos de tipo booleano, el default sirve para que por defecto se guarde el valor False
    user = models.ForeignKey(User, on_delete=models.CASCADE)    #ForeignKey sirve para crear una relacion entre tablas, en este caso la tabla Task y la tabla User, el on_delete sirve para que si se elimina un usuario se eliminen todas las tareas que ese usuario haya creado
  
    def __str__(self):
        return self.title + ' - by ' + str(self.user.username)

    