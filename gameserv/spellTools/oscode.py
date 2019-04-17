#!/usr/bin/env python2
import sys
worked = False
file_name = ''
if len(sys.argv) < 2:
	file_name = raw_input('please specify a file > ')
else:
	file_name = sys.argv[1]
while worked == False:
	try:
		f = open(file_name,'rb')
		worked = True
	except:
		file_name = raw_input('please specify a valid file name > ')
data = f.read()
f.close()
for i in range(0,len(data)):
	sys.stdout.write('\\' + hex(ord(data[i])))
sys.stdout.write('\n')
