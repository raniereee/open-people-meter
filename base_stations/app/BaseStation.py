import subprocess, sys
import datetime
from twisted.internet import reactor
import tarfile, requests

from dejavu import Dejavu

import logging

import socket, struct, fcntl
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd = sock.fileno()
SIOCGIFADDR = 0x8915

#serial="39"
serial = sys.argv[1]
city   = sys.argv[2]

class StatioBase():
	def __init__(self):
		self.count_error       = 0
		self.count_try_wait_ip = 0
		self.count_cmd_count   = 0
		self.port     = "/dev/ttyUSB2"
		#self.baudrate = 460800
		self.baudrate = 921600
		self.rtscts   = 0

		self.rxbuffer = ""
		self.step = None
		self.tmr_cmd = None
		self.tmr_new_command = 1
		self.timer_reconnect = None
		self.cmd_at_error = 0

                logging.basicConfig(filename='/tmp/basestation.log',level=logging.DEBUG)


		logging.info( "Instanced  base station class")

		reactor.callLater(1, self.main_loop)

	def get_ip(self, iface = 'usb0'):

		ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)

		try:
			res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
		except:
			return None

		ip = struct.unpack('16sH2x4s8x', res)[2]
		return socket.inet_ntoa(ip)



	def __check_usb_modem(self):
		try:
			subprocess.check_output("lsusb | grep WCDMA", shell=True)
		except:
			logging.info( "There is not MODEM 3G - REBOOT")
			subprocess.check_output("reboot -n", shell=True)
			reactor.stop()
                	sys.exit(0)
			return False

		return True



	def __ppp_iface_monitor(self):

		ip_address = self.get_ip('usb0')
		if ip_address is not None:
			logging.info( "Ip address in usb0: %s " % ip_address)
			reactor.callLater(0.01, self.main_loop)
			return True

		reactor.callLater(30, self.__ppp_iface_monitor)

		return False

	def __check_ifc_ppp(self):

		ip_address = self.get_ip('usb0')
		if ip_address is not None:
			return True

		self.__check_usb_modem()

		logging.info( "Waiting for ip...")
		return False


	def main_loop(self):
		self.date = datetime.datetime.now()

		if self.__check_ifc_ppp() == False:
			reactor.callLater(5, self.main_loop)
			return

		if self.date.second == 14:
			logging.info( "Second 14: Now, its time to work. ERROR COUNT: %d" % self.count_error)
			reactor.callLater(0.01, self.__exec_record)
			return

		if self.__check_usb_modem() is False: return

		if self.count_error >= 3:
			logging.info( "Count Error is tree. Reboot")
			subprocess.check_output("reboot -n", shell=True)
			reactor.stop()
                	sys.exit(0)
			self.count_error = 0
			return

		reactor.callLater(0.3, self.main_loop)
		

	def __exec_record(self):
		hora_gravacao="%d-%d-%d-%d-%d" %(self.date.year, self.date.month, self.date.day, self.date.hour, self.date.minute)

		self.audio_file="/mnt/ram/hashes_" + serial + "_" + hora_gravacao + ".wav"
		self.hashfile  ="/mnt/ram/hashes_" +  serial + "_" + hora_gravacao + ".wav.txt"

		cmd = "sox -v 0.80 -r 44100 -c 1 -d " + self.audio_file + " trim 0 00:07  >> /dev/null 2>&1"
		subprocess.call(cmd, shell=True)

		reactor.callLater(0.01, self.__exec_fp)


	def __exec_fp(self):

		config = {"database": {"host": "127.0.0.1","user": "root","passwd": "dev","db": "",},"database_type" : "mysql"}
		djv = Magic(config)

		djv.fp_file(self.audio_file)
		logging.info( "Process finger print of audio: %s " % self.audio_file)

		subprocess.call("rm " + self.audio_file, shell=True)

		reactor.callLater(0.01, self.__compact_hashes)

	def __compact_hashes(self):

		self.tarhash = self.hashfile + ".tar.gz"
		tar = tarfile.open(self.tarhash, "w:gz")
		tar.add(self.hashfile)
		tar.close()

		subprocess.call("rm " + self.hashfile, shell=True)

		reactor.callLater(0.01, self.main_loop)
		reactor.callLater(0.01, self.__send_hashes_file, self.tarhash)

	def __send_hashes_file(self, tarhash):

		url = 'http://192.168.1.254:8080/upload.php'
		fd = open(tarhash, 'rb')
		files = {'upfile': fd}
		headers = {'serial': serial, 'minute': "%02d" % self.date.minute, 'city': city}

		try:
			logging.info( "Try post")
			self.request = requests.post(url, files=files, timeout=30, headers=headers)
		except:
			logging.info( "Conection fail.")
			fd.close()
			subprocess.call("rm " + tarhash, shell=True)
			self.count_error = self.count_error  + 1
			return


		fd.close()
		subprocess.call("rm " + tarhash, shell=True)

		if self.request.status_code == 200:
			logging.info( "Sent with success:  %d   Text: %s" % (self.request.status_code, self.request.text))
			self.count_error = 0

def main():
	sb=StatioBase()

	reactor.run()

if __name__ == "__main__":
	main()
