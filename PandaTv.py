#!/usr/bin/env python
#coding=utf8

import socket
import httplib2
import time
import json
import re

#def getstatus(res):

#cookie="" #复制cookie到这

def getfollow():
    url="http://www.panda.tv/myfollow"
    conn = httplib2.Http('.cache')
    headers={'Cookie':cookie}
    response,content = conn.request(url,'GET',headers=headers)
    content=content.decode('utf8')
    f=open("test.txt",'w')
    f.write(content)
    m=re.findall(r"<li class=\"video-list-item  \" data-id=\"[\d]+\">",content)
    roomid=[]
    roominfo=[]
    for s in m:
        index=s.find('id=')
        roomid.append(s[index+4:-2])
    for i in roomid:
        url='http://www.panda.tv/api_room?roomid='+str(i);
        conn = httplib2.Http('.cache')
        response,content = conn.request(url)
        data=json.loads(content.decode('utf-8'));
        t={}
        t['title']=data['data']['roominfo']['name']
        t['name']=data['data']['hostinfo']['name']
        t['pic']=data['data']['roominfo']['pictures']['img']
        t['roomid']=str(i)
        if(int(data['data']['videoinfo']['status'])==2):
            roominfo.append(t)
    return roominfo

def getroomstatus(room,TextEdit):
    url='http://www.panda.tv/api_room?roomid='+str(room);
    conn = httplib2.Http('.cache')
    response,content = conn.request(url)
    data=json.loads(content.decode('utf-8'));
    if response.status != 200:
       TextEdit.append("连接失败")
       return -1
    elif data['errno']!=0:
       TextEdit.append("不存在该房间")
       return -1
    else:
       return data['data']['videoinfo']['status']

def getdm(room,thread):
    t=int(time.time()*1000);
    url1='http://www.panda.tv/ajax_chatroom?roomid='+str(room)+'&_='+str(t)
    conn = httplib2.Http('.cache')
    response,content = conn.request(url1)
    if response.status != 200:
        #TextEdit.append("连接失败")
        thread.trigger.emit("连接失败")
        return
    data_url1=json.loads(content.decode('utf-8'));


    rid=data_url1['data']['rid']
    roomid=data_url1['data']['roomid']
    sign=data_url1['data']['sign']
    ts=data_url1['data']['ts']
    t=time.time();
    t=t*1000;
    t=int(t);
    url2='http://api.homer.panda.tv/chatroom/getinfo?rid='+str(rid)+'&roomid='+str(roomid)+'&retry=0&sign='+str(sign)+'&ts='+str(ts)+'&_='+str(t)
    conn = httplib2.Http('.cache')
    response,content = conn.request(url2)
    if response.status != 200:
        #TextEdit.append("连接失败")
        thread.trigger.emit("连接失败")
        return
    data_url2=json.loads(content.decode('utf-8'));

    rid=str(data_url2['data']['rid'])
    appid=str(data_url2['data']['appid'])
    k=str(1)
    ts=str(data_url2['data']['ts'])
    sign=str(data_url2['data']['sign'])
    authType=str(data_url2['data']['authType'])
    URL=str(data_url2['data']['chat_addr_list'][0])
    URL=URL.split(':',1);
    Host=URL[0]
    Port=URL[1]

    msg='u:' + rid + '@' + appid + '\n' +'k:' + k + '\n' + 't:' + str(t) + '\n' + 'ts:' + ts + '\n' + 'sign:' + sign + '\n' + 'authtype:' + authType;
    bmsg=bytearray(msg,'utf8');
    head=bytearray([0x00, 0x06, 0x00, 0x02, 0x00, len(bmsg)])
    bmsg=head+bmsg;

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((Host,int(Port)))
    time.sleep(2)
    s.send(bmsg)
    s.send(bytearray([0x00,0x06,0x00,0x00]))
    t=int(time.time()*1000)
    #f=open("Pandatv.txt","w")
    #TextEdit.append("连接成功")
    thread.trigger.emit("连接成功")
    while (True):
        r=s.recv(1024)
        if(r[3]==0x03 and r[40]==0x31):
            temp=r[11]*256*256*256+r[12]*256*256+r[13]*256+r[14]*1
            head=r[23:27]
            r=r[27:31+temp]
            index=4
            while (True):
                temp2=r[0]*256*256*256+r[1]*256*256+r[2]*256+r[3]
                sr=r[index:index+temp2]
                #print (sr)
                sr=sr.decode('utf8')
                jr=json.loads(sr)
                thread.trigger.emit("<font color=\"red\">"+jr["data"]["from"]["nickName"]+"</font>:"+jr["data"]["content"])
                #TextEdit.append("<font color=\"red\">"+jr["data"]["from"]["nickName"]+"</font>:"+jr["data"]["content"])
                #f.flush()
                r=r[index+temp2+12:len(r)]
                if(len(r)<10 or sr[9]!=0x31 or sr[len(sr)-1]!=0x7d):
                    break
        if(int(time.time()*1000)-t>60*1000):
            t=int(time.time()*1000)
            s.send(bytearray([0x00,0x06,0x00,0x00]))
        if(thread.flag==0):
            return