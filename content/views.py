# Create your views here.
from content.models import SMS
from content.models import Contenido
from content.models import Dynpath
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404,render_to_response
from random import getrandbits
from datetime import date,timedelta
from content.tasks import wap_push
import mimetypes
import os
def sms_entrance(request):
    try:
        sms = SMS()
        sms.fromnum = request.GET.__getitem__('fromnum')
        sms.tonum = request.GET.__getitem__('tonum')
        sms.smsc = request.GET.__getitem__('smsc')
        sms.msg = request.GET.__getitem__('msg')

        content = keyword_matches(sms.msg)
        if content:
            sms.valid = True
        else:
            sms.valid = False
        sms.save()
    except KeyError:
        raise Http404
    
    if sms.valid:
         d = create_dynpath(sms,content)
         wap_push(sms.smsc,sms.fromnum,d.url_path,'Descarga tu contenido de este link')
         return render_to_response('delivery.txt',{'url':d.url_path})
    else:
        return HttpResponse("Invalid keyword")


def keyword_matches(txt):
    """Searches all existing keywords for a positive match
    If it matches, returns Contenido object, else returns False"""
    try:
        content = Contenido.objects.get(keyword=txt)
        return content
    except Contenido.DoesNotExist:
        return False


def create_dynpath(sms,content):
    """Creates and stores dynamic content pointers"""
    d = Dynpath()
    d.url_path = getrandbits(64)
    d.payload = content
    d.sms = sms
    d.created = date.today()
    d.save()
    return d

def tempurl(request,hash):
    yesterday = date.today()-timedelta(days=1)
    p = get_object_or_404(Dynpath, url_path=hash,created__gt=yesterday)
    try:
        fname = str(p.payload.wallpaper.archivo)
    except DoesNotExist:
        fname = str(p.payload.ringtone.archivo)
    
    fn = open(fname,'rb')
    response = HttpResponse(fn.read())
    fn.close()
    file_name = os.path.basename(fname)
    type, encoding = mimetypes.guess_type(file_name)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Disposition'] = ('attachment; filename=%s') % file_name
    return response 
