import ds_messenger

#testing base ds_messenger
#accesses the paolotest123 acount in the server and then sends a message to paul
#then we check the new messages of paul and every message ever
dm = ds_messenger.DirectMessenger('168.235.86.101', 'dingus123', '123', '' )
print(dm.send('testing', 'paolo1'))

#we should see at least the message 'test' in dm2, but every message ever sent 