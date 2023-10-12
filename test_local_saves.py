from pathlib import Path
from Profile import Profile, MessageHandler, Post
from ds_messenger import DirectMessenger

dm = DirectMessenger('168.235.86.101', 'paul', '123', '' )
l = dm.retrieve_all()
mh = MessageHandler(l)
mh.SortByUsers()
print(mh.UserMessages)
prof = Profile('168.235.86.101', 'paul', '123')

prof.save_profile(r'C:\Users\Urani\ics32stuff\Final Project-paolo andrew john\test2.dsu')
prof.update_UserMSGs(mh.UserMessages)
prof.add_post(Post('testing adding a post', 0, prof.username, 'ittapuppy'), 'ittapuppy')
prof.save_profile(r'C:\Users\Urani\ics32stuff\Final Project-paolo andrew john\test2.dsu')
#check if the profile in this file has all the messages sent to the user

prof2 = Profile()
prof2.load_profile(r'C:\Users\Urani\ics32stuff\Final Project-paolo andrew john\test2.dsu')
print(prof2.userMessages)
print(prof2.Organize_Messages())
#check if the usermessages are the same, we can now get the messages from a stored place and store the messages in a dsu file
#check if the messages are stored from latest messages to the oldest ones
#1647415103.4233444   
#1647415100.512346

