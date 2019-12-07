from Tkinter import * 
import tkMessageBox 
from PIL import Image, ImageTk 
import socket, threading, sys, traceback, os 
from RtpPacket import RtpPacket 

CACHE_FILE_NAME = "cache-" 
CACHE_FILE_EXIT + ".jpg" 

class Client: 
    INIT = 0 
    READY = 1 
    PLAYING = 2 
    state = INIT 
    SETUP = 0 
    PLAY = 1 
    PAUSE = 2 
    TEARDOWN = 3 
    
    def _init_(self, master, serveraddr, serverport, rtpport, filename): 
      self.master = master 
      self.master.protocol("WM_DELETE_WINDOW", self.handler) 
      self.createWidgets() 
      self.serverAddr = serveraddr 
      self.serverPort = int(serverport) 
      self.rtpPort = int(rtpport) 
      self.fileName = filename 
      self.rtspSeq = 0 
      self.sessionid = 0 
      self.requestSent = -1
      self.teardownAcked = 0 
      self.connectToServer() 
      self.framNbr = 0 
      
   def createWidgets(self): 
      self.setup = Button(self.master, width = 20, padx = 3, pady = 3) 
      self.setup["text"] = "Setup" 
      self.setup["command"] = self.setupMovie 
      self.setup.grid(row = 1, column = 0, padx = 2, pady = 2) 
      
      self.start = Button(self.master, width = 20, padx = 3, pady = 3) 
      self.start["text" = "Play" 
      self.start["command"] = self.playMovie 
      
      self.start.grid(row = 1, column = 1, padx = 2, pady = 2) 
      
      self.pause = Button(self.master, width = 20, padx = 3, pady = 3) 
      self.pause["text"] = "Pause" 
      self.pause["command"] = self.pauseMovie
      self.pause.grid(row = 1, column = 2, padx = 2, pady = 2) 
      
      self.teardown = Button(self.master, width = 20, padx = 3, pady 3) 
      self.teardown["text"] = "Teardown" 
      self.teardown["command"] = self.exitClient 
      self.teardown.grid(row = 1, column = 3, padx = 2, pady = 2) 
      
      self.label = Label(self.master, height = 19) 
      self.label.grid(row = 0, column = 0, columnspan = 4, sticky = W+E+N+S, padx = 5, pady = 5) 
      
  def setupMovie(self): 
      if self.state = self.INIT: 
          self.sendRtspRequest(self.SETUP) 
          
  def exitClient(self): 
      self.sendRtspRequest(self.TEARDOWN) 
      self.master.destroy() 
      os.remove(CACHE_FILE_NAME + str(self.sessionid) + CACHE_FILE_EXT) 
 
  def pauseMovie(self): 
      if self.state = self.PLAYING: 
          self.sendRtspRequest(self.PAUSE) 
          
  def playMovie(self): 
      if self.state == self.READY: 
          threading = Thread(target = self.listenRtp).start() 
          self.playEvent = threading.Event() 
          self.playEvent.clear() 
          self.sendRtspRequest(self.PLAY) 
  
  def listenRtp(self): 
      while True: 
          try:   
              data = self.rtpSocket.recv(20480)
  
      
