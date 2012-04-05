from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render_to_response
from content.models import SMS

# Create your views here.

def overview(request,rtype):
    sms_list = SMS.objects.all()
    return render_to_response('sms_list.html', {"sms_list": sms_list})

