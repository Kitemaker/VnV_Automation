import os,sys

# Get File  name without path
print(os.path.basename(__file__))
print(__file__)
print(os.path.basename(__file__).split('.')[0] + '.log')
sys.path.append(r'C:\Users\295563\Documents\01 PROJECTS\VnV\VnV_Automation\DTVT_BLUE')
import TisLib
import TisLib.SydbReader



#const = TisLib.Utility.Get_C_Late_Change_Distance(r'C:\Users\295563\Documents\01 PROJECTS\VnV\VnV_Automation\DTVT_BLUE\Input\Constant\C_Late_Change_Distance.xlsx')
#for k,v in const.items():
#   print(k,' => ' ,v)

#sdb = TisLib.SydbReader.SydbReader(r'C:\Users\295563\Documents\01 PROJECTS\VnV\SCMA\SCMA_4.3.1\INPUTS\SyDB_4.3.1\DataPackage oF SCMA _RO_4.3.1\RO_4.3.1_SyDB\SyDB_SCMA_RO_4.3.1.xml')

#print(sdb.Get_Point_Deadlocking_Block_ID_List('PT_W1719A_HDS'))

import Trg_Test
import Trg_Test.Constants

