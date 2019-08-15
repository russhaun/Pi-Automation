# -*- coding: utf-8 -*-
#
#  windows.py
#
#  Copyright 2018 Rhaun <Rhaun@RUSS-PC>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# File contains functions for use in Artillery from BinaryDefense specific to windows
#
#
import subprocess
import re
import os
import sys
import threading
#from datetime import datetime
#import datetime
import time
from win32evtlogutil import ReportEvent, AddSourceToRegistry, RemoveSourceFromRegistry
from win32api import GetCurrentProcess, GetCurrentProcessId
from win32security import GetTokenInformation, TokenUser, OpenProcessToken
from win32con import TOKEN_READ
import win32evtlog
#from Artillery.ArtilleryFinal(testing).src.core import write_log
#
def is_windows():
    return os.name == "nt"
#
def is_posix():
    return os.name == "posix"
#
if is_windows():
    try:
        from _winreg import *
    except ImportError:
        from winreg import *

if is_posix():
    print("[!] Linux detected!!!!!!!!!.This script wil only run on windows. please try again")
    sys.exit()
#Function to return lists for most functions in this file
#that way all there is to change is this function. this will insert all info
#into list to use for referencing different things through out file
#
def get_config(cfg):
    '''get various pre-set config options used throughout script'''
    #Current client version
    current = ['0.1']
    #Known Os versions
    oslst = ['Windows 7 Pro', 'Windows Server 2008 R2 Standard', 'Windows 8.1 Pro', 'Windows 10 Pro', 'Windows Small Business Server 2011 Essentials',
             'Windows Server 2012 R2 Essentials', 'Hyper-V Server 2012 R2']
    #Known Build numbers
    builds = ['7601', '9600', '1709', '17134']
    regkeys = [r'SOFTWARE\Microsoft\Windows NT\CurrentVersion']
    #list to hold variables of host system tried to grab most important ones
    path_vars = ['SYSTEMDRIVE','PROGRAMFILES','COMPUTERNAME', 'PROCESSOR_ARCHITECTURE','PSMODULEPATH','NUMBER_OF_PROCESSORS','WINDIR']
    #temp list
    temp = []
    if cfg == 'CurrentBuild':
        return current
    elif cfg == 'OsList':
        return oslst
    elif cfg == 'Builds':
        return builds
    elif cfg == 'Reg':
        return regkeys
    elif cfg == 'Temp':
        return temp
    elif cfg == 'Path':
        return path_vars
    else:
        pass
#Artillery version info
####################################################################################
def current_version():
    get_ver = get_config('CurrentBuild')
    ver = get_ver[0]
    info = "[*] Artillery Build: " + ver
    print(info)
    write_log(info)
#OS functions
####################################################################################
def current_process_id():
    val = GetCurrentProcessId()
    return(val)

def get_path_info():
    '''grabs current host path info and returns needed values for functions in script
    currently returns windows drive, systemdrive ,programfiles(x86) , architecture, computername'''
    pathcfg = []
    lines = []
    keywords = get_config('Path')
    exp = re.compile("|".join(keywords), re.I)
    for line in os.environ:
        line = line.strip()
        lines.append(line)
        if re.findall(exp, line):
            line = line.strip()
            pathcfg.append(line)
    # sort all the lists i did reverse here for 2 reasons. without reverse true it
    # did not sort same order with default method of just plain .sort()
    # 2 tried reverse false had no effect.
    keywords.sort(reverse=True)
    lines.sort()
    pathcfg.sort(reverse=True)
    #this setion is used for testing only used when adding new variables
    ################################################################################
    def keyword_list():
        print("*********************lines from keyword list**********************")
        for item in keywords:
            print(item)
    def retrieved_items():
        print("*********************lines from created path list******************")
        for item in pathcfg:
            print(item)
    def avail_items():
        print("*********************availible items from host list****************")
        for item in lines:
            print(item)
    ##################################################################################
    dv = "default_value"
    #these take retrived path vars and resolve to true value
    windrive = os.environ.get(pathcfg[0], dv)
    sysdrive = os.environ.get(pathcfg[1], dv)
    programfiles = os.environ.get(pathcfg[3], dv)
    arch = os.environ.get(pathcfg[5], dv)
    compname = os.environ.get(pathcfg[7], dv)
    return(sysdrive,windrive,programfiles,arch,compname)
#
#
def freeze_check():
        '''check to see if we are runnning in a frozen executable or from the .py file. ex. pyinstaller'''
        frozen = 'not'
        if getattr(sys, 'frozen', False):
                # we are running in a bundle
                frozen = 'ever so'
                bundle_dir = sys._MEIPASS
                temp = 'cold'
        else:
        # we are running in a normal Python environment
                bundle_dir = os.path.dirname(os.path.abspath(__file__))
                temp = 'hot'
        if temp == 'cold':
            print( '[*] Freeze Check: we are',frozen,'frozen')
            print( '[*] Freeze Check: os.getcwd is', os.getcwd() )
        else:
            pass
#
#
def get_os():
    '''This function uses pre-compiled lists to try and determine host os by comparing values to host entries
    if a match is found reports version'''
    if is_posix:
        pass
    if is_windows:
        OsName = ""
        OsBuild = ""
        #reg key list
        reg = get_config('Reg')
        #known os list
        kvl = get_config('OsList')
        #known builds
        b1 = get_config('Builds')
        #final client cfg list
        ccfg = []
        try:
            oskey = reg[0]
            oskeyctr = 0
            oskeyval = OpenKey(HKEY_LOCAL_MACHINE, oskey)
            while True:
                ossubkey = EnumValue(oskeyval, oskeyctr)
                #dumps all results to txt file to parse for needed strings below
                osresults = open("version_check.txt", "a")
                osresults.write(str(ossubkey)+'\n')
                oskeyctr += 1
        #catch the error when it hits end of the key
        except WindowsError:
            osresults.close()
            #open up file and read what we got
            data = open('version_check.txt', 'r')
            # keywords from registry key in file
            keywords = ['ProductName', 'CurrentVersion', 'CurrentBuildNumber']
            exp = re.compile("|".join(keywords), re.I)
            for line in data:
                #write out final info wanted to list
                if re.findall(exp, line):
                    line = line.strip()
                    ccfg.append(line)
            data.close()
            #delete the version info file. we dont need it any more
            subprocess.call(['cmd', '/C', 'del', 'version_check.txt'])
            # now compare 3 lists from get_config function and client_config.txt to use for id
            #sort clientconfig list to have items in same spot accross platforms
            ccfg.sort(reverse=True)
            osresults = ccfg[0]
            buildresults = ccfg[2]
            for name in kvl:
                if name in osresults:
                    OsName = name
                    for build in b1:
                        if build in buildresults:
                            OsBuild = build
                            #when were done comparing print what was found
                            print("[*] Detected OS: " + OsName, "Build: " + OsBuild)
#
