from content.models import Ringtone,Estilo,Artista,Categoria,Wallpaper,Contenido
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe
from django.contrib.contenttypes import generic
from django import forms

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



admin.site.register(Ringtone)
admin.site.register(Estilo)
admin.site.register(Artista)
admin.site.register(Categoria)
admin.site.register(Wallpaper,WallpaperAdmin)
