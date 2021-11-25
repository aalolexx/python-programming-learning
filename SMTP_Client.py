## This script connects to googles smtp server and sends a simple mail

import socket
import base64

TCP_IP = "localhost"
TCP_PORT = 25
BUFFER_SIZE = 1024
SENDER = "xxxxx"
RECEIVER = "xxxxx"
PASSWORD = "xxxxx"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
recv = s.recv(1024)
recv = recv.decode()
if recv[:3] != '220':
    print("220 reply not received from server.")

#
# say helo
#

heloCommand = 'helo google\r\n'
s.send(heloCommand.encode())
recv1 = s.recv(1024)
recv1 = recv1.decode()
print("Message after helo command: " + recv1)
if recv1[:3] != '250':
    print("250 reply not received from server.")


#
# Authentification
#

base64_str = ("\x00"+SENDER+"\x00"+PASSWORD).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
s.send(authMsg)
recv_auth = s.recv(1024)
recv_auth = recv_auth.decode()
print("Message after authentification: " + recv_auth)
if recv_auth[:3] != '235':
    print('250 reply not received from server.')

#
# Defining headers and sending the actual mail
#

mailFrom = "MAIL FROM:<"+SENDER+">\r\n"
s.send(mailFrom.encode())
recv2 = s.recv(1024)
recv2 = recv2.decode()
print("After MAIL FROM command: "+recv2)
rcptTo = "RCPT TO:<"+RECEIVER+">\r\n"
s.send(rcptTo.encode())
recv3 = s.recv(1024)
recv3 = recv3.decode()
print("After RCPT TO command: "+recv3)
data = "DATA\r\n"
s.send(data.encode())
recv4 = s.recv(1024)
recv4 = recv4.decode()
print("After DATA command: "+recv4)
subject = "Subject: testing my client\r\n\r\n"
s.send(subject.encode())
body = "Test Body content\r\n\r\n.\r\n"
s.send(body.encode())
recv_msg = s.recv(1024)
print("Response after sending message body: "+recv_msg.decode())
quit = "QUIT\r\n"
s.send(quit.encode())
recv5 = s.recv(1024)
print(recv5.decode())

# close the connection
s.close()