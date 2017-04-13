### ========= Template =========================================================================
import sys
import os,os.path
import logging
from openpyxl import workbook, worksheet

# add root folder in search path
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(root_folder)

import TisLib
from TisLib import Utility, Configuration , CSVReader

try:
    # Get Tis_Logger and specify the log file name   
    log_file_path = os.path.join(root_folder + "\\Logs\\" , os.path.basename(__file__).split('.')[0] + '.log')
    result_file_path = os.path.join(root_folder + "\\Results\\" ,'Test_Results_' + os.path.basename(__file__).split('.')[0] + '.xlsx')
    tis_log = Utility.GetLogger(log_file_path)
except:
    print("Error while creating logger")

config = Configuration.Configuration(root_folder)
# read constant
proj_const = dict()
proj_const = Utility.GetProjectConstants(config.config_File_Path)
print("Executing " + os.path.basename(__file__))
tis_log.info("Executing " + os.path.basename(__file__))

### ======== Template Ends===========================================================================

### =========Rule RULE_TMS_SIGNAL_0012 ===================================================================
# Author : Saleem Javed
# Updated 13 April 2017
# Caps Used : SYDB used, Points, Signals
# Constant used :  None
###==================================================================================================
from TisLib import SydbReader
import xml.etree.ElementTree as ET

sydb_reader = SydbReader.SydbReader(config.sydb_file_path)
point_deadlocking_blocks = sydb_reader.Point_Deadlocking_Block_ID_List()
signal_kp_pair = sydb_reader.Get_Signal_ID_Kp_Pairs()

for route in sydb_reader.root_node.findall('./Routes/Route'):
    route_sig_pair = sydb_reader.Get_Route_OriginSignal_Pairs() 
    signal = route_sig_pair[route.attrib['Name']]   
    sig_kp = int(signal_kp_pair[signal])
    sig_blk = ''

    # Get block of signal
    for block in sydb_reader.root_node.findall('./Blocks/Block'):
        kp_begin = block.find('Kp_Begin').text
        kp_end   = block.find('Kp_End').text
        temp = list([int(kp_begin),int(kp_end),sig_kp])
        temp.sort()
        if temp.index(sig_kp) ==1:
            sig_blk = block.attrib['ID']
            break
    # Get Points of the route
    points_of_route = list()
    #sw_pts_pair = sydb_reader

    for switch in route.findall('./Switch_ID_List/Switch_ID'):
        switch_pt_pairs = sydb_reader.Get_Switch_Points_Pairs()
        print(switch_pt_pairs[switch.text])

    
    





    
