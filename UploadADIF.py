#! /usr/bin/python3

#Realtime ADIF uploaded for JS8Call
#By Mark - M0IAX
#http://m0iax.com/findme

import threading
from socket import socket, AF_INET, SOCK_DGRAM
import requests
import json
import time
import configparser
import os
import sys
import errno
from time import sleep
import urllib3
import LocalLog
import Settings

LOGFILENAME='./REALTIMEADIFUPLOAD.log'

#def createConfigFile(configFileName):
#    #cretes the config file if it does not exist
#    if not os.path.isfile(configFileName):
            
#        config = configparser.ConfigParser()
                            
#        config['QRZ.COM'] = {'apikey': 'APIKEY',
#                             'username': 'qrzuser',
#                             'password': 'qrzpass'
#                            }  
#        config['EQSL.CC'] = {'username': 'USERNAME',
#                             'password': 'PASSWORD',
#                             'qthnickname': ''
#                            }
#        config['HRDLOG'] = {'username': 'USERNAME',
#                             'password': 'PASSWORD'
#                            }
#        config['CLUBLOG'] = {'username': 'USERNAME',
#                             'password': 'PASSWORD'
#                            }
          
#        config['SERVICES-AT-STARTUP'] = {'eqsl': 0,
#                             'qrz': 0,
#                             'clublog': 0,
#                             'hrdlog': 0
#                            }  
#        config['SERVICES-INUSE'] = {'eqsl': 1,
#                             'qrz': 1,
#                             'clublog': 0,
#                             'hrdlog': 0
#                            }  
        
#        with open(configFileName, 'w') as configfile:
#            config.write(configfile)
#            configfile.close()
    
#configfilename="./loguploader.cfg"
#createConfigFile(configfilename)

#if os.path.isfile(configfilename):
#    config = configparser.ConfigParser()
#    config.read(configfilename)

   
#    qrzAPIKey= config.get('QRZ.COM', 'apikey')
#    qrzUserName=config.get('QRZ.COM', 'username')
#    qrzPassword=config.get('QRZ.COM', 'password')
    
#    eqsluser= config.get('EQSL.CC', 'username')
#    eqslpassword= config.get('EQSL.CC', 'password')
#    eqslqthnicjname = config.get('EQSL.CC', 'qthnickname')
    
#    qrz=int(config.get('SERVICES-AT-STARTUP','qrz'))
#    qrzEnabled=False
#    if qrz==1:
#        qrzEnabled=True
    
#    eqsl=int(config.get('SERVICES-AT-STARTUP','eqsl'))
#    eqslEnabled=False
#    if eqsl==1:
#        eqslEnabled=True
    
#    hrd=int(config.get('SERVICES-AT-STARTUP','hrdlog'))
#    hrdlogEnabled=False
#    if hrd==1:
#        hrdlogEnabled=True
    
 #   club=int(config.get('SERVICES-AT-STARTUP','clublog'))
 #   clublogEnabled=False
 #   if club==1:
 #       clublogEnabled=True
    
