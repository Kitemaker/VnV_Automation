### ========= Template ============================================================================
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
SyDT             = param['SyDT']

### ======== Template Ends=========================================================================

### =========Rule_DB_General_0001 ===============================================================
# Author : Saleem Javed
# Updated 31 May 2017
# Caps Used : All caps having column "Name",
# Constant used :  None 

###================================================================================================

# Create report file
global_test_results = list()
wbReport = workbook.Workbook()
wsRpt=wbReport.active
wsRpt.title = "Test_Results"
rwCount = 1
Utility.WriteToWorkSheet(wsRpt,rwCount,["Cap Name", "Item Name", "Other Cap Name","Cap With Duplicate Items","Result"])
rwCount = rwCount+1

# Read Caps
full_list = dict()
# Prepare dictionary of Cap and items of column "Name" 
for name, cap in SyDT.items():
    try:

        if cap.get('Name') != None:
           if len(cap['Name']) > 0:
               full_list[name] = cap['Name']
    except:
        dtvt_log.error(name ,'\t', sys.exc_info()[0])

for name, items in full_list.items():
    # First check within individual Cap for the duplicate names
    for index in range(len(items)):  
        _result = ''    
        itemCopy = list(items).copy()
        val = itemCopy.pop(index)
        if(val in itemCopy):
            _result = 'NOK'
            dtvt_log.error(name +'\t'+ "has duplicate values "+ val)
        else:
            _result = 'OK'
            
        global_test_results.append(_result)
        Utility.WriteToWorkSheet(wsRpt,rwCount,[name, val ,name,'',_result])
        rwCount = rwCount+1

     # check name with all other caps for duplicacy ZCs_Cap
    for value in items:
        _result  = ''
        _duplicate_item_cap=list()
        _other_cap_tested = list()
        for other_cap_name ,other_name_list in full_list.items():
            if(name != other_cap_name and other_cap_name != "ZCs_Cap" and other_cap_name != "ATC_Equipments_Cap"):
                _other_cap_tested.append(other_cap_name)
                if value in other_name_list:
                    global_test_results.append('NOK')                     
                    dtvt_log.error(name +'\t'+value)
                    _duplicate_item_cap.append(other_cap_name)                        
                    
        
        if len(_duplicate_item_cap) > 0:
            Utility.WriteToWorkSheet(wsRpt,rwCount,[name, value ,Utility.ConvertToString(_other_cap_tested),Utility.ConvertToString(_duplicate_item_cap),'NOK'])
            rwCount = rwCount+1
        else:
            Utility.WriteToWorkSheet(wsRpt,rwCount,[name, value ,Utility.ConvertToString(_other_cap_tested),'','OK'])
            rwCount = rwCount+1

            
#Save Report
Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
