#coding=utf-8
import socket
import pickle
from datetime import datetime
HOST = '47.93.204.170'
PORT = 8080
from sys import argv
import time,os

def temp(ip):
        a = os.popen("ping -n 2 "+ip).read()
        if(len(a.split("\n"))<3 or len(a.split('\n')[2].split(" "))<5):
                return -1,-1
        ti = a.split('\n')[2].split(" ")[4].split("=")[1].split("m")[0]
        ttl = a.split('\n')[2].split(" ")[5].split("=")[1]
        return int(ti),int(ttl)

def syn_scan(host,port,filename,id):
	f = open(filename,"rb")
	ff = open(filename+"_res_"+id,"wb")
	for i in f.readlines():
		line = i
		ip = i.split(" ")[0]
		port = int(i.split(" ")[2][0:-2])
		print line
		for j in range(10):
			print ip

                        t,ttl = temp(ip)
			
			ff.write(str(t)+"\t"+str(128-ttl)+"\t"+line)
			
	f.close()
	ff.close()


if __name__ == '__main__':
	func = {
		"scan":syn_scan
	}
	if len(argv)<6:
		print "usage:python socket_client.py scan [ip] [port] [filename] [id]"
	else:
		print func[argv[1]](argv[2],int(argv[3]),argv[4],argv[5])