class UploadServer(threading.Thread):
    messageType='';
    messageText=''
    pttCount=0
    
    def toggleEQSL(self):
        self.eqslEnabled = not self.eqslEnabled
        return self.eqslEnabled
    def toggleQRZ(self):
        self.qrzEnabled = not self.qrzEnabled
        return self.qrzEnabled
    def toggleHRDLOG(self):
        self.hrdLogEnabled = not self.hrdLogEnabled
        return self.hrdLogEnabled
    def toggleCLUBLOG(self):
        self.clublogEnabled = not self.clublogEnabled
        return self.clublogEnabled
    
    def getQRZEnabled(self):
        return self.qrzEnabled
    def getEQSLEnabled(self):
        return self.eqslEnabled
    def getclublogEnabled(self):
        return self.clublogEnabled;
    def getHRDLOGEnabled(self):
        return self.hrdLogEnabled
    
    def setQRZEnabled(self, enabled):
        self.qrzEnabled=enabled
    def setEQSLEnabled(self, enabled):
        self.eqslEnabled=enabled
    def setQRZAPIKey(self, apikey):
        self.qrzAPIKey=apikey
        
    def __init__(self):
        t = threading.Thread.__init__(self)
        
        self.config=Settings.ConfigAndSettings()

        self.locallog=LocalLog.LocalLogger()
                
        #we can ignore the ssl warnings as the two domains we are uploading to are trusted
        urllib3.disable_warnings()
        self.showdebug=False
        self.listening = True
       
        self.hrdLogEnabled=self.config.getHRDLogEnabled() # hrdlogEnabled
        self.clublogEnabled=self.config.getClubLogEnabled() # clublogEnabled
        
        self.qrzEnabled=self.config.getQRZEnabled() #qrzEnabled
        
        self.eqslEnabled=self.config.getEQSLEnabled() # eqslEnabled
        
        self.qrzAPIKey = self.config.getQRZAPIKey() #qrzAPIKey
        self.qrzUserName = self.config.getQRZUserName() # qrzUserName
        self.qrzPassword = self.config.getQRZPassword() # qrzPassword
        self.eqslUser = self.config.getEQSLUser() #eqsluser
        self.eqslPassword = self.config.getEQSLPassword() # eqslpassword
        
        self.first = False
        self.messageText=None
        self.messageType=None
        self.pttCount = 0

    def getQRZUserName(self):
        return self.qrzUserName
    def getQRZPassword(self):
        return self.qrzPassword



    def processMessage(self,value):
        if self.qrzEnabled:
            self.uploadToQRZ(value)
        if self.eqslEnabled:
            self.uploadToEQSL(value)
        if self.clublogEnabled:
            self.uploadToCLUBLOG(value)
        if self.hrdLogEnabled:
            self.uploadToHRDLOG(value)
        if not self.qrzEnabled and not self.eqslEnabled and not self.clublogEnabled and not hrdlogEnabled:
            print ('No ADIF upload enabled. ADIF not uploaded.')
    
    def sendToQRZ(self, urlString, adif):
      
        self._session = requests.Session()
        self._session.verify = False
        r = self._session.get(urlString)
        if r.status_code == 200:
            if self.showdebug:
                print(r)
                print('rtext '+r.text)
            if "STATUS=FAIL" in r.text:
                print("Failed to upload to QRZ.com returned status is: ")
                print(r.text)
                self.locallog.addToOfflineLogFile(adif,LocalLog.uploadedQRZ)
            else:
                self.locallog.addToLogFile(adif,LocalLog.uploadedQRZ)
            return True
        
        print('Response: '+r)
        raise Exception("Could not send to QRZ")    
    
    def sendToEQSL(self, urlString, adif):
          
        self._session = requests.Session()
        r = self._session.get(urlString, verify=False)
        if r.status_code == 200:
            if self.showdebug:
                print(r)
                print(r.text)
            
            if "Result: 1 out of 1" not in r.text:
                print("Failed to upload to eQSL.cc returned status is: ")
                print(r.text)
                self.locallog.addToOfflineLogFile(adif,LocalLog.uploadedEQSL)
            else:
                self.locallog.addToLogFile(adif,LocalLog.uploadedEQSL)
            return True
        
        print('Response: '+r)
        raise Exception("Could not send to eQSL")    

    def sendToHRDLOG(self, urlString, adif):

        self._session = requests.Session()
        r = self._session.get(urlString, verify=False)
        if r.status_code == 200:
            if self.showdebug:
                print(r)
                print(r.text)
            
            if "Result: 1 out of 1" not in r.text:
                print("Failed to upload to eQSL.cc returned status is: ")
                print(r.text)
                self.locallog.addToOfflineLogFile(adif,LocalLog.uploadedEQSL)
            else:
                self.locallog.addToLogFile(adif,LocalLog.uploadedEQSL)
            return True
        
        print('Response: '+r)
        raise Exception("Could not send to eQSL")    

    def sendToCLUBLOG(self, urlString, adif):
          
        self._session = requests.Session()
        r = self._session.get(urlString, verify=False)
        if r.status_code == 200:
            if self.showdebug:
                print(r)
                print(r.text)
            
            if "Result: 1 out of 1" not in r.text:
                print("Failed to upload to eQSL.cc returned status is: ")
                print(r.text)
                self.locallog.addToOfflineLogFile(adif,LocalLog.uploadedEQSL)
            else:
                self.locallog.addToLogFile(adif,LocalLog.uploadedEQSL)
            return True
        
        print('Response: '+r)
        raise Exception("Could not send to eQSL")    
                
    def uploadToEQSL(self, adifEntry):
        print('Uploading to eQSL.cc')
        url='https://eQSL.cc/qslcard/importADIF.cfm?ADIFData={0}&EQSL_USER={1}&EQSL_PSWD={2}'
        url=url.format(adifEntry,self.eqslUser,self.eqslPassword)
        
        if self.showdebug:
            print('eqsl '+url)
        self.sendToEQSL(url, adifEntry)
        
    def uploadToQRZ(self, logEntry):
        print('Uploading to QRZ.com')
        url = ' https://logbook.qrz.com/api'
        url = url+'?KEY={0}&'
        url = url+'ACTION=INSERT&ADIF={1}'
        url = url.format(self.qrzAPIKey, logEntry)
        
        if self.showdebug:
            print(url)
        self.sendToQRZ(url,logEntry)
    
    def uploadToCLUBLOG(self, adifEntry):

        print('Club Log Upload not yet implemented')  
        return True

        print('Uploading to ClubLog')
        url=' https://clublog.org/realtime.php?email={0}&password={1}&callsign={2}&adif={3}&api={4}'
        url=url.format(self.clublogEmail,self.clublogPassword,self.clublogCallsign, adifEntry, self.clublogAPI)
        
        if self.showdebug:
            print('clublog '+url)
        self.sendToCLUBLOG(url, adifEntry)
    
    def uploadToHRDLOG(self, adifEntry):

        print('HRD Log Upload not yet implemented')  
        return True
        
        print('Uploading to eQSL.cc')
        url='https://eQSL.cc/qslcard/importADIF.cfm?ADIFData={0}&EQSL_USER={1}&EQSL_PSWD={2}'
        url=url.format(adifEntry,self.eqslUser,self.eqslPassword)
        
        if self.showdebug:
            print('eqsl '+url)
        self.sendToHRDLOG(url, adifEntry)
        
    def setListen(self, listen):
        self.listening=listen
            
    def close(self):
        self.listening = False

if __name__ == "__main__":
    
    server = UploadServer()