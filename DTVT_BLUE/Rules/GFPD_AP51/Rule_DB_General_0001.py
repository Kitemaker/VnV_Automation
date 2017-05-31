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

### =========Rule_WZ_0009===============================================================
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
Utility.WriteToWorkSheet(wsRpt,rwCount,["Boundary Name", "Boundary Type", "Direction"])
rwCount = rwCount+1

# Read Caps
full_list = dict()
for name, cap in SyDT.items():
    try:

        if cap.get('Name') != None:
           if len(cap['Name']) > 0:
               full_list[name] = cap['Name']
    except:
        dtvt_log.error(name ,'\t', sys.exc_info()[0])



for name, items in full_list.items():
    for index in range(len(items)):       
        itemCopy = list(items).copy()
        val = itemCopy.pop(index)
        try:

            if(itemCopy.index(val)):
                _result = 'NOK'
                dtvt_log.error(name ,'\t', "has duplicate values"+ val)
        except ValueError:
            pass
        except:
            dtvt_log.error(name ,'\t', "has duplicate values"+ val)



    for k,vlist in full_list.items():
        if(name != k):
            for value in items:
                try:
                    if(vlist.index(value)):
                        _result = 'NOK'
                        dtvt_log.error(name +'\t'+value)
                except ValueError:
                    pass
                except:
                    dtvt_log.error(name ,'\t', sys.exc_info()[0])




      


#    Utility.WriteToWorkSheet(wsRpt,rwCount,[bnd_name,bnd_type,bnd_dir,_result])
#    rwCount = rwCount+1

## Save Report
#Utility.SaveReport(wbReport,global_test_results,root_folder,result_file_name)
