#========================Template =========================================================================

import sys, os
import logging
from openpyxl import workbook, worksheet
# add root folder in search path
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
config_folder = root_folder + "\\" + "Configuration"
sys.path.append(root_folder)
from TisLib import Utility
# read constant
proj_const = dict()
proj_const = Utility.GetProjectConstants(config_folder + "\\" + "Config.xml")
report_path=os.path.basename(__file__).split('.')[0] + '.log'
try:
    # Get Tis_Logger and specify the log file name, if launched from Command Line then take first argument as log filename  
    if len(sys.argv)>1:
        reportPath = sys.argv[1]
        log = Utility.GetLogger(report_path)
    else:
        log = Utility.GetLogger(report_path)
except:
    print("Error while creating logger")
# ==========================================================================================================

# import Cap required for the rule execution
from TisLib import  CSVReader,Signals_Cap,SDDB_Cap

log_string ="{}: Method={} File={} Msg={}"
csv_reader = CSVReader.CSVReader()
signalData = csv_reader.GetSignals()
sddbData = csv_reader.GetSDDBs()
trackData = csv_reader.GetTracksData()

signalID = signalData.SignalID
signalName = signalData.SignalName
signalKp = signalData.SignalKp
signalTrack = signalData.Track_ID
signalDir = signalData.Direction
Signal_Type_Function = signalData.Signal_Type_Function

sigUp,sigUpKp,sigDn,sigDnKp = [],[],[],[]
sigIdSortedUp,sigIdSortedDn = [],[]

wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Rule_TMS_SDD_0013"
rwCount = 1
wsRpt.cell(row = rwCount, column = 1, value = "Sig1 ID")
wsRpt.cell(row = rwCount, column = 2, value = "Sig1_Type_Function")
wsRpt.cell(row = rwCount, column = 3, value = "Sig1 Kp")
wsRpt.cell(row = rwCount, column = 4, value = "Sig1 Track")
wsRpt.cell(row = rwCount, column = 5, value = "Sig2 ID")
wsRpt.cell(row = rwCount, column = 6, value = "Sig2_Type_Function")
wsRpt.cell(row = rwCount, column = 7, value = "Sig2 Kp")
wsRpt.cell(row = rwCount, column = 8, value = "Sig2 Track")
wsRpt.cell(row = rwCount, column = 9, value = "Dir")
wsRpt.cell(row = rwCount, column = 10, value = "SDDB Count")

rwCount = rwCount+1

for tr in trackData.TrackName:

    sigUp, sigUpKp , sigDn , sigDnKp= [],[],[],[]      
    log.info("Getting Signals for track : " + tr)
    for item in range(len(signalTrack)):
        if(tr == signalTrack[item]) and (signalDir[item] == 'Up') and (Signal_Type_Function[item] != 'Virtual'):
            sigUp.append(signalID[item])
            sigUpKp.append(signalKp[item])
        if (tr == signalTrack[item]) and (signalDir[item] == 'Down') and (Signal_Type_Function[item] != 'Virtual'):
            sigDn.append(signalID[item])
            sigDnKp.append(signalKp[item])
                
    log.info("Call Arrange for Track "+ tr + "Dir: UP")
    sigIdSortedUp = Utility.Arrange(sigUp,sigUpKp,False)        
    for i in range(len(sigIdSortedUp)-1):
        kp1 = signalKp[signalID.index(sigIdSortedUp[i])]
        kp2 = signalKp[signalID.index(sigIdSortedUp[i+1])]
        sddbCount = Utility.getSDDBBetSignals(kp1,kp2,tr,sddbData)
                                      
        wsRpt.cell(row = rwCount, column = 1, value = signalName[signalID.index(sigIdSortedUp[i])])
        wsRpt.cell(row = rwCount, column = 2, value = Signal_Type_Function[signalID.index(sigIdSortedUp[i])])
        wsRpt.cell(row = rwCount, column = 3, value = str(kp1))
        wsRpt.cell(row = rwCount, column = 4, value = signalTrack[signalID.index(sigIdSortedUp[i])])
        wsRpt.cell(row = rwCount, column = 5, value = signalName[signalID.index(sigIdSortedUp[i+1])])
        wsRpt.cell(row = rwCount, column = 6, value = Signal_Type_Function[signalID.index(sigIdSortedUp[i+1])])
        wsRpt.cell(row = rwCount, column = 7, value = str(kp2))
        wsRpt.cell(row = rwCount, column = 8, value = signalTrack[signalID.index(sigIdSortedUp[i+1])])
        wsRpt.cell(row = rwCount, column = 9, value = "Up")
        wsRpt.cell(row = rwCount, column = 10, value = str(sddbCount))

        if(sddbCount == 0):           
            log.error("SDDB Count =0 for  " + signalName[signalID.index(sigIdSortedUp[i])]+"," + signalName[signalID.index(sigIdSortedUp[i+1])])
        rwCount=rwCount+1
            
    log.info("Call Arrange for Track " + tr + "Dir: DN ")
    sigIdSortedDn=Utility.Arrange(sigDn,sigDnKp,False)
    for i in range(len(sigDnKp)-1):
        wsRpt.cell(row = rwCount, column = 1, value = signalName[signalID.index(sigIdSortedDn[i])])
        wsRpt.cell(row = rwCount, column = 2, value = Signal_Type_Function[signalID.index(sigIdSortedDn[i])])
        wsRpt.cell(row = rwCount, column = 3, value = str(kp1))
        wsRpt.cell(row = rwCount, column = 4, value = signalTrack[signalID.index(sigIdSortedDn[i])])
        wsRpt.cell(row = rwCount, column = 5, value = signalName[signalID.index(sigIdSortedDn[i+1])])
        wsRpt.cell(row = rwCount, column = 6, value = Signal_Type_Function[signalID.index(sigIdSortedDn[i+1])])
        wsRpt.cell(row = rwCount, column = 7, value = str(kp2))
        wsRpt.cell(row = rwCount, column = 8, value = signalTrack[signalID.index(sigIdSortedDn[i+1])])
        wsRpt.cell(row = rwCount, column = 9, value = "Dn")
        wsRpt.cell(row = rwCount, column = 10, value = str(sddbCount))
        if(sddbCount==0):            
            log.error("SDDB Count =0 for  " + signalName[signalID.index(sigIdSortedDn[i])]+" , " + signalName[signalID.index(sigIdSortedDn[i+1])])
        rwCount=rwCount+1
try:
    wbReport.save(reportPath)
    log.info("Report generated successfully at " + reportPath + "\nTracks Checked: "+str(len(signalTrack)) + "\nSignal Couples Checked: " +str(rwCount) ) 
    print("Report generated successfully at " + reportPath + "\nTracks Checked: "+str(len(signalTrack)) + "\nSignal Couples Checked: " +str(rwCount))
except:
    log.error("Unexpected error in writing report excel :"+ sys.exc_info()[0])

