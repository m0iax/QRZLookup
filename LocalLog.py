import time
import sys
import os
from datetime import date

uploadedQRZ='QRZ.COM'
uploadedEQSL='EQSL.CC'

MAINLOGFILENAME=sys.path[0]+"/logs/UploadedADIFs.log"
DAILYLOGFILENAME=None


class LocalLogger():
    def createLogFile(self, fileName):
        file = open(fileName, "w+")
        file.close()
        return True
    def getDailyLogFileName(self):
        dailyFileName=self.getTodaysFileName()
        if not os.path.isfile(dailyFileName):
            self.createLogFile(dailyFileName)
        return dailyFileName
   
    def getLogFileName(self):
        if not os.path.isfile(MAINLOGFILENAME):
            self.createLogFile(MAINLOGFILENAME)
        return(MAINLOGFILENAME)

    def appendToFile(self, filename, stringtoappend):
        file = open(filename, "a+") 
        file.write(stringtoappend+"\n")
        file.close()
        
    def addToLogFile(self, entryadif, uploadedTo):
        file = self.getLogFileName()
        addString=entryadif+","+uploadedTo
        self.appendToFile(file,addString)
        return True
    def addToOfflineLogFile(self, entryadif, uploadedTo):
        file = self.getDailyLogFileName()
        addString=entryadif+","+uploadedTo
        self.appendToFile(file,addString)
        return True
    
    def initlogs(self):
        self.checkForLogDir()
        offlineFile=self.getDailyLogFileName()
        logFile=self.getLogFileName() 
        return True
    def checkForLogDir(self):
        if not os.path.exists(sys.path[0]+'/logs'):
            os.makedirs(sys.path[0]+'/logs')
    def getTodaysFileName(self):
        today = date.today()
        todaysDateString=today.strftime("%Y-%m-%d")
        filename='%s/logs/%s-OffLine.log' % (sys.path[0],todaysDateString)
        return filename
    def __init__(self):
        self.initlogs()   
    def getTimeInMillis(self):
        timeNum=int(round(time.time() * 1000))
        return timeNum


if __name__=="__main__":
    locallog = LocalLogger()
    string = str(int(round(time.time() * 1000)))
    locallog.addToLogFile(string,uploadedEQSL)
    
    string = str(int(round(time.time() * 1000)))
    locallog.addToLogFile(string,uploadedQRZ)
    
    string = str(int(round(time.time() * 1000)))
    locallog.addToOfflineLogFile(string,uploadedEQSL)
    
    string = str(int(round(time.time() * 1000)))
    locallog.addToOfflineLogFile(string,uploadedQRZ)
    
    