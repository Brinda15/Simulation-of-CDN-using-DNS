#local dns
#User requests video
#Send to local dns
#Make counter for transaction ID (Same for request and reply)
def convert_to_16(tr_id):
    tr_id=bin(tr_id)
    tr_id=tr_id[2::]
    n=len(tr_id)
    for i in range(0,16-n):
        tr_id="0"+tr_id
    return tr_id
def bin_to_str(b):
    n=len(b)
    low=0
    high=8
    q=""
    for i in range(0,int(n/8)):
        ch=b[low:high:]
        ch_ascii=int(ch,2)
        low+=8
        high+=8
        q+=chr(ch_ascii)
    return q
def str_to_bin(str):
    op=""
    for i in str:
        x=bin(ord(i))[2::]
        for j in range(0,8-len(x)):
            x="0"+x
        op+=x
    return op
def ip_to_bin(ip):
    arr=ip.split('.')
    print(arr)
    str=""
    for i in range(len(arr)):
        print(arr[i])
        x=bin(int(arr[i]))[2::]
        for j in range(0, 8 - len(x)):
            x = "0" + x
        str+=x
    print(str)
    return str
from socket import*
addr="192.168.0.130" # own ip
port=8001
sock=socket(AF_INET,SOCK_DGRAM)
sock.bind((addr,port))
print("Ready to recieve")
while 1:
    ques,c_addr=sock.recvfrom(2048)
    print("got msg from",c_addr)
    serv_addr="192.168.0.107"# root dns 
    serv_port=8000
    client_sock=socket(AF_INET,SOCK_DGRAM)
    ques_str_bin=ques[96:len(ques)-32:]
    question_full=bin_to_str(ques_str_bin)
    question=question_full[:len(question_full)-2:]
    print(question)



    #query 1
    trans_id=0
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
    #question=question_full[:len(question_full)-2:]
    #print("q=",question)
    #question="www.cdn25.com"
    #print(str_to_bin(question))
    #print(len(str_to_bin(question)))
    payload+=str_to_bin(question)
    type_https="0000000001000001"
    payload+=type_https
    class_in="0000000000000001"
    payload+=class_in
    print("Payload to be sent to  root DNS: ",payload)

    msg=payload
    client_sock.sendto(msg.encode(),(serv_addr,serv_port))
    mod_msg,s=client_sock.recvfrom(2048)
    print("From root DNS Server:",mod_msg.decode())
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

    print("IP of TLD server as received from root DNS:",ip)
    serv_addr1=ip.strip()
    serv_port1=8000
    client_sock1=socket(AF_INET,SOCK_DGRAM)
    trans_id+=1
    #print(len(msg))
    msg=msg[16::]
    #print(len(msg))
    msg=convert_to_16(trans_id)+msg
    client_sock1.sendto(msg.encode(),(serv_addr1,serv_port1))
    mod_msg1,s=client_sock1.recvfrom(2048)
    mod_msg1=mod_msg1.decode()
    print("From TLD DNS Server:",mod_msg1)

    ip_bin=mod_msg1[len(mod_msg1)-32::]
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
    print("IP address of authoritative server 1 as received from TLD server:",ip)

    client_sock1.close()
    serv_addr1=ip.strip()
    serv_port1=8000
    client_sock1=socket(AF_INET,SOCK_DGRAM)
    trans_id+=1
    msg=convert_to_16(trans_id)+flags+convert_to_16(no_questions)+convert_to_16(no_answers)+convert_to_16(authorityrr)+convert_to_16(additionalrr)+str_to_bin(r"www.cdn25.com/1")+type_https+class_in
    client_sock1.sendto(msg.encode(),(serv_addr1,serv_port1))
    mod_msg1,s=client_sock1.recvfrom(2048)
    mod_msg1=mod_msg1.decode()
    print("From authoritative Server 1:",mod_msg1)
    client_sock1.close()


    ip_bin=mod_msg1[len(mod_msg1)-32::]
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
    print("IP address of authoritative server 2 as sent by authoritative server 1:",ip)
    msg="000000000000101010000100000000000000000000000001000000000000000100000000000000000000000000000000"+""+ip_to_bin(ip)
    sock.sendto(msg.encode(),c_addr)
    print("Message to be sent to requesting host:",msg)