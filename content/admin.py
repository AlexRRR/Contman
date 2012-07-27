from content.models import Ringtone,Estilo,Artista,Categoria,Wallpaper,Contenido,SMS
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe
from django.contrib.contenttypes import generic
from django import forms
from djcelery.models import (TaskState, WorkerState,
                         PeriodicTask, IntervalSchedule, CrontabSchedule)


ADMIN_THUMBS_SIZE = '60x60'

class MyWallpaperAdminForm(forms.ModelForm):
    class Meta:
        model = Wallpaper

    def clean_keyword(self):
        data = self.cleaned_data['keyword']
        if Contenido.objects.all().filter(keyword=data).exists():
            raise forms.ValidationError("This keyword is already in use!")
        return data

class WallpaperAdmin(AdminImageMixin,admin.ModelAdmin):
    list_display = ('my_image_thumb','nombre','fecha_creacion','archivo')
    form = MyWallpaperAdminForm    
    def my_image_thumb(self,obj):
        if obj.archivo:
            thumb = get_thumbnail(obj.archivo.file, ADMIN_THUMBS_SIZE)
            return (u'<img width="%s" src="%s">' % (thumb.width, thumb.url))
        else:
            return "No Image" 
    my_image_thumb.allow_tags = True

class SMSAdmin(admin.ModelAdmin):
    list_display = ('format_date','smsc', 'fromnum', 'tonum', 'msg')
    date_hierarchy = 'received'
    actions = None 
    list_filter = ('smsc',)
    list_per_page = 30
    search_fields = ['fromnum','tonum','msg']

    def format_date(self, obj):
        return obj.received.strftime('%d-%m-%Y %H:%M:%S')
    
    format_date.short_description = 'Received date'
    format_date.admin_order_field = 'received'

    def has_add_permission(self, request):
        return False

admin.site.register(Ringtone)
admin.site.register(Estilo)
admin.site.register(Artista)
admin.site.register(Categoria)
admin.site.register(Wallpaper,WallpaperAdmin)
admin.site.register(SMS,SMSAdmin)
admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)

