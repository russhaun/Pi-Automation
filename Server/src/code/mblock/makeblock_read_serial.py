#!/usr/bin/python3
import serial
import os
import sys


uno = serial.Serial("/dev/ttyUSB0", 9600)

def read_serial():
	result = uno.readline()
	ctemp = result.rstrip('\r\n')
	temp = ctemp.strip('Temperature=')
	ctemp = int(float(temp))
	txttemp = str(ctemp)
	return(ctemp)
	
