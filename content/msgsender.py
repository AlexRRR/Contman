'''Module to send messages (text, binary) using Kannel PPG'''
import uuid
import httplib
import kannel_settings
import xml.dom.minidom as minidom
import logging

logger = logging.getLogger('to_file')


def generate_si_body(smsc,phone,url,text):
    '''generates body of SI message'''
    unique_id = uuid.uuid4()
    template = "--multipart-boundary\r\n\
Content-type: application/xml\r\n\r\n\
<?xml version=\"1.0\"?>\r\n\
<!DOCTYPE pap PUBLIC \"-//WAPFORUM//DTD PAP 1.0//EN\"\r\n\
\"http://www.wapforum.org/DTD/pap_1.0.dtd\">\r\n\
<pap>\r\n\
<push-message push-id=\"%s\">\r\n\
<address address-value=\"WAPPUSH=%s/TYPE=PLMN@ppg.nokia.com\"/>\r\n\
<quality-of-service delivery-method=\"unconfirmed\" network=\"GSM\" bearer=\"SMS\"/>\
</push-message>\r\n\
</pap>\r\n\r\n\
--multipart-boundary\r\n\"\
Content-type: text/vnd.wap.si\r\n\r\n\
<?xml version=\"1.0\"?>\r\n\
<!DOCTYPE si PUBLIC \"-//WAPFORUM//DTD SI 1.0//EN\"\r\n\
\"http://www.wapforum.org/DTD/si.dtd\">\r\n\
<si>\r\n\
<indication action=\"signal-high\" si-id=\"%s\" href=\"%s\">%s</indication>\r\n\
</si>\r\n\
--multipart-boundary--\r\n"
    
    body = template % (unique_id,phone,unique_id,url,text)

    return body

def post_si_message(body,smsc,shortcode):
    '''sends POST data to host:port at entry_path'''
    h = httplib.HTTPConnection(kannel_settings.PPG_URL,kannel_settings.PPG_PORT)
    h.putrequest('POST',kannel_settings.PPG_ENTRY)
    h.putheader('Content-Type', 'multipart/related; boundary=multipart-boundary; type="application/xml"')
    h.putheader('Content-Length',str(len(body)))
    h.putheader('X-Kannel-SMSC', smsc)
    h.putheader('X-Kannel-From', shortcode)
    h.endheaders()
    h.send(body)
    response = h.getresponse()
    return response.read()

def send_wap_push(smsc,phone,shortcode,url,text):
    '''calls body generation and posts to URL'''
    signed_phone = format_phone(phone)
    body = generate_si_body(smsc,signed_phone,url,text)
    ppg_response = post_si_message(body,smsc,shortcode)
    code, desc = parse_pap_xml(ppg_response)
    if code[0] == "1":
        logger.info("PPG Response %s: %s" % (code,desc))
    elif code[0] == "2":
        logger.error("PPG Response %s: %s" % (code,desc))
    else:
        logger.warning("Unexpected PPG Response %s:%s" % (code,desc))


def format_phone(phone):
    if phone[0] != "+":
        signed_phone = ("+%s" % phone)
    else:
        signed_phone = phone
    return signed_phone

def parse_pap_xml(xmlstring):
    doc = minidom.parseString(xmlstring)
    node = doc.documentElement
    pap = doc.getElementsByTagName("pap")[0]
    result = pap.getElementsByTagName("response-result")[0]
    (code, desc) = (result.getAttribute('code'),result.getAttribute('desc'))
    return (code,desc)

    


