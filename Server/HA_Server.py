##!/usr/bin/python3
import sys
import os
import socket
import traceback
import threading
from threading import Thread
import serial
import time
from datetime import datetime
from win32api import SetConsoleTitle
SetConsoleTitle("Automation Server console")
#######################################DO NOT EDIT!!!!!!!!!!!!!!!####################################

#################################################fileserver section################################

srvbanner = '''###################################################################################################
##                              The Computer Guys Home automation system.                        ##
##                             https://github.com/russhaun/Pi-Automation                        ##
##                                                                                               ##
###################################################################################################'''
def fileserver():
    host = '192.168.2.24'
    port = 2525
    skServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    #
    try:
        skServer.bind((host, port))
    except:
        print("[*] Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    #
    skServer.listen(10)       # queue up to 10 requests
    bFileFound = 0
    print("[*] File Server Active...")
    # infinite loop- do not reset for every request
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("[*] Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("[*] Thread did not start.")
            traceback.print_exc()
    #
    skServer.close()

  

###########################################controlserversection####################################
def controlserver():
    '''this is the main server for controlling and monitoring the pi and all other nodes.
    it will poll or be contacted from active clients'''

    host = "192.168.2.24"
    port = 8888         # arbitrary non-privileged port
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    #print("Socket created")
    try:
        soc.bind((host, port))
    except:
        print("[*] Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
   #
    print("[*] cmd Server now listening")
    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("[*] Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()

        except:
            print("[*] Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True
    while is_active:
        try:
            client_input = receive_input(connection, max_buffer_size)
        except ConnectionAbortedError as err:
            print('[*] Connection was lost:', err)
            connection.close()
            is_active = False

        if "--QUIT--" in client_input:
            print("[*] Client is requesting to quit")
            connection.close()
            print("[*] Connection " + ip + ":" + port + " closed")
            is_active = False
        elif "--STATUS--" in client_input:
            m = "current temp: "
            ct = ctemp
            mctf = str(m + ct)
            print("[*] Sent " + mctf)
            connection.sendall(mctf.encode("utf8"))
        elif "--UPDATE--" in client_input:
            print("[*] Processed result: {}".format(client_input))
            selection = "No Updates at this time."
            cleaned = str(selection)
            connection.sendall(cleaned.encode("utf8"))
            print("[*] Sent " + selection)
        elif "--FILE--" in client_input:
            print("[*] Processed result: {}".format(client_input))
            selection = "Enter Filename: "
            cleaned = str(selection)
            connection.sendall(cleaned.encode("utf8"))
            print("[*] Sent " + cleaned)
        elif "--NODES--" in client_input:
            w = "No Nodes have been registered."
            word = str(w)
            print("[*] Processed result: {}".format(client_input))
            connection.sendall(word.encode("utf8"))
            print("[*] Sent " + word)
        elif "--NODEINFO--" in client_input:
            pass
            #result
        elif "--ADDNODE--" in client_input:
            #result
            pass
        elif "--REMOVENODE--" in client_input:
            #result
            pass
        else:
            try:
                print("[*] Processed result: {}".format(client_input))
                unknown = "[*] Unknown option.Please try again"
                warning = str(unknown)
                connection.sendall(warning.encode("utf8"))
                print("[*] Sent " + warning)
            except OSError as err:
                print('[*] Socket does not exist:', err)
            finally:
                pass


def receive_input(connection, max_buffer_size):
    try:
        client_input = connection.recv(max_buffer_size)
        client_input_size = sys.getsizeof(client_input)
    except ConnectionResetError as err:
        print('[*] Connection was lost:', err)
        return
        #pass

    if client_input_size > max_buffer_size:
        print("[*] The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result


def process_input(input_str):
    print("[*] Processing the input received from client")
    return str(input_str).upper()
    #pass

######################################makeblock and raspi section######################################################
#alarms = 0
#nodes = 0
#timer = True #use timer
#interval = 10 #check interval 5 min
timeout = None #read constantly from port
fan1 = "fan 1 loaded"
speed = 'mid'
today= str(datetime.now().strftime("%d_%m_%Y"))
#alertlog= "/var/automation/logs/alerts_" + today + ".log"
#remotelog = "/var/automation/logs/remote_" + today + ".log"
#serverlog =  "/var/automation/logs/server_" + today + ".log"
#nodelog = "/var/automation/nodes/nodes.log"
#uno = serial.Serial("/dev/ttyUSB0", 9600)
low = ''
mid = ''
high =''
r1 = ''
r2 = ''
r3 = ''
r4 = ''
currenttemp = 32
#currenttemp = read_serial()
ctemp = str(currenttemp)

def piserver():
    print("[*] PI server running. current temp is " +ctemp+ " celsius.")
    ##create_logfile()
    #while timer == True:
#	get_temp = read_serial()
	#print(get_temp)
#	if (get_temp > 32):
#		too_hot()
#		write_log(get_temp)	
#	else:
#		low_speed()
#		write_log(get_temp)
#	time.sleep(interval)
    
#print("[*] Server running.......")
#start_client()
#create_logfile()
#while timer == True:
#	get_temp = read_serial()
	#print(get_temp)
#	if (get_temp > 32):
#		too_hot()
#		write_log(get_temp)	
#	else:
#		low_speed()
#		write_log(get_temp)
#	time.sleep(interval)

def too_hot():
	'''increases fan speed. default for now is mid_speed()'''
	#write_log("[*] Too Hot!!!!!!!. engaging fans")
	increase_fan_speed(1,speed)
	
def increase_fan_speed(fans,speed):
	'''changes speed of fans based on info recieved'''
	fan = fans
	status =''
	if speed == 'mid':
		mid_speed()
		status = 1
	elif speed == 'high':
		high_speed()
		status = 1
	return(status)
#this section will hold all logic to work with 5v relays 
#to increase fanspeed it uses 5,9,12 volt ranges.
#all ranges wil be controlled by relays
#also colder air input will be done with servos
def low_speed():
	'''the fans in this section are all 5v supplied'''
	print("[*] running fans at default speed")
	
def mid_speed():
	'''the fans in this section are all 9v supplied'''
	print("[*] running fans half speed")
	
	
def high_speed():
	'''the fans in this section are all 12v supplied'''
	print("[*] running fans at high speed")
	
def decrease_fan_speed(fans,speed):
	pass
	#servo control logic is in next two functions
def increase_cold_air():
	pass

def decrease_cold_air():
	pass
	
###################################################data collection section#########################
def read_serial():
	result = uno.readline()
	ctemp = result.rstrip('\r\n')
	temp = ctemp.strip('Temperature=')
	ctemp = int(float(temp))
	txttemp = str(ctemp)
	return(ctemp)
	
def create_logfile(logfile):
	if not os.path.isfile(logfile):
		filewrite = open(logfile, "w")
		filewrite.write("***** Automation script alerts Log *****\n")
		print("[*] Log file created.")
		filewrite.close()
		#print(logfile)
	
def write_log(logfile,alert):
	if os.path.isfile(logfile):
		filewrite = open(logfile, "a")
		filewrite.write(str(alert) + "\n")
		filewrite.close
	else:
		print("[*] log file not found")

	
if __name__=='__main__':
    print(srvbanner)
    #try:
    #s1 = threading.Thread(target=fileserver)
    s2 = threading.Thread(target=controlserver)
    s3 =  threading.Thread(target=piserver)
    #s1.start()
    s2.start()
    s3.start()

#print("[*] Server running.......")
#alertlog= "/var/automation/logs/alerts_" + today + ".log"
#remotelog = "/var/automation/logs/remote_" + today + ".log"
#serverlog =  "/var/automation/logs/server_" + today + ".log"
#nodelog = "/var/automation/nodes/nodes.log"
#create_logfile(alertlog)
#create_logfile(remotelog)
#create_logfile(serverlog)
#create_logfile(nodelog)
#while timer == True:
#	get_temp = read_serial()
	#print(get_temp)
#	if (get_temp > 32):
#		too_hot()
#		write_log(get_temp)	
#	else:
#		low_speed()
#		write_log(get_temp)
#	time.sleep(interval)
