### ========= Template =====================================================================================================
import sys
import os,os.path
import logging
from openpyxl import workbook, worksheet

# add root folder in search path
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(root_folder)

import DtvtLib
from DtvtLib import Utility, Configuration , CSVReader

try:
    # Get Dtvt_Logger and specify the log file name   
    log_file_path = os.path.join(root_folder + "\\Logs\\" , os.path.basename(__file__).split('.')[0] + '.log')
    result_file_name = os.path.basename(__file__).split('.')[0] + '.xlsx'
    result_file_path = os.path.join(root_folder + "\\Results\\" ,'Test_Results_' + result_file_name)
    dtvt_log = Utility.GetLogger(log_file_path)
except:
    print("Error while creating logger")

config = Configuration.Configuration(root_folder)
# read constant
proj_const = dict()
proj_const = Utility.GetProjectConstants(config.config_File_Path)
print("Executing " + os.path.basename(__file__))
dtvt_log.info("Executing " + os.path.basename(__file__))

### ======== Template Ends===============================================================================================

### =========Rule RULE_TMS_SDD_0046 ===================================================================================
# Author : Saleem Javed
# Updated 10 May 2017
# Caps Used : Signal, Point and Block Nodes from SyDB
# Constant used :  None
###======================================================================================================================

from DtvtLib import SydbReader
import xml.etree.ElementTree as ET

sydb_reader = SydbReader.SydbReader(config.sydb_file_path)
point_deadlock_Blocks = sydb_reader.Point_Deadlocking_Block_ID_List()
#sig_id_blk_dict =sydb_reader.Get_Signals_ID_BlockID_Pairs()


# Create Report
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Signal","Track" ,"Signal Kp", "Point", "Block ID","Block Name", "Block Track", "Block Kp Begin", "Block Kp End", "Result"])
rwCount = rwCount+1

for block in sydb_reader.root_node.findall('./Blocks/Block'):
    res = ""                    
    blk_id =   int(block.attrib['ID'])
    blk_name =  block.attrib['Name']                    
    blk_kp_begin = int(block.find('Kp_Begin').text)
    blk_kp_end = int(block.find('Kp_End').text)  
    blk_trk = int(block.find('Track_ID').text)
    for point in  sydb_reader.root_node.findall('./Points/Point'):
        pt_name = point.attrib['Name']   
        if blk_id in point_deadlock_Blocks[pt_name]:
            for signal in sydb_reader.root_node.findall('./Signals/Signal'):
                sig_type = str.upper(signal.find('Signal_Type_Function').text)
                signal_name = signal.attrib['Name']
                signal_track = int(signal.find('Track_ID').text)
                signal_id =  int(signal.attrib['ID'])
                if (sig_type == "ROUTE SIGNAL" or sig_type == "VIRTUAL SIGNAL") and ( signal_track == blk_trk):                                    
                    kp_node = signal.find('Kp')
                    signal_kp  = int(kp_node.attrib['Value']) +int( kp_node.attrib['Corrected_Gap_Value']) + int(kp_node.attrib['Corrected_Trolley_Value'])                
                    
                    if(signal_kp < min(blk_kp_begin,blk_kp_end)) or (signal_kp > max(blk_kp_begin,blk_kp_end)):
                        res =  'OK'
                        global_test_results.append('OK')
                    elif (signal_kp >= min(blk_kp_begin,blk_kp_end)) and (signal_kp <= max(blk_kp_begin,blk_kp_end)):
                        res =  'NOK'
                        global_test_results.append('NOK')
                        dtvt_log.error("Kp of Signal: "+ signal_name + " exist in deadlocking block: " + blk_name + " of Point: "+ pt_name)

                    Utility.WriteToWorkSheet(wsRpt,rwCount,[signal_name,signal_track,signal_kp,pt_name,blk_id,blk_name,blk_trk,blk_kp_begin,blk_kp_end,res])                   
                    rwCount = rwCount+1                                       
                   

# Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
