#QRZLookup
import xmltodict
import requests
import urllib3

APPNAME='M0IAXQRZLookup1.0'
class QRZLookup(object):

    def setSessionKey(self):
        self.sessionKey=None
        sessionKeyUrl = '''https://xmldata.qrz.com/xml/current/?username={0}&password={1}'''.format(self.userName, self.password)
        self.session = requests.Session()
        self.session.verify = False
        r = self.session.get(sessionKeyUrl)
        if r.status_code == 200:
            print(r)
            sessionkey_xml = xmltodict.parse(r.content)
            self.sessionKey = sessionkey_xml['QRZDatabase']['Session']['Key']
            if self.sessionKey:
                return True
        raise Exception("Could not get QRZ session")

    def __init__(self, userName, password):
        self.userName = userName
        self.password = password
        print('uname '+self.userName)
        self.sessionKey=None
        self.numretries=0
        urllib3.disable_warnings()
        if self.userName!="qrzuser":
            self.setSessionKey()
        
    def getSessionKey(self):
        return self.sessionKey

    def lookupCallsign(self, callsign):
        if self.sessionKey==None:
            self.getSessionKey()
        if self.userName=="qrzuser":
            return
        url = """http://xmldata.qrz.com/xml/current/?s={0}&callsign={1}&agent={2}""".format(self.sessionKey, callsign, APPNAME)
        r = self.session.get(url)
        if r.status_code != 200:
            raise Exception("Error Querying: Response code {}".format(r.status_code))
        
        xmldata = xmltodict.parse(r.content).get('QRZDatabase')
        
        
        if not xmldata:
            raise Exception('Unexpected QRZ Result')
        if xmldata['Session'].get('Error'):
            errormsg = xmldata['Session'].get('Error')
            if 'Session Timeout' in errormsg or 'Invalid session key' in errormsg:
                print(errormsg)
                self.setSessionKey()
                self.numretries += 1
                if self.numretries>=5:
                    print('Max Retries exceeded, unable to upload to qrz')
                else:    
                    self.lookupCallsign(callsign)
        else:
            stationdata = xmldata.get('Callsign')
            self.numretries = 0
            if stationdata:
                return stationdata
        #raise Exception("Unexcepcted error in qrz query")

if __name__=="__main__":
    qrz=QRZLookup('','')
    #print(qrz.getSessionKey())
    
    print("Getting data from QRZ.COM")
    
    callxmldata=qrz.lookupCallsign('M0IAX')
    
    print(callxmldata.get('call'))
    print(callxmldata.get('grid'))
    print(callxmldata.get('addr2'))
    print(callxmldata.get('land'))
    print(callxmldata.get('qslmgr'))
    
    print(callxmldata)
    
    
    
    