#host
from socket import*
serv_addr="192.168.12.116"#local server ip 
serv_port=8001
client_sock=socket(AF_INET,SOCK_DGRAM)


def convert_to_16(tr_id):
    tr_id=bin(tr_id)
    tr_id=tr_id[2::]
    n=len(tr_id)
    for i in range(0,16-n):
        tr_id="0"+tr_id
    return tr_id
def str_to_bin(str):
    op=""
    for i in str:
        x=bin(ord(i))[2::]
        for j in range(0,8-len(x)):
            x="0"+x
        op+=x
    return op

#query 
trans_id=100
flags="0000000000000000"
payload=convert_to_16(trans_id)+flags
no_questions=1
payload+=convert_to_16(no_questions)
no_answers=0
payload+=convert_to_16(no_answers)
authorityrr=0
payload+=convert_to_16(authorityrr)
additionalrr=0
payload+=convert_to_16(additionalrr)
question="www.cdn25.com/1"
payload+=str_to_bin(question)
type_https="0000000001000001"
payload+=type_https
class_in="0000000000000001"
payload+=class_in

msg=payload
client_sock.sendto(msg.encode(),(serv_addr,serv_port))
print('Sending....'+payload)
mod_msg,s=client_sock.recvfrom(2048)
print("From Server:",mod_msg.decode())
mod_msg=mod_msg.decode()

client_sock.close()
ip_bin=mod_msg[len(mod_msg)-32::]
str_ip=""
arr_ip=[]
ind=0
const=0
ip=""
for i in ip_bin:
    str_ip+=i
    const+=1
    if(const==8):
        arr_ip.append(int(str_ip,2))
        ind+=1
        const=0
        str_ip=""
ip=str(arr_ip[0])+"."+str(arr_ip[1])+"."+str(arr_ip[2])+"."+str(arr_ip[3])


import cv2, imutils, socket
import numpy as np
import time, os
import base64
import threading, wave, pickle, struct

BUFF_SIZE = 65536

BREAK = False
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip =ip  # socket.gethostbyname(host_name)
print("IP address received",ip)
port = 9688
message = b'Hello'

client_socket.sendto(message, (host_ip, port))


def video_stream():
    cv2.namedWindow('RECEIVING VIDEO')
    cv2.moveWindow('RECEIVING VIDEO', 10, 360)
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    while True:
        packet, _ = client_socket.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet, ' /')
        npdata = np.fromstring(data, dtype=np.uint8)

        frame = cv2.imdecode(npdata, 1)
        frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            client_socket.close()
            os._exit(1)
            break

        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1

    client_socket.close()
    cv2.destroyAllWindows()





from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(video_stream)