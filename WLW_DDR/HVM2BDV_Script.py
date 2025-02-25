from __future__ import division
from __future__ import print_function

# -------------------------------------------------------------------------
# Intel Corporation
# Copyright 2021 - All Rights Reserved
# Department  : IPG
# Written by  : Adanan, Omar Mukhtar & Tan, Eng Wah
# Date        : 7 Apr 2021
# Description : Various functions used on DV.
# Version	  : 22.5
# -------------------------------------------------------------------------
from builtins import input
from builtins import range
from builtins import object
from past.utils import old_div
from svtools.common import baseaccess
from colorama import init, Fore, Back, Style
#from pysvtools.dvengine.instruments import netBooter as net
import os
import csv
import sys
import math
import time
import psutil
import socket
import datetime
import smtplib
import traceback
import random
import namednodes
from namednodes import sv
socket = sv.socket0
import imp
from prettytable import PrettyTable

#ddrio = ddrioX.DDRIO(ReturnSingleValue=False)


#from pysvtools import SAT as SAT
#sat = SAT.sat
#sat.setProject("testchips")
#sat.setPlatform("avk_b_pc1")

def HVM_regdump_postprocess(filename,includeOri=True):


    ddrvccdll1_Register = [
                        "ddriolvr_cr_afe_ctrl0",
                        "ddriolvr_cr_afe_ctrl1_new",
                        "ddriolvr_cr_afe_ctrl2",
                        "ddriolvr_cr_afe_viewctrl",
                        ]

    Comp_New_Register = [
                        "dccdigobs",
                        "dcsctl0",
                        "dcsctl1",
                        "dcsctl2",
                        "dcsctl3",
                        "dcsdigclkgate",
                        "dcsinit",
                        "dcsoffset",
                        "dcsrunmode",
                        "dcsstatus1",
                        "ddrcomp_cr_ddrcompvisapremux_0_0_0_mchbar",
                        "ddrcomp_cr_ddrcrdatacomp1_0_0_0_mchbar",
                        "ddrcomp_cr_ddrcrdatacompvtt_0_0_0_mchbar",
                        "ddrcomp_cr_ddrcrdatacompvtt", #added manually
                        "ddrcomp_cr_pnccomp_ctrl3_0_0_0_mchbar",
                        "ddrcomp_cr_vccdllcompdataccc1_0_0_0_mchbar",
                        "ddrcomp_cr_vccdllcompdataccc_0_0_0_mchbar",
                        "ddrcomp_cr_vsshicomp_ctrl2_0_0_0_mchbar",
                        "ddrcomp_cr_vsshicomp_ctrl3_0_0_0_mchbar",
                        "dfxdcs_ctl",
                        "dfxdcs_run",
                        "dfxdcs_status",
                        "pllstatus",
                        "txdllsiggrpdccctl34",
                        "txdllsiggrpdccctl35",]


    HVM_Register_Correction_List = [
                                "ddrcomp_cr_ddrcrdatacompvtt",
                                "ddrcrmarginmodecontrol0",
                                "ddrcrmarginmodedebugmsb0",
                                "ddrcrmarginmodedebuglsb0",
                                "ddrcrdatacontrol3",
                                ]

    HVM_Register_Correction_Map = {
                                "ddrcomp_cr_ddrcrdatacompvtt":"ddrcomp_cr_ddrcrdatacompvtt_0_0_0_mchbar",
                                "ddrcrmarginmodecontrol0": "ddrdata_cr_ddrcrmarginmodecontrol0_0_0_0_mchbar",
                                "ddrcrmarginmodedebugmsb0":"ddrdata_cr_ddrcrmarginmodedebugmsb0_0_0_0_mchbar",
                                "ddrcrmarginmodedebuglsb0":"ddrdata_cr_ddrcrmarginmodedebuglsb0_0_0_0_mchbar",
                                "ddrcrdatacontrol3":"ddrdata_cr_ddrcrdatacontrol3_0_0_0_mchbar",
                                }

    HVM_RegisterField_Correction_List = [
                                "ddrdata_cr_ddrcrmarginmodedebugmsb0_0_0_0_mchbar",
                                "ddrdata_cr_ddrcrmarginmodedebuglsb0_0_0_0_mchbar",
                                ]

    HVM_RegisterField_Correction_Map = {
                                "ddrdata_cr_ddrcrmarginmodedebugmsb0_0_0_0_mchbar":['spareX','result'],
                                "ddrdata_cr_ddrcrmarginmodedebuglsb0_0_0_0_mchbar":['spareX','result'],
                                }


    ReadFile = open(filename, "r")
    Readlines_List = ReadFile.readlines()

    OutputFile_list=[]
    for Readline in Readlines_List:
        print(Readline)
        Ori_Readline=Readline
        Readline = Readline.replace("_READ","")
        #Readline = Readline.replace("_PARAM0","").replace("_PARAM1","").replace("_PARAM2","").replace("_PARAM3","").replace("_PARAM4","")
        if "0_tname_MIO_DDR::" in Readline:
            try:
                InstanceMemss = Readline.replace("_CH4CCC","").replace("_CH5CCC","").split("_CH")[1].split("_")[0].replace("\n","") #0_MCHBAR_ALL_CH0_1
            except:
                InstanceMemss = ""
            registername = Readline.split("REGDUMP_")[1].split("\n")[0].split("_ALL")[0].split("_DATA")[0].split("_CH")[0].lower()
            postprocessline = "xxxxxxx-- unable to post process --xxxxxxx\n"
            pysvobj=None
            if "_ALL_" in Readline:
                if registername.lower() in Comp_New_Register:
                    pysvobj = socket.wlb0.ddrphy0.ddrphy_comp_new.sb
                    partition = "ddrphy_comp_new"
                elif registername.lower() in ddrvccdll1_Register:
                    pysvobj = socket.wlb0.ddrphy0.ddrvccdll1.sb
                    partition = "ddrvccdll1"
                else:
                    pysvobj = socket.wlb0.ddrphy0.ddrphy_comp.sb
                    partition = "ddrphy_comp"
            elif ("DATA4CH0_" in Readline) or ("DATA4CH1_" in Readline) or ("DATA5CH0_" in Readline) or ("DATA5CH1_" in Readline) or ("DATA6CH0_" in Readline):
                pysvobj = socket.wlb0.ddrphy0.data4ch0.sb
                if "DATA4CH0_" in Readline:
                    partition = "data4ch0"
                elif "DATA4CH1_" in Readline:
                    partition = "data4ch1"
                elif "DATA5CH0_" in Readline:
                    partition = "data5ch0"
                elif "DATA5CH1_" in Readline:
                    partition = "data5ch1"
                elif "DATA6CH0_" in Readline:
                    partition = "data6ch0"
                else:
                    partition = "ddrdata"
            elif ("CH4CCC_" in Readline) or ("CH5CCC_" in Readline):
                pysvobj = socket.wlb0.ddrphy0.ch4ccc.sb
                if "CH4CCC_" in Readline:
                    partition = "ch4ccc"
                elif "CH5CCC_" in Readline:
                    partition = "ch5ccc"
                else:
                    partition = "ccc"

            elif ("CH4CCC_" in Readline) or ("CH5CCC_" in Readline):
                pysvobj = socket.wlb0.ddrphy0.ch4ccc.sb
                if "CH4CCC_" in Readline:
                    partition = "ch4ccc"
                elif "CH5CCC_" in Readline:
                    partition = "ch5ccc"
                else:
                    partition = "ccc"

            else: #ddrphy_misc_saug.
                pysvobj = socket.wlb0.ddrphy0.ddrphy_misc_saug
                partition = "misc_saug"

            if registername in HVM_Register_Correction_List:
                registername = HVM_Register_Correction_Map[registername]

            pysvobj_reg=pysvobj.getbypath(registername)

            if registername in HVM_RegisterField_Correction_List:
                pysv_regfield_list = HVM_RegisterField_Correction_Map[registername]
            else:
                pysv_regfield_list = pysvobj_reg.fields
            if includeOri:
                OutputFile_list.append(Ori_Readline)
        if "strgval" in Readline:
            Value_List=Readline.split("strgval_")[1].split("\n")[0].split("_")
            if len(Value_List) != len(pysv_regfield_list):
                postprocessline = "xxxxxxx-- unable to post process len(Value_List)(%s) != len(pysv_regfield_list)(%s) --xxxxxxx\n  %s  %s  %s \n"%(len(Value_List),len(pysv_regfield_list),registername,Value_List,pysv_regfield_list)
            else:
                postprocessline="[CH%s]  %s  %s   "%(InstanceMemss,partition,registername)

                for regfield_index in range(len(pysv_regfield_list)):
                    if "0x" in Value_List[regfield_index]:
                        postprocessline = postprocessline + "%s = %s   "%(pysv_regfield_list[regfield_index],(Value_List[regfield_index]))
                    else:
                        postprocessline = postprocessline + "%s = %s   "%(pysv_regfield_list[regfield_index],hex(int(Value_List[regfield_index])))
                postprocessline = postprocessline + "\n"

            if includeOri:
                OutputFile_list.append(Ori_Readline)

            OutputFile_list.append(postprocessline)
            print(postprocessline)


    TimeStamp=datetime.datetime.now().strftime("%d%b%y_%H.%M.%S")
    OutputFile = open(filename.replace(".txt","") + "_postprocess_" + "%s"%TimeStamp + ".txt", "x")
    for Writeline in OutputFile_list:
        OutputFile.write("%s"%Writeline)
    OutputFile.close()
    ReadFile.close()
    return 0


if __name__ == "__main__":
    HVM_regdump_postprocess(filename="C:/Users/anandare/source/repos/data-automations/data-automations/WLW_DDR/CLEAN_Unit208_DOUBLEINIT.txt")