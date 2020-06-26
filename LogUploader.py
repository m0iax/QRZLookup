#! /usr/bin/python3

#Realtime ADIF uploaded for JS8Call
#By Mark - M0IAX
#http://m0iax.com/findme

import QRZLookup
from tkinter import *
from tkinter import Frame
import UDPServer
import UploadADIF
import json
import Settings


WIDTH=270
HEIGHT=270
appName="Log Uploader for JS8Call"

class UI(Tk):
    
    def doLookupAndDisplay(self, callsign):
        
        if callsign:
            self.lastLookupCall=callsign
            callxmldata = self.qrz.lookupCallsign(callsign)
            if callxmldata:
                
                qslmgr=callxmldata.get('qslmgr')
                if qslmgr==None:
                    qslmgr=''

                self.qrzCall.set(callxmldata.get('call'))
                self.qrzFName.set(callxmldata.get('fname'))
                self.qrzGrid.set(callxmldata.get('grid'))
                self.qrzCity.set(callxmldata.get('addr2'))
                self.qrzCountry.set(callxmldata.get('land'))
                self.qrzMgr.set(qslmgr)
        
    def loadSettings(self, settingValues):
        print('Loading settings')
    
    def __exit__(self, exc_type, exc_val, exc_tb):
            print("Main Window is closing, call any function you'd like here!")

    def __enter__(self):
      
        print('Starting')
    def ask_quit(self):
        if self.upLoader!=None:
            print('Shutting down ADIF Listener')
            self.upLoader.setListen(False)
            self.upLoader.join()
        if self.udpserver!=None:
            print('Shutting down UDP Server')
            self.udpserver.close()
        if self.tcpClient!=None:
            print('Shutting down TCP Client')
            self.udpserver.close()
            
        print('Exiting. Thanks for using '+appName+' By M0IAX')
        
        self.destroy() 
    def updateeQSL(self):
        if self.upLoader!=None:
            enabled=self.upLoader.toggleEQSL()
            self.configureEQSLButton(enabled)
        if self.uploadADIF!=None:
            enabled=self.uploadADIF.toggleEQSL()
            self.configureEQSLButton(enabled)
            
    def updateQRZ(self):
        if self.upLoader!=None:
            enabled=self.upLoader.toggleQRZ()
            self.configureQRZButton(enabled)
        if self.uploadADIF!=None:
            enabled=self.uploadADIF.toggleQRZ()
            self.configureQRZButton(enabled)
            
    def configureQRZButton(self, enable):
        if enable:
            self.enableQRZButton.configure(bg="green")
            self.enableQRZButton.configure(text="QRZ Upload Enabled")
            
        else:
            self.enableQRZButton.configure(bg="red")
            self.enableQRZButton.configure(text="QRZ Upload Disabled")
            
    def configureEQSLButton(self, enable):
        if enable:
            self.enableQSLButton.configure(bg="green")
            self.enableQSLButton.configure(text="eQSL Upload Enabled")    
        else:
            self.enableQSLButton.configure(bg="red")
            self.enableQSLButton.configure(text="eQSL Upload Disabled")
     
    def selectedItem(self,event):
        selectedCallsign = self.callsignListbox.get(self.callsignListbox.curselection())
        #print(selectedCallsign)
        #self.qrz.lookupCallsign(selectedCallsign)
        self.doLookupAndDisplay(selectedCallsign)
        
    def show_qrzThings(self, frame, controller):
    
        self.callsignListbox = Listbox(frame, height=8, width=10)
        self.callsignListbox.grid(row=0, column=0)
        self.callsignListbox.bind('<<ListboxSelect>>',self.selectedItem)   
        self.detailsText = Text(frame, height=8, width=30)
        self.detailsText.grid(row=0, column=1)
        
    def showQRZInfoPane(self,frame,controller):

        if self.qrzLookupInUse:
            py=0

            self.callsignTitleLabel=Label(frame,text="Callsign",relief=RAISED )
            self.callsignTitleLabel.grid(row=0, column=0, padx=5, pady=py, stick='e')
            
            self.callsignLabel=Label(frame,textvariable=self.qrzCall)
            self.callsignLabel.grid(row=0, column=1, padx=5, pady=py, stick="w")
            #self.callsignLabel.place(relx = 0.5, rely = 0.1, anchor = CENTER)
            
            self.fnameTitleLabel=Label(frame,text="Name",relief=RAISED)
            self.fnameTitleLabel.grid(row=1, column=0, padx=5, pady=py, stick='e')
            #self.fnameTitleLabel.place(relx = 0.02, rely = 0.1, anchor = CENTER)
            
            self.fnameLabel=Label(frame,textvariable=self.qrzFName)
            self.fnameLabel.grid(row=1, column=1, padx=5, pady=py, stick='w')
            #self.fnameTitleLabel.place(relx = 0.02, rely = 0.5, anchor = CENTER)
            
            self.gridTitleLabel=Label(frame,text="Grid",relief=RAISED)
            self.gridTitleLabel.grid(row=2, column=0, padx=5, pady=py, stick='e')
            
            self.gridLabel=Label(frame,textvariable=self.qrzGrid)
            self.gridLabel.grid(row=2, column=1, padx=5, pady=py, stick='w')
            
            self.cityTitleLabel=Label(frame,text="City",relief=RAISED)
            self.cityTitleLabel.grid(row=3, column=0, padx=5, pady=py, stick='e')
            
            self.cityLabel=Label(frame,textvariable=self.qrzCity)
            self.cityLabel.grid(row=3, column=1, padx=5, pady=py, stick='w')
            
            self.countryTitleLabel=Label(frame,text="Country",relief=RAISED)
            self.countryTitleLabel.grid(row=4, column=0, padx=5, pady=py, stick='e')
            
            self.countryLabel=Label(frame,textvariable=self.qrzCountry)
            self.countryLabel.grid(row=4, column=1, padx=5, pady=py, stick='w')
            
            self.qslTitleLabel=Label(frame,text="QSL Mgr",relief=RAISED)
            self.qslTitleLabel.grid(row=5, column=0, padx=5, pady=py, stick='e')
            
            self.qslLabel=Label(frame,width=20,textvariable=self.qrzMgr,wraplength=150, justify=CENTER)
            self.qslLabel.grid(row=5, column=1, padx=5, pady=py)
        
    def show_buttons(self, frame, controller):

        self.enableQRZButton=Button(frame,text='QRZ Upload Disabled', bg="red", command=self.updateQRZ)
        self.enableQRZButton.grid(row=0, column=0, padx=5, pady=5)
                
        self.enableQSLButton=Button(frame,text='Enable eQSL Upload', bg="red", command=self.updateeQSL)
        self.enableQSLButton.grid(row=1, column=0, padx=5, pady=5)
        
