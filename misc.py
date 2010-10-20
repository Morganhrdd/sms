
import httplib
import datetime
import urllib
USER='changeme'
PASSWORD='changeme'
SENDERID='changeme'

def sms_send(user=USER, password=PASSWORD, senderid=SENDERID, nos=None, msg=None, schedule=None):
    for no in nos:
        params = urllib.urlencode({'user': user, 'pwd': password, 'senderid': senderid, 'mobileno':str(no), 'msgtext': msg, 'priority':'High'})
        conn = httplib.HTTPConnection('bulksmspune.mobi', 80)
        conn.request("GET", "/sendurl.asp?%s"%(params))
        response = conn.getresponse()
        conn.close()


if __name__ == '__main__':
    no = raw_input('Enter 10 digit number: ')
    sms_send(nos=[no], msg='testing...using http api')
