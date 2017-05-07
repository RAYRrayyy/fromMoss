###############################################################
#
# COMS3200 Assignment 2 PArt B - Webget
# Author: Raymond Sit 42881366
# Script which attempts to download off the specified URL
# Returns useful error messages if unsuccessful
#
###############################################################

import sys
import socket
import time
import base64

#####################INPUT ARGUMENT PROCESSING#################
print("Starting Program...")
print("Checking Input Arguments...")

#Checks for correct number of inputs, function and the URL#
if len(sys.argv) != 2:
    print("Error 1: Too many inputs, only accepts funtion name and url")
    sys.exit()
url = sys.argv[1];
#Checks for http protocol#
if url[0:7] != "http://":
    print("Error 2: Incorrect protocol, Only http:// is accepted")
    sys.exit()
#Get index of the final backslash to seperate host and filename#
slash_index = [];
for i in range(1, len(url)):
    if url[i] == '/':
        slash_index.append(i)
#Check for hostname#
hostname = url[7:slash_index[2]]
#Checks for directory if it exists#
if len(slash_index) > 3:
    directory = url[slash_index[2]+1:slash_index[-1]]
#Check for filename#
filename = url[slash_index[-1]+1:]
print("Input Arguments OK")

########################SOCKET BEGIN##########################
port = 80 #http welcome port

print("Creating Socket")
#Socket for communications#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remote_ip = socket.gethostbyname(hostname) #IP of host

print('Connecting to server ' + hostname + ' (' +remote_ip+')')
s.connect((remote_ip,port))
smtp_response = s.recv(4096) #Retrieves the reply msg
print("Reply to connection request:" + smtp_response)
if smtp_response[:3] != '220': #Check if error is recieved
    print('220 reply not recieved.')
    sys.exit()

print("Exiting Program...")
sys.exit()


    
