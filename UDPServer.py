import threading

#from __future__ import print_function

from socket import socket, AF_INET, SOCK_DGRAM

import json
import time
import configparser
import os
#import configAndSettings

TYPE_GET_CALL_ACTIVITY="RX.GET_CALL_ACTIVITY"
TYPE_CALL_ACTIVITY='RX.CALL_ACTIVITY'

def createConfigFile(configFileName):
    #cretes the config file if it does not exist
    if not os.path.isfile(configFileName):
            
        config = configparser.ConfigParser()
        config['NETWORK'] = {'serverip': '127.0.0.1',
                             'serverudpport': 2242,
                             'servertcpport':2442
                            }
            
        with open(configFileName, 'w') as configfile:
            config.write(configfile)
            configfile.close()
    

configfilename="./js8call.cfg"
createConfigFile(configfilename)

if os.path.isfile(configfilename):
    config = configparser.ConfigParser()
    config.read(configfilename)

    serverip = config.get('NETWORK','serverip')
    serverport = int(config.get('NETWORK', 'serverudpport'))

listen = (serverip, serverport)


def from_message(content):
    try:
        return json.loads(content)
    except ValueError:
        return {}


def to_message(typ, value='', params=None):
    if params is None:
        params = {}
    return json.dumps({'type': typ, 'value': value, 'params': params})


class Server(threading.Thread):
    messageType='';
    messageText=''
    pttCount=0
    

    def __init__(self, uploadadif):
        t = threading.Thread.__init__(self)

        if uploadadif==None:
            self.uploadADIF = UploadADIF.UploadServer()
        else:
            self.uploadADIF = uploadadif 
        
        self.showDebug=False
        self.listrequested=False
        self.heardList=None
        
        self.first = False
        self.messageText=None
        self.messageType=None
        self.pttCount = 0
        self.selectedCall=None
    
    def getSelectedCall(self):
        return self.selectedCall
        
    def checkForSelectedCallsign(self,params):
        #print(params.get('SELECTED',''))
        freq=params.get('DIAL','')
        if freq!=None:
            self.selectedCall=params.get('SELECTED', '')

    def getheardlist(self):
        return self.heardList
        
    def setMessage(self, mType, mText):
        self.messageText=mText
        self.messageType=mType
        
    def process(self, message):
        typ = message.get('type', '')
        value = message.get('value', '')
        params = message.get('params', {})
        
        if self.messageType!=None:
            self.send(self.messageType, self.messageText)
            self.messageText=None
            self.messageType=None
            self.listrequested=True
        
        self.checkForSelectedCallsign(params)

        if not typ:
            return
        
        if typ == 'LOG.QSO':
            value = value+' <eor>'
            
            self.uploadADIF.processMessage(value)
               
        if typ == 'RIG.PTT':
            if value == 'on':
                self.pttCount = self.pttCount+1
                if self.showDebug:
                    print("PTT COUNT=====",self.pttCount)

        elif typ == 'CLOSE':
            self.close()

    def send(self, *args, **kwargs):
        params = kwargs.get('params', {})
        if '_ID' not in params:
            params['_ID'] = int(time.time()*1000)
            kwargs['params'] = params
        message = to_message(*args, **kwargs)
        if self.showDebug:
            print('outgoing message:', message)
        self.sock.sendto(message.encode(), self.reply_to)
    
    def run(self):
        print('udp API listening on', ':'.join(map(str, listen)))
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(listen)
        self.listening = True
        try:
            while self.listening:
                content, addr = self.sock.recvfrom(65500)
                
                #print('incoming message:', ':'.join(map(str, addr)))

                try:
                    message = json.loads(content)
                except ValueError:
                    message = {}


                if not message:
                    continue

                if self.showDebug:
                    print(message)        

                self.reply_to = addr
                self.process(message)

        finally:
            self.sock.close()

    def close(self):
        self.listening = False


if __name__ == "__main__":
    #def main():
    server = Server()
    server.start()
    #s.listen()

