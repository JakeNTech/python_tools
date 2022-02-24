"""
Basic ping sweep demo
JakeNTech
11/11/2020
Will send one ICMP echo packet to each IP in a given class C address
"""
import subprocess
import argparse

def getargs():
	parser = argparse.ArgumentParser()
	parser.add_argument("-ip", "--class-c", dest="class_c", help="IP range to ping", metavar="NET_ID.<min_ip>-<max-ip>",required=True)
	return parser.parse_args()

print("Ping Sweep")
IP = getargs().class_c.split(".")
min_ip = IP[3].split("-")[0]
max_ip = IP[3].split("-")[1]
for i in range(int(min_ip),int(max_ip)+1):
	ping_address = IP[0]+"."+IP[1]+"."+IP[2]+"."+str(i)
	subprocess.call(["ping", "-c", "1","-W","2" ,ping_address])
