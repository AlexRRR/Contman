from celery.task import task
from content.models import Dynpath
from datetime import date,timedelta
from content.msgsender import send_wap_push

@task(name='tasks.clear_old_links')
def clear_old_links():
    '''This task deletes all dynamic links that are more
    than one day old'''
    yesterday = date.today()-timedelta(days=1)
    Dynpath.objects.filter(created__lt=yesterday).delete()

@task(name='tasks.send_wap_push')
def wap_push(smsc,phone,url,text):
    '''Non-blocking wap push tas to Kannel's ppg''' 
    send_wap_push(smsc,phone,url,text)
