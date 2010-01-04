#!/usr/bin/env python
# encoding: utf-8
"""
runForever.py

"""

from cherrypy.process.plugins import SimplePlugin
import Queue
import threading

class RunForever(SimplePlugin):
	thread = None
	
	def __init__(self, bus, callback):
		SimplePlugin.__init__(self, bus)
		self.callback = callback
	
	def start(self):
		self.running = True
		if not self.thread:
			self.thread = threading.Thread(target=self.run)
			self.thread.start()
			

	def stop(self):
		self.running = False
		if self.thread:
			self.thread.join()
			self.thread = None
	
	def run(self):
		while self.running:
			self.callback()
