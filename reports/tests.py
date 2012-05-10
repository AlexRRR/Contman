from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist
from content.models import SMS
from content.models import Contenido
from content.models import Dynpath
from content.views import keyword_matches
from content.views import create_dynpath
from reports.views import *
from datetime import date,timedelta




class EntryViewTestCase(TestCase):
    
    fixtures = ['reports.json']

    def setUp(self):
        self.expected_month_first_last_empty=[{'date_created': '2012-03-01', 'created_count': 0}, {'date_created': u'2012-04-01', 'created_count': 2}, {'date_created': u'2012-05-01', 'created_count': 1}, {'date_created': '2012-06-01', 'created_count': 0}, {'date_created': '2012-07-01', 'created_count': 0}]
        self.expected_month_first_last_match=[{'date_created': u'2012-04-01', 'created_count': 2}, {'date_created': u'2012-05-01', 'created_count': 1}]
        self.expected_date = [{'date_created': '2012-04-22', 'created_count': 0}, {'date_created': u'2012-04-23', 'created_count': 2}, {'date_created': '2012-04-24', 'created_count': 0}, {'date_created': '2012-04-25', 'created_count': 0}, {'date_created': '2012-04-26', 'created_count': 0}, {'date_created': '2012-04-27', 'created_count': 0}, {'date_created': '2012-04-28', 'created_count': 0}, {'date_created': '2012-04-29', 'created_count': 0}, {'date_created': '2012-04-30', 'created_count': 0}, {'date_created': '2012-05-01', 'created_count': 0}, {'date_created': '2012-05-02', 'created_count': 0}, {'date_created': '2012-05-03', 'created_count': 0}, {'date_created': '2012-05-04', 'created_count': 0}, {'date_created': '2012-05-05', 'created_count': 0}, {'date_created': '2012-05-06', 'created_count': 0}, {'date_created': '2012-05-07', 'created_count': 0}, {'date_created': '2012-05-08', 'created_count': 0}, {'date_created': '2012-05-09', 'created_count': 0}, {'date_created': '2012-05-10', 'created_count': 0}, {'date_created': u'2012-05-11', 'created_count': 1}, {'date_created': '2012-05-12', 'created_count': 0}]

    def test_report_date_list(self):
        self.assertEquals(report_by_month("2012-03-01","2012-07-21"),self.expected_month_first_last_empty)
        self.assertEquals(report_by_month("2012-04-01","2012-05-21"),self.expected_month_first_last_match)


    def test_report_day_list(self):
        self.assertEquals(report_by_date("2012-04-22","2012-05-12"),self.expected_date)



        
