from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Contenido(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField('fecha creacion', auto_now_add = True )
    keyword = models.CharField(max_length=100) 
    content_type = models.ForeignKey("contenttypes.ContentType") 

class Estilo(models.Model):
    estilo = models.CharField(max_length=100)

    def __unicode__(self):
        return self.estilo

class Artista(models.Model):
    artista = models.CharField(max_length=100)
    estilo = models.ManyToManyField(Estilo) 

    def __unicode__(self):
        return self.artista

class Ringtone(Contenido):
    grupo = models.ManyToManyField(Artista)
    archivo = models.FileField(upload_to="uploads")
    
    def __unicode__(self):
        return self.nombre


class Categoria(models.Model):
    categoria = models.CharField(max_length=100)
    

    def __unicode__(self):
        return self.categoria

class Wallpaper(Contenido):
    categoria = models.ForeignKey(Categoria)
    archivo = models.ImageField(upload_to="uploads")

    def __unicode__(self):
        return self.nombre


class SMS(models.Model):

    class Meta:
        verbose_name_plural = "SMS"

    received = models.DateTimeField(auto_now=True)
    fromnum = models.CharField(max_length=100)
    tonum = models.CharField(max_length=100)
    smsc = models.CharField(max_length=100)
    msg = models.CharField(max_length=100)
    valid = models.BooleanField(db_index=True)

class Dynpath(models.Model):
    created = models.DateTimeField(auto_now=True)
    url_path = models.CharField(max_length=100)
    payload = models.ForeignKey(Contenido)
    sms = models.ForeignKey(SMS)

    def __unicode__(self):
        return str(self.url_path)

