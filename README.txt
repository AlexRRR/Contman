

CONTMAN: Simple Mobile Content Distributor

This project is so far just a starting point for mobile content management & delivery using
Django and Kannel PPG (push proxy gateway) for delivering content via WAP PUSH Service Indication, via an SMPP connection or GSM modem.

Basic Functionality:
--------------------

-The idea is to have a central repository where Mobile content can be uploaded and managed: Ringtones orImages, each with a unique keyword assigned. 
-Then if an SMS is received in Kannel over a specific shortcode, it will be forwarded to the application. 
-The application tries to match the keyword sent in the SMS to those assigned in the content manager.
-The application creates a temporary  "dynamic URL" which points to the requested content.
-A standard default msg is returned to the mobile which sent the SMS.
-A Service Indication (SI) XML is then Sent to Kannel's PPG, this is done in a none blocking fashion, using Celery.
-The message is encoded to WBXML and sent over the network to the mobile that created the request.
-When the user clicks this link the content is downloaded to his mobile.
-After an specific period of time the Dynamic path expires and is no longer reachable.

Installation
------------

Requirements:
- django 1.3
- sorl-thumbnail
- django-celery
- kannel
- pymox (optional: for mocking kannel in unittests only)

Kannel configuration:
---------------------

Please read the sample.kannel.conf file included. This sample configuration setsup the Kannel Push Proxy Gateway like this:

group             = ppg
ppg-url           = /wappush
ppg-port          = 8080
concurrent-pushes = 100
users             = 1024
ppg-allow-ip      = "127.0.0.1"
trusted-pi        = true
service-name      = ppg1

This configuration should match with the one found in

content/kannel_settings.py i.e.:

PPG_URL = '127.0.0.1'
PPG_PORT = '8080'
PPG_ENTRY = '/wappush'


For the forwarding of the incoming SMS messages configure the sms-service group with the following configuration (this examples forwards all msgs coming to the shortcode 555 to the content management system). 

#PPG
group = sms-service
keyword-regex = .*
allowed-receiver-prefix-regex=^555
get-url = "http://localhost/contman/entry/?fromnum=%p&tonum=%P&msg=%a&smsc=%i"
accept-x-kannel-headers = true

Wishlist:
--------

So far the functionality is pretty basic, but slowly it is intented to add more basic feautures which include:

- Add the delivery of standard (non WAP PUSH) links, this would enable to deliver taking advantage of SMS billing to modern phones, which no longer support WAP PUSH.
- Reports, right now it is assumed that Kannel's SQLBOX is used for billing and there are no actual download reports, or any reports for that matter. This needs to change.
- Content adaptation: it would be very useful add some capabilities discovery using WURFL or DeviceAtlas (or both?) to have richer reports and finer grained delivery.
- Point of interest in images: It would be good to have a user defined point of interest to be more certain that the image cropping (described in the line above) for the devices that need it.


Hope you enjoy this!


A. Ramirez
