##########################################################################
#   COMS3200 Assingnment 1 Part B
#   Author: Raymond Sit 42881366
#   Script which connects from MOSS to localhost 22 and sends an email
#   Creates a log of the SMTP porotocol in smtplog.txt of local directory
#
###########################################################################

import socket
import time
import sys
import base64

###########################################################################
file = open("smtplog.txt","w") #SMTP Log File
file.write("Raymond Sit 42881366\n") #Initial Line
host = 'localhost' #Server Host Name
port = 25 #Mail Server

print('Starting the Program...')

print('Creating Socket')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket for communication

print('Getting IP address of server')
remote_ip = socket.gethostbyname(host) #Ip of host

#ESTABLISH CONNECTION TO SMTP#
print('Connecting to SMTP server ' + host + ' (' +remote_ip+')')
s.connect((remote_ip, port))
smtp_response = s.recv(4096) #Retrieves the reply msg
print("Reply to connection request:" + smtp_response)
if smtp_response[:3] != '220': #Check if error is recieved
    print('220 reply not recieved.')
    sys.exit()
    
server_name = smtp_response[4:-2] #Server Name saved for contents of email
file.write("RX> " + smtp_response.replace("\n","<n>").replace("\r","<r>")+ "\n") #Response recorded to log

#SEND GREETING TO THE MAIL SERVER#
print('Sending EHLO')
ehloCommand = bytes('EHLO itee.uq.edu.au\n\r')
s.sendall(ehloCommand)
file.write("TX> " + ehloCommand.replace("\n","<n>").replace("\r","<r>")+ "\n") #Transmit recorded to log
ehlo_response = s.recv(4096) #Retrieves Reply
print("EHLO Response:" + ehlo_response)
if ehlo_response[:3] != '250':
    print('250 reply not recieved.')
    sys.exit()
file.write("RX> " + ehlo_response.replace("\n","<n>").replace("\r","<r>")+ "\n")#Response recorded to log

#From EHLO Response, supported extensions are retrieved for contents of Mail#
nl_index = []; #Index Values of newline character in the response
for i in range(1,len(ehlo_response)):
    if ehlo_response[i] == '\n':
        nl_index.append(i);
extensions_list = []; #List of Extensions
for j in range(1,len(nl_index)):
    if ehlo_response[(nl_index[j-1]+1):(nl_index[j-1]+4)] == '250': #Only an extension if headed with 250 code
        extensions_list.append(ehlo_response[(nl_index[j-1]+5):(nl_index[j]-1)])
extensions_str = '\n\r'.join(extensions_list)

#Set the Sender eMAIL address#
print('Sending Mail command')
mailCommand = bytes('MAIL FROM:<robot@itee.uq.edu.au>\r\n')
s.sendall(mailCommand)
file.write("TX> " + mailCommand.replace("\n","<n>").replace("\r","<r>")+ "\n") #Transmit recorded to log
mail_response = s.recv(4096) #Retrieves Reply
print("MAIL Response:" + mail_response)
file.write("RX> " + mail_response.replace("\n","<n>").replace("\r","<r>")+ "\n")#Response recorded to log

#Set the RCPT of the email#
print('Sending Rcpt command')
rcptCommand = bytes('RCPT TO:<raymond.sit@uq.net.au>\r\n')
s.sendall(rcptCommand)
file.write("TX> " + rcptCommand.replace("\n","<n>").replace("\r","<r>")+ "\n") #Transmit recorded to log
rcpt_response = s.recv(4096) #Retrieves Reply
print("RCPT Response:" + rcpt_response)
file.write("RX> " + rcpt_response.replace("\n","<n>").replace("\r","<r>")+ "\n")#Response recorded to log

#Initiates the DATA input for Email#
print('Sending Email Data')
dataCommand = bytes('DATA\r\n')
s.sendall(dataCommand)
file.write("TX> " + dataCommand.replace("\n","<n>").replace("\r","<r>")+ "\n") #Transmit recorded to log
data_response = s.recv(4096) #Retrieves Reply
print("DATA Response"+ data_response)
file.write("RX> " + data_response.replace("\n","<n>").replace("\r","<r>")+ "\n")#Response recorded to log

#Sends the Contents of the Email#
subject = bytes("Subject: Test Email for Assignment 1 in Computer Networks\r\n") #Subject of Email
s.sendall(subject)

date = bytes(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())  + '\r\n\r\n') #Day, Date, and Time in GMT
s.sendall(date)

line1 = bytes('FROM:   ' + socket.gethostname() + '   [' + socket.gethostbyname(socket.gethostname()) + "]\r\n\r\n") #Sender Details
s.sendall(line1)

line2 = bytes('TO:   ' + server_name + '   [' + remote_ip + "]\r\n\r\n") #Server Details
s.sendall(line2)

line3 = bytes('SMTP extensions supported: \n\r' + extensions_str) #Server's List of Supported Extensions 
s.sendall(line3)

end_msg = bytes('\r\n.\r\n') #End Prompt
s.sendall(end_msg)

file.write("TX> " + subject.replace("\n","<n>").replace("\r","<r>")+ "\n" + date.replace("\n","<n>").replace("\r","<r>")
           + "\n" + line1.replace("\n","<n>").replace("\r","<r>") + "\n" + line2.replace("\n","<n>").replace("\r","<r>")
           + "\n" + line3.replace("\n","<n>").replace("\r","<r>") + "\n" + end_msg.replace("\n","<n>").replace("\r","<r>") + "\n") #Transmit recorded to log

end_response = s.recv(4096) #Retrieves Reply
print("Response after email data input has ended:" + end_response)
file.write("RX> " + end_response.replace("\n","<n>").replace("\r","<r>")+ "\n") #Response recorded to log

#Email should be sent, so Quit is sent to the Server#
print("Attempting to Quit")
quitCommand = bytes('QUIT\r\n')
s.sendall(quitCommand)
file.write("TX> " + quitCommand.replace("\n","<n>").replace("\r","<r>")+ "\n") #Transmit recorded to log
quit_response = s.recv(4096)#Retrieves Reply
print("Quit Response:" + quit_response)
file.write("RX> " + quit_response.replace("\n","<n>").replace("\r","<r>")+ "\n")#Response recorded to log

print("Exiting the program")
file.close() #Log File is closed
sys.exit() #Program Exited

