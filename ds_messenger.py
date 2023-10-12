# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Paolo Andrew, Manalo, Urani
# uranip@uci.edu
# 24555312
from cgi import test
from ctypes.wintypes import MSG
from email import message
from email.message import Message
from http import server
from lib2to3.pgen2 import token
from ntpath import join
from pydoc import cli
from pyexpat.errors import messages
import re
from shutil import unregister_unpack_format
import socket
import json
from tokenize import Token
from unicodedata import name
from urllib import response

import nacl
from Profile import Post
import ds_protocol
#from NaClProfile import NaClProfile

global messagePrint
messagePrint = ''

{"join": {"username": "paul","password": "123","token":""}}
{"token":"user_token", "post": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}
{"token":"user_token", "bio": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}

#connect('168.235.86.101', 3021)
'{"response": {"type": "error", "message": "Invalid DS Protocol format"}}'

#print(connectable('168.235.86.101', 3021))
#make a join json messaged encoded to send to the server
def makeJoin(usrnme:str, pswd:str, selfPubKey):
  m = '{"join": {"username": "' + usrnme + '","password": "' + pswd + '","token":"'+selfPubKey+'"}}'
  return m.encode('utf-8')

#sneds a string m to a server with a certain port, and obtains the message back from the server
def pushToServer(server:str, port:int, m:str):
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect((server, port))
      client.sendall(m)
      msg = client.recv(4096)
      return msg.decode('utf-8')
  except:
    return ''

      
{"token":"user_token", "post": {"entry": "Hello World!","timestamp": "1603167689.3928561"}}
#makes a message to send to the server given a msg str in a post json format and the token of the server
def makePost(msg:str, token: str):
  m = '{"token":"' + token + '", "post": ' + msg + '}'
  return m.encode('utf-8')

#makes a bio message to change the user's bio
def newBio(msg:str, token:str):
  m = '{"token":"' + token + '", "bio": ' + msg + '}'
  return m.encode('utf-8')


#print(command('{"join": {"username": "paul","password": "123","token":""}}'))
def getValidity(resp):
  obj = json.loads(resp)
  valid = None
  try:
    valid = obj['response']['type']
    return valid == 'ok'
  except:
    return False 

#recieved the public key of the server
def getToken(resp):
  obj = json.loads(resp)
  token = obj['response']['token']
  return token

#makes a post object, then creates a json formated object of that post to create messages to the server
def makeMSG(msg: str):
  m = Post(msg)
  return json.dumps(m)



class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None

class UserDoesntExistError(Exception):
  pass

