from celery.task import task
from content.models import Dynpath
from datetime import date,timedelta
from content.msgsender import send_wap_push
import logging

logger = logging.getLogger('to_file')



@task(name='tasks.clear_old_links')
def clear_old_links():
    '''This task deletes all dynamic links that are more
    than one day old'''
    logger.debug("Task execute: clearing old dynamic links")
    yesterday = date.today()-timedelta(days=1)
    Dynpath.objects.filter(created__lt=yesterday).delete()

@task(name='tasks.send_wap_push')
def wap_push(smsc,phone,shortcode,url,text):
    '''Non-blocking wap push tas to Kannel's ppg''' 
    logger.debug("Task execute: attemping to send WAP push to %s with link %s" % (phone,url))
    send_wap_push(smsc,phone,shortcode,url,text)
