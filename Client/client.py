##!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  server.py
#
#  Copyright 2018 russ <russ@RUSS-PC>
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
#
import subprocess
import threading
from threading import Thread
import socket
import sys
import os
from datetime import datetime
from src.code.dbase import *
from src.code.win import *
#
#
#for item in pathinfo:
#    print(item)
pid = current_process_id()
#print(pid)
pathinfo = get_path_info()
compname = pathinfo[4]
get_os()
result = get_db_info(compname)
if result:
    pass
else:
    print("config not present")


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.2.24"
    port = 8888

    try:
        soc.connect((host, port))
    except:
        print("[*] Connection error")
        sys.exit()

    print("[*] Enter 'quit' to exit")
    try:
        message = input("[*] Please type your message-> ")
    except KeyboardInterrupt as k:
        print("[*] ctrl-c detected closing.....", k)
        sys.exit()
    finally:
        pass

    while message != 'quit':
        try:
            unknown = "[*] Unknown option.Please try again"
            ukclean = str(unknown)
            #recpkts = soc.recv(5120).decode("utf8")
            #if recpkts == ukclean:
            #    print(recpkts)
        except UnboundLocalError as e:
            print("[!] closing software.....")
            sys.exit()
        finally:
            pass
        if message == "--status--":
            try:
                soc.sendall(message.encode("utf8"))
                recpkts = soc.recv(5120).decode("utf8")
                if recpkts == ukclean:
                    print(unknown)
                else:
                    print("[*] " +recpkts)
            except:
                print('')
         #   
        elif message == "--nodes--":
            try:
                soc.sendall(message.encode("utf8"))
                recpkts = soc.recv(5120).decode("utf8")
                if recpkts == ukclean:
                    print(unknown)
                else:
                    print("[*] " +recpkts)
            except:
                print('')
        #
        elif message == "--update--":
            try:
                soc.sendall(message.encode("utf8"))
                recpkts = soc.recv(5120).decode("utf8")
                if recpkts == ukclean:
                    print(unknown)
                else:
                    print("[*] " +recpkts)
            except:
                print('')
        
        try:
            message = input(" -> ")
        except KeyboardInterrupt as k:
            print("[!] ctrl-c detected closing....:", k)
            sys.exit()
        finally:
            pass

    soc.send(b'--quit--')
#
#def is_windows():
#    return os.name == "nt"

def create_logfile():
    if not os.path.isdir(install_path + log_path):
        os.makedirs(install_path + log_path)
    if not os.path.isfile(install_path +log_path +alerts):
        #os.makedirs(install_path + log_path)
        filewrite = open(install_path + log_path + alerts, "w")
        filewrite.write("***** HA Client Log *****\n")
        filewrite.close()
#
#
def write_log(logfile,alert):
	if os.path.isfile(logfile):
		filewrite = open(logfile, "a")
		filewrite.write(str(alert) + "\n")
		filewrite.close
	else:
		print("[*] log file not found")

today= str(datetime.now().strftime("%d_%m_%Y"))
alerts= "alerts_" + today + ".log"
install_path = os.getcwd()
log_path ="\\logs\\"
#print(install_path)

if __name__ == "__main__":
    if is_windows:
        from win32api import SetConsoleTitle
        create_logfile()
        SetConsoleTitle("Automation Server Client")
        
        main()
    else:
        print("[!] This client will only run on a windows machine")
        time.sleep(10)
        sys.exit()
