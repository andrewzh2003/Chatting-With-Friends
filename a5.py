# a5.py
# Paolo andrew, Manalo Urani
# uranip@uci.edu
# 24555312
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.

from email import message
from pickle import FALSE
from re import S
import tkinter as tk
from tkinter import END, ttk, filedialog
from Profile import MessageHandler, Post, Profile
from ds_messenger import DirectMessenger

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self.username = None

        # a list of the Post objects available in the active DSU file
        self.AllMessages = {}
        self.messages = []
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, idk:0):
        #print(self.messages)
        index = int(self.posts_tree.selection()[0])
        #print(index)
        entry = self.messages[index]
        #print(entry)
        self.set_text_entry(entry, self.username)
    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.textBox.get('1.0', 'end').rstrip()

    def add_Message(self, msg,):
        self.entry_editor.insert(tk.INSERT, msg + '\n', tk.END)
        self.entry_editor.tag_add('user', str(float(-1(len(msg)+1))), tk.END)
        self.entry_editor.tag_config('user', foreground='blue')

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, messages:list, selfName):
        # TODO: Write code to that deletes all current text in the self.entry_editor widget
        # and inserts the value contained within the text parameter.
        self.entry_editor.delete('0.0', END)
        for i in range(len(messages)):
            self.entry_editor.insert(str(float(i)), messages[i]['entry'] + '\n', tk.END)
            if messages[i]['From'] == selfName:
                self.entry_editor.tag_add('user', str(float(i)), tk.END)
            else:
                self.entry_editor.tag_add('recipient', str(float(i)), tk.END)
            
        self.entry_editor.tag_config('user', foreground='blue')
        self.entry_editor.tag_config('recipient', foreground='green')
        pass
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_posts(self, messages:dict):
        # TODO: Write code to populate self._posts with the post data passed
        # in the posts parameter and repopulate the UI with the new post entries.
        # HINT: You will have to write the delete code yourself, but you can take 
        # advantage of the self.insert_posttree method for updating the posts_tree
        # widget.
        self.AllMessages = messages
        keys = list(messages.keys())
        for i in range(len(messages)):
            self.messages.append(messages[keys[i]])
            self._insert_post_tree(i, keys[i])

        pass

    """
    Inserts a single post to the post_tree widget.
    """
    def insert_post(self, messages, reciever): 

        self.messages.append(messages)
        id = len(self.messages) -1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, reciever)
    

    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_entry("", self.username)
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []
        self.messages = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_post_tree(self, id, usr):
        self.posts_tree.insert('', id, id, text=usr)
    
    """
    Call only once upon initialization to add widgets to the fra
    """
    def _draw(self):
        posts_frame = tk.Frame(master=self.root, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self.root, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)
        
        editor_frame = tk.Frame(master=entry_frame, bg="grey")
        editor_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        box_fram = tk.Frame(master= self.root)
        box_fram.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.textBox = tk.Text(box_fram, width=0)
        self.textBox.pack(fill=tk.BOTH, side = tk.TOP, expand= False)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.TOP, expand=False, padx=5, pady=5)
        

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, online_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using he get() function:
        # chk_value = self.is_online.get()
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    """
    Calls the callback function specified in the online_callback class attribute, if
    available, when the chk_button widget has been clicked.
    """
    def online_click(self):
        # TODO: Add code that implements a callback to the chk_button click event.
        # The callback should support a single parameter that contains the value
        # of the self.is_online widget variable.
        print(self.is_online.get())
        isOnline = self.is_online.get() == 1
        print(isOnline)
        if self._save_callback is not None:
            self._online_callback(isOnline)
        

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()

    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        save_button = tk.Button(master=self, text="Save Post", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        self.chk_button.configure(command=self.online_click) 
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""

class newProfilePopUp(object):
    def __init__(self,master):
        top=self.top= tk.Toplevel(master)
        self.l=tk.Label(top,text="DSU Server IP:")
        self.l.pack()
        self.serv=tk.Entry(top)
        self.serv.insert(tk.INSERT, '168.235.86.101')
        self.serv.pack()
        self.u=tk.Label(top,text="UserName:")
        self.u.pack()

        self.user=tk.Entry(top)
        self.user.pack()
        self.p = tk.Label(top, text="Password: ")
        self.p.pack()
        self.pas = tk.Entry(top)
        self.pas.pack()
        self.b=tk.Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.server = self.serv.get()
        self.username = self.user.get()
        self.password = self.pas.get()
        self.top.destroy()

class newContactPopUp(object):
    def __init__(self,master):
        top=self.top= tk.Toplevel(master)
        self.l=tk.Label(top,text="New Contact Username:")
        self.l.pack()
        self.e=tk.Entry(top)
        self.e.pack()
        self.b=tk.Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = Profile()
        self.dmsnger = None
        self._is_online = False

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self._profile_filename = None

    """
    Creates a new DSU file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        self.body.reset_ui()
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name
        w = newProfilePopUp(self.root)
        self.master.wait_window(w.top)
        self._current_profile = Profile(w.server, w.username, w.password)
        self.body.reset_ui()
        self.dmsnger = DirectMessenger('168.235.86.101', self._current_profile.username, self._current_profile.password)
        self._current_profile.save_profile(filename.name)
        self.body.username = self._current_profile.username


        # TODO Write code to perform whatever operations are necessary to prepare the UI for
        # a new DSU file.
        # HINT: You will probably need to do things like generate encryption keys and reset the ui.
        
    
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self):
        self.body.reset_ui()
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        # TODO: Write code to perform whatever operations are necessary to prepare the UI for
        # an existing DSU file.
        # HINT: You will probably need to do things like load a profile, import encryption keys 
        # and update the UI with posts.
        self._profile_filename = filename.name
        print(filename.name)
        self._current_profile = Profile()
        self._current_profile.load_profile(filename.name)
        self.body.reset_ui()
        self.body.set_posts(self._current_profile.get_posts())
        self._current_profile.save_profile(filename.name)
        self.body.username = self._current_profile.username
        self.dmsnger = DirectMessenger('168.235.86.101', self._current_profile.username, self._current_profile.password)
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """
    def publish(self, post:Post, usr):
        return self.dmsnger.send(post.get_entry, usr)

    def save_profile(self):
        # TODO: Write code to perform whatever operations are necessary to save a 
        # post entry when the user clicks the save_button widget.
        # HINT: You will probably need to do things like create a new Post object,
        # fill it with text, add it to the active profile, save the profile, and
        # clear the editor_entry UI for a new post.
        # This might also be a good place to check if the user has selected the online
        # checkbox and if so send the message to the server.
            index = int(self.body.posts_tree.selection()[0])
            reciever = list(self._current_profile.userMessages.keys())
            reciever = reciever[index]
            print(reciever)
            post = Post(self.body.get_text_entry(), 0, self._current_profile.username, )
            self._current_profile.add_post(post, reciever)
            self._current_profile.save_profile(self._profile_filename)
            print(self._is_online)
            if self._is_online:
                #try:
                    if self.publish(post, reciever):
                        self._current_profile.Organize_Messages()

                        self.body.set_posts(self._current_profile.userMessages)
                        #self.body.set_text_entry(self._current_profile.userMessages[reciever], self._current_profile.username)
                        self.footer.set_status('Successfully posted online')
                #except:
                #    self.footer.set_status('unable to post online')

    """
    A callback function for responding to changes to the online chk_button.
    """
    def online_changed(self, value:bool):
        # TODO: 
        # 1. Remove the existing code. It has been left here to demonstrate
        # how to change the text displayed in the footer_label widget and
        # assist you with testing the callback functionality (if the footer_label
        # text changes when you click the chk_button widget, your callback is working!).
        # 2. Write code to support only sending posts to the DSU server when the online chk_button
        # is checked.
        if value == 1:
            self.footer.set_status("Online")
            self._is_online = True
        else:
            self.footer.set_status("Offline")
            self._is_online = False
        #self.body.set_text_entry("Hello World")
        print(self._is_online, 'here')

    def newContact(self):
        w = newContactPopUp(self.root)
        self.master.wait_window(w.top)
        self._current_profile.add_post(Post('', 0, w.value, self._current_profile.username), self._current_profile.username)
        self._current_profile.Organize_Messages()
        self._current_profile.save_profile(self._profile_filename)
        self.body.AllMessages = self._current_profile.userMessages
        #self.body.set_text_entry(self._current_profile.userMessages, self._current_profile.username)
        self.body.insert_post(self._current_profile.userMessages[w.value], w.value)

    def changeDSU(self):
        pass
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback = self.online_changed)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, anchor= 's')
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 
        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu = settings_file, label = 'Settings')
        settings_file.add_command(label = 'Add contact', command = self.newContact)
        settings_file.add_command(label = 'Change DSU info', command = self.changeDSU)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        #self.footer = Footer(self.root, save_callback=self.save_profile, online_callback = self.online_changed)
        #self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, anchor= 's')

    #every 5 seconds we will look if there was any new messages sent, and store them and display them
    def updateMessages(self):
        if self.dmsnger != None:
            #get new messages
            l = self.dmsnger.retrieve_new()
            msgs = MessageHandler(l)
            msgs.SortByUsers()

            self._current_profile.AddNewMessages(msgs.UserMessages)
            self._current_profile.Organize_Messages()
            self._current_profile.save_profile(self._profile_filename)
            self.body.reset_ui()
            self.body.set_posts(self._current_profile.get_posts())
            print('test')

        self.root.after(5000, self.updateMessages)

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()
    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Final")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("860x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    app = MainApp(main)
    app.after(5000, app.updateMessages())

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()