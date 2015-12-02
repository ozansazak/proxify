import sys

try:
	import os
	import socket
	import threading
except ImportError as err:
	print("[!] Something has gone wrong while trying to import necessary libraries.")
	print("[!]", err)
	sys.exit(1)
except Exception as e:
	print("[!] An unexpected error has occured.")
	print("[!]", e)
	sys.exit(1)

RECV_MAX = 4096
BINARY_DECODER = "utf-8"
CMD_WIDTH = 75

class ClientHandler(threading.Thread):
	def __init__(self, clientConnection, clientAddress):
		threading.Thread.__init__(self)
		self.clientConnection = clientConnection
		self.clientAddress = clientAddress

	def run(self):
		while True:
			self.request = self.clientConnection.recv(RECV_MAX)
			self.request = self.request.decode(BINARY_DECODER)

			print(self.clientAddress[0] + "> " + self.request)

class TCPServer:
	def __init__(self, serverAddress, serverPort, clientBufferSize):
		self._addr = serverAddress
		self._port = serverPort
		self._cliBufSiz = clientBufferSize

		self.activeConnections = 0
		self._connectionList = []

	def setup(self):
		print("[*] Setting up server at {0}:{1} ...".format(self._addr, self._port), end = " ")

		try:
			self.__serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.__serverSock.bind((self._addr, self._port))
		except socket.error as err:
			raise RuntimeError(err)
		except Exception as e:
			print("[!] An unexpected error has occured.")
			raise RuntimeError(e)

		print("done.")
		
	def activate(self):
		
		try:
			self.__serverSock.listen(self._cliBufSiz)
		except socket.error as err:
			raise RuntimeError(err)
		except Exception as e:
			print("[!] An unexpected error has occured.")
			raise RuntimeError(e)

		print("[*] Server is running at {0}:{1}".format(self._addr, self._port))
		self.printStatus()

		while True:
			self.conn, self.cli_addr = self.__serverSock.accept()
			self.client_thread = ClientHandler(self.conn, self.cli_addr)

			#self.client_thread.run()     # I think that this part of code is dangerous
			self.client_thread.start()		# So, I wrote this instead of line 76th.
			self._connectionList.append((self.cli_addr[0], self.cli_addr[1], "*", self.conn))
			self.activeConnections += 1

			print("[*] Got a connection from {0}:{1}".format(self.cli_addr[0], self.cli_addr[1]))
			self.printStatus()

	def printStatus(self):
		print("[*] Waiting for connection ...")
		print("\t=> Server : {0}:{1}".format(self._addr, self._port))
		print("\t=> Queue  : {0} connected, {1} at all.".format(self.activeConnections, self._cliBufSiz))

		if self.activeConnections:
			for conn in self._connectionList:
				print("\n\tClient\t: {0}:{1}".format(conn[0], conn[1]))
				print("\tStatus\t: " + conn[2])

		print("\n")

if __name__ == "__main__":
	server = TCPServer("localhost", 3333, 5)
	server.setup()
	server.activate()
