from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist
from content.models import SMS
from content.models import Contenido
from content.models import Dynpath
from content.views import keyword_matches
from content.views import create_dynpath
from datetime import date,timedelta
from content.tasks import clear_old_links
import content.msgsender
import time
import mox




class EntryViewTestCase(TestCase):

    fixtures = ['polls_views_testdata.json']

    def setUp(self):
        self.client = Client()
        self.existing_keyword = "chrome"
        self.not_existing_keyword = "gugaguga"
        self.invalid_text = "Invalid keyword"
        self.insert_two_sample_sms()
        delivery_template = 'delivery.txt'
        self.reply_template = [delivery_template]
        self.mox = mox.Mox()
        self.accepted_pap = """<?xml version="1.0"?><!DOCTYPE pap PUBLIC "-//WAPFORUM//DTD PAP 1.0//EN" "http://www.wapforum.org/DTD/pap_1.0.dtd"><pap><push-response push-id="ea3735c6-c3e6-42c2-882e-42fc21d9714b" sender-name="T-HAE0006.svoice.net; WAP/1.3 (Kannel/svn-r4952)" reply-time="2012-04-13T09:28:44Z" sender-address="/wappush"><response-result code ="1001" desc="The request has been accepted for processing"></response-result></push-response></pap>"""

    def tearDown(self):
        self.mox.UnsetStubs()


    def insert_two_sample_sms(self):
        accepted_pap = """<?xml version="1.0"?><!DOCTYPE pap PUBLIC "-//WAPFORUM//DTD PAP 1.0//EN" "http://www.wapforum.org/DTD/pap_1.0.dtd"><pap><push-response push-id="ea3735c6-c3e6-42c2-882e-42fc21d9714b" sender-name="T-HAE0006.svoice.net; WAP/1.3 (Kannel/svn-r4952)" reply-time="2012-04-13T09:28:44Z" sender-address="/wappush"><response-result code ="1001" desc="The request has been accepted for processing"></response-result></push-response></pap>"""

        for a in [1,2]:
            mx = mox.Mox()
            mx.StubOutWithMock(content.msgsender, 'post_si_message')
            content.msgsender.post_si_message(mox.IgnoreArg(),mox.IgnoreArg(),mox.IgnoreArg()).AndReturn(accepted_pap)
            mx.ReplayAll()
            self.client.get('/entry/', {'fromnum': '50240113163','tonum': '1650','smsc':'TIGO','msg': 'chrome'})
            mx.UnsetStubs()
            mx.VerifyAll()


    def test_sms_entrance(self):
        """SMS correctly saved in DB from post and renders the correct template"""
        self.mox.StubOutWithMock(content.msgsender, 'post_si_message')
        content.msgsender.post_si_message(mox.IgnoreArg(),mox.IgnoreArg(),mox.IgnoreArg()).AndReturn(self.accepted_pap)
        self.mox.ReplayAll()
        resp = self.client.get('/entry/', {'fromnum': '50240113163',
                                    'tonum': '1650',
                                    'smsc': 'TIGO', 
                                    'msg': 'chrome'})
        time.sleep(1)
        self.assertTrue('http://example.com/content/' in resp.content)
        self.assertTrue(SMS.objects.all().filter(fromnum='50240113163').exists())
        templates_used = []
        for template in resp.templates:
            templates_used.append(template.name)
        self.assertEquals(templates_used, self.reply_template)
        self.mox.VerifyAll()

    def test_matching_keyword(self):
        """Matching keyword"""
        self.assertTrue(keyword_matches(self.existing_keyword))

    def test_not_matching_keyword(self):
        """Not matching keyword"""
        self.assertFalse(keyword_matches(self.not_existing_keyword))

    def test_invalid_reply(self):
        """Invalid keyword reply is sent when needed"""
        resp = self.client.get('/entry/', {'fromnum': '50240113163',
                                    'tonum': '1650',
                                    'smsc': 'TIGO',
                                    'msg': 'invalidtext'})
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.content,self.invalid_text, "Wrong invalid keyword reply")

    def test_dynamic_path_creation(self):
        """check dynamic path is correctly generated and stored in DB"""
        content = Contenido.objects.get(keyword=self.existing_keyword)
        sms = SMS.objects.get(id=1) 
        dyn_path = create_dynpath(sms,content)
        stored_dyn = Dynpath.objects.get(id=dyn_path.id)
        self.assertEqual(stored_dyn,dyn_path)
        self.assertTrue(stored_dyn.url_path)
        
    def test_dynamic_path_access(self):
        """dynamic url exists and generates expected content"""
        content = Contenido.objects.get(keyword=self.existing_keyword)
        sms = SMS.objects.get(id=1)
        dyn_path = create_dynpath(sms,content)
        url = '/content/' + str(dyn_path.url_path) + "/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp.get('Content-Disposition'),"attachment; filename=chrome.jpg")


    def test_expired_link(self):
        """expired link must deliver a defined msg, not content (expired dynpath from fixture)"""
        dyn_path = Dynpath.objects.get(id=1)
        url = '/content/' + str(dyn_path.url_path) + "/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code,404)
        
    def test_delete_expired(self):
        clear_old_links.delay()
        with self.assertRaises(ObjectDoesNotExist) as cm:
            Dynpath.objects.get(id=1)


    def test_pap_parser(self):
        """Correct responses from the PPG should be parsed"""
        accepted_code = "1001"
        accepted_msg = "The request has been accepted for processing"
        (code, msg) = content.msgsender.parse_pap_xml(self.accepted_pap)
        self.assertEquals(code, accepted_code)
        self.assertEquals(msg, accepted_msg)

