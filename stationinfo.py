#stationinfo

def apiToStationInfo(apiOUtput):
    
    ret=stationinfo(call,snr,grid)
    return ret

class stationinfo(object):
    self.callsign=None
    self.snr=None
    self.grid=None
    self.operatorname=None
    self.fullname=None
    
    def __init__(self, callsign, snr, grid):
        self.callsign=callsign
        self.snr=snr
        self.grid=grid
        

    def getCallsign(self):
        return self.callsign
    
    def getname(self):
        return self.operatorname
    