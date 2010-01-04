#!/usr/bin/env python
# encoding: utf-8
"""
	BackgroundTaskQueue.py 

"""
from cherrypy.process.plugins import SimplePlugin
import Queue
import threading

class BackgroundTaskQueue(SimplePlugin):
	thread = None
	
	def __init__(self, bus, qsize=100, qwait=2):
		SimplePlugin.__init__(self, bus)
		self.q = Queue.Queue(qsize)
		self.qwait = qwait
	
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
		if hasattr(self.q, 'join'):
			self.q.join()
	
	def run(self):
		while self.running:
			try:
				try:
					func, args, kwargs = self.q.get(block=True, timeout=self.qwait)
				except Queue.Empty:
					continue
				else:
					func(*args, **kwargs)
					if hasattr(self.q, 'task_done'):
						self.q.task_done()
			except:
				self.bus.log("Error in BackgroundTaskQueue %r." % self,
							 level=40, traceback=True)
	
	def put(self, func, *args, **kwargs):
		"""Schedule the given func to be run."""
		self.q.put((func, args, kwargs))

