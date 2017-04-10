import sys
import os.path
import logging
import xml.etree.ElementTree as ET


def Arrange(DeviceID:list,Kp:list,rev:bool):

    """Arrange the DeviceID list in increasing or decreasing values of Kp List.
       DeviceID= List of Device to be arranged,Kp =Kp Values
       rev= True for Increasing,False for decreasing
    """
   
    _ids = list(DeviceID)
    _kps = list(Kp)
    outids = []
    try:
        if len(_ids) == len(_kps):
            _kps.sort(reverse=rev)
            for  i in range(len(_kps)):
                outids.append(_ids[Kp.index(_kps[i])])        
        else:
            return []                
    except:
       logging.error("Unexpected error:", sys.exc_info()[0])
    finally:        
        return outids

def getSDDBBetSignals(KpSig1:int,KpSig2:int,Track:str,SDDBData:dict):   
    count=0
    try:
        sddbKps = SDDBData.sddb_kp
        sddbTrack = SDDBData.sddb_trackID
        sddbTrackKps = []
        for item in range(len(sddbTrack)):
            if(sddbTrack[item] == Track):
                sddbTrackKps.append(sddbKps[item])

        for k in range(len(sddbTrackKps)):
            if(KpSig1<KpSig2):
                if(int(KpSig1)<int(sddbTrackKps[k]) & int(sddbTrackKps[k]) < int(KpSig2)):
                    count=count+1
            elif(KpSig1>KpSig2):
                if(int(KpSig1)>int(sddbTrackKps[k]) & int(sddbTrackKps[k]) > int(KpSig2)):
                    count=count+1
    except:
        logging.error("Error:Fun = getSDDBBetSignals,Module=Utility", sys.exc_info()[0])
    finally:        
        return count

def GetLogger(logFile):
    
    logger = logging.getLogger('Tis_Logger')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(logFile,mode='w')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s',datefmt='%Y/%m/%d %I:%M:%S %p')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

def GetProjectConstants(constantfile:str):
    """Returns the dictionalry of project constants defined in the constant file
       constantfile= full path of constant file
    """
    tis_logger=logging.getLogger('Tis_Logger')
    proj_const=dict()
    try:
        tis_logger.info("Reading project constant from " + constantfile)
        config = ET.parse(constantfile)
        rootXml = config.getroot()
        const_file_node = rootXml.find("Constant")
        const_file = ET.parse(const_file_node.attrib['file'])   
        const_root_xml = const_file.getroot()

        for el in const_root_xml.findall('constant'):
            # return the value 'None' if attrib is not found
            try:               
                proj_const[el.get('name')] = el.get('value')         
            except:
                tis_logger.error("Method=GetProjectConstants , Module=Utility" +  sys.exc_info()[0])
                continue
    except:
       tis_logger.error("Method=GetProjectConstants , Module=Utility" +  sys.exc_info()[0])
    finally:
        return proj_const

def GetSDDofPoint(point,SDD_Cap):
    for item in range(len(SDD_Cap['Name'])):
        sdd_name=''
        pt_list  = SDD_Cap['Point_ID_List'][item].split(';')
        if point in pt_list:
            sdd_name = SDD_Cap['Name'][item]
            return sdd_name

def GetPointsOfSwitch(switchIndex, SwitchsCap):
    try:

        convergent_Points = SwitchsCap['Convergent_Point_ID_List'][switchIndex] 
        divergent_Points  = SwitchsCap['Divergent_Point_ID_List'][switchIndex]
        if convergent_Points == '0' and divergent_Points == '0':
            return []
        elif convergent_Points == '0' and divergent_Points != '0':
            return divergent_Points.split(';')
        elif convergent_Points != '0' and divergent_Points == '0':
            return convergent_Points.split(';')
        else:
            return convergent_Points.split(';') + divergent_Points.split(';')
    except:
        tis_logger.error("Method = GetPointsOfSwitch , Module = Utility" +  sys.exc_info()[0])
        return []

def ConvertToString(listInput:list):
    out_text=''
    for item in listInput:
        out_text=out_text + item +';'

    return out_text