class DirectMessenger:
    #i want to add encryuption
    def __init__(self, dsuserver=None, username=None, password=None, bio = None):
      self.token = None
      self.dsuserver = dsuserver
      self.username = username
      self.password = password
      self.bio = bio

    
    # Send a directmessage to another DS user
    {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}

    # Request unread message from the DS server
    {"token":"user_token", "directmessage": "new"}

    # Request all messages from the DS server
    {"token":"user_token", "directmessage": "all"}

    def makeDirectMSG(self, Message: str, recipient:str, token:str):
      p = Post(Message) 
      msg = '{"token":"' + token + '", "directmessage": {"entry": "' + Message+ '","recipient":"' + recipient + '", "timestamp": "' + str(p.get_time()) + '"}}'
      return msg.encode('utf-8')

    def makeUnread(self):
      if self.token == None:
        return ''
      s = '{"token":"' + self.token + '", "directmessage": "new"}'
      return s.encode('utf-8')

    def makeAllMsg(self):
      if self.token == None:
        return ''
      s = '{"token":"' + self.token + '", "directmessage": "all"}'
      return s.encode('utf-8')

    def send(self, message:str, recipient:str):
      '''
      The send function joins a ds server and sends a message, bio, or both

      :param server: The ip address for the ICS 32 DS server.
      :param port: The port where the ICS 32 DS server is accepting connections.
      :param username: The user name to be assigned to the message.
      :param password: The password associated with the username.
      :param message: The message to be sent to the server.
      :param bio: Optional, a bio for the user.
      '''
      valid1 = True
      valid2 = True
      valid3 = True
      global messagePrint
      messagePrint = ''
      try:
        if ds_protocol.connectable(self.dsuserver, 3021):
          joinMSG = makeJoin(self.username, self.password, '')
          resp = pushToServer(self.dsuserver, 3021, joinMSG)
          #print(getMSG(resp))
          extractable = ds_protocol.extract_json(resp)
          print(extractable.message)
          try:
            valid1 = extractable.type == 'ok'
          except:
            valid1 = False
          if valid1:
            tokenn = getToken(resp)
            print(tokenn)
            if message != '':
              #print(encryptMSG, 'encryptMsg')
              #print(NaclProf.decrypt(NaclProf.recieverPublicKey, NaclProf.private_key, msg))
              #print('hi', NaclProf.recieverPublicKey, NaclProf.private_key, NaclProf.public_key)
              msg2 = ''
              msg2 = self.makeDirectMSG(message, recipient, tokenn)
              self.token = tokenn
              resp = pushToServer(self.dsuserver, 3021, msg2)
              extractable = ds_protocol.extract_json(resp)
              print(extractable.message)
              valid2 = extractable.type == 'ok'

            if self.bio != None and self.bio != '' and type(self.bio) == str and valid2:

              encryptBio = self.NaclProf.encrypt_entry(self.bio, tokenn)
              msg3 = newBio(makeMSG(encryptBio), self.NaclProf.public_key)
              resp = pushToServer(server, 3021, msg3)
              extractable = ds_protocol.extract_json(resp)
              print(extractable.message)
              valid3 = extractable.type == 'ok'
          else:
            #print(1)
            return False
          if valid1 and valid2 and valid3:
            #print(2)
            return True
          else:
            #print(3)
            return False
        else:
          print('The server you are trying to access does not work')
          return False

      
      except:
        #print(5)
        return False
  

    def retrieve_new(self) -> list:
      # returns a list of DirectMessage objects containing all new messages
      #try:
        if ds_protocol.connectable(self.dsuserver, 3021):
          joinMSG = makeJoin(self.username, self.password, '')
          resp = pushToServer(self.dsuserver, 3021, joinMSG)
          #print(getMSG(resp))
          extractable = ds_protocol.extract_json(resp)
          print(extractable.message)
          tokenn = getToken(resp)
          self.token = tokenn
          if extractable.type == 'ok':
            msg = self.makeUnread()
            print(msg)
            if msg == '':
              print('You have yet to connect to a server')
              return None
            else:
              resp = pushToServer(self.dsuserver, 3021, msg)
              print(resp)
              extractable = ds_protocol.extract_json(resp)
              try:
                return extractable.messages
              except:
                print('Error')
                return None
          else:
            print('couldnt connect to server')
            return None
      #except:
      #  return None
 
    def retrieve_all(self) -> list:
      # returns a list of DirectMessage objects containing all messages
      # returns a list of DirectMessage objects containing all new messages
      #try:
        if ds_protocol.connectable(self.dsuserver, 3021):
          joinMSG = makeJoin(self.username, self.password, '')
          resp = pushToServer(self.dsuserver, 3021, joinMSG)
          #print(getMSG(resp))
          extractable = ds_protocol.extract_json(resp)
          print(extractable.message)
          tokenn = getToken(resp)
          self.token = tokenn
          if extractable.type == 'ok':
            msg = self.makeAllMsg()
            print(msg)
            if msg == '':
              print('You have yet to connect to a server')
              return None
            else:
              resp = pushToServer(self.dsuserver, 3021, msg)
              
              extractable = ds_protocol.extract_json(resp)
              try:
                return extractable.messages
              except:
                print('Error')
                return None
          else:
            print('couldnt connect to server')
            return None
    
  
#print(send('168.235.86.101', 301, "andrew568", "123", '', '{"entry": "Hello World!","timestamp": "1603167689.3928561"}'))
#print(send('168.235.86.101', 3021, "dinger", "pissbaby", '{"token":"603ac67d-e6a8-4b81-8eae-bde90f0d105b", "bio": {"entry": "from pyke","timestamp": "1603167689.3928561"}}'))
#tester code to test out differnt values

if __name__ == '__main__':

  dm = DirectMessenger('168.235.86.101', 'Paolotest123', '123', '' )
  print(dm.makeDirectMSG('idk', 'paul', ''))
  dm.send('hello stranger! i hope you have a wonder day', 'paul')
  dm2 = DirectMessenger('168.235.86.101', 'paul', '123', '')
  print(dm2.retrieve_new())
  print(dm2.retrieve_all())
