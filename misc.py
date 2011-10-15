
import httplib
import datetime
import urllib

'''
def sms_send(user=USER, password=PASSWORD, senderid=SENDERID, nos=None, msg=None, schedule=None):
    for no in nos:
        try:
            params = urllib.urlencode({'user': user, 'pwd': password, 'senderid': senderid, 'mobileno':str(no), 'msgtext': msg, 'priority':'High'})
        except:
            tmp = {'user': user, 'pwd': password, 'senderid': senderid, 'mobileno':str(no), 'msgtext': msg.encode('utf-8'), 'priority':'High'}
            params = 'user=%(user)s&pwd=%(pwd)s&senderid=%(senderid)s&mobileno=%(mobileno)s&msgtext=%(msgtext)s&priority=High' % tmp
        conn = httplib.HTTPConnection('bulksmspune.mobi', 80)
        conn.request("GET", "/sendurl.asp?%s"%(params))
        response = conn.getresponse()
        conn.close()
        return response
'''
'''
def sms_send(user=USER, password=PASSWORD, senderid=SENDERID, nos=None, msg=None, schedule=None):

    for no in nos:
        try:
            params = urllib.urlencode({'username': user, 'api_password': password, 'sender': senderid, 'to':str(no), 'message': msg, 'priority':'1'})
        except:
            tmp = {'username': user, 'api_password': password, 'sender': senderid, 'to':str(no), 'message': msg.encode('utf-8'), 'priority':'1', 'unicode':'1'}
            params = 'username=%(username)s&api_password=%(api_password)s&sender=%(sender)s&to=%(to)s&message=%(message)s&priority=%(priority)s&unicode=%(unicode)s' % tmp
        conn = httplib.HTTPConnection('bulk.seasms.com', 80)
        conn.request("GET", "/pushsms.php?%s"%(params))
        response = conn.getresponse()
        conn.close()
        return response
'''
def sms_send(user=USER, password=PASSWORD, senderid=SENDERID, nos=None, msg=None, schedule=None, stype='normal'):
    for no in nos:
        #params = urllib.urlencode({'user': user, 'pwd': password, 'senderid': senderid, 'mobileno':str(no), 'msgtext': msg, 'priority':'High'})
        params = urllib.urlencode({'user': user, 'pass': password, 'sender': senderid, 'phone':str(no), 'priority':'ndnd', 'stype':stype, 'text':msg.encode('utf-8')})
        conn = httplib.HTTPConnection('bhashsms.com', 80)
        conn.request("GET", "/api/sendmsg.php?%s"%(params))
        response = conn.getresponse()
        print response.status, response.read()
        conn.close()


if __name__ == '__main__':
    no = raw_input('Enter 10 digit number: ')
    sms_send(nos=[no], msg='testing...using http api')
