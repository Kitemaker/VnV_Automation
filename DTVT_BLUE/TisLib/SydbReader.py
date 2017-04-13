import os.path
import sys
import xml.etree.ElementTree as ET
import logging

class SydbReader(object):
    
    def __init__(self, SydbPath):
        self.sydb_file = ET.parse(SydbPath)
        self.root_node = self.sydb_file.getroot()
        self.Tool_Version =  self.root_node.attrib['Tool_Version']
        self.Sector_ID = self.root_node.attrib['Sector_ID']
        self.SyPD_Version = self.root_node.attrib['SyPD_Version']
        self.XML_File_Version = self.root_node.attrib['XML_File_Version']        
        self.tis_log =  logging.getLogger('Tis_Logger')
        self.Data_L1 = self.GetFirsLevelItemNames()
        self.data_tables = dict()

    def GetFirsLevelItemNames(self):
        data_Level1=list()
        try:
            data_Level1 = [item.tag for item in self.root_node.getchildren()]
        except:
            self.tis_log.error((sys.exc_info()[0]))
    def GetSecondLevelItems(self,item):
        pass

    def GetDataTables(self):
        dts = dict()
        eqpdts = dict()
        for item in self.root_node.getchildren():
            eqps = item.getchildren()
            for k,v in eqps[0].attrib.items():
                eqpdts[k] = ''
            for key,value in eqpdts:
                eqpdts[k] = [item.attrib[k] for item in eqps]
            dts[item.tag] = eqpdts
        return dts

    def Point_Deadlocking_Block_ID_List(self):
        deadlocking_block_id_list = dict()
        try:
            point_list = self.root_node.findall('./Points/Point')
            for point in point_list:
                pt_name = point.attrib['Name']           
                deadlocking_block_id_list[pt_name]= [bl.text for bl in point.findall('./Deadlocking_Block_ID_List/Block_ID')]           
        except:
            self.tis_log.error("Module:SydbReader Method:Point_Deadlocking_Block_ID_List", sys.exc_info()[0])
            deadlocking_block_id_list = None
        finally:
            return deadlocking_block_id_list

    def Get_Route_OriginSignal_Pairs(self):
        route_signal_pairs = dict()
        try:
            for route in self.root_node.findall('./Routes/Route'):
                route_signal_pairs[route.attrib['Name']] = route.find('Origin_Signal_ID').text
        except:
            self.tis_log.error("Module:SydbReader Method:Get_Route_OriginSignal_Pair", sys.exc_info()[0])
            return None
        finally:
            return route_signal_pairs

    def Get_Signal_ID_Kp_Pairs(self):
        signal_id_kp_pairs = dict()
        try:
            for signal in self.root_node.findall('./Signals/Signal'):
                kp_node = signal.find('Kp')
                signal_id_kp_pairs[signal.attrib['ID']] = int(kp_node.attrib['Value']) + int(kp_node.attrib['Corrected_Gap_Value']) +  int(kp_node.attrib['Corrected_Trolley_Value'])
        except:
            self.tis_log.error("Module:SydbReader Method:Get_Signal_ID_Kp_Pairs", sys.exc_info()[0])
            return None
        finally:
            return signal_id_kp_pairs


    def Get_Switch_Points_Pairs(self):
        try:
            switch_points_pairs = dict()
            for sw in self.root_node.findall('./Switchs/Switch'):
                sw_id = sw.attrib['ID']
                conv_pts = sw.findall('./Convergent_Point_ID_List/Convergent_Point_ID')
                div_pts =  sw.findall('./Divergent_Point_ID_List/Divergent_Point_ID')
                switch_points_pairs[sw_id] = [item.text for item in (conv_pts + div_pts)]
            return switch_points_pairs
        except:
             self.tis_log.error("Module:SydbReader Method:Get_Switch_Points_Pairs", sys.exc_info()[0])
             return None