#        self.getheardButton=Button(frame,text='Lookup Heard Station List', bg="blue", command=self.getheard)
#        self.getheardButton.grid(row=2, column=0, padx=5, pady=5)
 
    def update_timer(self):
        self.selectedCall=self.udpserver.getSelectedCall()
        if self.selectedCall!=self.lastLookupCall:
            self.doLookupAndDisplay(self.selectedCall)

        self.after(1000, self.update_timer)
            
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        self.config=Settings.ConfigAndSettings()

        self.qrzCall = StringVar()
        self.qrzCall.set("                     ")
        self.qrzFName = StringVar()
        self.qrzGrid = StringVar()
        self.qrzCity = StringVar()
        self.qrzCountry = StringVar()
        self.qrzMgr = StringVar()
        self.selectedCall=None
        self.callsignlist=[]
        self.lastLookupCall=""
        
        self.upLoader=None
        
        qrzPassword = self.config.getQRZPassword()
        qrzUserName = self.config.getQRZUserName()
      
        self.uploadADIF = UploadADIF.UploadServer()
        self.qrz=QRZLookup.QRZLookup(qrzUserName, qrzPassword)
        
        self.udpserver = UDPServer.Server(self.uploadADIF)
        self.udpserver.daemon = True
        self.udpserver.start()
        
        self.tcpClient=None

        self.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.title(appName+" by M0IAX")
        
        qrzFrame=Frame(self, height=140, width=(270-5))
        qrzFrame.pack()
        
        self.qrzLookupInUse=self.config.getQRZLookupInUse()
        
        self.showQRZInfoPane(qrzFrame, self)
        
        buttonFrame=Frame(self)
        buttonFrame.pack()
        
        self.show_buttons(buttonFrame, self)
        
        labelFrame=Frame(self)
        labelFrame.pack()
        
        aboutLabel = Label(labelFrame,text="M0IAX QRZ Lookup for JS8Call 2.2")
        aboutLabel.grid(row=0,column=0, padx=5, pady=5)
        
        if self.upLoader!=None:
            self.configureEQSLButton(self.upLoader.getEQSLEnabled())
            self.configureQRZButton(self.upLoader.getQRZEnabled())
        if self.uploadADIF!=None:
            self.configureEQSLButton(self.uploadADIF.getEQSLEnabled())
            self.configureQRZButton(self.uploadADIF.getQRZEnabled())
        
        self.update_timer()
        

if __name__=="__main__":
    
    try:

        app = UI()
        app.protocol("WM_DELETE_WINDOW", app.ask_quit)
        app.mainloop()
        
    finally:
        print('Finally Quit')
    