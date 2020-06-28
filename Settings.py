
import os
import configparser

class ConfigAndSettings():
    
    def __init__(self, *args, **kwargs):

        self.LOGFILENAME='./REALTIMEADIFUPLOAD.log'
        self.configfilename="./loguploader.cfg"
        self.createConfigFile(self.configfilename)

        self.js8callIP=None
        self.tcpPort=None
        self.udpPort=None       
        self.qrzAPIKey= None
        self.qrzUserName=None
        self.qrzPassword=None
            
        self.eqsluser=None
        self.eqslpassword=None
        self.eqslqthnickname = None
            
        self.qrz=0
        self.qrzEnabled=False
            
        self.eqsl=0
        self.eqslEnabled=False
            
        self.hrd=0
        self.hrdlogEnabled=False
            
        self.club=0
        self.clublogEnabled=False
        
        self.qrzLookupEnabled=False
        self.qrzLookupInUse=False
        self.qrzInUse=False
        self.eqslInUse=False
        self.hrdInUse=False
        self.clubInUse=False

        self.loadSettings(self.configfilename)

    def setQRZAPIKey(self,value):
        self.qrzAPIKey=value
    def getQRZAPIKey(self):
        return self.qrzAPIKey
    def setQRZUserName(self,value):
        self.qrzUserName=value
    def getQRZUserName(self):
        return self.qrzUserName
    def setQRZPassword(self,value):
        self.qrzPassword=value
    def getQRZPassword(self):
        return self.qrzPassword
    def setEQSLUser(self,value):
        self.eqsluser=value
    def getEQSLUser(self):
        return self.eqsluser
    def setEQSLPassword(self,value):
        self.eqslpassword=value
    def getEQSLPassword(self):
        return self.eqslpassword
    def setEQSLQTHNickName(self,value):
        self.eqslqthnickname=value
    def getEQSLQTHNickName(self):
        return self.eqslqthnickname
    def setQRZEnabled(self,value):
        self.qrzEnabled=value
    def getQRZEnabled(self):
        return self.qrzEnabled
    def setEQSLEnabled(self,value):
        self.eqslEnabled=value
    def getEQSLEnabled(self):
        return self.eqslEnabled
    def setHRDLogEnabled(self, value):
        self.hrdlogEnabled=value
    def getHRDLogEnabled(self):
        return self.hrdlogEnabled
    def setClubLogEnabled(self,value):
        self.clublogEnabled=value
    def getClubLogEnabled(self):
        return self.clublogEnabled
    def setQRZLookupEnabled(self, value):
        self.qrzLookupEnabled=value
    def getQRZLookupEnabled(self):
        return self.qrzLookupEnabled
    def setQRZLookupInUse(self, value):
        self.qrzLookupInUse=value
    def getQRZLookupInUse(self):
        return self.qrzLookupInUse
    def setQRZInUse(self,value):
        self.qrzInUse=value
    def getQRZInUse(self):
        return self.qrzInUse
    def setEQSLInUse(self, value):
        self.eqslInUse=value
    def getEQSLInUse(self, value):
        return self.eqslInUse
    def setHRDInUse(self, value):
        self.hrdInUse=value    
    def getHRDInUse(self):
        return self.hrdInUse   
    def setClubLogInUse(self,value):
        self.clubInUse=value
    def getClubLogInUse(self):
        return self.clubInUse
    def getJS8CallIP(self):
        return self.js8callIP
    def setJS8CallIP(self, value):
        self.js8callIP=value
    def getUDPPort(self):
        return self.udpPort
    def setUDPPort(self, value):
        self.udpPort=value
    def getTCPPort(self):
        return self.tcpPort
    def setTCPPort(self, value):
        self.tcpPort=value

    def loadSettings(self,configfilename):
        self.createConfigFile(configfilename)

        if os.path.isfile(configfilename):
            config = configparser.ConfigParser()
            config.read(configfilename)

            
            self.qrzAPIKey= config.get('QRZ.COM', 'apikey')
            self.qrzUserName=config.get('QRZ.COM', 'username')
            self.qrzPassword=config.get('QRZ.COM', 'password')
            
            self.eqsluser= config.get('EQSL.CC', 'username')
            self.eqslpassword= config.get('EQSL.CC', 'password')
            self.eqslqthnickname = config.get('EQSL.CC', 'qthnickname')
            
            self.qrz=int(config.get('SERVICES-AT-STARTUP','qrz'))
            self.qrzEnabled=False
            if self.qrz==1:
                self.qrzEnabled=True
            
            self.eqsl=int(config.get('SERVICES-AT-STARTUP','eqsl'))
            self.eqslEnabled=False
            if self.eqsl==1:
                self.eqslEnabled=True
            
            self.hrd=int(config.get('SERVICES-AT-STARTUP','hrdlog'))
            self.hrdlogEnabled=False
            if self.hrd==1:
                self.hrdlogEnabled=True
            
            self.club=int(config.get('SERVICES-AT-STARTUP','clublog'))
            self.clublogEnabled=False
            if self.club==1:
                self.clublogEnabled=True
    
            self.isQRZLookupEnabled=int(config.get('SERVICES-AT-STARTUP','qrzlookup'))
            self.qrzLookupEnabled=False
            if self.isQRZLookupEnabled==1:
                self.qrzLookupEnabled=True
            
            self.isQRZLookupInUse=int(config.get('SERVICES-INUSE','qrzlookup'))
            self.qrzLookupInUse=False
            #print(self.isQRZLookupInUse)
            if self.isQRZLookupInUse==1:
                self.qrzLookupInUse=True

            try:
                self.js8callIP=config.get('JS8CALL', 'serverip')

                self.udpPort=int(config.get('JS8CALL', 'serverudpport'))
                self.tcpPort=int(config.get('JS8CALL', 'servertcpport'))

            except configparser.NoSectionError:
                
                #set defaults
                self.js8callIP='127.0.0.1'
                self.udpPort=2242
                self.tcpPort=2442

                config_update = configparser.RawConfigParser()
                config_update.add_section('JS8CALL')
                config_update.set('JS8CALL', 'serverudpport', self.udpPort)
                config_update.set('JS8CALL', 'servertcpport', self.tcpPort)
                config_update.set('JS8CALL', 'serverip', self.js8callIP)

                with open(configfilename, 'a') as f:
                    config_update.write(f)

    def saveConfigFile(self,configFileName):
                
        config = configparser.ConfigParser()
                            
        config['QRZ.COM'] = {'apikey': self.qrzAPIKey,
                            'username': self.qrzUserName,
                            'password': self.qrzPassword
                            }  
        config['EQSL.CC'] = {'username': self.eqsluser,
                            'password': self.qrzUserName,
                            'qthnickname': self.eqslqthnickname
                            }
        config['HRDLOG'] = {'username': 'USERNAME',
                            'password': 'PASSWORD'
                            }
        config['CLUBLOG'] = {'username': 'USERNAME',
                            'password': 'PASSWORD'
                            }
        
        config['SERVICES-AT-STARTUP'] = {'eqsl': 0,
                            'qrz': 0,
                            'clublog': 0,
                            'hrdlog': 0,
                            'qrzlookup':0
                            }  
        config['SERVICES-INUSE'] = {'eqsl': 1,
                            'qrz': 1,
                            'clublog': 0,
                            'hrdlog': 0,
                            'qrzlookup': 0
                            }  
        config['JS8CALL'] = {'serverip': self.js8callIP,
                             'serverudpport': self.udpPort,
                             'servertcpport': self.tcpPort
                            }

        with open(configFileName, 'w') as configfile:
            config.write(configfile)
            configfile.close()


    def createConfigFile(self,configFileName):
        if not os.path.isfile(configFileName):
                
            config = configparser.ConfigParser()
                                
            config['QRZ.COM'] = {'apikey': 'APIKEY',
                                'username': 'qrzuser',
                                'password': 'qrzpass'
                                }  
            config['EQSL.CC'] = {'username': 'USERNAME',
                                'password': 'PASSWORD',
                                'qthnickname': ''
                                }
            config['HRDLOG'] = {'username': 'USERNAME',
                                'password': 'PASSWORD'
                                }
            config['CLUBLOG'] = {'username': 'USERNAME',
                                'password': 'PASSWORD'
                                }
            
            config['SERVICES-AT-STARTUP'] = {'eqsl': 0,
                                'qrz': 0,
                                'clublog': 0,
                                'hrdlog': 0,
                                'qrzlookup': 0
                                }  
            config['SERVICES-INUSE'] = {'eqsl': 1,
                                'qrz': 1,
                                'clublog': 0,
                                'hrdlog': 0,
                                'qrzlookup': 1
                                }  
            config['JS8CALL'] = {'serverip': '127.0.0.1',
                             'serverudpport': 2242,
                             'servertcpport':2442
                            }

            with open(configFileName, 'w') as configfile:
                config.write(configfile)
                configfile.close()
        

if __name__=="__main__":
    config = ConfigAndSettings()
   # config.setQRZUserName("M6FLJ")
    #print(config.getQRZUserName())
