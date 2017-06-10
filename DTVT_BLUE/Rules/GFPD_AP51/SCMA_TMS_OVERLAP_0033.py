### ========= Template =========================================================================
import sys , os , os.path
import logging
from openpyxl import workbook, worksheet

# add root folder in search path
root_folder = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),".."),".."))
sys.path.append(root_folder)
import DtvtLib
from DtvtLib import Utility, Configuration , CSVReader
param = Utility.Initialise(root_folder,__file__)
log_file_path    = param['log_file_path']
result_file_name = param['result_file_name']
result_file_path = param['result_file_path']
dtvt_log         = param['dtvt_log']
proj_const       = param['proj_const']
sydb             = param['SyDB']

### ======== Template Ends=================================================================================================

### =========Rule SCMA_TMS_OVERLAP_0033 ====================================================================================
# Author : Saleem Javed
# Updated 13 April 2017
# Caps Used : SYDB Node used, Signa,Overlap,SSP,Points
# Constant used :  None
###========================================================================================================================
from DtvtLib import SydbReader
import xml.etree.ElementTree as ET

point_deadlocking_blocks = sydb.Point_Deadlocking_Block_ID_List()
signal_kp_pair = sydb.Get_Signal_ID_Kp_Pairs()
signals = sydb.DL2['Signals']


point_id_name_dict = sydb.Get_Point_ID_Name_Pairs()
sig_id_blk_dict =sydb.Get_Signals_ID_BlockID_Pairs()


# Create Report
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1

ssp_name_kp = dict()
overlap_id_maxdistance = dict()
conv_direction = str.upper(sydb.GetConventionalDirection())
up_sig = str.upper(sydb.GetUpSignification())
dn_sig = str.upper(sydb.GetDownSignification())
for ssp in sydb.DL2['Service_Stopping_Points']:
    kp_node = ssp.find('Kp')
    ssp_kp = int(kp_node.attrib['Value']) + int(kp_node.attrib['Corrected_Gap_Value']) +int(kp_node.attrib['Corrected_Trolley_Value'])
    ssp_name_kp[ssp.attrib['ID']] = ssp_kp

for olap in sydb.DL2['Overlaps']:
    
    try:
        ol_id = olap.attrib['ID']      
        overlap_id_maxdistance[ol_id] = max(int(olap.find('D_Overlap').text) , int(olap.find('D_Overlap_CBI').text))
    except:
         dtvt_log.error("Error while getting D_Overlap")


for sig in signals:
    sig_name = sig.attrib['Name'] 
    sig_kp = signal_kp_pair[sig.attrib['ID'].strip()]
   
    if(sig.find('Overlap_ID') != None ):

        sig_overlap_id = sig.find('Overlap_ID').text
        max_d_overlap = overlap_id_maxdistance[sig_overlap_id]
        if(sig.find('Track_ID') != None ):
            sig_track_id = sig.find('Track_ID').text
        else:
            sig_track_id = ''
        if(sig.find('SSP_ID') != None ):
            sig_ssp_id = sig.find('SSP_ID').text
            first_kp_point = ssp_name_kp[sig_ssp_id]
        else:
            sig_ssp_id = ''
            first_kp_point = int(sig_kp)                                             
        if(sig.find('Direction') != None ):
            sig_dir = str.upper(sig.find('Direction').text)
        else:
            sig_dir = ''

        if (conv_direction == up_sig and sig_dir == up_sig ) or  (conv_direction == dn_sig and sig_dir == dn_sig ):
            second_kp_point = first_kp_point + max_d_overlap
        elif (conv_direction == up_sig and sig_dir == dn_sig ) or  (conv_direction == dn_sig and sig_dir == up_sig ):
             second_kp_point = first_kp_point - max_d_overlap

        print(sig_name + '\tTrackID = '+ sig_track_id + '\tSigKp = '+ str(sig_kp)+ '\tfirst_kp_point = '+ str(first_kp_point) + '\t' + sig_ssp_id + '\t'+ sig_overlap_id + '\t' + sig_dir +'\tmax_d_overlap ' + str(max_d_overlap))