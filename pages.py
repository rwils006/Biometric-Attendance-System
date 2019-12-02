import tkinter as tk
from tkinter import ttk

from db import Database

db = Database('students.db')

class Attendance(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.geometry("700x350")
        container.grid(row=0, column=0, sticky=tk.N)
        self.frames = {}
        
        for F in (StartPage, CheckInPage, RegisterPage, EnrollNFCPage, AdminPage):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        
        self.show_frame(StartPage)
        
    def show_frame(self, container):
        
        frame = self.frames[container]
        frame.tkraise()

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.label = tk.Label(self, text="Home")
        self.label.grid(row=0, column=1, sticky=tk.N)
        
        self.checkInButton = ttk.Button(self, text="Check In", command=lambda: controller.show_frame(CheckInPage))
        self.checkInButton.grid(row=1, column=0)
        
        self.registerButton = ttk.Button(self, text="Register", command=lambda: controller.show_frame(RegisterPage))
        self.registerButton.grid(row=1, column=1)
        
        self.profileButton = ttk.Button(self, text="My Profile")
        self.profileButton.grid(row=2, column=0)
        
        self.adminButton = ttk.Button(self, text="Admin", command=lambda: controller.show_frame(AdminPage))
        self.adminButton.grid(row=2, column=1)
        
        
class CheckInPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.scanLabel = tk.Label(self, text="Please Scan NFC Card")
        self.scanLabel.grid(row=0, column=1)
        
        self.backButton = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        self.backButton.grid(row=3, column=0)
        
        self.scanCardButton = tk.Button(self, text="Scan Card", command=self.scanCard)
        self.scanCardButton.grid(row=1, column = 1)
        
        self.scanFingerButton = tk.Button(self, text="Scan Finger", command=self.scanFinger)
        self.scanFingerButton.grid(row=2, column = 1)
    
    def scanCard(self):
        
        print("Scanning Card Function")
        
    def scanFinger(self):
        
        print("Scanning Finger Function")
        
class RegisterPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.label = tk.Label(self, text="Register Page")
        self.label.grid(row=0, column=1)
        
        self.first_text = tk.StringVar()
        self.last_text = tk.StringVar()
        self.sid_text = tk.StringVar()
        
        self.first_label = tk.Label(self, text="First Name")
        self.first_label.grid(row=1, column=0)
        self.first_entry = tk.Entry(self, textvariable=self.first_text)
        self.first_entry.grid(row=1, column=1)
        
        self.last_label = tk.Label(self, text="Last Name")
        self.last_label.grid(row=2, column=0)
        self.last_entry = tk.Entry(self, textvariable=self.last_text)
        self.last_entry.grid(row=2, column=1)
        
        self.sid_label = tk.Label(self, text="Student ID")
        self.sid_label.grid(row=3, column=0)
        self.sid_entry = tk.Entry(self, textvariable=self.sid_text)
        self.sid_entry.grid(row=3, column=1)
        
        self.back_button = tk.Button(self, text="Back", command= lambda: controller.show_frame(StartPage))
        self.back_button.grid(row=4, column=0)
        
        self.enter_button = tk.Button(self, text="Enter", command= lambda: controller.show_frame(EnrollNFCPage))
        self.enter_button.grid(row=4, column=1)
        
        
        
class EnrollNFCPage(tk.Frame):
    
     
    def __init__(self, parent, controller):
         
         tk.Frame.__init__(self, parent)
         
         self.enroll_label = tk.Label(self, text="Enroll Your NFC Card")
         self.enroll_label.grid(row=0, column=1)
         
         self.enrollNFC_button = tk.Button(self, text="Enroll Card", command=self.enrollNFC)
         self.enrollNFC_button.grid(row=1, column=0)
         
         self.enrollFingerPrint_button = tk.Button(self, text="Enroll Fingerprint", command=self.enrollFingerprint)
         self.enrollFingerPrint_button.grid(row=1, column=1)
         
         self.returnHome_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
         self.returnHome_button.grid(row=2, column=1)
    def enrollNFC(self):
        
        print("Enroll NFC Card Function")
         
        
    def enrollFingerprint(self):
        
        print("Enroll Fingerprint image")
        

class AdminPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.admin_label = tk.Label(self, text="Admin View")
        self.admin_label.grid(row=0, column=0)
        
        self.list = tk.Listbox(self, height=8, width=50)
        self.list.grid(row=2, column=0)
        
        self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        self.back_button.grid(row=3, column=0)
        
        self.populate_list()
    
    def populate_list(self):
        
        self.list.delete(0, tk.END)
        
        for row in db.fetch():
            
            self.list.insert(tk.END, row)
        
        
        
        
app = Attendance()
app.mainloop()        
        
        
        
        