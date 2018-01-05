#coding=utf-8
import socket
import pickle
from datetime import datetime
HOST = '47.93.204.170'
PORT = 8080
from scapy.all import *
from sys import argv

def syn_scan(host,port,filename,id):
	f = open(filename,"rb")
	ff = open(filename+"_res_"+id,"wb")
	for i in f.readlines():
		line = i
		ip = i.split(" ")[0]
		port = int(i.split(" ")[2][0:-2])
		print line
		for j in range(50):
			print ip
			t = datetime.utcnow()
			a = sr1(IP(dst=ip)/TCP(dport=port,flags="S"))
			t = datetime.utcnow() - t
			t = t.total_seconds()*1000
			#print (t,255-a.ttl)
			ff.write(str(t)+"\t"+str(255-a.ttl)+"\t"+line)
	f.close()
	ff.close()

def measure(host,port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	data = {
		"head":"measure",
		"contents":[datetime.utcnow(),0,0]
	}
	req = pickle.dumps(data)
	sock.sendto(req + "\n", (host, port))
	print "sent data to "+host+" "+str(port)
	print "waiting..."
	received = sock.recv(1024)
	t = datetime.utcnow()
	res = pickle.loads(received)
	#res[2] = t
	#delay0 = res[1]-res[0]
	#delay0 = delay0.total_seconds()
	#delay1 = res[2]-res[1]
	#delay1 = delay1.total_seconds()
	
	delay0 = t-res[0]
	delay1 = res[1]-res[0]
	delay2 = t-res[2]
	return (delay0,delay1,delay2)

if __name__ == '__main__':
	func = {
		"scan":syn_scan,
		"measure":measure
	}
	if len(argv)<6:
		print "usage:python socket_client.py scan [ip] [port] [filename] [id]"
	else:
		print func[argv[1]](argv[2],int(argv[3]),argv[4],argv[5])
