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
                deadlocking_block_id_list[pt_name]= [int(bl.text) for bl in point.findall('./Deadlocking_Block_ID_List/Block_ID')]           
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


    def Get_Route_Points_Pairs(self):
        try:
            route_points_pair = dict()
            switch_pt_pairs = self.Get_Switch_Points_Pairs()
            for route in self.root_node.findall('./Routes/Route'):
                ptList = list()                     
                for switch in route.findall('./Switch_ID_List/Switch_ID'):
                    ptList.extend(switch_pt_pairs[switch.text])

                route_points_pair[route.attrib['Name']] = ptList
            return route_points_pair
        except:

             self.tis_log.error("Module:SydbReader Method:Get_Route_Points_Pairs", sys.exc_info()[0])
             return None


    def Get_Point_ID_Name_Pairs(self):
        try:
            point_id_name_pair = dict()            
            for point in self.root_node.findall('./Points/Point'):
                point_id_name_pair[point.attrib['ID']] = point.attrib['Name']
            return point_id_name_pair
        except:
            self.tis_log.error("Module:SydbReader Method:Get_Point_ID_Name_Pairs", sys.exc_info()[0])
            return None

    def Get_Switch_ID_Name_Pairs(self):
        try:
            switch_id_name_pair = dict()            
            for sw in self.root_node.findall('./Switchs/Switch'):
                switch_id_name_pair[sw.attrib['ID']] = sw.attrib['Name']
            return switch_id_name_pair
        except:
            self.tis_log.error("Module:SydbReader Method:Get_Switch_ID_Name_Pairs", sys.exc_info()[0])
            return None

    def Get_Signals_ID_Name_Pairs(self):
        try:
            sig_id_name_pair = dict()            
            for sig in self.root_node.findall('./Signals/Signal'):
                sig_id_name_pair[sig.attrib['ID']] = sig.attrib['Name']
            return sig_id_name_pair
        except:
            self.tis_log.error("Module:SydbReader Method:Get_Signals_ID_Name_Pairs", sys.exc_info()[0])
            return None
    def Get_Signals_ID_BlockID_Pairs(self):
        """
        Returns  dictionary of Singnal ID (int) and Block ID (int)
        """
        try:
            sig_id_blk_pair = dict()
            sig_id_kp_pair = self.Get_Signal_ID_Kp_Pairs()          
            for sig in self.root_node.findall('./Signals/Signal'):
                sig_kp = sig_id_kp_pair[sig.attrib['ID']]
                for block in self.root_node.findall('./Blocks/Block'):
                    if sig.find('Track_ID').text == block.find('Track_ID').text:
                        kp_begin = block.find('Kp_Begin').text
                        kp_end   = block.find('Kp_End').text
                        temp = list([int(kp_begin),int(kp_end),sig_kp])
                        temp.sort()
                        if temp.index(sig_kp) ==1:
                            sig_id_blk_pair[int(sig.attrib['ID'])] = int(block.attrib['ID'])
                            break          
                
            return sig_id_blk_pair
        except:
            self.tis_log.error("Module:SydbReader Method:Get_Signals_ID_BlockID_Pairs", sys.exc_info()[0])
            return None


