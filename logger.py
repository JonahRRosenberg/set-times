import logging

def initialize():
  logging.basicConfig(
      filename='settimes.log',
      format='%(asctime)s %(levelname)s %(message)s',
      level=logging.DEBUG)

def info(msg):
  logging.info(msg)
  print 'INFO: ' + msg

def error(msg):
  logging.error(msg)
  print 'ERROR: ' + msg
  
def warn(msg):
  logging.warn(msg)
  print 'WARN: ' + msg

def debug(msg):
  logging.debug(msg)
  print 'DEBUG: ' + msg
